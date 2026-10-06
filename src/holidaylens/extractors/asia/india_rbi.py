"""RBI bank holiday schedule extractor.

Parses the Reserve Bank of India's Negotiable Instruments Act
Section 25 holiday schedule published at:
https://www.rbi.org.in/Scripts/HolidayMatrixDisplay.aspx
"""

from __future__ import annotations

from pathlib import Path

from holidaylens.extractors.base import BaseExtractor, ExtractionResult
from holidaylens.extractors.registry import register
from holidaylens.models import Holiday, SourceMetadata
from holidaylens.sources import load_csv


@register("IN", "bank")
class IndiaRBIExtractor(BaseExtractor):
    """Extract RBI bank holidays from reference data.

    Loads curated CSVs from ``data/official/IN/bank/``.
    Future versions will scrape the RBI holiday matrix HTML table.
    """

    country_code = "IN"
    category = "bank"
    source_url = "https://www.rbi.org.in/Scripts/HolidayMatrixDisplay.aspx"
    authority_name = "Reserve Bank of India"

    def __init__(
        self,
        *,
        data_dir: str | Path = "data/official",
    ) -> None:
        self.data_dir = Path(data_dir)

    def extract(self, year: int) -> ExtractionResult:
        """Load RBI bank holidays for the given year."""

        result = ExtractionResult(
            metadata=self.build_metadata(year),
        )

        csv_path = self.data_dir / "IN" / "bank" / f"{year}.csv"

        if csv_path.exists():
            try:
                holidays = load_csv(str(csv_path))
                result.holidays = [
                    Holiday(
                        date=h.date,
                        name=h.name,
                        category="bank",
                        source=self.source_url,
                        authority=self.authority_name,
                    )
                    for h in holidays
                ]
            except ValueError as exc:
                result.errors.append(f"CSV parse error: {exc}")
        else:
            result.warnings.append(
                f"No RBI bank holiday CSV found: {csv_path}"
            )

        return result
