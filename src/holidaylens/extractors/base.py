"""Base extractor interface.

All country/category-specific extractors must inherit from
``BaseExtractor`` and implement the ``extract()`` method.
"""

from __future__ import annotations

import abc
from dataclasses import dataclass, field
from datetime import datetime, timezone

from holidaylens.models import Holiday, SourceMetadata


@dataclass
class ExtractionResult:
    """Container for extractor output with provenance."""

    holidays: list[Holiday] = field(default_factory=list)
    metadata: SourceMetadata | None = None
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def success(self) -> bool:
        return len(self.holidays) > 0 and len(self.errors) == 0


class BaseExtractor(abc.ABC):
    """Abstract base class for holiday data extractors.

    Subclasses must implement ``extract()`` which fetches and parses
    holiday data from an official source for the given year.
    """

    country_code: str = ""
    category: str = "government"
    source_url: str = ""
    authority_name: str = ""

    @abc.abstractmethod
    def extract(self, year: int) -> ExtractionResult:
        """Extract holidays for the given year.

        Returns an ``ExtractionResult`` containing the parsed holidays
        and provenance metadata.
        """

    def build_metadata(self, year: int) -> SourceMetadata:
        """Build standard metadata for this extractor."""

        return SourceMetadata(
            source_url=self.source_url,
            authority_name=self.authority_name,
            country_code=self.country_code,
            category=self.category,
            retrieved_at=datetime.now(timezone.utc),
        )

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}"
            f"(country={self.country_code!r}, "
            f"category={self.category!r})"
        )
