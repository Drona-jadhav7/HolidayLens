import csv
from datetime import date
from pathlib import Path

from holidaylens.models import Holiday


REQUIRED_COLUMNS = {"date", "name"}


def load_csv(path: str | Path) -> list[Holiday]:
    """Load holidays from a CSV file."""
    path = Path(path)

    with path.open("r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)

        if reader.fieldnames is None:
            raise ValueError("CSV file is missing a header.")

        missing = REQUIRED_COLUMNS - set(reader.fieldnames)
        if missing:
            raise ValueError(
                f"CSV file is missing required columns: {', '.join(sorted(missing))}"
            )

        holidays = []

        for row_number, row in enumerate(reader, start=2):
            raw_date = (row.get("date") or "").strip()
            name = (row.get("name") or "").strip()

            if not raw_date:
                raise ValueError(f"Missing date on CSV row {row_number}.")

            if not name:
                raise ValueError(f"Missing holiday name on CSV row {row_number}.")

            try:
                holiday_date = date.fromisoformat(raw_date)
            except ValueError as exc:
                raise ValueError(
                    f"Invalid date on CSV row {row_number}: {raw_date!r}"
                ) from exc

            category = (row.get("category") or "public").strip()
            source = (row.get("source") or "").strip() or None

            holidays.append(
                Holiday(
                    date=holiday_date,
                    name=name,
                    category=category,
                    source=source,
                )
            )

    return holidays