from holiday_gap.normalizer import name_similarity, normalize_name


def test_normalize_name():
    assert normalize_name("  Republic Day! ") == "republic day"


def test_identical_names():
    assert name_similarity("Republic Day", "Republic Day") == 1.0
