from datetime import date

import pytest

from holidaylens.sources import load_csv


def test_load_csv():
    holidays = load_csv("data/official/IN/MH/2026.csv")

    assert len(holidays) == 24
    assert holidays[0].date == date(2026, 1, 26)
    assert holidays[0].name == "Republic Day"
    assert holidays[0].category == "public"
    assert holidays[0].source.startswith("https://")


def test_load_csv_rejects_invalid_date(tmp_path):
    path = tmp_path / "invalid.csv"

    path.write_text(
        "date,name\n"
        "not-a-date,Example Holiday\n",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="Invalid date"):
        load_csv(path)


def test_load_csv_rejects_missing_name(tmp_path):
    path = tmp_path / "invalid.csv"

    path.write_text(
        "date,name\n"
        "2026-01-01,\n",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="Missing holiday name"):
        load_csv(path)

def test_load_csv_metadata(tmp_path):
    csv_file = tmp_path / "holidays.csv"

    csv_file.write_text(
        "date,name,category,source\n"
        "2026-05-01,Maharashtra Day,public,government\n",
        encoding="utf-8",
    )

    holidays = load_csv(csv_file)

    assert len(holidays) == 1
    assert holidays[0].category == "public"
    assert holidays[0].source == "government"

def test_load_csv_uses_metadata_defaults(tmp_path):
    csv_file = tmp_path / "holidays.csv"

    csv_file.write_text(
        "date,name\n"
        "2026-05-01,Maharashtra Day\n",
        encoding="utf-8",
    )

    holidays = load_csv(csv_file)

    assert holidays[0].category == "public"
    assert holidays[0].source == "unknown"