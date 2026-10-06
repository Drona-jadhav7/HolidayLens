"""Multi-country / batch execution runner.

Orchestrates audits across multiple countries, subdivisions,
categories, and years, aggregating results for batch reporting.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from holidaylens.compare import build_audit_result, compare
from holidaylens.library import (
    load_bank_holidays,
    load_financial_holidays,
    load_holidays,
)
from holidaylens.models import AuditResult, Holiday
from holidaylens.sources import load_csv, resolve_reference_path


@dataclass
class AuditConfig:
    """Configuration for a single audit run."""

    country: str
    year: int
    category: str = "public"
    subdivision: str | None = None
    reference_path: str | Path | None = None
    market: str | None = None  # For financial holidays (e.g., "XNSE")


@dataclass
class SuiteConfig:
    """Configuration for a batch suite run."""

    audits: list[AuditConfig] = field(default_factory=list)
    data_dir: str | Path = "data/official"
    output_dir: str | Path = "reports"


@dataclass
class SuiteResult:
    """Aggregated results from a suite run."""

    results: list[AuditResult] = field(default_factory=list)
    errors: list[tuple[AuditConfig, str]] = field(default_factory=list)

    @property
    def total_audits(self) -> int:
        return len(self.results) + len(self.errors)

    @property
    def passed(self) -> int:
        return sum(1 for r in self.results if not r.has_issues)

    @property
    def failed(self) -> int:
        return sum(1 for r in self.results if r.has_issues)

    @property
    def errored(self) -> int:
        return len(self.errors)


def _resolve_reference(
    config: AuditConfig,
    data_dir: str | Path,
) -> str | Path | None:
    """Resolve the reference CSV path for an audit config."""

    if config.reference_path:
        return config.reference_path

    return resolve_reference_path(
        data_dir,
        config.country,
        config.year,
        subdivision=config.subdivision,
        category=config.category,
    )


def _load_dataset(config: AuditConfig) -> list[Holiday]:
    """Load the library dataset based on audit configuration."""

    if config.category == "financial" and config.market:
        return load_financial_holidays(
            config.market,
            years=config.year,
        )

    if config.category in ("bank", "bank+public"):
        return load_bank_holidays(
            config.country,
            subdiv=config.subdivision,
            years=config.year,
        )

    # Default: public holidays
    categories = tuple(config.category.split("+"))
    language = "en_US" if config.country in ("JP", "TH", "KR") else None

    return load_holidays(
        config.country,
        subdiv=config.subdivision,
        years=config.year,
        categories=categories,
        language=language,
    )


def run_single_audit(
    config: AuditConfig,
    *,
    data_dir: str | Path = "data/official",
) -> AuditResult:
    """Execute a single audit and return the result.

    Raises ``FileNotFoundError`` if the reference CSV cannot be found.
    """

    ref_path = _resolve_reference(config, data_dir)

    if ref_path is None or not Path(ref_path).exists():
        raise FileNotFoundError(
            f"Reference CSV not found for {config.country}"
            f"/{config.subdivision or 'national'}"
            f"/{config.year} (category={config.category})"
        )

    reference = load_csv(str(ref_path))
    dataset = _load_dataset(config)
    comparisons = compare(reference, dataset)

    return build_audit_result(
        country=config.country,
        year=config.year,
        category=config.category,
        subdivision=config.subdivision,
        reference=reference,
        dataset=dataset,
        comparisons=comparisons,
    )


def run_suite(suite_config: SuiteConfig) -> SuiteResult:
    """Execute a batch of audits and aggregate results."""

    suite_result = SuiteResult()

    for audit_config in suite_config.audits:
        try:
            result = run_single_audit(
                audit_config,
                data_dir=suite_config.data_dir,
            )
            suite_result.results.append(result)
        except Exception as exc:
            suite_result.errors.append(
                (audit_config, str(exc))
            )

    return suite_result


def build_asia_suite(
    year: int,
    *,
    data_dir: str | Path = "data/official",
) -> SuiteConfig:
    """Build a suite config for all supported Asian countries.

    Includes public, bank, and financial audits where reference
    data is available.
    """

    audits: list[AuditConfig] = []

    # India – state subdivisions
    india_dir = Path(data_dir) / "IN"

    if india_dir.exists():
        for subdir in sorted(india_dir.iterdir()):
            if subdir.is_dir() and subdir.name not in ("bank", "stock"):
                for csv_file in subdir.glob(f"{year}.csv"):
                    audits.append(
                        AuditConfig(
                            country="IN",
                            year=year,
                            category="public",
                            subdivision=subdir.name,
                        )
                    )

    # India – bank holidays
    if (india_dir / "bank" / f"{year}.csv").exists():
        audits.append(
            AuditConfig(
                country="IN",
                year=year,
                category="bank",
            )
        )

    # India – stock exchange
    if (india_dir / "stock" / f"{year}.csv").exists():
        audits.append(
            AuditConfig(
                country="IN",
                year=year,
                category="financial",
                market="XNSE",
            )
        )

    # Other Asian countries – government holidays
    for country_code in ("JP", "SG", "MY", "PH", "TH", "KR"):
        gov_csv = Path(data_dir) / country_code / "government" / f"{year}.csv"
        plain_csv = Path(data_dir) / country_code / f"{year}.csv"

        if gov_csv.exists() or plain_csv.exists():
            audits.append(
                AuditConfig(
                    country=country_code,
                    year=year,
                    category="public",
                )
            )

    return SuiteConfig(
        audits=audits,
        data_dir=data_dir,
    )
