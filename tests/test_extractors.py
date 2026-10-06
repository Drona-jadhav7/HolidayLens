"""Tests for holidaylens.extractors subsystem."""

from pathlib import Path

import pytest

from holidaylens.extractors.asia.india_gov import IndiaGovExtractor
from holidaylens.extractors.asia.india_nse import IndiaNSEExtractor
from holidaylens.extractors.asia.india_rbi import IndiaRBIExtractor
from holidaylens.extractors.asia.japan_cao import JapanCAOExtractor
from holidaylens.extractors.asia.malaysia_gov import MalaysiaGovExtractor
from holidaylens.extractors.asia.philippines_gov import PhilippinesGovExtractor
from holidaylens.extractors.asia.singapore_mom import SingaporeMOMExtractor
from holidaylens.extractors.asia.south_korea_gov import SouthKoreaGovExtractor
from holidaylens.extractors.asia.thailand_gov import ThailandGovExtractor
from holidaylens.extractors.base import BaseExtractor, ExtractionResult
from holidaylens.extractors.registry import (
    get_all_extractors_for_country,
    get_extractor,
    list_extractors,
    register,
)


def test_extraction_result_success():
    res = ExtractionResult(holidays=[], errors=["Something failed"])
    assert not res.success

    res2 = ExtractionResult(holidays=[1, 2], errors=[])
    assert res2.success


def test_registry_list_extractors():
    extractors = list_extractors()
    assert len(extractors) >= 9
    countries = {e[0] for e in extractors}
    assert "IN" in countries
    assert "JP" in countries
    assert "SG" in countries
    assert "MY" in countries
    assert "PH" in countries
    assert "TH" in countries
    assert "KR" in countries


def test_registry_get_extractor():
    ext = get_extractor("JP", "government")
    assert isinstance(ext, JapanCAOExtractor)
    assert ext.country_code == "JP"
    assert ext.category == "government"

    # Non-existent extractor
    assert get_extractor("ZZ", "nonexistent") is None


def test_registry_get_all_for_country():
    in_extractors = get_all_extractors_for_country("IN")
    assert "government" in in_extractors
    assert "bank" in in_extractors
    assert "financial" in in_extractors


def test_japan_cao_extractor(tmp_path):
    csv_file = tmp_path / "JP" / "government" / "2026.csv"
    csv_file.parent.mkdir(parents=True)
    csv_file.write_text(
        "date,name,category,source\n"
        "2026-01-01,New Year's Day,government,https://cao.go.jp\n",
        encoding="utf-8",
    )

    extractor = JapanCAOExtractor(data_dir=tmp_path)
    result = extractor.extract(2026)

    assert result.success
    assert len(result.holidays) == 1
    assert result.holidays[0].name == "New Year's Day"
    assert result.metadata.country_code == "JP"


def test_japan_cao_parse_static():
    raw_csv = (
        "国民の祝日・休日月日,国民の祝日・休日名称\n"
        "2026/1/1,元日\n"
        "2026/1/12,成人の日\n"
    )
    holidays = JapanCAOExtractor.parse_cao_csv(raw_csv, 2026)
    assert len(holidays) == 2
    assert holidays[0].name == "元日"


def test_extractor_missing_file_warning(tmp_path):
    extractor = SingaporeMOMExtractor(data_dir=tmp_path)
    result = extractor.extract(2026)

    assert not result.success
    assert len(result.warnings) > 0
    assert "No Singapore MOM CSV found" in result.warnings[0]


def test_extractor_csv_error(tmp_path):
    csv_file = tmp_path / "SG" / "government" / "2026.csv"
    csv_file.parent.mkdir(parents=True)
    # Missing required 'name' column
    csv_file.write_text("date,foo\n2026-01-01,bar\n", encoding="utf-8")

    extractor = SingaporeMOMExtractor(data_dir=tmp_path)
    result = extractor.extract(2026)

    assert not result.success
    assert len(result.errors) > 0
    assert "CSV parse error" in result.errors[0]


def test_custom_extractor_registration():
    @register("TEST", "custom")
    class CustomExtractor(BaseExtractor):
        country_code = "TEST"
        category = "custom"

        def extract(self, year: int) -> ExtractionResult:
            return ExtractionResult(holidays=[])

    ext = get_extractor("TEST", "custom")
    assert isinstance(ext, CustomExtractor)
    assert "CustomExtractor" in repr(ext)
