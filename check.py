from holidaylens.compare import compare
from holidaylens.library import load_holidays
from holidaylens.report import format_report
from holidaylens.sources import load_csv


country = "ET"
subdivision = ""
year = 2026

reference = load_csv(
    "data/official/ET/2026.csv"
)

dataset = load_holidays(
    country,
    years=year,
)

results = compare(reference, dataset)

print(
    format_report(
        results,
        country=country,
        subdivision=subdivision,
        year=year,
        reference_count=len(reference),
        dataset_count=len(dataset),
    )
)