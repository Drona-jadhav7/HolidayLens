from datetime import date

from holidaylens.matching import names_match, normalize_name, split_names
from holidaylens.models import Holiday
from holidaylens.aliases import canonical_name



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

def test_split_names():
    assert split_names("Buddha Purnima; Maharashtra Day") == [
        "buddha purnima",
        "maharashtra day",
    ]


def test_name_matches_combined_dataset_name():
    reference = Holiday(
        date=date(2026, 5, 1),
        name="Maharashtra Day",
    )

    dataset = Holiday(
        date=date(2026, 5, 1),
        name="Buddha Purnima; Maharashtra Day",
    )

    assert names_match(reference, dataset)

def test_canonical_name():
    assert canonical_name("Maharashtra Din") == "maharashtra day"
    assert canonical_name("Maharashtra Day") == "maharashtra day"


def test_canonical_name_dasara():
    assert canonical_name("Dasara") == "dussehra"

def test_names_match_alias():
    reference = Holiday(
        date=date(2026, 5, 1),
        name="Maharashtra Din",
    )

    dataset = Holiday(
        date=date(2026, 5, 1),
        name="Maharashtra Day",
    )

    assert names_match(reference, dataset)


def test_canonical_name_unknown():
    assert canonical_name("Ganesh Chaturthi") == "ganesh chaturthi"