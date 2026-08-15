from holiday_gap.loader import load_official


def test_load_official(tmp_path):
    path = tmp_path / "holidays.csv"
    path.write_text(
        "date,name,type\n"
        "2026-01-26,Republic Day,general\n"
        '2026-12-28,"Shahidi Sabha, Sri Fatehgarh Sahib",regional\n',
        encoding="utf-8",
    )

    df = load_official(path)
    assert len(df) == 2
    assert df.iloc[1]["name"] == "Shahidi Sabha, Sri Fatehgarh Sahib"
