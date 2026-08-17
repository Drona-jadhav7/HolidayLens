from dataclasses import dataclass
from enum import Enum

from holidaylens.matching import names_match
from holidaylens.models import Holiday


class MatchStatus(Enum):
    MATCH = "match"
    MISSING = "missing"
    EXTRA = "extra"
    NAME_MISMATCH = "name_mismatch"


@dataclass(frozen=True)
class Comparison:
    status: MatchStatus
    reference: Holiday | None = None
    dataset: Holiday | None = None


def compare(
    reference: list[Holiday],
    dataset: list[Holiday],
) -> list[Comparison]:
    """Compare reference holidays against dataset holidays."""

    results: list[Comparison] = []

    used_dataset: set[int] = set()

    for reference_index, reference_holiday in enumerate(reference):
        matched_index = None

        for dataset_index, dataset_holiday in enumerate(dataset):
            if dataset_index in used_dataset:
                continue

            if reference_holiday.date != dataset_holiday.date:
                continue

            if names_match(reference_holiday, dataset_holiday):
                matched_index = dataset_index
                break

        if matched_index is not None:
            used_dataset.add(matched_index)

            results.append(
                Comparison(
                    status=MatchStatus.MATCH,
                    reference=reference_holiday,
                    dataset=dataset[matched_index],
                )
            )
            continue

        same_date_index = next(
            (
                index
                for index, holiday in enumerate(dataset)
                if index not in used_dataset
                and holiday.date == reference_holiday.date
            ),
            None,
        )

        if same_date_index is not None:
            used_dataset.add(same_date_index)

            results.append(
                Comparison(
                    status=MatchStatus.NAME_MISMATCH,
                    reference=reference_holiday,
                    dataset=dataset[same_date_index],
                )
            )
        else:
            results.append(
                Comparison(
                    status=MatchStatus.MISSING,
                    reference=reference_holiday,
                )
            )

    for dataset_index, dataset_holiday in enumerate(dataset):
        if dataset_index not in used_dataset:
            results.append(
                Comparison(
                    status=MatchStatus.EXTRA,
                    dataset=dataset_holiday,
                )
            )

    return results