from datetime import date

from holidaylens.compare import compare_dates
from holidaylens.models import Holiday


def test_compare_dates():
    reference = [
        Holiday(date(2026, 1, 26), "Republic Day"),
        Holiday(date(2026, 5, 1), "Maharashtra Day"),
        Holiday(date(2026, 9, 14), "Ganesh Chaturthi"),
    ]

    dataset = [
        Holiday(date(2026, 1, 26), "Republic Day"),
        Holiday(date(2026, 5, 1), "Maharashtra Day"),
        Holiday(date(2026, 12, 25), "Christmas"),
    ]

    result = compare_dates(reference, dataset)

    assert len(result.matching) == 2
    assert len(result.missing) == 1
    assert len(result.extra) == 1

    assert result.missing[0].date == date(2026, 9, 14)
    assert result.missing[0].name == "Ganesh Chaturthi"

    assert result.extra[0].date == date(2026, 12, 25)
    assert result.extra[0].name == "Christmas"

def test_compare_handles_multiple_holidays_on_same_date():
    reference = [
        Holiday(date(2026, 5, 1), "Buddha Purnima"),
        Holiday(date(2026, 5, 1), "Maharashtra Day"),
    ]

    dataset = [
        Holiday(date(2026, 5, 1), "Maharashtra Day"),
    ]

    result = compare_dates(reference, dataset)

    assert len(result.missing) == 0
    assert len(result.extra) == 0
    assert len(result.matching) == 2