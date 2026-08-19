
from holidaylens.cli import main


def test_cli_help(capsys):
    try:
        main()
    except SystemExit as exc:
        assert exc.code == 2

    captured = capsys.readouterr()

    assert "usage:" in captured.err
    assert "audit" in captured.err


def test_cli_audit_with_reference(tmp_path, capsys):
    reference = tmp_path / "2026.csv"

    reference.write_text(
        "date,name,category,source\n"
        "2026-01-26,Republic Day,public,government\n",
        encoding="utf-8",
    )

    exit_code = main_with_args(
        "audit",
        "--country",
        "IN",
        "--year",
        "2026",
        "--reference",
        str(reference),
    )

    captured = capsys.readouterr()

    assert exit_code == 1
    assert "HolidayLens Report" in captured.out
    assert "Country:       IN" in captured.out
    assert "Year:          2026" in captured.out
    assert "Reference:     1" in captured.out


def test_cli_missing_reference(capsys, tmp_path):
    missing = tmp_path / "missing.csv"

    exit_code = main_with_args(
        "audit",
        "--country",
        "IN",
        "--year",
        "2026",
        "--reference",
        str(missing),
    )

    captured = capsys.readouterr()

    assert exit_code == 2
    assert "reference CSV not found" in captured.out


def test_cli_audit_returns_issue_status(tmp_path):
    reference = tmp_path / "2026.csv"

    reference.write_text(
        "date,name,category,source\n"
        "2026-01-26,Republic Day,public,government\n",
        encoding="utf-8",
    )

    exit_code = main_with_args(
        "audit",
        "--country",
        "IN",
        "--year",
        "2026",
        "--reference",
        str(reference),
    )

    assert exit_code == 1


def test_cli_parser_accepts_subdivision(tmp_path, capsys):
    reference = tmp_path / "2026.csv"

    reference.write_text(
        "date,name,category,source\n"
        "2026-01-26,Republic Day,public,government\n",
        encoding="utf-8",
    )

    exit_code = main_with_args(
        "audit",
        "--country",
        "IN",
        "--subdivision",
        "MH",
        "--year",
        "2026",
        "--reference",
        str(reference),
    )

    captured = capsys.readouterr()

    assert exit_code == 1
    assert "Subdivision:   MH" in captured.out


def main_with_args(*args):
    import sys

    original_argv = sys.argv
    sys.argv = ["holidaylens", *args]

    try:
        return main()
    finally:
        sys.argv = original_argv
