from __future__ import annotations

from dataclasses import dataclass
from math import ceil
from typing import Iterable

from .operators import RapSignature, ced_confluence, ced_state, rap_signature


@dataclass(frozen=True)
class CandidatePartition:
    N: int
    a: int
    b: int
    a_rap: RapSignature
    b_rap: RapSignature
    n_rap: RapSignature
    epsilon: int
    center_distance: float
    ced_pair: tuple[str, str]
    ced_result: str
    pair_rap_integrity: int
    combined_rap_loss: int
    is_goldbach_pair: bool

    @property
    def key(self) -> tuple[int, int]:
        return (self.a, self.b)


@dataclass(frozen=True)
class CommutatorObservation:
    N: int
    r: float
    min_term: int
    candidate_count: int
    ced_count: int
    rap_count: int
    ced_after_rap: tuple[tuple[int, int], ...]
    rap_after_ced: tuple[tuple[int, int], ...]
    intersection_count: int
    union_count: int
    distance: float


@dataclass(frozen=True)
class KappaWindow:
    start: int
    end: int
    r: float
    min_term: int
    observations: tuple[CommutatorObservation, ...]
    kappa: float


@dataclass(frozen=True)
class RapRankingObservation:
    N: int
    r: float
    min_term: int
    direction: str
    selected_count: int
    goldbach_selected: int
    goldbach_total: int
    precision: float
    recall: float
    selected_pairs: tuple[tuple[int, int], ...]


@dataclass(frozen=True)
class RapRankingWindow:
    start: int
    end: int
    r: float
    min_term: int
    direction: str
    observations: tuple[RapRankingObservation, ...]
    selected_total: int
    goldbach_selected_total: int
    goldbach_total: int
    mean_precision: float
    mean_recall: float
    pooled_precision: float
    pooled_recall: float
    combined_rap_loss_auc_higher_for_goldbach: float
    combined_rap_loss_separation_auc: float
    combined_rap_loss_preferred_direction: str


@dataclass(frozen=True)
class CandidateFeatureRow:
    N: int
    a: int
    b: int
    is_goldbach_pair: bool
    a_potential: int
    b_potential: int
    n_potential: int
    a_loss: int
    b_loss: int
    loss_sum: int
    a_integrity: int
    b_integrity: int
    integrity_sum: int
    integrity_defect: int
    combined_rap_loss: int
    epsilon: int
    center_distance: float
    ced_a: str
    ced_b: str
    ced_is_dd: bool

    @property
    def key(self) -> tuple[int, int]:
        return (self.a, self.b)


@dataclass(frozen=True)
class FeatureSeparation:
    feature: str
    positive_count: int
    negative_count: int
    positive_mean: float
    negative_mean: float
    auc_higher_for_goldbach: float
    separation_auc: float
    preferred_direction: str


FEATURE_NAMES = (
    "a_potential",
    "b_potential",
    "a_loss",
    "b_loss",
    "loss_sum",
    "a_integrity",
    "b_integrity",
    "integrity_sum",
    "integrity_defect",
    "combined_rap_loss",
    "epsilon",
    "center_distance",
    "ced_is_dd",
)


def candidate_partitions(even_number: int, *, min_term: int = 1) -> tuple[CandidatePartition, ...]:
    if even_number <= 2 or even_number % 2 != 0:
        raise ValueError("Candidate partitions require an even number greater than 2.")
    if min_term < 1:
        raise ValueError("min_term must be at least 1.")

    n_rap = rap_signature(even_number)
    partitions: list[CandidatePartition] = []

    for a in range(min_term, (even_number // 2) + 1):
        b = even_number - a
        if b < min_term:
            continue

        a_rap = rap_signature(a)
        b_rap = rap_signature(b)
        a_state = ced_state(a)
        b_state = ced_state(b)

        partitions.append(
            CandidatePartition(
                N=even_number,
                a=a,
                b=b,
                a_rap=a_rap,
                b_rap=b_rap,
                n_rap=n_rap,
                epsilon=abs(a - b),
                center_distance=abs(a - (even_number / 2)),
                ced_pair=(a_state, b_state),
                ced_result=ced_confluence(a_state, b_state),
                pair_rap_integrity=a_rap.integrity + b_rap.integrity,
                combined_rap_loss=a_rap.potential + b_rap.potential - n_rap.potential,
                is_goldbach_pair=a_rap.is_prime and b_rap.is_prime,
            )
        )

    return tuple(partitions)


def ced_operator(partitions: Iterable[CandidatePartition]) -> tuple[CandidatePartition, ...]:
    return tuple(item for item in partitions if item.ced_pair == ("D", "D"))


def rap_order_key(partition: CandidatePartition) -> tuple[int, int, int, int]:
    return (
        partition.combined_rap_loss,
        partition.pair_rap_integrity,
        partition.epsilon,
        partition.a,
    )


def rap_selection_operator(partitions: Iterable[CandidatePartition], r: float) -> tuple[CandidatePartition, ...]:
    if r <= 0.0 or r > 1.0:
        raise ValueError("r must satisfy 0 < r <= 1.")

    ordered = tuple(sorted(partitions, key=rap_order_key))
    if not ordered:
        return ()

    cutoff_index = ceil(r * len(ordered)) - 1
    cutoff_loss = ordered[cutoff_index].combined_rap_loss
    return tuple(item for item in ordered if item.combined_rap_loss <= cutoff_loss)


def rap_reverse_order_key(partition: CandidatePartition) -> tuple[int, int, int, int]:
    return (
        -partition.combined_rap_loss,
        partition.pair_rap_integrity,
        partition.epsilon,
        partition.a,
    )


def rap_reverse_selection_operator(partitions: Iterable[CandidatePartition], r: float) -> tuple[CandidatePartition, ...]:
    if r <= 0.0 or r > 1.0:
        raise ValueError("r must satisfy 0 < r <= 1.")

    ordered = tuple(sorted(partitions, key=rap_reverse_order_key))
    if not ordered:
        return ()

    cutoff_index = ceil(r * len(ordered)) - 1
    cutoff_loss = ordered[cutoff_index].combined_rap_loss
    return tuple(item for item in ordered if item.combined_rap_loss >= cutoff_loss)


def rap_selection_by_direction(
    partitions: Iterable[CandidatePartition],
    r: float,
    *,
    direction: str = "min",
) -> tuple[CandidatePartition, ...]:
    if direction == "min":
        return rap_selection_operator(partitions, r)
    if direction == "max":
        return rap_reverse_selection_operator(partitions, r)
    raise ValueError("direction must be 'min' or 'max'.")


def partition_keys(partitions: Iterable[CandidatePartition]) -> frozenset[tuple[int, int]]:
    return frozenset(item.key for item in partitions)


def inverse_jaccard_distance(
    left: Iterable[CandidatePartition],
    right: Iterable[CandidatePartition],
) -> float:
    left_keys = partition_keys(left)
    right_keys = partition_keys(right)
    union = left_keys | right_keys
    if not union:
        return 0.0
    return 1.0 - (len(left_keys & right_keys) / len(union))


def commutator_observation(even_number: int, r: float, *, min_term: int = 1) -> CommutatorObservation:
    candidates = candidate_partitions(even_number, min_term=min_term)
    ced_first = ced_operator(candidates)
    rap_first = rap_selection_operator(candidates, r)
    ced_after_rap = ced_operator(rap_first)
    rap_after_ced = rap_selection_operator(ced_first, r)
    left_keys = partition_keys(ced_after_rap)
    right_keys = partition_keys(rap_after_ced)
    union = left_keys | right_keys

    return CommutatorObservation(
        N=even_number,
        r=r,
        min_term=min_term,
        candidate_count=len(candidates),
        ced_count=len(ced_first),
        rap_count=len(rap_first),
        ced_after_rap=tuple(sorted(left_keys)),
        rap_after_ced=tuple(sorted(right_keys)),
        intersection_count=len(left_keys & right_keys),
        union_count=len(union),
        distance=0.0 if not union else 1.0 - (len(left_keys & right_keys) / len(union)),
    )


def kappa_window(start: int, end: int, r: float, *, min_term: int = 1) -> KappaWindow:
    if start > end:
        raise ValueError("start must be less than or equal to end.")

    first = start if start % 2 == 0 else start + 1
    last = end if end % 2 == 0 else end - 1
    observations = tuple(
        commutator_observation(even_number, r, min_term=min_term)
        for even_number in range(first, last + 1, 2)
        if even_number > 2
    )
    kappa = 0.0 if not observations else sum(item.distance for item in observations) / len(observations)

    return KappaWindow(
        start=first,
        end=last,
        r=r,
        min_term=min_term,
        observations=observations,
        kappa=kappa,
    )


def rap_ranking_observation(
    even_number: int,
    r: float,
    *,
    min_term: int = 1,
    direction: str = "min",
) -> RapRankingObservation:
    candidates = candidate_partitions(even_number, min_term=min_term)
    selected = rap_selection_by_direction(candidates, r, direction=direction)
    selected_keys = tuple(item.key for item in selected)
    goldbach_total = sum(1 for item in candidates if item.is_goldbach_pair)
    goldbach_selected = sum(1 for item in selected if item.is_goldbach_pair)
    precision = 0.0 if not selected else goldbach_selected / len(selected)
    recall = 0.0 if goldbach_total == 0 else goldbach_selected / goldbach_total

    return RapRankingObservation(
        N=even_number,
        r=r,
        min_term=min_term,
        direction=direction,
        selected_count=len(selected),
        goldbach_selected=goldbach_selected,
        goldbach_total=goldbach_total,
        precision=precision,
        recall=recall,
        selected_pairs=selected_keys,
    )


def rap_reverse_ranking_observation(even_number: int, r: float, *, min_term: int = 1) -> RapRankingObservation:
    return rap_ranking_observation(even_number, r, min_term=min_term, direction="max")


def rap_ranking_window(
    start: int,
    end: int,
    r: float,
    *,
    min_term: int = 1,
    direction: str = "min",
) -> RapRankingWindow:
    if start > end:
        raise ValueError("start must be less than or equal to end.")

    first = start if start % 2 == 0 else start + 1
    last = end if end % 2 == 0 else end - 1
    observations = tuple(
        rap_ranking_observation(even_number, r, min_term=min_term, direction=direction)
        for even_number in range(first, last + 1, 2)
        if even_number > 2
    )
    selected_total = sum(item.selected_count for item in observations)
    goldbach_selected_total = sum(item.goldbach_selected for item in observations)
    goldbach_total = sum(item.goldbach_total for item in observations)
    separation = feature_separation_window(
        first,
        last,
        min_term=min_term,
        features=("combined_rap_loss",),
    )[0]

    return RapRankingWindow(
        start=first,
        end=last,
        r=r,
        min_term=min_term,
        direction=direction,
        observations=observations,
        selected_total=selected_total,
        goldbach_selected_total=goldbach_selected_total,
        goldbach_total=goldbach_total,
        mean_precision=_mean([item.precision for item in observations]),
        mean_recall=_mean([item.recall for item in observations]),
        pooled_precision=0.0 if selected_total == 0 else goldbach_selected_total / selected_total,
        pooled_recall=0.0 if goldbach_total == 0 else goldbach_selected_total / goldbach_total,
        combined_rap_loss_auc_higher_for_goldbach=separation.auc_higher_for_goldbach,
        combined_rap_loss_separation_auc=separation.separation_auc,
        combined_rap_loss_preferred_direction=separation.preferred_direction,
    )


def feature_matrix(even_number: int, *, min_term: int = 1) -> tuple[CandidateFeatureRow, ...]:
    return tuple(feature_row_from_partition(item) for item in candidate_partitions(even_number, min_term=min_term))


def feature_row_from_partition(partition: CandidatePartition) -> CandidateFeatureRow:
    return CandidateFeatureRow(
        N=partition.N,
        a=partition.a,
        b=partition.b,
        is_goldbach_pair=partition.is_goldbach_pair,
        a_potential=partition.a_rap.potential,
        b_potential=partition.b_rap.potential,
        n_potential=partition.n_rap.potential,
        a_loss=partition.a_rap.loss,
        b_loss=partition.b_rap.loss,
        loss_sum=partition.a_rap.loss + partition.b_rap.loss,
        a_integrity=partition.a_rap.integrity,
        b_integrity=partition.b_rap.integrity,
        integrity_sum=partition.pair_rap_integrity,
        integrity_defect=partition.pair_rap_integrity - partition.n_rap.integrity,
        combined_rap_loss=partition.combined_rap_loss,
        epsilon=partition.epsilon,
        center_distance=partition.center_distance,
        ced_a=partition.ced_pair[0],
        ced_b=partition.ced_pair[1],
        ced_is_dd=partition.ced_pair == ("D", "D"),
    )


def feature_value(row: CandidateFeatureRow, feature: str) -> float:
    if feature not in FEATURE_NAMES:
        raise ValueError(f"Unknown feature: {feature}")

    value = getattr(row, feature)
    if isinstance(value, bool):
        return 1.0 if value else 0.0
    return float(value)


def feature_separation(
    rows: Iterable[CandidateFeatureRow],
    *,
    features: Iterable[str] = FEATURE_NAMES,
) -> tuple[FeatureSeparation, ...]:
    row_tuple = tuple(rows)
    separations = tuple(_separate_feature(row_tuple, feature) for feature in features)
    return tuple(sorted(separations, key=lambda item: item.separation_auc, reverse=True))


def feature_separation_for_even(
    even_number: int,
    *,
    min_term: int = 1,
    features: Iterable[str] = FEATURE_NAMES,
) -> tuple[FeatureSeparation, ...]:
    return feature_separation(feature_matrix(even_number, min_term=min_term), features=features)


def feature_separation_window(
    start: int,
    end: int,
    *,
    min_term: int = 1,
    features: Iterable[str] = FEATURE_NAMES,
) -> tuple[FeatureSeparation, ...]:
    if start > end:
        raise ValueError("start must be less than or equal to end.")

    first = start if start % 2 == 0 else start + 1
    last = end if end % 2 == 0 else end - 1
    rows: list[CandidateFeatureRow] = []
    for even_number in range(first, last + 1, 2):
        if even_number > 2:
            rows.extend(feature_matrix(even_number, min_term=min_term))
    return feature_separation(rows, features=features)


def _separate_feature(rows: tuple[CandidateFeatureRow, ...], feature: str) -> FeatureSeparation:
    positives = [feature_value(row, feature) for row in rows if row.is_goldbach_pair]
    negatives = [feature_value(row, feature) for row in rows if not row.is_goldbach_pair]
    positive_mean = _mean(positives)
    negative_mean = _mean(negatives)
    auc = _pairwise_auc(positives, negatives)
    separation_auc = max(auc, 1.0 - auc)
    preferred_direction = "higher_for_goldbach" if auc >= 0.5 else "lower_for_goldbach"

    return FeatureSeparation(
        feature=feature,
        positive_count=len(positives),
        negative_count=len(negatives),
        positive_mean=positive_mean,
        negative_mean=negative_mean,
        auc_higher_for_goldbach=auc,
        separation_auc=separation_auc,
        preferred_direction=preferred_direction,
    )


def _mean(values: list[float]) -> float:
    if not values:
        return 0.0
    return sum(values) / len(values)


def _pairwise_auc(positives: list[float], negatives: list[float]) -> float:
    if not positives or not negatives:
        return 0.5

    wins = 0.0
    for positive in positives:
        for negative in negatives:
            if positive > negative:
                wins += 1.0
            elif positive == negative:
                wins += 0.5
    return wins / (len(positives) * len(negatives))
