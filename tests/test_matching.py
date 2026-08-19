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
        "Buddha Purnima",
        "Maharashtra Day",
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

def test_canonical_name_moharum():
    assert canonical_name("Moharum") == "ashura"


def test_canonical_name_mahatma_gandhi_jayanti():
    assert canonical_name(
        "Mahatma Gandhi Jayanti"
    ) == "mahatma gandhi s birthday"


def test_canonical_name_guru_nanak_jayanti():
    assert canonical_name(
        "Guru Nanak Jayanti"
    ) == "guru nanak s birthday"

def test_canonical_name_buddha_pournima():
    assert canonical_name("Buddha Pournima") == "buddha purnima"


def test_canonical_name_bakri_id():
    assert canonical_name(
        "Bakri Id (Id-Uz-Zuha)"
    ) == "eid al adha"


def test_canonical_name_ambedkar_jayanti():
    assert canonical_name(
        "Dr. Babasaheb Ambedkar Jayanti"
    ) == "dr b r ambedkar s birthday"

def test_names_match_buddha_pournima_alias():
    reference = Holiday(
        date=date(2026, 5, 1),
        name="Buddha Pournima",
    )

    dataset = Holiday(
        date=date(2026, 5, 1),
        name="Buddha Purnima",
    )

    assert names_match(reference, dataset)


def test_names_match_bakri_id_alias():
    reference = Holiday(
        date=date(2026, 5, 28),
        name="Bakri Id (Id-Uz-Zuha)",
    )

    dataset = Holiday(
        date=date(2026, 5, 27),
        name="Eid al-Adha",
    )

    assert names_match(reference, dataset)


def test_names_match_ambedkar_alias():
    reference = Holiday(
        date=date(2026, 4, 14),
        name="Dr. Babasaheb Ambedkar Jayanti",
    )

    dataset = Holiday(
        date=date(2026, 4, 14),
        name="Dr. B. R. Ambedkar's Birthday",
    )

    assert names_match(reference, dataset)