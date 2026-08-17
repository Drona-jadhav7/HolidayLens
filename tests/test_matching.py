from datetime import date

from holidaylens.matching import names_match, normalize_name
from holidaylens.models import Holiday


def test_normalize_name():
    assert normalize_name("Republic Day") == "republic day"
    assert normalize_name("  Republic   Day  ") == "republic day"
    assert normalize_name("Republic-Day") == "republic day"


def test_names_match():
    reference = Holiday(
        date=date(2026, 1, 26),
        name="Republic Day",
    )

    dataset = Holiday(
        date=date(2026, 1, 26),
        name="Republic-Day",
    )

    assert names_match(reference, dataset)


def test_different_names_do_not_match():
    reference = Holiday(
        date=date(2026, 1, 26),
        name="Republic Day",
    )

    dataset = Holiday(
        date=date(2026, 1, 26),
        name="Independence Day",
    )

    assert not names_match(reference, dataset)