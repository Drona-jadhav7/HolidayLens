from dataclasses import dataclass

from holidaylens.models import Holiday


@dataclass(frozen=True)
class ComparisonResult:
    matching: list[Holiday]
    missing: list[Holiday]
    extra: list[Holiday]


def _group_by_date(holidays: list[Holiday]) -> dict:
    """Group holidays by date."""
    grouped = {}

    for holiday in holidays:
        grouped.setdefault(holiday.date, []).append(holiday)

    return grouped


def compare_dates(
    reference: list[Holiday],
    dataset: list[Holiday],
) -> ComparisonResult:
    """Compare holidays using their dates."""

    reference_by_date = _group_by_date(reference)
    dataset_by_date = _group_by_date(dataset)

    reference_dates = set(reference_by_date)
    dataset_dates = set(dataset_by_date)

    matching_dates = reference_dates & dataset_dates
    missing_dates = reference_dates - dataset_dates
    extra_dates = dataset_dates - reference_dates

    return ComparisonResult(
        matching=[
            holiday
            for holiday_date in sorted(matching_dates)
            for holiday in reference_by_date[holiday_date]
        ],
        missing=[
            holiday
            for holiday_date in sorted(missing_dates)
            for holiday in reference_by_date[holiday_date]
        ],
        extra=[
            holiday
            for holiday_date in sorted(extra_dates)
            for holiday in dataset_by_date[holiday_date]
        ],
    )