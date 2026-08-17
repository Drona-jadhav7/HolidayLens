from datetime import date

from holidaylens.library import load_holidays


def test_load_india_holidays():
    holidays = load_holidays("IN", years=2026)

    assert holidays
    assert all(holiday.category == "public" for holiday in holidays)
    assert all(holiday.source == "holidays" for holiday in holidays)


def test_load_maharashtra_holidays():
    holidays = load_holidays(
        "IN",
        subdiv="MH",
        years=2026,
    )

    assert holidays
    assert all(holiday.source == "holidays" for holiday in holidays)


def test_holiday_dates_are_sorted():
    holidays = load_holidays("IN", years=2026)

    dates = [holiday.date for holiday in holidays]

    assert dates == sorted(dates)


def test_india_has_republic_day():
    holidays = load_holidays("IN", years=2026)

    assert any(
        holiday.date == date(2026, 1, 26)
        and "Republic Day" in holiday.name
        for holiday in holidays
    )