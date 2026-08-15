from __future__ import annotations

import holidays
import pandas as pd
from .normalizer import normalize_name


def get_library_holidays(country: str, subdivision: str | None, year: int) -> pd.DataFrame:
    calendar = holidays.country_holidays(
        country, subdiv=subdivision, years=year, language="en"
    )

    records = []
    for holiday_date, holiday_names in sorted(calendar.items()):
        names = [
            name.strip()
            for name in str(holiday_names).split(";")
            if name.strip()
        ]
        for name in names:
            records.append({
                "date": holiday_date,
                "name": name,
                "normalized_name": normalize_name(name),
                "type": "library",
            })

    return pd.DataFrame(
        records,
        columns=["date", "name", "normalized_name", "type"],
    )
