"""India Central & State government holiday extractor.

Parses official gazette notifications from state General Administration
Departments.  For states where structured data is unavailable, falls
back to a curated reference CSV bundled in ``data/official/IN/``.
"""

from __future__ import annotations

from pathlib import Path

from holidaylens.extractors.base import BaseExtractor, ExtractionResult
from holidaylens.extractors.registry import register
from holidaylens.models import Holiday, SourceMetadata
from holidaylens.sources import discover_csv_files, load_csv


# Supported state subdivision codes
SUPPORTED_SUBDIVISIONS = (
    "MH", "MP", "UK", "AS", "KA", "TN", "KL", "DL", "GJ",
    "RJ", "WB", "UP", "BR", "JH", "OR", "AP", "TS", "GA",
    "HP", "PB", "HR", "CG", "MN", "ML", "MZ", "NL", "SK",
    "TR", "AR",
)


@register("IN", "government")
class IndiaGovExtractor(BaseExtractor):
    """Extract government holidays for India (central + states).

    Currently loads from curated reference CSVs.  Future versions
    will scrape gazette PDFs and HTML tables directly.
    """

    country_code = "IN"
    category = "government"
    source_url = "https://mmrda.maharashtra.gov.in/en/public-holidays"
    authority_name = "Government of India / State Governments"

    def __init__(
        self,
        *,
        data_dir: str | Path = "data/official",
        subdivision: str | None = None,
    ) -> None:
        self.data_dir = Path(data_dir)
        self.subdivision = subdivision

    def extract(self, year: int) -> ExtractionResult:
        """Load holidays from reference CSVs for the given year."""

        result = ExtractionResult(
            metadata=self.build_metadata(year),
        )

        # Determine which path to look for
        if self.subdivision:
            csv_path = (
                self.data_dir / "IN" / self.subdivision / f"{year}.csv"
            )

            if csv_path.exists():
                try:
                    holidays = load_csv(str(csv_path))
                    result.holidays = holidays
                except ValueError as exc:
                    result.errors.append(f"CSV parse error: {exc}")
            else:
                result.warnings.append(
                    f"No reference CSV found: {csv_path}"
                )
        else:
            # Scan all available subdivisions
            csv_files = discover_csv_files(
                self.data_dir, "IN",
            )

            for csv_file in csv_files:
                if csv_file.stem == str(year):
                    try:
                        holidays = load_csv(str(csv_file))
                        result.holidays.extend(holidays)
                    except ValueError as exc:
                        result.warnings.append(
                            f"Skipped {csv_file}: {exc}"
                        )

        return result
