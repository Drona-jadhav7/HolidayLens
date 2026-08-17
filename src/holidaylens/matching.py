import re
from holidaylens.models import Holiday


def normalize_name(name: str) -> str:
    """Normalize a holiday name for comparison."""

    name = name.casefold()
    name = re.sub(r"[^\w\s]", " ", name)
    name = re.sub(r"\s+", " ", name)

    return name.strip()


def names_match(reference: Holiday, dataset: Holiday) -> bool:
    """Return whether two holidays have equivalent normalized names."""

    return normalize_name(reference.name) == normalize_name(dataset.name)