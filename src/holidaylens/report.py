from collections import Counter

from holidaylens.compare import Comparison, MatchStatus


def summarize(results: list[Comparison]) -> dict[str, int]:
    """Return summary counts for comparison results."""

    counts = Counter(result.status.value for result in results)

    return {
        "matching": counts.get(MatchStatus.MATCH.value, 0),
        "missing": counts.get(MatchStatus.MISSING.value, 0),
        "extra": counts.get(MatchStatus.EXTRA.value, 0),
        "name_mismatch": counts.get(MatchStatus.NAME_MISMATCH.value, 0),
        "date_mismatch": counts.get(MatchStatus.DATE_MISMATCH.value, 0),
    }


def calculate_coverage(
    results: list[Comparison],
    reference_count: int,
) -> float:
    """Calculate the percentage of reference holidays matched exactly."""

    if reference_count == 0:
        return 100.0

    matching = sum(
        result.status == MatchStatus.MATCH
        for result in results
    )

    return matching / reference_count * 100


def _format_holiday(holiday) -> str:
    """Format a holiday for display."""

    return f"{holiday.date.isoformat()} | {holiday.name}"


def format_report(
    results: list[Comparison],
    *,
    country: str,
    subdivision: str | None,
    year: int,
    reference_count: int,
    dataset_count: int,
) -> str:
    """Format comparison results as a human-readable report."""

    summary = summarize(results)
    coverage = calculate_coverage(results, reference_count)

    subdivision_text = subdivision or "N/A"

    lines = [
        "HolidayLens Report",
        "────────────────────────────────",
        f"Country:       {country}",
        f"Subdivision:   {subdivision_text}",
        f"Year:          {year}",
        "",
        f"Reference:     {reference_count}",
        f"Dataset:       {dataset_count}",
        f"Coverage:      {coverage:.1f}%",
        "",
        f"Matched:       {summary['matching']}",
        f"Missing:       {summary['missing']}",
        f"Extra:         {summary['extra']}",
        f"Name mismatch: {summary['name_mismatch']}",
        f"Date mismatch: {summary['date_mismatch']}",
    ]

    missing = [
        result
        for result in results
        if result.status == MatchStatus.MISSING
    ]

    extra = [
        result
        for result in results
        if result.status == MatchStatus.EXTRA
    ]

    name_mismatches = [
        result
        for result in results
        if result.status == MatchStatus.NAME_MISMATCH
    ]

    date_mismatches = [
        result
        for result in results
        if result.status == MatchStatus.DATE_MISMATCH
    ]

    if missing:
        lines.extend(
            [
                "",
                "Missing Holidays",
                "────────────────────────────────",
            ]
        )

        for result in missing:
            lines.append(_format_holiday(result.reference))

    if extra:
        lines.extend(
            [
                "",
                "Extra Holidays",
                "────────────────────────────────",
            ]
        )

        for result in extra:
            lines.append(_format_holiday(result.dataset))

    if name_mismatches:
        lines.extend(
            [
                "",
                "Name Mismatches",
                "────────────────────────────────",
            ]
        )

        for result in name_mismatches:
            lines.append(
                f"{result.reference.date.isoformat()} | "
                f"{result.reference.name} ↔ {result.dataset.name}"
            )

    if date_mismatches:
        lines.extend(
            [
                "",
                "Date Mismatches",
                "────────────────────────────────",
            ]
        )

        for result in date_mismatches:
            lines.append(
                f"{result.reference.name}: "
                f"{result.reference.date.isoformat()} → "
                f"{result.dataset.date.isoformat()}"
            )

    return "\n".join(lines)

def report_data(
    results: list[Comparison],
    *,
    country: str,
    subdivision: str | None,
    year: int,
    reference_count: int,
    dataset_count: int,
) -> dict:
    """Return comparison results as JSON-serializable data."""

    summary = summarize(results)
    coverage = calculate_coverage(results, reference_count)

    comparisons = []

    for result in results:
        item = {
            "status": result.status.value,
        }

        if result.reference is not None:
            item["reference"] = {
                "date": result.reference.date.isoformat(),
                "name": result.reference.name,
                "category": result.reference.category,
                "source": result.reference.source,
            }

        if result.dataset is not None:
            item["dataset"] = {
                "date": result.dataset.date.isoformat(),
                "name": result.dataset.name,
                "category": result.dataset.category,
                "source": result.dataset.source,
            }

        comparisons.append(item)

    return {
        "country": country,
        "subdivision": subdivision,
        "year": year,
        "reference_count": reference_count,
        "dataset_count": dataset_count,
        "coverage": round(coverage, 1),
        "summary": summary,
        "comparisons": comparisons,
    }
