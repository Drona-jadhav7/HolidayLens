import argparse
from pathlib import Path

from holidaylens.compare import compare
from holidaylens.library import load_holidays
from holidaylens.report import format_report
from holidaylens.sources import load_csv


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="holidaylens",
        description="Audit holiday calendars for data-quality issues.",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    audit_parser = subparsers.add_parser(
        "audit",
        help="Compare an official reference calendar with the holidays library.",
    )

    audit_parser.add_argument(
        "--country",
        required=True,
        help="ISO country code, for example IN.",
    )

    audit_parser.add_argument(
        "--subdivision",
        help="Subdivision code, for example MH.",
    )

    audit_parser.add_argument(
        "--year",
        required=True,
        type=int,
        help="Year to audit, for example 2026.",
    )

    audit_parser.add_argument(
        "--reference",
        type=Path,
        help="Path to a reference CSV file.",
    )

    return parser


def run_audit(args: argparse.Namespace) -> int:
    country = args.country.upper()
    subdivision = args.subdivision.upper() if args.subdivision else None

    if args.reference:
        reference_path = args.reference
    else:
        reference_path = Path("data") / "official" / country

        if subdivision:
            reference_path /= subdivision

        reference_path /= f"{args.year}.csv"

    if not reference_path.exists():
        print(f"Error: reference CSV not found: {reference_path}")
        return 2

    try:
        reference = load_csv(str(reference_path))
        dataset = load_holidays(
            country,
            subdiv=subdivision,
            years=args.year,
        )
    except (ValueError, KeyError) as exc:
        print(f"Error: {exc}")
        return 2

    results = compare(reference, dataset)

    report = format_report(
        results,
        country=country,
        subdivision=subdivision,
        year=args.year,
        reference_count=len(reference),
        dataset_count=len(dataset),
    )

    print(report)

    has_issues = any(
        result.status.value != "match"
        for result in results
    )

    return 1 if has_issues else 0


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "audit":
        return run_audit(args)

    parser.error("Unknown command")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
