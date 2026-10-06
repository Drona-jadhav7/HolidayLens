"""Text normalization utilities for holiday name comparison.

Handles Unicode decomposition, accent stripping, casing, and punctuation
rules to produce a canonical token stream for fuzzy matching.
"""

from __future__ import annotations

import re
import unicodedata


def strip_accents(text: str) -> str:
    """Remove diacritics/accents by decomposing Unicode and dropping combining marks."""

    nfkd = unicodedata.normalize("NFKD", text)

    return "".join(
        char
        for char in nfkd
        if unicodedata.category(char) != "Mn"
    )


def normalize_name(name: str) -> str:
    """Normalize a holiday name for comparison.

    Pipeline:
    1. Strip accents / diacritics
    2. Casefold for locale-insensitive comparison
    3. Replace all non-word / non-space chars with a space
    4. Collapse runs of whitespace
    5. Strip leading/trailing whitespace
    """

    name = strip_accents(name)
    name = name.casefold()
    name = re.sub(r"[^\w\s]", " ", name)
    name = re.sub(r"\s+", " ", name)

    return name.strip()


def normalize_tokens(name: str) -> set[str]:
    """Return the set of normalized word tokens from a holiday name.

    Useful for token-level comparison where word order does not matter.
    """

    return set(normalize_name(name).split())


def similarity_score(name_a: str, name_b: str) -> float:
    """Compute Jaccard similarity between two holiday name token sets.

    Returns a value between 0.0 (no overlap) and 1.0 (identical).
    """

    tokens_a = normalize_tokens(name_a)
    tokens_b = normalize_tokens(name_b)

    if not tokens_a and not tokens_b:
        return 1.0

    if not tokens_a or not tokens_b:
        return 0.0

    intersection = tokens_a & tokens_b
    union = tokens_a | tokens_b

    return len(intersection) / len(union)