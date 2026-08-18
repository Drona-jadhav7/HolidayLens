from datetime import date

from holidaylens.compare import Comparison, MatchStatus
from holidaylens.models import Holiday
from holidaylens.report import (
    calculate_coverage,
    format_report,
    summarize,
)


def test_summarize():
    results = [
        Comparison(
            status=MatchStatus.MATCH,
            reference=Holiday(date(2026, 1, 26), "Republic Day"),
            dataset=Holiday(date(2026, 1, 26), "Republic Day"),
        ),
        Comparison(
            status=MatchStatus.MISSING,
            reference=Holiday(date(2026, 9, 14), "Ganesh Chaturthi"),
        ),
        Comparison(
            status=MatchStatus.EXTRA,
            dataset=Holiday(date(2026, 12, 25), "Christmas"),
        ),
        Comparison(
            status=MatchStatus.NAME_MISMATCH,
            reference=Holiday(date(2026, 5, 1), "Maharashtra Day"),
            dataset=Holiday(date(2026, 5, 1), "Buddha Purnima"),
        ),
    ]

    summary = summarize(results)

    assert summary == {
        "matching": 1,
        "missing": 1,
        "extra": 1,
        "name_mismatch": 1,
        "date_mismatch": 0,
    }


def test_format_report():
    results = [
        Comparison(
            status=MatchStatus.MATCH,
            reference=Holiday(date(2026, 1, 26), "Republic Day"),
            dataset=Holiday(date(2026, 1, 26), "Republic Day"),
        )
    ]

    report = format_report(
        results,
        country="IN",
        subdivision="MH",
        year=2026,
        reference_count=1,
        dataset_count=1,
    )

    assert "HolidayLens Report" in report
    assert "Country:       IN" in report
    assert "Subdivision:   MH" in report
    assert "Year:          2026" in report
    assert "Matched:       1" in report
    assert "Coverage:      100.0%" in report
    assert "Date mismatch: 0" in report


def test_format_report_includes_details():
    results = [
        Comparison(
            status=MatchStatus.MISSING,
            reference=Holiday(
                date(2026, 9, 14),
                "Ganesh Chaturthi",
            ),
        ),
        Comparison(
            status=MatchStatus.EXTRA,
            dataset=Holiday(
                date(2026, 12, 25),
                "Christmas",
            ),
        ),
        Comparison(
            status=MatchStatus.NAME_MISMATCH,
            reference=Holiday(
                date(2026, 5, 1),
                "Maharashtra Day",
            ),
            dataset=Holiday(
                date(2026, 5, 1),
                "Buddha Purnima",
            ),
        ),
    ]

    report = format_report(
        results,
        country="IN",
        subdivision="MH",
        year=2026,
        reference_count=1,
        dataset_count=2,
    )

    assert "Missing Holidays" in report
    assert "2026-09-14 | Ganesh Chaturthi" in report

    assert "Extra Holidays" in report
    assert "2026-12-25 | Christmas" in report

    assert "Name Mismatches" in report
    assert "Maharashtra Day ↔ Buddha Purnima" in report

def test_summarize_date_mismatch():
    results = [
        Comparison(
            status=MatchStatus.DATE_MISMATCH,
            reference=Holiday(
                date(2026, 3, 3),
                "Holi",
            ),
            dataset=Holiday(
                date(2026, 3, 4),
                "Holi",
            ),
        )
    ]

    summary = summarize(results)

    assert summary["date_mismatch"] == 1

def test_calculate_coverage():
    results = [
        Comparison(
            status=MatchStatus.MATCH,
            reference=Holiday(
                date(2026, 1, 26),
                "Republic Day",
            ),
            dataset=Holiday(
                date(2026, 1, 26),
                "Republic Day",
            ),
        ),
        Comparison(
            status=MatchStatus.MISSING,
            reference=Holiday(
                date(2026, 9, 14),
                "Ganesh Chaturthi",
            ),
        ),
    ]

    assert calculate_coverage(results, 2) == 50.0