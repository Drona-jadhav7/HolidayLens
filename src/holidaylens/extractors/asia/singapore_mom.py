"""Singapore Ministry of Manpower (MOM) public holiday extractor.

Parses the MOM's published holiday list:
https://www.mom.gov.sg/employment-practices/public-holidays
"""

from __future__ import annotations

from pathlib import Path

from holidaylens.extractors.base import BaseExtractor, ExtractionResult
from holidaylens.extractors.registry import register
from holidaylens.models import Holiday
from holidaylens.sources import load_csv


@register("SG", "government")
class SingaporeMOMExtractor(BaseExtractor):
    """Extract Singapore public holidays from MOM data.

    Loads curated CSVs from ``data/official/SG/government/``.
    Future versions will use the MOM API or data.gov.sg open data.
    """

    country_code = "SG"
    category = "government"
    source_url = "https://www.mom.gov.sg/employment-practices/public-holidays"
    authority_name = "Ministry of Manpower, Singapore"

    def __init__(
        self,
        *,
        data_dir: str | Path = "data/official",
    ) -> None:
        self.data_dir = Path(data_dir)

    def extract(self, year: int) -> ExtractionResult:
        """Load Singapore public holidays for the given year."""

        result = ExtractionResult(
            metadata=self.build_metadata(year),
        )

        csv_path = self.data_dir / "SG" / "government" / f"{year}.csv"

        if csv_path.exists():
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
                f"No Singapore MOM CSV found: {csv_path}"
            )

        return result
