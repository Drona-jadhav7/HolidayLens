"""Tests for holidaylens.suite batch execution runner."""

from pathlib import Path

import pytest

from holidaylens.models import AuditResult
from holidaylens.suite import (
    AuditConfig,
    SuiteConfig,
    SuiteResult,
    _resolve_reference,
    build_asia_suite,
    run_single_audit,
    run_suite,
)


def test_suite_result_properties():
    res1 = AuditResult(
        country="JP",
        year=2026,
        category="public",
        coverage=100.0,
        summary={"matching": 5},
    )
    res2 = AuditResult(
        country="IN",
        year=2026,
        category="public",
        coverage=80.0,
        summary={"missing": 1, "matching": 4},
    )
    suite_res = SuiteResult(
        results=[res1, res2],
        errors=[(AuditConfig(country="XX", year=2026), "Not found")],
    )

    assert suite_res.total_audits == 3
    assert suite_res.passed == 1
    assert suite_res.failed == 1
    assert suite_res.errored == 1


def test_resolve_reference(tmp_path):
    # Year-level fallback
    in_dir = tmp_path / "IN" / "MH"
    in_dir.mkdir(parents=True)
    csv_file = in_dir / "2026.csv"
    csv_file.write_text("date,name\n2026-01-01,Test\n")

    cfg = AuditConfig(country="IN", year=2026, subdivision="MH")
    resolved = _resolve_reference(cfg, tmp_path)
    assert resolved == csv_file


def test_run_single_audit(tmp_path):
    jp_dir = tmp_path / "JP" / "government"
    jp_dir.mkdir(parents=True)
    csv_file = jp_dir / "2026.csv"
    csv_file.write_text("date,name\n2026-01-01,New Year's Day\n")

    cfg = AuditConfig(country="JP", year=2026, category="public")
    result = run_single_audit(cfg, data_dir=tmp_path)

    assert isinstance(result, AuditResult)
    assert result.country == "JP"
    assert result.year == 2026
    assert result.reference_count == 1


def test_run_single_audit_missing_ref(tmp_path):
    cfg = AuditConfig(country="ZZ", year=2026)
    with pytest.raises(FileNotFoundError):
        run_single_audit(cfg, data_dir=tmp_path)


def test_run_suite_handles_errors(tmp_path):
    # One valid, one missing
    jp_dir = tmp_path / "JP" / "government"
    jp_dir.mkdir(parents=True)
    (jp_dir / "2026.csv").write_text("date,name\n2026-01-01,New Year's Day\n")

    cfg_valid = AuditConfig(country="JP", year=2026, category="public")
    cfg_invalid = AuditConfig(country="ZZ", year=2026, category="public")

    suite_cfg = SuiteConfig(
        audits=[cfg_valid, cfg_invalid],
        data_dir=tmp_path,
    )
    result = run_suite(suite_cfg)

    assert len(result.results) == 1
    assert len(result.errors) == 1
    assert result.total_audits == 2


def test_build_asia_suite_finds_official_data():
    suite_cfg = build_asia_suite(2026, data_dir="data/official")
    assert len(suite_cfg.audits) >= 5
    countries = {a.country for a in suite_cfg.audits}
    assert "IN" in countries
    assert "JP" in countries
    assert "SG" in countries
