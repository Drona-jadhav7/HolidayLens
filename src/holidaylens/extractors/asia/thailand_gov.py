"""Thailand public and financial institutions holiday extractor.

Parses official holiday notices published by the Bank of Thailand (BOT)
and Royal Thai Government Cabinet:
https://www.bot.or.th/en/financial-innovation/financial-landscape/holidays.html
"""

from __future__ import annotations

from pathlib import Path

from holidaylens.extractors.base import BaseExtractor, ExtractionResult
from holidaylens.extractors.registry import register
from holidaylens.models import Holiday
from holidaylens.sources import load_csv


@register("TH", "government")
@register("TH", "bank")
class ThailandGovExtractor(BaseExtractor):
    """Extract Thailand public and bank holidays.

    Loads curated reference CSVs from ``data/official/TH/government/``,
    ``data/official/TH/bank/``, or ``data/official/TH/``.
    """

    country_code = "TH"
    category = "government"
    source_url = (
        "https://www.bot.or.th/en/financial-innovation/"
        "financial-landscape/holidays.html"
    )
    authority_name = "Bank of Thailand / Royal Thai Government"

    def __init__(
        self,
        *,
        data_dir: str | Path = "data/official",
        category: str = "government",
    ) -> None:
        self.data_dir = Path(data_dir)
        self.category = category

    def extract(self, year: int) -> ExtractionResult:
        """Load Thailand holidays for the given year."""

        result = ExtractionResult(
            metadata=self.build_metadata(year),
        )

        candidates = [
            self.data_dir / "TH" / self.category / f"{year}.csv",
            self.data_dir / "TH" / "government" / f"{year}.csv",
            self.data_dir / "TH" / f"{year}.csv",
        ]

        csv_path = next((p for p in candidates if p.exists()), None)

        if csv_path:
            try:
                holidays = load_csv(str(csv_path))
                result.holidays = [
                    Holiday(
                        date=h.date,
                        name=h.name,
                        category=self.category,
                        source=self.source_url,
                        authority=self.authority_name,
                    )
                    for h in holidays
                ]
            except ValueError as exc:
                result.errors.append(f"CSV parse error: {exc}")
        else:
            result.warnings.append(
                f"No Thailand reference CSV found in {self.data_dir / 'TH'}"
            )

        return result
