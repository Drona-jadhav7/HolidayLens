"""Core data models for HolidayLens v2."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime
from enum import Enum


class HolidayCategory(Enum):
    """Supported holiday categories for multi-scope comparison."""

    PUBLIC = "public"
    BANK = "bank"
    FINANCIAL = "financial"
    GOVERNMENT = "government"


@dataclass(frozen=True)
class Holiday:
    """A single holiday record with optional provenance metadata."""

    date: date
    name: str
    category: str = "public"
    source: str | None = None
    subdivision: str | None = None
    authority: str | None = None


@dataclass(frozen=True)
class SourceMetadata:
    """Provenance metadata for a reference dataset.

    Tracks the origin URL, issuing authority, and retrieval timestamp
    so every record can be traced back to its official gazette or notice.
    """

    source_url: str
    authority_name: str
    country_code: str
    category: str = "public"
    subdivision: str | None = None
    retrieved_at: datetime | None = None
    checksum: str | None = None

    def __post_init__(self) -> None:
        if not self.source_url.strip():
            raise ValueError("source_url must not be empty")
        if not self.authority_name.strip():
            raise ValueError("authority_name must not be empty")
        if not self.country_code.strip():
            raise ValueError("country_code must not be empty")


@dataclass(frozen=True)
class AuditResult:
    """Aggregated output of a single audit run.

    Captures the configuration used, raw comparisons, and summary
    statistics so downstream reporters and serializers have everything
    they need in one object.
    """

    country: str
    year: int
    category: str
    subdivision: str | None = None
    reference_count: int = 0
    dataset_count: int = 0
    coverage: float = 0.0
    summary: dict[str, int] = field(default_factory=dict)
    comparisons: list = field(default_factory=list)
    metadata: SourceMetadata | None = None

    @property
    def has_issues(self) -> bool:
        """Return True if any non-match results exist."""
        return self.coverage < 100.0 or any(
            k != "matching" and v > 0
            for k, v in self.summary.items()
        )