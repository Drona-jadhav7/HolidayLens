"""Philippines Official Gazette holiday extractor.

Parses nationwide regular and special non-working holidays issued via
Presidential Proclamations published in the Official Gazette:
https://www.officialgazette.gov.ph/nationwide-holidays/
"""

from __future__ import annotations

from pathlib import Path

from holidaylens.extractors.base import BaseExtractor, ExtractionResult
from holidaylens.extractors.registry import register
from holidaylens.models import Holiday
from holidaylens.sources import load_csv


@register("PH", "government")
class PhilippinesGovExtractor(BaseExtractor):
    """Extract Philippines nationwide public holidays.

    Loads curated reference CSVs from ``data/official/PH/government/`` or
    ``data/official/PH/``.
    """

    country_code = "PH"
    category = "government"
    source_url = "https://www.officialgazette.gov.ph/nationwide-holidays/"
    authority_name = "Official Gazette, Republic of the Philippines"

    def __init__(
        self,
        *,
        data_dir: str | Path = "data/official",
    ) -> None:
        self.data_dir = Path(data_dir)

    def extract(self, year: int) -> ExtractionResult:
        """Load Philippine nationwide holidays for the given year."""

        result = ExtractionResult(
            metadata=self.build_metadata(year),
        )

        candidates = [
            self.data_dir / "PH" / "government" / f"{year}.csv",
            self.data_dir / "PH" / f"{year}.csv",
        ]

        csv_path = next((p for p in candidates if p.exists()), None)

        if csv_path:
            try:
                holidays = load_csv(str(csv_path))
                result.holidays = [
                    Holiday(
                        date=h.date,
                        name=h.name,
                        category="government",
                        source=self.source_url,
                        authority=self.authority_name,
                    )
                    for h in holidays
                ]
            except ValueError as exc:
                result.errors.append(f"CSV parse error: {exc}")
        else:
            result.warnings.append(
                f"No Philippines reference CSV found in {self.data_dir / 'PH'}"
            )

        return result
