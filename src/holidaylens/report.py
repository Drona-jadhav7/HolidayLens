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
    }


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
        "",
        f"Matched:       {summary['matching']}",
        f"Missing:       {summary['missing']}",
        f"Extra:         {summary['extra']}",
        f"Name mismatch: {summary['name_mismatch']}",
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

    mismatches = [
        result
        for result in results
        if result.status == MatchStatus.NAME_MISMATCH
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

    if mismatches:
        lines.extend(
            [
                "",
                "Name Mismatches",
                "────────────────────────────────",
            ]
        )

        for result in mismatches:
            lines.append(
                f"{result.reference.date.isoformat()} | "
                f"{result.reference.name} ↔ {result.dataset.name}"
            )

    return "\n".join(lines)