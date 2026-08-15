from __future__ import annotations

import re
from difflib import SequenceMatcher


def normalize_name(name: str) -> str:
    """Normalize superficial formatting differences only."""
    value = str(name).lower().strip()
    value = re.sub(r"[^\w\s]", " ", value)
    return " ".join(value.split())


def name_similarity(name1: str, name2: str) -> float:
    return SequenceMatcher(
        None, normalize_name(name1), normalize_name(name2)
    ).ratio()
