from __future__ import annotations

import cmath
import csv
import json
import math
import random
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path

from .operators import factorize, goldbach_partitions, primes_from_flags, sieve_primes

try:
    import numpy as _np
except ImportError:  # pragma: no cover - exercised only when numpy is absent.
    _np = None


@dataclass(frozen=True)
class GoldbachRow:
    N: int
    partition_count: int
    epsilon_min: int | None
    centrality: float
    best_pair: tuple[int, int] | None
    max_merged_rap_loss: int | None


@dataclass(frozen=True)
class GoldbachExperiment:
    max_even: int
    evidence_level: str
    rows: list[GoldbachRow]
    counterexamples: list[int]


@dataclass(frozen=True)
class FrequencyPower:
    frequency: float
    power: float


@dataclass(frozen=True)
class RationalApproximation:
    numerator: int
    denominator: int
    value: float
    error: float
    candidate_modulus: int


@dataclass(frozen=True)
class SpectralPeak:
    frequency: float
    period: float
    nearest_rational: str
    candidate_modulus: int
    absolute_power: float
    raw_power: float
    normalized_power: float
    windowed_power: float
    total_spectral_energy: float
    fraction_of_total_energy: float
    global_empirical_p: float
    rank_within_channel: int
    stability_across_ranges: str


@dataclass(frozen=True)
class SpectrumChannel:
    name: str
    evidence_level: str
    values: tuple[float, ...]
    peaks: tuple[SpectralPeak, ...]


@dataclass(frozen=True)
class MultiSpectrumExperiment:
    max_even: int
    min_even: int
    evidence_level: str
    rows: list[GoldbachRow]
    channels: tuple[SpectrumChannel, ...]
    counterexamples: list[int]


@dataclass(frozen=True)
class PersistenceCandidate:
    candidate_frequency: str
    nearest_rational: str
    windows_detected: int
    coverage: float
    mean_frequency: float
    frequency_std: float
    mean_power_fraction: float
    control_percentile: float
    global_empirical_p: float
    normalizers_survived: int
    structural_origin: str
    novelty_status: str
    exclude_from_candidate_ranking: bool
    classification: str


@dataclass(frozen=True)
class PersistenceExperiment:
    windows: tuple[tuple[int, int], ...]
    evidence_level: str
    channel_name: str
    control_seeds: tuple[int, ...]
    candidates: tuple[PersistenceCandidate, ...]


@dataclass(frozen=True)
class ExtractionStage:
    name: str
    values: tuple[float, ...]
    total_spectral_energy: float
    peaks: tuple[SpectralPeak, ...]


@dataclass(frozen=True)
class ExtractionExperiment:
    max_even: int
    evidence_level: str
    modular_primes: tuple[int, ...]
    stages: tuple[ExtractionStage, ...]
    control_seeds: tuple[int, ...]


def build_goldbach_experiment(max_even: int, min_even: int = 4) -> GoldbachExperiment:
    if max_even < 4:
        raise ValueError("max_even must be at least 4.")
    if min_even < 4 or min_even % 2 != 0:
        raise ValueError("min_even must be an even number greater than or equal to 4.")

    if max_even % 2 != 0:
        max_even -= 1

    prime_flags = sieve_primes(max_even)
    primes = primes_from_flags(prime_flags)
    rows: list[GoldbachRow] = []
    counterexamples: list[int] = []

    for even_number in range(min_even, max_even + 1, 2):
        partitions = goldbach_partitions(even_number, prime_flags=prime_flags, primes=primes)

        if not partitions:
            rows.append(
                GoldbachRow(
                    N=even_number,
                    partition_count=0,
                    epsilon_min=None,
                    centrality=0.0,
                    best_pair=None,
                    max_merged_rap_loss=None,
                )
            )
            counterexamples.append(even_number)
            continue

        best = min(partitions, key=lambda item: (item.epsilon, item.p))
        max_loss = max(item.merged_rap_loss for item in partitions)

        rows.append(
            GoldbachRow(
                N=even_number,
                partition_count=len(partitions),
                epsilon_min=best.epsilon,
                centrality=1.0 / (1.0 + best.epsilon),
                best_pair=(best.p, best.q),
                max_merged_rap_loss=max_loss,
            )
        )

    return GoldbachExperiment(
        max_even=max_even,
        evidence_level="Observación",
        rows=rows,
        counterexamples=counterexamples,
    )


def local_goldbach_factor(n: int) -> float:
    if n < 1:
        raise ValueError("Local Goldbach factor is defined for positive integers.")

    factor = 1.0
    for prime, _ in factorize(n):
        if prime > 2:
            factor *= (prime - 1) / (prime - 2)
    return factor


def goldbach_scale(n: int) -> float:
    if n < 4:
        raise ValueError("Goldbach scale is defined for n >= 4.")
    return local_goldbach_factor(n) * n / (math.log(n) ** 2)


def nearest_rational(frequency: float, max_denominator: int = 30) -> RationalApproximation:
    if frequency <= 0:
        return RationalApproximation(0, 1, 0.0, abs(frequency), 1)

    fraction = Fraction(frequency).limit_denominator(max_denominator)
    value = fraction.numerator / fraction.denominator
    return RationalApproximation(
        numerator=fraction.numerator,
        denominator=fraction.denominator,
        value=value,
        error=abs(frequency - value),
        candidate_modulus=fraction.denominator,
    )


def moving_average(values: list[float], radius: int = 25) -> list[float]:
    if radius < 1:
        return values[:]

    averaged: list[float] = []
    for index in range(len(values)):
        start = max(0, index - radius)
        end = min(len(values), index + radius + 1)
        window = values[start:end]
        averaged.append(sum(window) / len(window))
    return averaged


def hann_window(values: list[float]) -> list[float]:
    if len(values) <= 1:
        return values[:]
    return [
        value * (0.5 - 0.5 * math.cos((2.0 * math.pi * index) / (len(values) - 1)))
        for index, value in enumerate(values)
    ]


def residual_series(values: list[float], radius: int = 25) -> list[float]:
    trend = moving_average(values, radius=radius)
    return [value - trend[index] for index, value in enumerate(values)]


def mean_center(values: list[float]) -> list[float]:
    if not values:
        return []
    mean = sum(values) / len(values)
    return [value - mean for value in values]


def log_linear_detrend(ns: list[int], values: list[float]) -> list[float]:
    if len(ns) != len(values):
        raise ValueError("ns and values must have the same length.")
    if not values:
        return []

    xs = [math.log(n) for n in ns]
    x_mean = sum(xs) / len(xs)
    y_mean = sum(values) / len(values)
    denominator = sum((x - x_mean) ** 2 for x in xs)
    slope = 0.0 if denominator == 0 else sum((x - x_mean) * (y - y_mean) for x, y in zip(xs, values)) / denominator
    intercept = y_mean - slope * x_mean
    return [value - (intercept + slope * x) for value, x in zip(values, xs)]


def modular_basis(ns: list[int], modular_primes: tuple[int, ...]) -> list[list[float]]:
    columns: list[list[float]] = []
    for prime in modular_primes:
        for harmonic in range(1, (prime // 2) + 1):
            angle_factor = (2.0 * math.pi * harmonic) / prime
            columns.append([math.cos(angle_factor * n) for n in ns])
            columns.append([math.sin(angle_factor * n) for n in ns])
    return columns


def modular_projection_residual(
    ns: list[int],
    values: list[float],
    *,
    modular_primes: tuple[int, ...] = (3, 5, 7, 11, 13),
) -> list[float]:
    if len(ns) != len(values):
        raise ValueError("ns and values must have the same length.")
    if not values:
        return []

    residual = values[:]
    orthonormal: list[list[float]] = []

    for column in modular_basis(ns, modular_primes):
        vector = column[:]
        for basis_vector in orthonormal:
            coefficient = sum(v * b for v, b in zip(vector, basis_vector))
            vector = [v - coefficient * b for v, b in zip(vector, basis_vector)]
        norm = math.sqrt(sum(v * v for v in vector))
        if norm <= 1e-12:
            continue
        orthonormal.append([v / norm for v in vector])

    for basis_vector in orthonormal:
        coefficient = sum(value * b for value, b in zip(residual, basis_vector))
        residual = [value - coefficient * b for value, b in zip(residual, basis_vector)]

    return residual


def dft_power_spectrum(values: list[float], sample_spacing: float = 2.0) -> list[FrequencyPower]:
    n = len(values)
    if n == 0:
        return []

    if _np is not None:
        array = _np.asarray(values, dtype=float)
        transformed = _np.fft.rfft(array)
        powers = (transformed.real * transformed.real) + (transformed.imag * transformed.imag)
        return [
            FrequencyPower(frequency=index / (n * sample_spacing), power=float(power))
            for index, power in enumerate(powers)
        ]

    spectrum: list[FrequencyPower] = []
    max_k = n // 2
    for k in range(0, max_k + 1):
        total = 0j
        for index, value in enumerate(values):
            angle = -2.0j * math.pi * k * index / n
            total += value * cmath.exp(angle)
        frequency = k / (n * sample_spacing)
        spectrum.append(FrequencyPower(frequency=frequency, power=(total.real * total.real) + (total.imag * total.imag)))

    return spectrum


def dominant_frequencies(
    values: list[float],
    *,
    sample_spacing: float = 2.0,
    limit: int = 10,
    min_power: float = 1e-12,
) -> list[FrequencyPower]:
    nonzero = [
        item
        for item in dft_power_spectrum(values, sample_spacing=sample_spacing)
        if item.frequency > 0 and item.power > min_power
    ]
    return sorted(nonzero, key=lambda item: item.power, reverse=True)[:limit]


def shuffled_control(values: list[float], seed: int) -> list[float]:
    shuffled = values[:]
    random.Random(seed).shuffle(shuffled)
    return shuffled


def _peak_stability(candidate_modulus: int, channel_name: str) -> str:
    if channel_name == "random_control":
        return "control_randomizado"
    if candidate_modulus in {3, 5, 6, 7, 10, 14}:
        return "candidato_modular"
    return "pendiente_por_subventanas"


def analyze_channel(
    name: str,
    values: list[float],
    *,
    peak_limit: int = 10,
    sample_spacing: float = 2.0,
    max_denominator: int = 30,
) -> SpectrumChannel:
    windowed_values = hann_window(values)
    raw_spectrum = dft_power_spectrum(values, sample_spacing=sample_spacing)
    windowed_spectrum = dft_power_spectrum(windowed_values, sample_spacing=sample_spacing)
    max_windowed_power = max((item.power for item in windowed_spectrum if item.frequency > 0), default=1.0) or 1.0
    total_windowed_power = sum(item.power for item in windowed_spectrum if item.frequency > 0) or 1.0
    raw_by_frequency = {item.frequency: item.power for item in raw_spectrum}
    top = dominant_frequencies(windowed_values, sample_spacing=sample_spacing, limit=peak_limit)
    peaks: list[SpectralPeak] = []

    for rank, item in enumerate(top, start=1):
        rational = nearest_rational(item.frequency, max_denominator=max_denominator)
        period = math.inf if item.frequency == 0 else 1.0 / item.frequency
        peaks.append(
            SpectralPeak(
                frequency=item.frequency,
                period=period,
                nearest_rational=f"{rational.numerator}/{rational.denominator}",
                candidate_modulus=rational.candidate_modulus,
                absolute_power=item.power,
                raw_power=raw_by_frequency.get(item.frequency, 0.0),
                normalized_power=item.power / max_windowed_power,
                windowed_power=item.power,
                total_spectral_energy=total_windowed_power,
                fraction_of_total_energy=item.power / total_windowed_power,
                global_empirical_p=1.0,
                rank_within_channel=rank,
                stability_across_ranges=_peak_stability(rational.candidate_modulus, name),
            )
        )

    return SpectrumChannel(
        name=name,
        evidence_level="Observación",
        values=tuple(values),
        peaks=tuple(peaks),
    )


def build_multispectrum_experiment(
    max_even: int,
    *,
    min_even: int = 4,
    random_seed: int = 1436,
    peak_limit: int = 10,
    trend_radius: int = 25,
) -> MultiSpectrumExperiment:
    experiment = build_goldbach_experiment(max_even, min_even=min_even)
    counts = [float(row.partition_count) for row in experiment.rows]
    smooth_residual = residual_series(counts, radius=trend_radius)
    desingularized = [
        row.partition_count / goldbach_scale(row.N)
        for row in experiment.rows
    ]
    random_control = shuffled_control(smooth_residual, seed=random_seed)

    channels = (
        analyze_channel("raw_counts", counts, peak_limit=peak_limit),
        analyze_channel("smooth_residual", smooth_residual, peak_limit=peak_limit),
        analyze_channel("desingularized_ratio", desingularized, peak_limit=peak_limit),
        analyze_channel("random_control", random_control, peak_limit=peak_limit),
    )

    return MultiSpectrumExperiment(
        max_even=experiment.max_even,
        min_even=min_even,
        evidence_level="Identificación heurística de firma modular",
        rows=experiment.rows,
        channels=channels,
        counterexamples=experiment.counterexamples,
    )


def _channel_by_name(experiment: MultiSpectrumExperiment, channel_name: str) -> SpectrumChannel:
    for channel in experiment.channels:
        if channel.name == channel_name:
            return channel
    raise ValueError(f"Unknown channel: {channel_name}")


def _std(values: list[float]) -> float:
    if len(values) <= 1:
        return 0.0
    mean = sum(values) / len(values)
    variance = sum((value - mean) ** 2 for value in values) / len(values)
    return math.sqrt(variance)


def _classification(coverage: float, frequency_std: float, mean_resolution: float, control_percentile: float) -> str:
    if coverage >= 0.75 and frequency_std <= mean_resolution and control_percentile >= 0.95:
        return "evidencia_heuristica_multiescala"
    if coverage >= 0.5 and control_percentile >= 0.75:
        return "observacion_persistente"
    return "observacion_local"


def _structural_origin(nearest_rational_value: str) -> tuple[str, str, bool]:
    if nearest_rational_value == "0/1":
        return "residual_trend", "not_applicable", True

    try:
        denominator = int(nearest_rational_value.split("/", 1)[1])
    except (IndexError, ValueError):
        return "unresolved_residual_candidate", "not_established", False

    known_denominators = {5, 6, 7, 10, 11, 13, 14, 22, 26, 30}
    if denominator in known_denominators:
        return "known_modular_candidate", "not_established", False
    return "unresolved_residual_candidate", "not_established", False


def build_persistence_experiment(
    *,
    windows: list[tuple[int, int]],
    control_seeds: list[int],
    channel_name: str = "desingularized_ratio",
    peak_limit: int = 12,
    trend_radius: int = 25,
) -> PersistenceExperiment:
    if not windows:
        raise ValueError("At least one window is required.")
    if not control_seeds:
        raise ValueError("At least one control seed is required.")

    normalized_windows = tuple((start, end - (end % 2)) for start, end in windows)
    detections: dict[str, list[SpectralPeak]] = {}
    control_fractions: dict[str, list[float]] = {}
    control_global_fractions: list[float] = []
    normalizer_keys: dict[str, set[str]] = {}
    resolutions: list[float] = []

    for start, end in normalized_windows:
        experiment = build_multispectrum_experiment(
            end,
            min_even=start,
            random_seed=control_seeds[0],
            peak_limit=peak_limit,
            trend_radius=trend_radius,
        )
        selected = _channel_by_name(experiment, channel_name)
        resolutions.append(1.0 / (len(experiment.rows) * 2.0))

        selected_by_key: dict[str, SpectralPeak] = {}
        for peak in selected.peaks:
            current = selected_by_key.get(peak.nearest_rational)
            if current is None or peak.fraction_of_total_energy > current.fraction_of_total_energy:
                selected_by_key[peak.nearest_rational] = peak

        for key, peak in selected_by_key.items():
            detections.setdefault(key, []).append(peak)

        for deterministic_name in ("raw_counts", "smooth_residual", "desingularized_ratio"):
            channel = _channel_by_name(experiment, deterministic_name)
            for peak in channel.peaks:
                normalizer_keys.setdefault(peak.nearest_rational, set()).add(deterministic_name)

        selected_values = list(selected.values)
        for seed in control_seeds:
            control = analyze_channel(
                "random_control",
                shuffled_control(selected_values, seed=seed),
                peak_limit=peak_limit,
            )
            control_global_fractions.append(max((peak.fraction_of_total_energy for peak in control.peaks), default=0.0))
            control_by_key: dict[str, float] = {}
            for peak in control.peaks:
                control_by_key[peak.nearest_rational] = max(
                    control_by_key.get(peak.nearest_rational, 0.0),
                    peak.fraction_of_total_energy,
                )
            for key in selected_by_key:
                control_fractions.setdefault(key, []).append(control_by_key.get(key, 0.0))

    candidates: list[PersistenceCandidate] = []
    mean_resolution = sum(resolutions) / len(resolutions)

    for key, peaks in detections.items():
        frequencies = [peak.frequency for peak in peaks]
        fractions = [peak.fraction_of_total_energy for peak in peaks]
        mean_fraction = sum(fractions) / len(fractions)
        controls = control_fractions.get(key, [0.0])
        control_percentile = sum(1 for value in controls if value <= mean_fraction) / len(controls)
        global_empirical_p = (
            1 + sum(1 for value in control_global_fractions if value >= mean_fraction)
        ) / (1 + len(control_global_fractions))
        coverage = len(peaks) / len(normalized_windows)
        mean_frequency = sum(frequencies) / len(frequencies)
        frequency_std = _std(frequencies)
        structural_origin, novelty_status, exclude_from_candidate_ranking = _structural_origin(key)
        classification = (
            "residual_trend"
            if exclude_from_candidate_ranking
            else _classification(coverage, frequency_std, mean_resolution, control_percentile)
        )

        candidates.append(
            PersistenceCandidate(
                candidate_frequency=f"{mean_frequency:.10f}",
                nearest_rational=key,
                windows_detected=len(peaks),
                coverage=coverage,
                mean_frequency=mean_frequency,
                frequency_std=frequency_std,
                mean_power_fraction=mean_fraction,
                control_percentile=control_percentile,
                global_empirical_p=global_empirical_p,
                normalizers_survived=len(normalizer_keys.get(key, set())),
                structural_origin=structural_origin,
                novelty_status=novelty_status,
                exclude_from_candidate_ranking=exclude_from_candidate_ranking,
                classification=classification,
            )
        )

    candidates.sort(
        key=lambda item: (
            item.classification != "evidencia_heuristica_multiescala",
            -item.coverage,
            -item.control_percentile,
            -item.mean_power_fraction,
        )
    )

    return PersistenceExperiment(
        windows=normalized_windows,
        evidence_level="Observación multiescala",
        channel_name=channel_name,
        control_seeds=tuple(control_seeds),
        candidates=tuple(candidates),
    )


def _desingularized_values(rows: list[GoldbachRow]) -> list[float]:
    return [row.partition_count / goldbach_scale(row.N) for row in rows]


def _global_empirical_p_for_peaks(peaks: tuple[SpectralPeak, ...], control_maxima: list[float]) -> tuple[SpectralPeak, ...]:
    if not control_maxima:
        return peaks

    updated: list[SpectralPeak] = []
    for peak in peaks:
        global_empirical_p = (1 + sum(1 for value in control_maxima if value >= peak.fraction_of_total_energy)) / (
            1 + len(control_maxima)
        )
        updated.append(
            SpectralPeak(
                frequency=peak.frequency,
                period=peak.period,
                nearest_rational=peak.nearest_rational,
                candidate_modulus=peak.candidate_modulus,
                absolute_power=peak.absolute_power,
                raw_power=peak.raw_power,
                normalized_power=peak.normalized_power,
                windowed_power=peak.windowed_power,
                total_spectral_energy=peak.total_spectral_energy,
                fraction_of_total_energy=peak.fraction_of_total_energy,
                global_empirical_p=global_empirical_p,
                rank_within_channel=peak.rank_within_channel,
                stability_across_ranges=peak.stability_across_ranges,
            )
        )
    return tuple(updated)


def build_extraction_experiment(
    max_even: int,
    *,
    min_even: int = 4,
    modular_primes: tuple[int, ...] = (3, 5, 7, 11, 13),
    control_seeds: list[int] | None = None,
    peak_limit: int = 12,
) -> ExtractionExperiment:
    seeds = control_seeds if control_seeds is not None else [1436, 2718, 3141, 5772, 16180]
    experiment = build_goldbach_experiment(max_even, min_even=min_even)
    ns = [row.N for row in experiment.rows]
    r0 = _desingularized_values(experiment.rows)
    r1 = mean_center(r0)
    r2 = log_linear_detrend(ns, r0)
    r3 = modular_projection_residual(ns, r2, modular_primes=modular_primes)
    stage_values = [
        ("R0_desingularized", r0),
        ("R1_mean_centered", r1),
        ("R2_log_detrended", r2),
        ("R3_modular_orthogonal", r3),
    ]

    stages: list[ExtractionStage] = []
    for name, values in stage_values:
        channel = analyze_channel(name, values, peak_limit=peak_limit)
        control_maxima: list[float] = []
        for seed in seeds:
            control = analyze_channel(
                f"{name}_random_control",
                shuffled_control(values, seed=seed),
                peak_limit=peak_limit,
            )
            control_maxima.append(max((peak.fraction_of_total_energy for peak in control.peaks), default=0.0))
        peaks = _global_empirical_p_for_peaks(channel.peaks, control_maxima)
        stages.append(
            ExtractionStage(
                name=name,
                values=channel.values,
                total_spectral_energy=peaks[0].total_spectral_energy if peaks else 0.0,
                peaks=peaks,
            )
        )

    return ExtractionExperiment(
        max_even=max_even if max_even % 2 == 0 else max_even - 1,
        evidence_level="Observación de extracción ortogonal",
        modular_primes=modular_primes,
        stages=tuple(stages),
        control_seeds=tuple(seeds),
    )


def write_rows_csv(path: Path, experiment: GoldbachExperiment) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "N",
                "partition_count",
                "epsilon_min",
                "centrality",
                "best_pair",
                "max_merged_rap_loss",
            ],
        )
        writer.writeheader()
        for row in experiment.rows:
            payload = asdict(row)
            payload["best_pair"] = "" if row.best_pair is None else f"{row.best_pair[0]}+{row.best_pair[1]}"
            writer.writerow(payload)


def write_spectrum_csv(path: Path, spectrum: list[FrequencyPower]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["frequency", "power"])
        writer.writeheader()
        for item in spectrum:
            writer.writerow(asdict(item))


def write_channel_values_csv(path: Path, experiment: MultiSpectrumExperiment) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        fieldnames = ["N"] + [channel.name for channel in experiment.channels]
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for index, row in enumerate(experiment.rows):
            payload = {"N": row.N}
            for channel in experiment.channels:
                payload[channel.name] = channel.values[index]
            writer.writerow(payload)


def write_multispectrum_peaks_csv(path: Path, experiment: MultiSpectrumExperiment) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        fieldnames = [
            "channel",
            "frequency",
            "period",
            "nearest_rational",
            "candidate_modulus",
            "absolute_power",
            "raw_power",
            "normalized_power",
            "windowed_power",
            "total_spectral_energy",
            "fraction_of_total_energy",
            "global_empirical_p",
            "rank_within_channel",
            "stability_across_ranges",
        ]
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for channel in experiment.channels:
            for peak in channel.peaks:
                payload = asdict(peak)
                payload["channel"] = channel.name
                writer.writerow(payload)


def write_persistence_candidates_csv(path: Path, experiment: PersistenceExperiment) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        fieldnames = [
            "candidate_frequency",
            "nearest_rational",
            "windows_detected",
            "coverage",
            "mean_frequency",
            "frequency_std",
            "mean_power_fraction",
            "control_percentile",
            "global_empirical_p",
            "normalizers_survived",
            "structural_origin",
            "novelty_status",
            "exclude_from_candidate_ranking",
            "classification",
        ]
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for candidate in experiment.candidates:
            writer.writerow(asdict(candidate))


def write_extraction_values_csv(path: Path, experiment: ExtractionExperiment) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not experiment.stages:
        path.write_text("", encoding="utf-8")
        return

    row_count = len(experiment.stages[0].values)
    with path.open("w", newline="", encoding="utf-8") as handle:
        fieldnames = ["index"] + [stage.name for stage in experiment.stages]
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for index in range(row_count):
            payload = {"index": index}
            for stage in experiment.stages:
                payload[stage.name] = stage.values[index]
            writer.writerow(payload)


def write_extraction_peaks_csv(path: Path, experiment: ExtractionExperiment) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        fieldnames = [
            "stage",
            "frequency",
            "period",
            "nearest_rational",
            "candidate_modulus",
            "absolute_power",
            "raw_power",
            "normalized_power",
            "windowed_power",
            "total_spectral_energy",
            "fraction_of_total_energy",
            "global_empirical_p",
            "rank_within_channel",
            "stability_across_ranges",
        ]
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for stage in experiment.stages:
            for peak in stage.peaks:
                payload = asdict(peak)
                payload["stage"] = stage.name
                writer.writerow(payload)


def write_summary_json(path: Path, experiment: GoldbachExperiment, top: list[FrequencyPower]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "experiment_id": "G4",
        "window": {"min": 4, "max": experiment.max_even},
        "evidence_level": experiment.evidence_level,
        "even_numbers": len(experiment.rows),
        "counterexamples": list(experiment.counterexamples),
        "top_frequencies": [asdict(item) for item in top],
        "interpretation": "FFT sobre residuo de conteos Goldbach; observación finita, no demostración.",
    }
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def write_multispectrum_summary_json(path: Path, experiment: MultiSpectrumExperiment) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "experiment_id": "G4-002",
        "window": {"min": 4, "max": experiment.max_even},
        "evidence_level": experiment.evidence_level,
        "status": "computationally_verified_on_interval" if not experiment.counterexamples else "counterexample_detected",
        "formal_proof": False,
        "even_inputs": len(experiment.rows),
        "counterexamples": experiment.counterexamples,
        "channels": [
            {
                "name": channel.name,
                "evidence_level": channel.evidence_level,
                "peaks": [asdict(peak) for peak in channel.peaks],
            }
            for channel in experiment.channels
        ],
        "interpretation": (
            "Comparación entre conteos crudos, residuo suavizado, residuo desingularizado "
            "por factores locales y control aleatorio. Observación finita, no demostración."
        ),
    }
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def write_persistence_summary_json(path: Path, experiment: PersistenceExperiment) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "experiment_id": "G4-003",
        "evidence_level": experiment.evidence_level,
        "channel_name": experiment.channel_name,
        "windows": [list(window) for window in experiment.windows],
        "control_seeds": list(experiment.control_seeds),
        "formal_proof": False,
        "candidates": [asdict(candidate) for candidate in experiment.candidates],
        "interpretation": (
            "Persistencia multiescala del residuo Goldbach tras desingularización. "
            "La promoción de picos depende de cobertura, estabilidad y comparación contra controles."
        ),
    }
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def write_extraction_summary_json(path: Path, experiment: ExtractionExperiment) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "experiment_id": "G4-004",
        "evidence_level": experiment.evidence_level,
        "window": {"min": 4, "max": experiment.max_even},
        "modular_primes": list(experiment.modular_primes),
        "control_seeds": list(experiment.control_seeds),
        "formal_proof": False,
        "stages": [
            {
                "name": stage.name,
                "total_spectral_energy": stage.total_spectral_energy,
                "peaks": [asdict(peak) for peak in stage.peaks],
            }
            for stage in experiment.stages
        ],
        "interpretation": (
            "Extracción sucesiva R0, R1, R2 y R3: desingularización, sustracción de media, "
            "detrending log-lineal y proyección ortogonal fuera de ruedas modulares pequeñas."
        ),
    }
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def render_spectrum_svg(path: Path, spectrum: list[FrequencyPower], *, width: int = 1000, height: int = 560) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    plot_left = 70
    plot_right = width - 30
    plot_top = 35
    plot_bottom = height - 65
    usable_width = plot_right - plot_left
    usable_height = plot_bottom - plot_top

    nonzero = [item for item in spectrum if item.frequency > 0]
    if not nonzero:
        points = ""
        max_frequency = 1.0
        max_log_power = 1.0
    else:
        max_frequency = max(item.frequency for item in nonzero)
        log_powers = [math.log10(item.power + 1.0) for item in nonzero]
        max_log_power = max(log_powers) or 1.0
        coords = []
        for item, log_power in zip(nonzero, log_powers):
            x = plot_left + (item.frequency / max_frequency) * usable_width
            y = plot_bottom - (log_power / max_log_power) * usable_height
            coords.append(f"{x:.2f},{y:.2f}")
        points = " ".join(coords)

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <rect width="100%" height="100%" fill="#fbfaf7"/>
  <text x="{plot_left}" y="24" font-family="Arial, sans-serif" font-size="18" fill="#1f2933">Transformada de Goldbach - espectro de potencia</text>
  <line x1="{plot_left}" y1="{plot_bottom}" x2="{plot_right}" y2="{plot_bottom}" stroke="#1f2933" stroke-width="1"/>
  <line x1="{plot_left}" y1="{plot_top}" x2="{plot_left}" y2="{plot_bottom}" stroke="#1f2933" stroke-width="1"/>
  <polyline points="{points}" fill="none" stroke="#275d8c" stroke-width="1.5"/>
  <text x="{plot_left}" y="{height - 24}" font-family="Arial, sans-serif" font-size="12" fill="#1f2933">frecuencia normalizada por paso par; max={max_frequency:.6f}</text>
  <text x="16" y="{plot_top + 18}" font-family="Arial, sans-serif" font-size="12" fill="#1f2933" transform="rotate(-90 16,{plot_top + 18})">log10(potencia + 1); max={max_log_power:.3f}</text>
</svg>
"""
    path.write_text(svg, encoding="utf-8")
