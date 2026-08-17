from holidays import country_holidays

from holidaylens.models import Holiday


def load_holidays(
    country: str,
    *,
    subdiv: str | None = None,
    years: int | list[int] | set[int] | None = None,
) -> list[Holiday]:
    """Load holidays from the Python holidays library."""

    calendar = country_holidays(
        country,
        subdiv=subdiv,
        years=years,
    )

    return [
        Holiday(
            date=holiday_date,
            name=name,
            category="public",
            source="holidays",
        )
        for holiday_date, name in sorted(calendar.items())
    ]