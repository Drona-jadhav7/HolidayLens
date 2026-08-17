import csv
from datetime import date

from holidaylens.models import Holiday


REQUIRED_COLUMNS = {"date", "name"}


def load_csv(path: str) -> list[Holiday]:
    """Load holidays from a CSV reference file."""

    holidays = []

    with open(path, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        if reader.fieldnames is None:
            raise ValueError("CSV file has no header")

        missing_columns = REQUIRED_COLUMNS - set(reader.fieldnames)

        if missing_columns:
            raise ValueError(
                f"CSV file is missing required columns: "
                f"{', '.join(sorted(missing_columns))}"
            )

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
                )
            )

    return holidays