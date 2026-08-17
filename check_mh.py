from holidaylens.compare import compare
from holidaylens.library import load_holidays
from holidaylens.report import format_report
from holidaylens.sources import load_csv


country = "IN"
subdivision = "MH"
year = 2026

reference = load_csv(
    "data/official/IN/MH/2026.csv"
)

dataset = load_holidays(
    country,
    subdiv=subdivision,
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