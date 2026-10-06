"""Provenance tracking for reference data sources.

Validates source metadata, computes checksums for CSV files, and
verifies URL patterns for official government / regulatory portals.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


@dataclass(frozen=True)
class Source:
    """A reference data source with validation support."""

    name: str
    url: str
    authority: str
    country_code: str = ""
    category: str = "public"
    retrieved_at: str | None = None


def validate_source(source: Source) -> None:
    """Validate a reference source.

    Raises ``ValueError`` if any required field is empty.
    """

    if not source.name.strip():
        raise ValueError("Source name is required")

    if not source.url.strip():
        raise ValueError("Source URL is required")

    if not source.authority.strip():
        raise ValueError("Source authority is required")


def validate_url(url: str) -> bool:
    """Return True if the URL looks like a valid HTTP(S) URL."""

    stripped = url.strip()

    return stripped.startswith("http://") or stripped.startswith("https://")


def compute_checksum(path: str | Path) -> str:
    """Compute SHA-256 hex digest for a file."""

    hasher = hashlib.sha256()

    with open(path, "rb") as file:
        for chunk in iter(lambda: file.read(8192), b""):
            hasher.update(chunk)

    return hasher.hexdigest()


def now_iso() -> str:
    """Return the current UTC time in ISO 8601 format."""

    return datetime.now(timezone.utc).isoformat()


# ---------------------------------------------------------------------------
# Known official sources registry
# ---------------------------------------------------------------------------

OFFICIAL_SOURCES: dict[str, Source] = {
    "IN:government:MH": Source(
        name="Maharashtra Government Holiday Notification",
        url="https://mmrda.maharashtra.gov.in/en/public-holidays",
        authority="Government of Maharashtra",
        country_code="IN",
        category="government",
    ),
    "IN:bank": Source(
        name="RBI Negotiable Instruments Act Section 25 Holiday List",
        url="https://www.rbi.org.in/Scripts/HolidayMatrixDisplay.aspx",
        authority="Reserve Bank of India",
        country_code="IN",
        category="bank",
    ),
    "IN:stock:XNSE": Source(
        name="NSE Trading Holidays",
        url="https://www.nseindia.com/regulations/listing-compliance/nse-market-timings-holidays",
        authority="National Stock Exchange of India",
        country_code="IN",
        category="financial",
    ),
    "IN:stock:XBOM": Source(
        name="BSE Trading Holidays",
        url="https://www.bseindia.com/static/about/tradingholidays.aspx",
        authority="Bombay Stock Exchange",
        country_code="IN",
        category="financial",
    ),
    "JP:government": Source(
        name="Japan Cabinet Office Public Holidays",
        url="https://www8.cao.go.jp/chosei/shukujitsu/gaiyou.html",
        authority="Cabinet Office, Government of Japan",
        country_code="JP",
        category="government",
    ),
    "JP:stock:XTKS": Source(
        name="Tokyo Stock Exchange Trading Holidays",
        url="https://www.jpx.co.jp/english/corporate/about-jpx/calendar/",
        authority="Japan Exchange Group",
        country_code="JP",
        category="financial",
    ),
    "SG:government": Source(
        name="Singapore Ministry of Manpower Public Holidays",
        url="https://www.mom.gov.sg/employment-practices/public-holidays",
        authority="Ministry of Manpower, Singapore",
        country_code="SG",
        category="government",
    ),
    "SG:stock:XSES": Source(
        name="Singapore Exchange Trading Holidays",
        url="https://www.sgx.com/securities/trading",
        authority="Singapore Exchange",
        country_code="SG",
        category="financial",
    ),
    "MY:government": Source(
        name="Malaysia Public Holidays",
        url="https://www.malaysia.gov.my/portal/content/30118",
        authority="Government of Malaysia",
        country_code="MY",
        category="government",
    ),
    "PH:government": Source(
        name="Philippines Official Gazette Holidays",
        url="https://www.officialgazette.gov.ph/nationwide-holidays/",
        authority="Official Gazette, Republic of the Philippines",
        country_code="PH",
        category="government",
    ),
    "TH:government": Source(
        name="Thailand Public Holidays",
        url="https://www.bot.or.th/en/financial-innovation/financial-landscape/holidays.html",
        authority="Bank of Thailand",
        country_code="TH",
        category="government",
    ),
    "KR:government": Source(
        name="South Korea Public Holidays",
        url="https://www.law.go.kr",
        authority="Government of the Republic of Korea",
        country_code="KR",
        category="government",
    ),
}


def get_source(key: str) -> Source | None:
    """Look up a registered official source by key."""

    return OFFICIAL_SOURCES.get(key)