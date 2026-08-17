from datetime import date

from holidaylens.compare import MatchStatus, compare
from holidaylens.models import Holiday


def test_matching_holiday():
    reference = [
        Holiday(date(2026, 1, 26), "Republic Day"),
    ]

    dataset = [
        Holiday(date(2026, 1, 26), "Republic Day"),
    ]

    results = compare(reference, dataset)

    assert len(results) == 1
    assert results[0].status == MatchStatus.MATCH
    assert results[0].reference.name == "Republic Day"
    assert results[0].dataset.name == "Republic Day"


def test_missing_holiday():
    reference = [
        Holiday(date(2026, 9, 14), "Ganesh Chaturthi"),
    ]

    dataset = []

    results = compare(reference, dataset)

    assert len(results) == 1
    assert results[0].status == MatchStatus.MISSING
    assert results[0].reference.name == "Ganesh Chaturthi"
    assert results[0].dataset is None


def test_extra_holiday():
    reference = []

    dataset = [
        Holiday(date(2026, 12, 25), "Christmas"),
    ]

    results = compare(reference, dataset)

    assert len(results) == 1
    assert results[0].status == MatchStatus.EXTRA
    assert results[0].reference is None
    assert results[0].dataset.name == "Christmas"


def test_name_mismatch():
    reference = [
        Holiday(date(2026, 5, 1), "Maharashtra Day"),
    ]

    dataset = [
        Holiday(date(2026, 5, 1), "Buddha Purnima"),
    ]

    results = compare(reference, dataset)

    assert len(results) == 1
    assert results[0].status == MatchStatus.NAME_MISMATCH

    assert results[0].reference.name == "Maharashtra Day"
    assert results[0].dataset.name == "Buddha Purnima"


def test_multiple_holidays_same_date():
    reference = [
        Holiday(date(2026, 5, 1), "Maharashtra Day"),
        Holiday(date(2026, 5, 1), "Buddha Purnima"),
    ]

    dataset = [
        Holiday(date(2026, 5, 1), "Maharashtra Day"),
        Holiday(date(2026, 5, 1), "Buddha Purnima"),
    ]

    results = compare(reference, dataset)

    assert len(results) == 2
    assert all(result.status == MatchStatus.MATCH for result in results)


def test_multiple_holidays_one_missing():
    reference = [
        Holiday(date(2026, 5, 1), "Maharashtra Day"),
        Holiday(date(2026, 5, 1), "Buddha Purnima"),
    ]

    dataset = [
        Holiday(date(2026, 5, 1), "Maharashtra Day"),
    ]

    results = compare(reference, dataset)

    assert len(results) == 2

    statuses = [result.status for result in results]

    assert statuses.count(MatchStatus.MATCH) == 1
    assert statuses.count(MatchStatus.MISSING) == 1