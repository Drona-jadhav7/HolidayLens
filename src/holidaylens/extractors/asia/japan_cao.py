"""Japan Cabinet Office (CAO) public holidays extractor.

The Cabinet Office publishes the official list of Japanese national
holidays (祝日) as a CSV file:
https://www8.cao.go.jp/chosei/shukujitsu/syukujitsu.csv
"""

from __future__ import annotations

import csv
from datetime import date
from io import StringIO
from pathlib import Path

from holidaylens.extractors.base import BaseExtractor, ExtractionResult
from holidaylens.extractors.registry import register
from holidaylens.models import Holiday
from holidaylens.sources import load_csv


@register("JP", "government")
class JapanCAOExtractor(BaseExtractor):
    """Extract Japanese public holidays from Cabinet Office data.

    Loads curated CSVs from ``data/official/JP/government/``.
    Future versions will directly download and parse the CAO CSV.
    """

    country_code = "JP"
    category = "government"
    source_url = "https://www8.cao.go.jp/chosei/shukujitsu/gaiyou.html"
    authority_name = "Cabinet Office, Government of Japan"

    def __init__(
        self,
        *,
        data_dir: str | Path = "data/official",
    ) -> None:
        self.data_dir = Path(data_dir)

    def extract(self, year: int) -> ExtractionResult:
        """Load Japanese public holidays for the given year."""

        result = ExtractionResult(
            metadata=self.build_metadata(year),
        )

        csv_path = self.data_dir / "JP" / "government" / f"{year}.csv"

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
                f"No Japan CAO CSV found: {csv_path}"
            )

        return result

    @staticmethod
    def parse_cao_csv(content: str, year: int) -> list[Holiday]:
        """Parse the raw CAO CSV content (Shift_JIS, Japanese format).

        The CAO CSV has columns: 国民の祝日・休日月日, 国民の祝日・休日名称
        (Date, Name) in YYYY/M/D format.

        This static method is provided for future use when downloading
        directly from the CAO website.
        """

        holidays = []
        reader = csv.reader(StringIO(content))

        # Skip header
        next(reader, None)

        for row in reader:
            if len(row) < 2:
                continue

            raw_date = row[0].strip()
            name = row[1].strip()

            if not raw_date or not name:
                continue

            try:
                parts = raw_date.split("/")
                holiday_date = date(
                    int(parts[0]),
                    int(parts[1]),
                    int(parts[2]),
                )
            except (ValueError, IndexError):
                continue

            if holiday_date.year != year:
                continue

            holidays.append(
                Holiday(
                    date=holiday_date,
                    name=name,
                    category="government",
                    source="https://www8.cao.go.jp/chosei/shukujitsu/syukujitsu.csv",
                    authority="Cabinet Office, Government of Japan",
                )
            )

        return holidays
