from __future__ import annotations

from .normalizer import name_similarity


def _group_by_date(df):
    result = {}
    for _, row in df.iterrows():
        result.setdefault(row["date"], []).append(row)
    return result


def compare_holidays(official, library, similarity_threshold: float = 0.70) -> dict:
    results = {
        "match": [], "review": [], "missing": [], "extra": [], "date_mismatch": []
    }

    official_by_date = _group_by_date(official)
    library_by_date = _group_by_date(library)
    official_dates = set(official_by_date)
    library_dates = set(library_by_date)

    for holiday_date in sorted(official_dates & library_dates):
        official_rows = official_by_date[holiday_date]
        library_rows = library_by_date[holiday_date]
        used_library = set()

        for official_row in official_rows:
            best_index = None
            best_row = None
            best_score = 0.0

            for index, library_row in enumerate(library_rows):
                if index in used_library:
                    continue
                score = name_similarity(
                    official_row["name"], library_row["name"]
                )
                if score > best_score:
                    best_score = score
                    best_index = index
                    best_row = library_row

            if best_row is None:
                results["review"].append({
                    "date": holiday_date,
                    "official": official_row["name"],
                    "library": None,
                    "similarity": 0.0,
                })
                continue

            used_library.add(best_index)
            item = {
                "date": holiday_date,
                "official": official_row["name"],
                "library": best_row["name"],
                "similarity": round(best_score, 2),
            }

            if best_score >= similarity_threshold:
                results["match"].append(item)
            else:
                results["review"].append(item)

        for index, library_row in enumerate(library_rows):
            if index not in used_library:
                results["review"].append({
                    "date": holiday_date,
                    "official": None,
                    "library": library_row["name"],
                    "similarity": 0.0,
                })

    for holiday_date in sorted(official_dates - library_dates):
        for row in official_by_date[holiday_date]:
            results["missing"].append({
                "date": holiday_date,
                "official": row["name"],
                "type": row["type"],
            })

    for holiday_date in sorted(library_dates - official_dates):
        for row in library_by_date[holiday_date]:
            results["extra"].append({
                "date": holiday_date,
                "library": row["name"],
            })

    for missing in results["missing"]:
        best = None
        best_score = 0.0
        for extra in results["extra"]:
            score = name_similarity(missing["official"], extra["library"])
            if score > best_score:
                best_score = score
                best = extra

        if best is not None and best_score >= similarity_threshold:
            results["date_mismatch"].append({
                "official_date": missing["date"],
                "official": missing["official"],
                "library_date": best["date"],
                "library": best["library"],
                "similarity": round(best_score, 2),
            })

    return results
