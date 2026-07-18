"""Controlled truncated calibration for the mixed Goldbach channel C03."""

from __future__ import annotations

import cmath
import csv
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np

from athena_azr.cesaro_calibration import (
    CesaroPrefixMoments,
    cesaro_c2_direct,
    cesaro_c2_from_prefix,
    cesaro_prefix_moments,
    complex_log_gamma,
    logarithmic_integer_grid,
    riemann_zeros_up_to,
    von_mangoldt_values,
)


CHI3_ZERO_SOURCE = (
    "Primitive Dirichlet character 3/2; local Hurwitz-zeta validation, "
    "with the first zero cross-checked against the LMFDB reference"
)

# Positive ordinates of L(s, chi_3), evaluated from
# L(s, chi_3) = 3**(-s) * (zeta(s, 1/3) - zeta(s, 2/3)).
CHI3_ZERO_ORDINATES = (
    8.039737155681468,
    11.249206207772939,
    15.704619176721625,
    18.261997495693130,
    20.455770807742496,
    24.059414856493447,
    26.577868735774580,
    28.218164506233386,
    30.745040261382499,
    33.897388927259414,
    35.608412653938643,
    37.551796556364621,
    39.485207260929343,
    42.616379226157562,
    44.120572912072205,
    46.274118023513154,
    47.514104510117321,
    50.375138650636259,
    52.496749599060749,
    54.193843101551906,
    55.642558700216227,
    57.584056360449182,
    60.026857456715902,
    62.206078122282136,
    63.176992767339115,
    65.294925544083696,
    66.623134625532941,
    69.513022985980001,
    70.819798695547149,
    72.656149070696671,
    74.005428521004177,
    75.622406964030716,
    78.217481270926612,
    79.637975751907788,
    81.611987609471441,
    82.470252512221975,
    84.412286638293409,
    86.327646283014133,
    88.652617208539397,
    89.646402756841695,
    91.335610354433101,
    92.753464387119152,
    94.394358797163392,
    96.874252089785301,
    98.126454904241911,
    99.533489264058602,
    101.374963467900017,
    102.116361845064944,
    104.765375470164514,
    106.246061848876366,
    107.970316117138111,
    109.137603914491734,
    110.523351036813324,
    112.154771842199978,
    114.217148271564241,
    115.898142441843135,
    117.369750996605347,
    118.299418307897611,
    120.255182238494427,
    121.278841596507391,
    123.890490659809643,
    125.010783500604020,
    126.397312255835033,
    128.052677184236131,
    128.937236928623747,
    130.811369910238568,
    133.032449649300531,
    133.990862643415312,
    135.820891223149545,
    136.826373271550040,
    138.095359556468850,
    139.998280075504510,
    141.647847111848762,
    143.638477145126728,
)

_HURWITZ_COEFFICIENTS = (
    1.0 / 12.0,
    -1.0 / 720.0,
    1.0 / 30240.0,
    -1.0 / 1209600.0,
    1.0 / 47900160.0,
    -691.0 / 1307674368000.0,
    7.0 / 523069747200.0,
    -3617.0 / 10670622842880000.0,
    43867.0 / 5109094217170944000.0,
    -174611.0 / 802857662698291200000.0,
)


@dataclass(frozen=True)
class C03Sample:
    x: int
    c03: float
    observed_z03: float
    m0_pole: float
    m1_pole_lzeros: float
    m2_pole_lzeros_cross: float
    split: str


@dataclass(frozen=True)
class C03ConvolutionCheck:
    n: int
    direct: float
    fft: float
    absolute_error: float


@dataclass(frozen=True)
class C03Metric:
    chi3_zero_height: float
    chi3_zero_count: int
    zeta_zero_height: float
    zeta_zero_count: int
    split: str
    model: str
    rmse: float
    mae: float
    max_absolute_error: float


@dataclass(frozen=True)
class C03CoefficientAudit:
    chi3_zero_height: float
    zero_index: int
    ordinate: float
    theoretical_real: float
    theoretical_imag: float
    estimated_real: float
    estimated_imag: float
    amplitude_ratio: float
    phase_error: float


@dataclass(frozen=True)
class C03Experiment:
    min_x: int
    max_x: int
    log_samples_requested: int
    discovery_fraction: float
    chi3_zero_source: str
    chi3_zero_table_max: float
    chi3_zero_heights: tuple[float, ...]
    zeta_zero_height: float
    frozen_channels: tuple[str, ...]
    explicit_formula_complete: bool
    samples: tuple[C03Sample, ...]
    convolution_checks: tuple[C03ConvolutionCheck, ...]
    metrics: tuple[C03Metric, ...]
    coefficient_audits: tuple[C03CoefficientAudit, ...]


def chi3_values(limit: int) -> np.ndarray:
    if limit < 0:
        raise ValueError("limit must be non-negative")
    indices = np.arange(limit + 1, dtype=np.int64)
    residues = indices % 3
    values = np.zeros(limit + 1, dtype=np.int8)
    values[residues == 1] = 1
    values[residues == 2] = -1
    return values


def chi3_log_derivative_at_zero() -> float:
    """Return (L'/L)(0, chi_3) in closed form."""
    return -math.log(3.0) + (3.0 * (math.lgamma(1.0 / 3.0) - math.lgamma(2.0 / 3.0)))


def hurwitz_zeta_euler_maclaurin(
    value: complex,
    shift: float,
    *,
    terms: int = 128,
) -> complex:
    s = complex(value)
    if not 0.0 < shift <= 1.0:
        raise ValueError("shift must satisfy 0 < shift <= 1")
    if terms < 8:
        raise ValueError("terms must be at least 8")
    if abs(s - 1.0) < 1e-15:
        raise ValueError("Hurwitz zeta has a pole at s=1")

    endpoint = terms + shift
    total = sum((index + shift) ** (-s) for index in range(terms))
    total += (endpoint ** (1.0 - s)) / (s - 1.0)
    total += 0.5 * (endpoint ** (-s))

    rising = 1.0 + 0.0j
    for order, coefficient in enumerate(_HURWITZ_COEFFICIENTS, start=1):
        if order == 1:
            rising = s
        else:
            rising *= (s + (2 * order) - 3) * (s + (2 * order) - 2)
        total += coefficient * rising * (endpoint ** (-s - (2 * order) + 1))
    return total


def dirichlet_l_chi3(value: complex) -> complex:
    s = complex(value)
    return cmath.exp(-s * math.log(3.0)) * (
        hurwitz_zeta_euler_maclaurin(s, 1.0 / 3.0)
        - hurwitz_zeta_euler_maclaurin(s, 2.0 / 3.0)
    )


def chi3_zeros_up_to(height: float) -> tuple[float, ...]:
    if height <= 0:
        return ()
    if height > CHI3_ZERO_ORDINATES[-1]:
        raise ValueError(
            f"height {height} exceeds the local chi3 table limit "
            f"{CHI3_ZERO_ORDINATES[-1]}"
        )
    return tuple(value for value in CHI3_ZERO_ORDINATES if value <= height)


def mixed_convolution_direct(
    left: np.ndarray,
    right: np.ndarray,
    *,
    max_n: int | None = None,
) -> np.ndarray:
    upper = min(len(left), len(right)) - 1 if max_n is None else max_n
    if upper >= len(left) or upper >= len(right):
        raise ValueError("max_n must be smaller than both input lengths")
    result = np.zeros(upper + 1, dtype=np.float64)
    for n in range(2, upper + 1):
        result[n] = sum(float(left[m]) * float(right[n - m]) for m in range(1, n))
    return result


def mixed_convolution_fft(
    left: np.ndarray,
    right: np.ndarray,
    *,
    max_n: int | None = None,
) -> np.ndarray:
    upper = min(len(left), len(right)) - 1 if max_n is None else max_n
    if upper >= len(left) or upper >= len(right):
        raise ValueError("max_n must be smaller than both input lengths")

    left_active = np.asarray(left[: upper + 1], dtype=np.float64)
    right_active = np.asarray(right[: upper + 1], dtype=np.float64)
    convolution_length = len(left_active) + len(right_active) - 1
    fft_length = 1 << (convolution_length - 1).bit_length()
    result = np.fft.irfft(
        np.fft.rfft(left_active, fft_length) * np.fft.rfft(right_active, fft_length),
        fft_length,
    )[: upper + 1]
    result[np.abs(result) < 1e-12] = 0.0
    return result


def mixed_convolution_value(left: np.ndarray, right: np.ndarray, n: int) -> float:
    if n < 2 or n >= len(left) or n >= len(right):
        raise ValueError("n must index both input arrays and satisfy n >= 2")
    return float(sum(float(left[m]) * float(right[n - m]) for m in range(1, n)))


def mixed_cesaro_c2_from_prefix(moments: CesaroPrefixMoments, x: int) -> float:
    return cesaro_c2_from_prefix(moments, x)


def mixed_cesaro_c2_direct(values: np.ndarray, x: int) -> float:
    return cesaro_c2_direct(values, x)


def c03_pole_normalized(xs: np.ndarray) -> np.ndarray:
    x_values = np.asarray(xs, dtype=np.float64)
    coefficient = -chi3_log_derivative_at_zero() / 6.0
    return coefficient / np.sqrt(x_values)


def c03_linear_coefficient(rho: complex) -> complex:
    return -1.0 / (rho * (rho + 1.0) * (rho + 2.0) * (rho + 3.0))


def c03_linear_normalized(
    xs: np.ndarray,
    positive_chi3_zero_ordinates: tuple[float, ...],
) -> np.ndarray:
    x_values = np.asarray(xs, dtype=np.float64)
    logs = np.log(x_values)
    result = np.zeros(len(x_values), dtype=np.float64)
    for ordinate in positive_chi3_zero_ordinates:
        rho = 0.5 + (1j * ordinate)
        coefficient = c03_linear_coefficient(rho)
        result += 2.0 * np.real(coefficient * np.exp(1j * ordinate * logs))
    return result


def c03_cross_normalized(
    xs: np.ndarray,
    positive_zeta_zero_ordinates: tuple[float, ...],
    positive_chi3_zero_ordinates: tuple[float, ...],
) -> np.ndarray:
    x_values = np.asarray(xs, dtype=np.float64)
    zeta_rhos = [0.5 + (1j * ordinate) for ordinate in positive_zeta_zero_ordinates]
    chi3_rhos = [0.5 + (1j * ordinate) for ordinate in positive_chi3_zero_ordinates]
    zeta_rhos.extend(rho.conjugate() for rho in tuple(zeta_rhos))
    chi3_rhos.extend(rho.conjugate() for rho in tuple(chi3_rhos))

    frequencies: list[float] = []
    coefficients: list[complex] = []
    for zeta_rho in zeta_rhos:
        for chi3_rho in chi3_rhos:
            log_coefficient = (
                complex_log_gamma(zeta_rho)
                + complex_log_gamma(chi3_rho)
                - complex_log_gamma(zeta_rho + chi3_rho + 3.0)
            )
            frequencies.append((zeta_rho + chi3_rho).imag)
            coefficients.append(cmath.exp(log_coefficient))

    frequency_array = np.asarray(frequencies, dtype=np.float64)
    coefficient_array = np.asarray(coefficients, dtype=np.complex128)
    result = np.empty(len(x_values), dtype=np.float64)
    for index, x_value in enumerate(x_values):
        phase = np.exp(1j * frequency_array * math.log(float(x_value)))
        result[index] = float(np.real(np.dot(coefficient_array, phase)) / math.sqrt(float(x_value)))
    return result


def _error_metrics(observed: np.ndarray, predicted: np.ndarray) -> tuple[float, float, float]:
    errors = np.asarray(observed, dtype=np.float64) - np.asarray(predicted, dtype=np.float64)
    return (
        float(np.sqrt(np.mean(errors * errors))),
        float(np.mean(np.abs(errors))),
        float(np.max(np.abs(errors))),
    )


def _coefficient_audits(
    xs: np.ndarray,
    observed_without_pole_and_cross: np.ndarray,
    positive_chi3_zero_ordinates: tuple[float, ...],
    *,
    chi3_zero_height: float,
) -> list[C03CoefficientAudit]:
    if not positive_chi3_zero_ordinates:
        return []
    logs = np.log(np.asarray(xs, dtype=np.float64))
    columns: list[np.ndarray] = []
    for ordinate in positive_chi3_zero_ordinates:
        columns.append(np.cos(ordinate * logs))
        columns.append(np.sin(ordinate * logs))
    design = np.column_stack(columns)
    fitted, _, _, _ = np.linalg.lstsq(design, observed_without_pole_and_cross, rcond=None)

    audits: list[C03CoefficientAudit] = []
    for index, ordinate in enumerate(positive_chi3_zero_ordinates):
        theoretical = c03_linear_coefficient(0.5 + (1j * ordinate))
        estimated = complex(fitted[2 * index] / 2.0, -fitted[(2 * index) + 1] / 2.0)
        phase_delta = cmath.phase(estimated) - cmath.phase(theoretical)
        phase_error = math.atan2(math.sin(phase_delta), math.cos(phase_delta))
        audits.append(
            C03CoefficientAudit(
                chi3_zero_height=float(chi3_zero_height),
                zero_index=index + 1,
                ordinate=float(ordinate),
                theoretical_real=float(theoretical.real),
                theoretical_imag=float(theoretical.imag),
                estimated_real=float(estimated.real),
                estimated_imag=float(estimated.imag),
                amplitude_ratio=float(abs(estimated) / abs(theoretical)),
                phase_error=float(phase_error),
            )
        )
    return audits


def build_c03_experiment(
    *,
    max_x: int,
    min_x: int,
    log_samples: int,
    chi3_zero_heights: tuple[float, ...],
    zeta_zero_height: float,
    discovery_fraction: float = 0.65,
) -> C03Experiment:
    if max_x < min_x:
        raise ValueError("max_x must be at least min_x")
    if not 0.0 < discovery_fraction < 1.0:
        raise ValueError("discovery_fraction must be between 0 and 1")
    if not chi3_zero_heights:
        raise ValueError("at least one chi3 zero height is required")

    mangoldt = von_mangoldt_values(max_x)
    twisted = mangoldt * chi3_values(max_x)
    mixed = mixed_convolution_fft(mangoldt, twisted, max_n=max_x)
    moments = cesaro_prefix_moments(mixed)
    grid = logarithmic_integer_grid(min_x, max_x, log_samples)
    split_index = max(1, min(len(grid) - 1, int(len(grid) * discovery_fraction)))
    x_values = np.asarray(grid, dtype=np.float64)
    c03_values = np.asarray(
        [mixed_cesaro_c2_from_prefix(moments, x) for x in grid],
        dtype=np.float64,
    )
    observed = c03_values / np.power(x_values, 1.5)
    pole = c03_pole_normalized(x_values)
    zeta_zeros = riemann_zeros_up_to(zeta_zero_height)

    checks = tuple(
        C03ConvolutionCheck(
            n=n,
            direct=(direct := mixed_convolution_value(mangoldt, twisted, n)),
            fft=float(mixed[n]),
            absolute_error=abs(direct - float(mixed[n])),
        )
        for n in sorted(
            {
                value
                for value in (4, 5, 6, 10, 20, max_x // 2, max_x)
                if 2 <= value <= max_x
            }
        )
    )

    split_slices = {
        "discovery": slice(0, split_index),
        "validation": slice(split_index, len(grid)),
    }
    metrics: list[C03Metric] = []
    audits: list[C03CoefficientAudit] = []
    predictions_by_height: dict[float, dict[str, np.ndarray]] = {}
    for height in chi3_zero_heights:
        chi3_zeros = chi3_zeros_up_to(height)
        linear = c03_linear_normalized(x_values, chi3_zeros)
        cross = c03_cross_normalized(x_values, zeta_zeros, chi3_zeros)
        predictions = {
            "M0_pole": pole,
            "M1_pole_lzeros": pole + linear,
            "M2_pole_lzeros_cross": pole + linear + cross,
        }
        predictions_by_height[float(height)] = predictions
        audits.extend(
            _coefficient_audits(
                x_values[:split_index],
                observed[:split_index] - pole[:split_index] - cross[:split_index],
                chi3_zeros,
                chi3_zero_height=height,
            )
        )
        for split_name, split_slice in split_slices.items():
            for model_name, prediction in predictions.items():
                rmse, mae, max_error = _error_metrics(
                    observed[split_slice],
                    prediction[split_slice],
                )
                metrics.append(
                    C03Metric(
                        chi3_zero_height=float(height),
                        chi3_zero_count=len(chi3_zeros),
                        zeta_zero_height=float(zeta_zero_height),
                        zeta_zero_count=len(zeta_zeros),
                        split=split_name,
                        model=model_name,
                        rmse=rmse,
                        mae=mae,
                        max_absolute_error=max_error,
                    )
                )

    reporting_height = max(float(height) for height in chi3_zero_heights)
    reporting_predictions = predictions_by_height[reporting_height]
    samples = tuple(
        C03Sample(
            x=x,
            c03=float(c03_values[index]),
            observed_z03=float(observed[index]),
            m0_pole=float(reporting_predictions["M0_pole"][index]),
            m1_pole_lzeros=float(reporting_predictions["M1_pole_lzeros"][index]),
            m2_pole_lzeros_cross=float(
                reporting_predictions["M2_pole_lzeros_cross"][index]
            ),
            split="discovery" if index < split_index else "validation",
        )
        for index, x in enumerate(grid)
    )

    return C03Experiment(
        min_x=min_x,
        max_x=max_x,
        log_samples_requested=log_samples,
        discovery_fraction=discovery_fraction,
        chi3_zero_source=CHI3_ZERO_SOURCE,
        chi3_zero_table_max=CHI3_ZERO_ORDINATES[-1],
        chi3_zero_heights=tuple(float(height) for height in chi3_zero_heights),
        zeta_zero_height=float(zeta_zero_height),
        frozen_channels=("C05", "C35", "C15"),
        explicit_formula_complete=False,
        samples=samples,
        convolution_checks=checks,
        metrics=tuple(metrics),
        coefficient_audits=tuple(audits),
    )


def _artifact_label(max_x: int) -> str:
    if max_x > 0:
        exponent = round(math.log10(max_x))
        if 10**exponent == max_x:
            return f"X1e{exponent}"
    return f"X{max_x}"


def write_c03_artifacts(output_dir: Path, experiment: C03Experiment) -> dict[str, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    label = _artifact_label(experiment.max_x)
    paths = {
        "series_csv": output_dir / f"c03_series_{label}.csv",
        "metrics_csv": output_dir / f"c03_metrics_{label}.csv",
        "checks_csv": output_dir / f"c03_convolution_checks_{label}.csv",
        "audits_csv": output_dir / f"c03_coefficient_audits_{label}.csv",
        "summary_json": output_dir / f"c03_summary_{label}.json",
    }

    with paths["series_csv"].open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(asdict(experiment.samples[0]).keys()))
        writer.writeheader()
        writer.writerows(asdict(sample) for sample in experiment.samples)

    with paths["metrics_csv"].open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(asdict(experiment.metrics[0]).keys()))
        writer.writeheader()
        writer.writerows(asdict(metric) for metric in experiment.metrics)

    with paths["checks_csv"].open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=list(asdict(experiment.convolution_checks[0]).keys()),
        )
        writer.writeheader()
        writer.writerows(asdict(check) for check in experiment.convolution_checks)

    with paths["audits_csv"].open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=list(asdict(experiment.coefficient_audits[0]).keys()),
        )
        writer.writeheader()
        writer.writerows(asdict(audit) for audit in experiment.coefficient_audits)

    validation_metrics = [metric for metric in experiment.metrics if metric.split == "validation"]
    best_validation = min(validation_metrics, key=lambda metric: metric.rmse)
    calibration_height = max(experiment.chi3_zero_heights)
    calibration_metrics = {
        metric.model: metric
        for metric in validation_metrics
        if metric.chi3_zero_height == calibration_height
    }
    calibration_audits = sorted(
        (
            audit
            for audit in experiment.coefficient_audits
            if audit.chi3_zero_height == calibration_height
        ),
        key=lambda audit: audit.zero_index,
    )[:5]
    m1_improves = (
        calibration_metrics["M1_pole_lzeros"].rmse
        < calibration_metrics["M0_pole"].rmse
    )
    m2_improves = (
        calibration_metrics["M2_pole_lzeros_cross"].rmse
        < calibration_metrics["M1_pole_lzeros"].rmse
    )
    amplitude_recovered = bool(calibration_audits) and all(
        0.5 <= audit.amplitude_ratio <= 2.0 for audit in calibration_audits
    )
    phase_recovered = bool(calibration_audits) and all(
        abs(audit.phase_error) <= 0.5 for audit in calibration_audits
    )
    calibration_passed = (
        m1_improves and m2_improves and amplitude_recovered and phase_recovered
    )

    summary = {
        "experiment_id": "G5B-005",
        "channel": "C03",
        "evidence_level": "Calibracion numerica de expansion truncada controlada",
        "formal_proof": False,
        "novelty_claim": False,
        "explicit_formula_complete": experiment.explicit_formula_complete,
        "expansion_status": "controlled_truncation",
        "calibration_passed": calibration_passed,
        "calibration_status": (
            "passed" if calibration_passed else "inconclusive_truncated_expansion"
        ),
        "calibration_criteria": {
            "chi3_zero_height": calibration_height,
            "audited_zero_count": len(calibration_audits),
            "validation_rmse_m0": calibration_metrics["M0_pole"].rmse,
            "validation_rmse_m1": calibration_metrics["M1_pole_lzeros"].rmse,
            "validation_rmse_m2": calibration_metrics["M2_pole_lzeros_cross"].rmse,
            "requires_m1_below_m0": m1_improves,
            "requires_m2_below_m1": m2_improves,
            "amplitude_ratio_interval": [0.5, 2.0],
            "amplitude_ratios_within_interval": amplitude_recovered,
            "maximum_absolute_phase_error": 0.5,
            "phase_errors_within_limit": phase_recovered,
        },
        "window": {"min": experiment.min_x, "max": experiment.max_x},
        "log_samples_requested": experiment.log_samples_requested,
        "log_samples_realized": len(experiment.samples),
        "discovery_fraction": experiment.discovery_fraction,
        "chi3_zero_source": experiment.chi3_zero_source,
        "chi3_zero_table_max": experiment.chi3_zero_table_max,
        "chi3_zero_heights": list(experiment.chi3_zero_heights),
        "zeta_zero_height": experiment.zeta_zero_height,
        "first_chi3_zero": CHI3_ZERO_ORDINATES[0],
        "rejected_foreign_frequencies": [4.5324, 7.8096],
        "chi3_log_derivative_at_zero": chi3_log_derivative_at_zero(),
        "pole_coefficient_before_normalization": -chi3_log_derivative_at_zero() / 6.0,
        "frozen_channels": list(experiment.frozen_channels),
        "best_validation_metric": asdict(best_validation),
        "convolution_max_absolute_error": max(
            check.absolute_error for check in experiment.convolution_checks
        ),
        "metrics": [asdict(metric) for metric in experiment.metrics],
        "interpretation": (
            "Control del canal mixto C03 mediante una expansion truncada conocida. "
            "No incluye todos los ceros triviales ni todos los residuos auxiliares y no "
            "constituye evidencia de una frecuencia nueva."
        ),
    }
    paths["summary_json"].write_text(
        json.dumps(summary, indent=2, ensure_ascii=False, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    return paths
