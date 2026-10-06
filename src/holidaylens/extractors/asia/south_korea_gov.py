"""South Korea public holiday extractor.

Parses official public office holidays prescribed under the
"Regulations on Holidays of Public Offices" (관공서의 공휴일에 관한 규정)
maintained by the Ministry of Personnel Management:
https://www.law.go.kr
"""

from __future__ import annotations

from pathlib import Path

from holidaylens.extractors.base import BaseExtractor, ExtractionResult
from holidaylens.extractors.registry import register
from holidaylens.models import Holiday
from holidaylens.sources import load_csv


@register("KR", "government")
class SouthKoreaGovExtractor(BaseExtractor):
    """Extract South Korean public holidays (Gonghyuil).

    Loads curated reference CSVs from ``data/official/KR/government/`` or
    ``data/official/KR/``.
    """

    country_code = "KR"
    category = "government"
    source_url = "https://www.law.go.kr"
    authority_name = "Ministry of Personnel Management, Republic of Korea"

    def __init__(
        self,
        *,
        data_dir: str | Path = "data/official",
    ) -> None:
        self.data_dir = Path(data_dir)

    def extract(self, year: int) -> ExtractionResult:
        """Load South Korean public holidays for the given year."""

        result = ExtractionResult(
            metadata=self.build_metadata(year),
        )

        candidates = [
            self.data_dir / "KR" / "government" / f"{year}.csv",
            self.data_dir / "KR" / f"{year}.csv",
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
                f"No South Korea reference CSV found in {self.data_dir / 'KR'}"
            )

        return result
