import pandas as pd

from holiday_gap.comparator import compare_holidays


def test_same_date_matches():
    official = pd.DataFrame([
        {
            "date": pd.Timestamp("2026-01-26").date(),
            "name": "Republic Day",
            "type": "general",
        }
    ])
    library = pd.DataFrame([
        {
            "date": pd.Timestamp("2026-01-26").date(),
            "name": "Republic Day",
            "normalized_name": "republic day",
            "type": "library",
        }
    ])

    result = compare_holidays(official, library)
    assert len(result["match"]) == 1
    assert not result["missing"]
    assert not result["extra"]
