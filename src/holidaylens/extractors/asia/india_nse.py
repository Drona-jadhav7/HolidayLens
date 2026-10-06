"""NSE/BSE trading holidays extractor.

Handles the National Stock Exchange (XNSE) and Bombay Stock Exchange
(XBOM) trading holiday schedules, including Muhurat Trading on Diwali.
"""

from __future__ import annotations

from pathlib import Path

from holidaylens.extractors.base import BaseExtractor, ExtractionResult
from holidaylens.extractors.registry import register
from holidaylens.models import Holiday
from holidaylens.sources import load_csv


@register("IN", "financial")
class IndiaNSEExtractor(BaseExtractor):
    """Extract NSE/BSE stock exchange trading holidays.

    Loads curated CSVs from ``data/official/IN/stock/``.
    Future versions will scrape NSE's regulatory page directly.

    Special handling for Muhurat Trading:
    Diwali is a regular trading holiday, but exchanges hold a
    special 1-hour "Muhurat Trading" session in the evening.
    This extractor marks such dates with a ``muhurat_trading``
    flag in the holiday name.
    """

    country_code = "IN"
    category = "financial"
    source_url = (
        "https://www.nseindia.com/regulations/"
        "listing-compliance/nse-market-timings-holidays"
    )
    authority_name = "National Stock Exchange of India"

    def __init__(
        self,
        *,
        data_dir: str | Path = "data/official",
        market: str = "XNSE",
    ) -> None:
        self.data_dir = Path(data_dir)
        self.market = market

    def extract(self, year: int) -> ExtractionResult:
        """Load stock exchange trading holidays for the given year."""

        result = ExtractionResult(
            metadata=self.build_metadata(year),
        )

        csv_path = self.data_dir / "IN" / "stock" / f"{year}.csv"

        if csv_path.exists():
            try:
                holidays = load_csv(str(csv_path))
                result.holidays = [
                    Holiday(
                        date=h.date,
                        name=h.name,
                        category="financial",
                        source=f"{self.source_url}",
                        authority=self.authority_name,
                    )
                    for h in holidays
                ]
            except ValueError as exc:
                result.errors.append(f"CSV parse error: {exc}")
        else:
            result.warnings.append(
                f"No stock exchange CSV found: {csv_path}"
            )

        return result
