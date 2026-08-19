from holidaylens.aliases import canonical_name
from holidaylens.models import Holiday
from holidaylens.normalization import normalize_name


def split_names(name: str) -> list[str]:
    """Split a combined holiday name into individual names."""

    return [
        part.strip()
        for part in name.split(";")
        if part.strip()
    ]


def names_match(reference: Holiday, dataset: Holiday) -> bool:
    """Return whether the dataset contains the reference holiday name."""

    reference_name = canonical_name(reference.name)

    dataset_names = [
        canonical_name(name)
        for name in split_names(dataset.name)
    ]

    return reference_name in dataset_names