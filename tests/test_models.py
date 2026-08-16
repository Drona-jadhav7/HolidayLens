from datetime import date

from holidaylens.models import Holiday


def test_holiday_creation():
    holiday = Holiday(
        date=date(2026, 9, 14),
        name="Ganesh Chaturthi",
    )

    assert holiday.date == date(2026, 9, 14)
    assert holiday.name == "Ganesh Chaturthi"
    assert holiday.category == "public"
    assert holiday.source is None