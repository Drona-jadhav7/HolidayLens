"""CLI with subcommands for auditing, suite runs, and report generation.

Subcommands:
  audit    – Compare a single reference calendar against the holidays library
  suite    – Run batch audits across multiple countries/categories
  extract  – Run an extractor to harvest official holiday data
  report   – Generate a GitHub issue or PR template from a JSON report
  list     – List registered extractors
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from holidaylens.compare import compare
from holidaylens.library import (
    load_bank_holidays,
    load_financial_holidays,
    load_holidays,
)
from holidaylens.report import (
    format_report,
    generate_github_issue,
    report_data,
    save_json_report,
)
from holidaylens.sources import load_csv, resolve_reference_path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="holidaylens",
        description="Audit holiday calendars for data-quality issues.",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # ── audit ──────────────────────────────────────────────────────
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

    audit_parser.add_argument(
        "--category",
        choices=("public", "bank", "financial"),
        default="public",
        help="Holiday category to audit. Defaults to public.",
    )

    audit_parser.add_argument(
        "--market",
        help="Financial market code (e.g. XNSE, XTKS). Required for financial category.",
    )

    audit_parser.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        help="Output format. Defaults to text.",
    )

    audit_parser.add_argument(
        "--output",
        type=Path,
        help="Save JSON report to file (only with --format json).",
    )

    # ── suite ──────────────────────────────────────────────────────
    suite_parser = subparsers.add_parser(
        "suite",
        help="Run batch audits across multiple countries.",
    )

    suite_parser.add_argument(
        "--year",
        required=True,
        type=int,
        help="Year to audit.",
    )

    suite_parser.add_argument(
        "--data-dir",
        type=Path,
        default=Path("data/official"),
        help="Root directory for reference data.",
    )

    suite_parser.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        help="Output format.",
    )

    # ── extract ────────────────────────────────────────────────────
    extract_parser = subparsers.add_parser(
        "extract",
        help="Run an extractor to harvest official holiday data.",
    )

    extract_parser.add_argument(
        "--country",
        required=True,
        help="ISO country code.",
    )

    extract_parser.add_argument(
        "--category",
        default="government",
        help="Extractor category (government, bank, financial).",
    )

    extract_parser.add_argument(
        "--year",
        required=True,
        type=int,
        help="Year to extract.",
    )

    extract_parser.add_argument(
        "--output",
        type=Path,
        help="Output CSV path.",
    )

    # ── report ─────────────────────────────────────────────────────
    report_parser = subparsers.add_parser(
        "report",
        help="Generate a GitHub issue template from a JSON report.",
    )

    report_parser.add_argument(
        "input",
        nargs="?",
        type=Path,
        help="Path to a JSON report file.",
    )

    report_parser.add_argument(
        "--input",
        dest="input_opt",
        type=Path,
        help="Path to a JSON report file (alternative to positional argument).",
    )

    report_parser.add_argument(
        "--output",
        type=Path,
        help="Save GitHub issue markdown to file.",
    )

    # ── list ───────────────────────────────────────────────────────
    subparsers.add_parser(
        "list",
        help="List registered extractors.",
    )

    return parser


def _load_dataset_for_audit(args: argparse.Namespace, country: str):
    """Load the appropriate dataset based on audit arguments."""

    subdivision = args.subdivision.upper() if args.subdivision else None

    if args.category == "financial":
        market = args.market or "XNSE"
        return load_financial_holidays(market, years=args.year)

    if args.category == "bank":
        return load_bank_holidays(
            country,
            subdiv=subdivision,
            years=args.year,
        )

    language = "en_US" if country in ("JP", "TH", "KR") else None
    return load_holidays(
        country,
        subdiv=subdivision,
        years=args.year,
        language=language,
    )


def run_audit(args: argparse.Namespace) -> int:
    country = args.country.upper()
    subdivision = args.subdivision.upper() if args.subdivision else None

    category = getattr(args, "category", "public")

    if args.reference:
        reference_path = args.reference
    else:
        reference_path = resolve_reference_path(
            Path("data") / "official",
            country,
            args.year,
            subdivision=subdivision,
            category=category,
        )

    if reference_path is None or not Path(reference_path).exists():
        print(f"Error: reference CSV not found: {reference_path or f'{country}/{args.year}.csv'}")
        return 2

    try:
        reference = load_csv(str(reference_path))
        dataset = _load_dataset_for_audit(args, country)
    except (ValueError, KeyError, ImportError) as exc:
        print(f"Error: {exc}")
        return 2

    results = compare(reference, dataset)

    category = getattr(args, "category", "public")

    if args.format == "json":
        data = report_data(
            results,
            country=country,
            subdivision=subdivision,
            year=args.year,
            reference_count=len(reference),
            dataset_count=len(dataset),
            category=category,
        )

        output = json.dumps(data, indent=2, ensure_ascii=False)
        print(output)

        if args.output:
            save_json_report(data, args.output)
            print(f"\nReport saved to {args.output}")
    else:
        print(
            format_report(
                results,
                country=country,
                subdivision=subdivision,
                year=args.year,
                reference_count=len(reference),
                dataset_count=len(dataset),
                category=category,
            )
        )

    has_issues = any(
        result.status.value != "match"
        for result in results
    )

    return 1 if has_issues else 0


def run_suite_command(args: argparse.Namespace) -> int:
    from holidaylens.suite import build_asia_suite, run_suite

    suite_config = build_asia_suite(
        args.year,
        data_dir=args.data_dir,
    )

    if not suite_config.audits:
        print(f"No reference data found for year {args.year}")
        return 2

    suite_result = run_suite(suite_config)

    print(f"Suite Results: {args.year}")
    print("-" * 32)
    print(f"Total audits:  {suite_result.total_audits}")
    print(f"Passed:        {suite_result.passed}")
    print(f"Failed:        {suite_result.failed}")
    print(f"Errors:        {suite_result.errored}")
    print()

    for result in suite_result.results:
        status = "[PASS]" if not result.has_issues else "[FAIL]"
        label = f"{result.country}/{result.subdivision or 'national'}"
        print(
            f"  {status} {label:<20} "
            f"coverage={result.coverage}% "
            f"({result.category})"
        )

    for config, error in suite_result.errors:
        label = f"{config.country}/{config.subdivision or 'national'}"
        print(f"  [!] {label:<20} ERROR: {error}")

    return 1 if suite_result.failed > 0 or suite_result.errored > 0 else 0


def run_extract(args: argparse.Namespace) -> int:
    from holidaylens.extractors.registry import get_extractor
    from holidaylens.sources import write_csv

    # Ensure Asian extractors are registered
    import holidaylens.extractors.asia  # noqa: F401

    country = args.country.upper()
    extractor = get_extractor(country, args.category)

    if extractor is None:
        print(f"No extractor registered for {country}/{args.category}")
        return 2

    result = extractor.extract(args.year)

    if result.errors:
        for error in result.errors:
            print(f"Error: {error}")
        return 2

    for warning in result.warnings:
        print(f"Warning: {warning}")

    if not result.holidays:
        print("No holidays extracted.")
        return 2

    if args.output:
        write_csv(result.holidays, args.output)
        print(f"Wrote {len(result.holidays)} holidays to {args.output}")
    else:
        for holiday in result.holidays:
            print(f"{holiday.date.isoformat()}\t{holiday.name}")

    return 0


def run_report(args: argparse.Namespace) -> int:
    input_path = args.input or args.input_opt

    if not input_path:
        print("Error: input JSON file is required.")
        return 2

    if not input_path.exists():
        print(f"Error: file not found: {input_path}")
        return 2

    with open(input_path, encoding="utf-8") as f:
        data = json.load(f)

    issue_md = generate_github_issue(data)

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(issue_md, encoding="utf-8")
        print(f"GitHub issue template saved to {args.output}")
    else:
        print(issue_md)

    return 0


def run_list_command(args: argparse.Namespace) -> int:
    from holidaylens.extractors.registry import list_extractors

    # Ensure Asian extractors are registered
    import holidaylens.extractors.asia  # noqa: F401

    extractors = list_extractors()

    if not extractors:
        print("No extractors registered.")
        return 0

    print(f"{'Country':<10} {'Category':<15} {'Class'}")
    print("-" * 50)

    for country, category, class_name in extractors:
        print(f"{country:<10} {category:<15} {class_name}")

    return 0


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "audit":
        return run_audit(args)

    if args.command == "suite":
        return run_suite_command(args)

    if args.command == "extract":
        return run_extract(args)

    if args.command == "report":
        return run_report(args)

    if args.command == "list":
        return run_list_command(args)

    parser.error("Unknown command")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
