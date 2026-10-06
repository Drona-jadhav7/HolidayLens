"""Normalized token matching & alias resolution.

Provides matching functions that handle semicolon-delimited multi-holiday
names, alias resolution, and fuzzy token overlap.
"""

from __future__ import annotations

from holidaylens.aliases import canonical_name
from holidaylens.models import Holiday
from holidaylens.normalization import normalize_name, similarity_score


def split_names(name: str) -> list[str]:
    """Split a combined holiday name into individual names.

    The ``holidays`` library sometimes combines multiple holidays on
    the same date with a semicolon separator.
    """

    return [
        part.strip()
        for part in name.split(";")
        if part.strip()
    ]


def names_match(reference: Holiday, dataset: Holiday) -> bool:
    """Return whether the dataset contains the reference holiday name.

    Checks exact canonical match first.  If either side has
    semicolon-delimited names, checks each sub-name independently.
    """

    reference_name = canonical_name(reference.name)

    dataset_names = [
        canonical_name(name)
        for name in split_names(dataset.name)
    ]

    return reference_name in dataset_names


def fuzzy_names_match(
    reference: Holiday,
    dataset: Holiday,
    *,
    threshold: float = 0.5,
) -> bool:
    """Return whether names match above the similarity threshold.

    Uses Jaccard similarity on normalized tokens.  The default threshold
    of 0.5 captures most transliteration variants while avoiding false
    positives on unrelated holidays.
    """

    ref_canonical = canonical_name(reference.name)

    for name in split_names(dataset.name):
        ds_canonical = canonical_name(name)

        if ref_canonical == ds_canonical:
            return True

        if similarity_score(ref_canonical, ds_canonical) >= threshold:
            return True

    return False


def best_name_match(
    reference: Holiday,
    candidates: list[Holiday],
) -> tuple[int, float] | None:
    """Find the best matching candidate by name similarity.

    Returns ``(index, score)`` of the best match, or ``None`` if no
    candidate scores above 0.0.
    """

    best_index: int | None = None
    best_score = 0.0

    ref_canonical = canonical_name(reference.name)

    for index, candidate in enumerate(candidates):
        for name in split_names(candidate.name):
            score = similarity_score(ref_canonical, canonical_name(name))

            if score > best_score:
                best_score = score
                best_index = index

    if best_index is None or best_score <= 0.0:
        return None

    return best_index, best_score