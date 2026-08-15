from __future__ import annotations


def print_results(results, country, subdivision, year):
    print("\n" + "=" * 75)
    print("HOLIDAY GAP REPORT")
    print("=" * 75)
    print(f"Country       : {country}")
    print(f"Subdivision   : {subdivision or 'None'}")
    print(f"Year          : {year}")
    print(f"Exact matches : {len(results['match'])}")
    print(f"Review        : {len(results['review'])}")
    print(f"Missing       : {len(results['missing'])}")
    print(f"Extra         : {len(results['extra'])}")
    print(f"Date mismatch : {len(results['date_mismatch'])}")

    print("\n" + "-" * 75)
    print("MATCH")
    print("-" * 75)
    if not results["match"]:
        print("None")
    for item in results["match"]:
        print(
            f"{item['date']}: {item['official']} <-> "
            f"{item['library']} (similarity={item['similarity']})"
        )

    print("\n" + "-" * 75)
    print("REVIEW — SAME DATE, DIFFERENT/UNCERTAIN NAME")
    print("-" * 75)
    if not results["review"]:
        print("None")
    for item in results["review"]:
        print(f"\nDate: {item['date']}")
        print(f"  Official: {item['official']}")
        print(f"  Library : {item['library']}")
        print(f"  Similarity: {item['similarity']}")

    print("\n" + "-" * 75)
    print("POTENTIALLY MISSING FROM HOLIDAYS LIBRARY")
    print("-" * 75)
    if not results["missing"]:
        print("None")
    for item in results["missing"]:
        print(f"{item['date']}: {item['official']} [type={item['type']}]")

    print("\n" + "-" * 75)
    print("POTENTIALLY EXTRA IN HOLIDAYS LIBRARY")
    print("-" * 75)
    if not results["extra"]:
        print("None")
    for item in results["extra"]:
        print(f"{item['date']}: {item['library']}")

    print("\n" + "-" * 75)
    print("POSSIBLE DATE MISMATCHES")
    print("-" * 75)
    if not results["date_mismatch"]:
        print("None")
    for item in results["date_mismatch"]:
        print(
            f"\nOfficial: {item['official_date']} {item['official']}\n"
            f"Library : {item['library_date']} {item['library']}\n"
            f"Similarity: {item['similarity']}"
        )
