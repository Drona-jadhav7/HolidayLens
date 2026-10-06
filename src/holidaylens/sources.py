"""Reference CSV loaders & schema validators.

Loads official holiday reference data from CSV files, validates
schemas, and supports the expanded v2 column set including
provenance fields.
"""

from __future__ import annotations

import csv
from datetime import date
from pathlib import Path

from holidaylens.models import Holiday


REQUIRED_COLUMNS = {"date", "name"}

OPTIONAL_COLUMNS = {"category", "source", "authority", "subdivision"}


def validate_schema(fieldnames: list[str] | None) -> None:
    """Validate that the CSV header contains required columns.

    Raises ``ValueError`` if required columns are missing.
    """

    if fieldnames is None:
        raise ValueError("CSV file has no header")

    missing_columns = REQUIRED_COLUMNS - set(fieldnames)

    if missing_columns:
        raise ValueError(
            f"CSV file is missing required columns: "
            f"{', '.join(sorted(missing_columns))}"
        )


def load_csv(path: str | Path) -> list[Holiday]:
    """Load holidays from a CSV reference file.

    Supports both the v1 schema (date, name, category, source)
    and the v2 extended schema with authority and subdivision.
    """

    holidays: list[Holiday] = []

    with open(path, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        validate_schema(reader.fieldnames)

        for row in reader:
            if not row.get("date"):
                raise ValueError("Holiday date is required")

            if not row.get("name"):
                raise ValueError("Missing holiday name")

            try:
                holiday_date = date.fromisoformat(row["date"])
            except ValueError as exc:
                raise ValueError(f"Invalid date: {row['date']}") from exc

            holidays.append(
                Holiday(
                    date=holiday_date,
                    name=row["name"],
                    category=row.get("category") or "public",
                    source=row.get("source") or "unknown",
                    subdivision=row.get("subdivision") or None,
                    authority=row.get("authority") or None,
                )
            )

    return holidays


def discover_csv_files(
    base_dir: str | Path,
    country: str,
    *,
    subdivision: str | None = None,
    category: str | None = None,
) -> list[Path]:
    """Discover reference CSV files for a given country/subdivision.

    Searches the directory tree under ``base_dir/country/[subdivision/]``
    and optionally filters by category subdirectory.
    """

    root = Path(base_dir) / country

    if subdivision:
        root = root / subdivision

    if category:
        root = root / category

    if not root.exists():
        return []

    return sorted(root.rglob("*.csv"))


def write_csv(
    holidays: list[Holiday],
    path: str | Path,
    *,
    include_provenance: bool = True,
) -> Path:
    """Write holidays to a CSV file.

    Returns the path written to.
    """

    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = ["date", "name", "category", "source"]

    if include_provenance:
        fieldnames.extend(["authority", "subdivision"])

    with open(path, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        for holiday in sorted(holidays, key=lambda h: h.date):
            row: dict[str, str] = {
                "date": holiday.date.isoformat(),
                "name": holiday.name,
                "category": holiday.category,
                "source": holiday.source or "",
            }

            if include_provenance:
                row["authority"] = holiday.authority or ""
                row["subdivision"] = holiday.subdivision or ""

            writer.writerow(row)

    return path


def resolve_reference_path(
    data_dir: str | Path,
    country: str,
    year: int,
    *,
    subdivision: str | None = None,
    category: str = "public",
) -> Path | None:
    """Resolve the reference CSV file path for given parameters.

    Checks category-specific subdirectories (e.g. ``stock/``, ``bank/``,
    ``government/``) before falling back to the year file directly.
    """

    root = Path(data_dir) / country.upper()

    if subdivision:
        root = root / subdivision.upper()

    candidates: list[Path] = []

    if category == "financial":
        candidates.extend([
            root / "stock" / f"{year}.csv",
            root / "financial" / f"{year}.csv",
        ])
    elif category == "bank":
        candidates.extend([
            root / "bank" / f"{year}.csv",
        ])
    elif category in ("public", "government"):
        candidates.extend([
            root / "government" / f"{year}.csv",
            root / "public" / f"{year}.csv",
            root / f"{year}.csv",
        ])

    candidates.extend([
        root / category / f"{year}.csv",
        root / f"{year}.csv",
    ])

    for candidate in candidates:
        if candidate.exists():
            return candidate

    return None