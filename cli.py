from __future__ import annotations

import argparse

from .comparator import compare_holidays
from .library import get_library_holidays
from .loader import load_official
from .report import print_results


def main():
    parser = argparse.ArgumentParser(
        description="Compare official holiday data with the holidays library."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    compare = subparsers.add_parser("compare")
    compare.add_argument("--country", required=True)
    compare.add_argument("--subdiv", default=None)
    compare.add_argument("--year", required=True, type=int)
    compare.add_argument("--official", required=True)
    compare.add_argument("--threshold", type=float, default=0.70)

    args = parser.parse_args()

    official = load_official(args.official)
    library = get_library_holidays(args.country, args.subdiv, args.year)
    results = compare_holidays(
        official, library, similarity_threshold=args.threshold
    )
    print_results(results, args.country, args.subdiv, args.year)
