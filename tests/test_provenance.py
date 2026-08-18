import pytest

from holidaylens.provenance import Source, validate_source


def test_valid_source():
    source = Source(
        name="Maharashtra Government Holiday Notification",
        url="https://example.gov.in/holidays",
        authority="Government of Maharashtra",
    )

    validate_source(source)


def test_source_requires_name():
    source = Source(
        name="",
        url="https://example.gov.in/holidays",
        authority="Government of Maharashtra",
    )

    with pytest.raises(ValueError, match="Source name is required"):
        validate_source(source)


def test_source_requires_url():
    source = Source(
        name="Holiday Notification",
        url="",
        authority="Government of Maharashtra",
    )

    with pytest.raises(ValueError, match="Source URL is required"):
        validate_source(source)


def test_source_requires_authority():
    source = Source(
        name="Holiday Notification",
        url="https://example.gov.in/holidays",
        authority="",
    )

    with pytest.raises(ValueError, match="Source authority is required"):
        validate_source(source)