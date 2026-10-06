
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
def test_cli_list(capsys):
    exit_code = main_with_args("list")
    assert exit_code == 0
    captured = capsys.readouterr()
    assert "Country" in captured.out
    assert "IndiaGovExtractor" in captured.out
    assert "JapanCAOExtractor" in captured.out


def test_cli_audit_json(tmp_path, capsys):
    reference = tmp_path / "2026.csv"
    reference.write_text(
        "date,name,category,source\n"
        "2026-01-26,Republic Day,public,gov\n",
        encoding="utf-8",
    )
    output_json = tmp_path / "report.json"

    exit_code = main_with_args(
        "audit",
        "--country",
        "IN",
        "--year",
        "2026",
        "--reference",
        str(reference),
        "--format",
        "json",
        "--output",
        str(output_json),
    )

    assert exit_code == 1
    assert output_json.exists()
    import json
    data = json.loads(output_json.read_text(encoding="utf-8"))
    assert data["country"] == "IN"
    assert data["year"] == 2026


def test_cli_extract(capsys):
    exit_code = main_with_args(
        "extract",
        "--country",
        "JP",
        "--category",
        "government",
        "--year",
        "2026",
    )
    assert exit_code == 0
    captured = capsys.readouterr()
    assert "2026-01-01" in captured.out


def test_cli_extract_to_file(tmp_path):
    output_csv = tmp_path / "extracted.csv"
    exit_code = main_with_args(
        "extract",
        "--country",
        "JP",
        "--category",
        "government",
        "--year",
        "2026",
        "--output",
        str(output_csv),
    )
    assert exit_code == 0
    assert output_csv.exists()
    content = output_csv.read_text(encoding="utf-8")
    assert "2026-01-01" in content


def test_cli_report(tmp_path, capsys):
    import json
    report_file = tmp_path / "report.json"
    data = {
        "country": "IN",
        "year": 2026,
        "coverage": 80.0,
        "summary": {"missing": 1, "extra": 0, "name_mismatch": 0, "date_mismatch": 0},
        "comparisons": [
            {"status": "missing", "reference": {"date": "2026-08-15", "name": "Independence Day"}}
        ],
    }
    report_file.write_text(json.dumps(data), encoding="utf-8")

    exit_code = main_with_args("report", str(report_file))
    assert exit_code == 0
    captured = capsys.readouterr()
    assert "[IN] Holiday data gaps for 2026" in captured.out


def test_cli_report_output_file(tmp_path):
    import json
    report_file = tmp_path / "report.json"
    out_md = tmp_path / "issue.md"
    data = {
        "country": "JP",
        "year": 2026,
        "coverage": 100.0,
        "summary": {"missing": 0, "extra": 0, "name_mismatch": 0, "date_mismatch": 0},
        "comparisons": [],
    }
    report_file.write_text(json.dumps(data), encoding="utf-8")

    exit_code = main_with_args("report", "--input", str(report_file), "--output", str(out_md))
    assert exit_code == 0
    assert out_md.exists()
    assert "[JP] Holiday data gaps for 2026" in out_md.read_text(encoding="utf-8")


def test_cli_suite(capsys):
    exit_code = main_with_args("suite", "--year", "2026")
    # Some audits have gaps so returns 1
    assert exit_code in (0, 1)
    captured = capsys.readouterr()
    assert "Suite Results: 2026" in captured.out
    assert "Total audits:" in captured.out


def main_with_args(*args):
    import sys

    original_argv = sys.argv
    sys.argv = ["holidaylens", *args]

    try:
        return main()
    finally:
        sys.argv = original_argv
