"""Terminal tables, JSON export, and GitHub issue generator.

Produces human-readable terminal reports, structured JSON output,
and templated GitHub issue / PR markdown for upstream contributions.
"""

from __future__ import annotations

import json
from collections import Counter
from datetime import date
from pathlib import Path

from holidaylens.models import Holiday


def summarize(results: list) -> dict[str, int]:
    """Return summary counts for comparison results.

    Accepts a list of Comparison objects (imported lazily to avoid
    circular dependency with compare.py).
    """

    counts = Counter(result.status.value for result in results)

    return {
        "matching": counts.get("match", 0),
        "missing": counts.get("missing", 0),
        "extra": counts.get("extra", 0),
        "name_mismatch": counts.get("name_mismatch", 0),
        "date_mismatch": counts.get("date_mismatch", 0),
    }


def calculate_coverage(
    results: list,
    reference_count: int,
) -> float:
    """Calculate the percentage of reference holidays matched exactly."""

    if reference_count == 0:
        return 100.0

    matching = sum(
        result.status.value == "match"
        for result in results
    )

    return matching / reference_count * 100


def _format_holiday(holiday: Holiday) -> str:
    """Format a holiday for display."""

    return f"{holiday.date.isoformat()} | {holiday.name}"


def format_report(
    results: list,
    *,
    country: str,
    subdivision: str | None,
    year: int,
    reference_count: int,
    dataset_count: int,
    category: str = "public",
) -> str:
    """Format comparison results as a human-readable report."""

    summary = summarize(results)
    coverage = calculate_coverage(results, reference_count)

    subdivision_text = subdivision or "N/A"

    lines = [
        "HolidayLens Report",
        "-" * 32,
        f"Country:       {country}",
        f"Subdivision:   {subdivision_text}",
        f"Year:          {year}",
        f"Category:      {category}",
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

    missing = [r for r in results if r.status.value == "missing"]
    extra = [r for r in results if r.status.value == "extra"]
    name_mismatches = [r for r in results if r.status.value == "name_mismatch"]
    date_mismatches = [r for r in results if r.status.value == "date_mismatch"]

    if missing:
        lines.extend(
            [
                "",
                "Missing Holidays",
                "-" * 32,
            ]
        )

        for result in missing:
            lines.append(_format_holiday(result.reference))

    if extra:
        lines.extend(
            [
                "",
                "Extra Holidays",
                "-" * 32,
            ]
        )

        for result in extra:
            lines.append(_format_holiday(result.dataset))

    if name_mismatches:
        lines.extend(
            [
                "",
                "Name Mismatches",
                "-" * 32,
            ]
        )

        for result in name_mismatches:
            lines.append(
                f"{result.reference.date.isoformat()} | "
                f"{result.reference.name} <-> {result.dataset.name}"
            )

    if date_mismatches:
        lines.extend(
            [
                "",
                "Date Mismatches",
                "-" * 32,
            ]
        )

        for result in date_mismatches:
            lines.append(
                f"{result.reference.name}: "
                f"{result.reference.date.isoformat()} -> "
                f"{result.dataset.date.isoformat()}"
            )

    return "\n".join(lines)


def report_data(
    results: list,
    *,
    country: str,
    subdivision: str | None,
    year: int,
    reference_count: int,
    dataset_count: int,
    category: str = "public",
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
        "category": category,
        "reference_count": reference_count,
        "dataset_count": dataset_count,
        "coverage": round(coverage, 1),
        "summary": summary,
        "comparisons": comparisons,
    }


def save_json_report(data: dict, path: str | Path) -> Path:
    """Write a JSON report to disk.

    Returns the path written to.
    """

    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)

    return path


def generate_github_issue(
    data: dict,
    *,
    repo: str = "vacanza/python-holidays",
) -> str:
    """Generate a GitHub issue markdown template from report data.

    Produces a structured issue body suitable for filing upstream
    bug reports or data-quality improvement requests.
    """

    country = data["country"]
    subdivision = data.get("subdivision") or "N/A"
    year = data["year"]
    category = data.get("category", "public")
    summary = data["summary"]
    coverage = data["coverage"]

    title = (
        f"[{country}] Holiday data gaps for {year} "
        f"(subdivision={subdivision}, category={category})"
    )

    lines = [
        f"# {title}",
        "",
        "## Summary",
        "",
        f"| Metric | Value |",
        f"|--------|-------|",
        f"| Country | `{country}` |",
        f"| Subdivision | `{subdivision}` |",
        f"| Year | {year} |",
        f"| Category | {category} |",
        f"| Coverage | {coverage}% |",
        f"| Missing | {summary['missing']} |",
        f"| Extra | {summary['extra']} |",
        f"| Name Mismatch | {summary['name_mismatch']} |",
        f"| Date Mismatch | {summary['date_mismatch']} |",
        "",
    ]

    missing = [
        c for c in data.get("comparisons", [])
        if c["status"] == "missing"
    ]

    if missing:
        lines.extend([
            "## Missing Holidays",
            "",
            "The following holidays appear in official government records "
            "but are absent from `python-holidays`:",
            "",
            "| Date | Name | Source |",
            "|------|------|--------|",
        ])

        for item in missing:
            ref = item["reference"]
            lines.append(
                f"| {ref['date']} | {ref['name']} | {ref.get('source', 'N/A')} |"
            )

        lines.append("")

    name_mismatches = [
        c for c in data.get("comparisons", [])
        if c["status"] == "name_mismatch"
    ]

    if name_mismatches:
        lines.extend([
            "## Name Mismatches",
            "",
            "| Date | Official Name | Library Name |",
            "|------|--------------|--------------|",
        ])

        for item in name_mismatches:
            ref = item["reference"]
            ds = item["dataset"]
            lines.append(
                f"| {ref['date']} | {ref['name']} | {ds['name']} |"
            )

        lines.append("")

    date_mismatches = [
        c for c in data.get("comparisons", [])
        if c["status"] == "date_mismatch"
    ]

    if date_mismatches:
        lines.extend([
            "## Date Mismatches",
            "",
            "| Holiday | Official Date | Library Date |",
            "|---------|--------------|--------------|",
        ])

        for item in date_mismatches:
            ref = item["reference"]
            ds = item["dataset"]
            lines.append(
                f"| {ref['name']} | {ref['date']} | {ds['date']} |"
            )

        lines.append("")

    lines.extend([
        "## Reproduction",
        "",
        "```bash",
        f"holidaylens audit --country {country} "
        + (f"--subdivision {subdivision} " if subdivision != "N/A" else "")
        + f"--year {year} --format json",
        "```",
        "",
        f"Generated by [HolidayLens](https://github.com/{repo})",
    ])

    return "\n".join(lines)
