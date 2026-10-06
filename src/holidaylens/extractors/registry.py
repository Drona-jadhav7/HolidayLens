"""Extractor registry by (country, category, year).

Provides lookup and auto-discovery of registered extractors.
"""

from __future__ import annotations

from typing import Type

from holidaylens.extractors.base import BaseExtractor


# Registry: (country_code, category) -> ExtractorClass
_REGISTRY: dict[tuple[str, str], Type[BaseExtractor]] = {}


def register(
    country_code: str,
    category: str,
) -> callable:
    """Decorator to register an extractor class.

    Usage::

        @register("IN", "government")
        class IndiaGovExtractor(BaseExtractor):
            ...
    """

    def decorator(cls: Type[BaseExtractor]) -> Type[BaseExtractor]:
        key = (country_code.upper(), category.lower())
        _REGISTRY[key] = cls
        return cls

    return decorator


def _auto_discover() -> None:
    """Ensure built-in regional extractor packages are loaded."""
    try:
        import holidaylens.extractors.asia  # noqa: F401
    except ImportError:
        pass


def get_extractor(
    country_code: str,
    category: str,
) -> BaseExtractor | None:
    """Look up and instantiate an extractor by country and category.

    Returns ``None`` if no extractor is registered for the combination.
    """

    _auto_discover()
    key = (country_code.upper(), category.lower())
    cls = _REGISTRY.get(key)

    if cls is None:
        return None

    return cls()


def list_extractors() -> list[tuple[str, str, str]]:
    """Return a list of ``(country, category, class_name)`` for all registered extractors."""

    _auto_discover()
    return [
        (country, category, cls.__name__)
        for (country, category), cls in sorted(_REGISTRY.items())
    ]


def get_all_extractors_for_country(
    country_code: str,
) -> dict[str, BaseExtractor]:
    """Return all registered extractors for a given country.

    Returns a dict mapping category to extractor instance.
    """

    _auto_discover()

    result = {}

    for (country, category), cls in _REGISTRY.items():
        if country == country_code.upper():
            result[category] = cls()

    return result
