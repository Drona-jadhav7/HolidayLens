import re


def normalize_name(name: str) -> str:
    """Normalize a holiday name for comparison."""

    name = name.casefold()
    name = re.sub(r"[^\w\s]", " ", name)
    name = re.sub(r"\s+", " ", name)

    return name.strip()