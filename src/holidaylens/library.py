"""Interface to the python-holidays library.

Provides unified loaders for public, bank, and financial holidays,
abstracting over the ``holidays`` library's multiple entry points.
"""

from __future__ import annotations

from holidays import country_holidays

from holidaylens.models import Holiday


def load_holidays(
    country: str,
    *,
    subdiv: str | None = None,
    years: int | list[int] | set[int] | None = None,
    categories: tuple[str, ...] = ("public",),
    language: str | None = None,
) -> list[Holiday]:
    """Load holidays from the Python holidays library.

    Parameters
    ----------
    country : str
        ISO 3166-1 alpha-2 country code (e.g. ``"IN"``, ``"JP"``).
    subdiv : str | None
        Subdivision / state code (e.g. ``"MH"``).
    years : int | list[int] | set[int] | None
        Year(s) to load.
    categories : tuple[str, ...]
        Holiday categories to include (e.g. ``("public",)``,
        ``("public", "bank")``).
    language : str | None
        Language code to request (e.g. ``"en_US"``).
    """

    # Filter categories to only those supported by the country
    try:
        sample = country_holidays(country, subdiv=subdiv)
        supported = getattr(sample, "supported_categories", ())
        if supported:
            filtered = tuple(c for c in categories if c in supported)
            if filtered:
                categories = filtered
            elif "public" in supported:
                categories = ("public",)
    except Exception:
        pass

    kwargs: dict = {
        "subdiv": subdiv,
        "years": years,
        "categories": categories,
    }
    if language is not None:
        kwargs["language"] = language

    calendar = country_holidays(
        country,
        **kwargs,
    )

    category_label = "+".join(sorted(categories))

    return [
        Holiday(
            date=holiday_date,
            name=name,
            category=category_label,
            source="holidays",
            subdivision=subdiv,
        )
        for holiday_date, name in sorted(calendar.items())
    ]


def load_financial_holidays(
    market: str,
    *,
    years: int | list[int] | set[int] | None = None,
) -> list[Holiday]:
    """Load financial / stock exchange holidays.

    Parameters
    ----------
    market : str
        Market identifier code (e.g. ``"XNSE"``, ``"XBOM"``, ``"XTKS"``).
    years : int | list[int] | set[int] | None
        Year(s) to load.
    """

    try:
        from holidays import financial_holidays as _fin
    except ImportError as exc:
        raise ImportError(
            "Your holidays version does not support financial_holidays(). "
            "Upgrade to holidays >= 0.46."
        ) from exc

    calendar = _fin(market, years=years)

    return [
        Holiday(
            date=holiday_date,
            name=name,
            category="financial",
            source=f"holidays:{market}",
        )
        for holiday_date, name in sorted(calendar.items())
    ]


def load_bank_holidays(
    country: str,
    *,
    subdiv: str | None = None,
    years: int | list[int] | set[int] | None = None,
) -> list[Holiday]:
    """Load bank holidays (public + bank categories combined).

    Filters to supported categories if the country does not support 'bank'.
    """

    cal = country_holidays(country, subdiv=subdiv)
    supported = getattr(cal, "supported_categories", ())
    available = tuple(c for c in ("public", "bank") if c in supported)
    categories = available if available else ("public",)

    return load_holidays(
        country,
        subdiv=subdiv,
        years=years,
        categories=categories,
    )