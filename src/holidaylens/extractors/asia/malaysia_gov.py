"""Malaysia government public holiday extractor.

Parses official holiday schedules published by the Prime Minister's
Department (Bahagian Kabinet, Perlembagaan dan Perhubungan Antara Kerajaan,
Jabatan Perdana Menteri):
https://www.malaysia.gov.my/portal/content/30118
"""

from __future__ import annotations

from pathlib import Path

from holidaylens.extractors.base import BaseExtractor, ExtractionResult
from holidaylens.extractors.registry import register
from holidaylens.models import Holiday
from holidaylens.sources import load_csv


@register("MY", "government")
class MalaysiaGovExtractor(BaseExtractor):
    """Extract Malaysian federal and state public holidays.

    Loads curated reference CSVs from ``data/official/MY/government/`` or
    ``data/official/MY/``.
    """

    country_code = "MY"
    category = "government"
    source_url = "https://www.malaysia.gov.my/portal/content/30118"
    authority_name = "Bahagian Kabinet, Jabatan Perdana Menteri, Malaysia"

    def __init__(
        self,
        *,
        data_dir: str | Path = "data/official",
        state: str | None = None,
    ) -> None:
        self.data_dir = Path(data_dir)
        self.state = state

    def extract(self, year: int) -> ExtractionResult:
        """Load Malaysian public holidays for the given year."""

        result = ExtractionResult(
            metadata=self.build_metadata(year),
        )

        candidates = [
            self.data_dir / "MY" / "government" / f"{year}.csv",
            self.data_dir / "MY" / f"{year}.csv",
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
                        subdivision=self.state,
                    )
                    for h in holidays
                ]
            except ValueError as exc:
                result.errors.append(f"CSV parse error: {exc}")
        else:
            result.warnings.append(
                f"No Malaysia reference CSV found in {self.data_dir / 'MY'}"
            )

        return result
