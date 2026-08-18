from dataclasses import dataclass
from enum import Enum

from holidaylens.matching import names_match
from holidaylens.models import Holiday


class MatchStatus(Enum):
    MATCH = "match"
    MISSING = "missing"
    EXTRA = "extra"
    NAME_MISMATCH = "name_mismatch"
    DATE_MISMATCH = "date_mismatch"


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

    for reference_holiday in reference:
        matched_index = None

        # 1. Same date + same name -> MATCH
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

        # 2. Same date + different name -> NAME_MISMATCH
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
            continue

        # 3. Different date + same name -> DATE_MISMATCH
        date_mismatch_index = next(
            (
                index
                for index, holiday in enumerate(dataset)
                if index not in used_dataset
                and names_match(reference_holiday, holiday)
            ),
            None,
        )

        if date_mismatch_index is not None:
            used_dataset.add(date_mismatch_index)

            results.append(
                Comparison(
                    status=MatchStatus.DATE_MISMATCH,
                    reference=reference_holiday,
                    dataset=dataset[date_mismatch_index],
                )
            )
            continue

        # 4. No corresponding holiday -> MISSING
        results.append(
            Comparison(
                status=MatchStatus.MISSING,
                reference=reference_holiday,
            )
        )

    # 5. Anything unused in the dataset -> EXTRA
    for dataset_index, dataset_holiday in enumerate(dataset):
        if dataset_index not in used_dataset:
            results.append(
                Comparison(
                    status=MatchStatus.EXTRA,
                    dataset=dataset_holiday,
                )
            )

    return results