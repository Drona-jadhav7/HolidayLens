import re

from holidaylens.models import Holiday


def normalize_name(name: str) -> str:
    """Normalize a holiday name for comparison."""

    name = name.casefold()
    name = re.sub(r"[^\w\s]", " ", name)
    name = re.sub(r"\s+", " ", name)

    return name.strip()


def split_names(name: str) -> list[str]:
    """Split a combined holiday name into individual names."""

    return [
        normalize_name(part)
        for part in name.split(";")
        if part.strip()
    ]


def names_match(reference: Holiday, dataset: Holiday) -> bool:
    """Return whether the dataset contains the reference holiday name."""

    reference_name = normalize_name(reference.name)
    dataset_names = split_names(dataset.name)

    return reference_name in dataset_names