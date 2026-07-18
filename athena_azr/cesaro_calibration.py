"""Deterministic Cesaro calibration for the weighted Goldbach convolution."""

from __future__ import annotations

import cmath
import csv
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np


# First 50 positive ordinates, as tabulated by A. Odlyzko.
# https://www-users.cse.umn.edu/~odlyzko/zeta_tables/
RIEMANN_ZERO_SOURCE = "Andrew Odlyzko, Tables of zeros of the Riemann zeta function"
RIEMANN_ZERO_ORDINATES = (
    14.134725141734693790,
    21.022039638771554993,
    25.010857580145688763,
    30.424876125859513210,
    32.935061587739189691,
    37.586178158825671257,
    40.918719012147495187,
    43.327073280914999519,
    48.005150881167159727,
    49.773832477672302181,
    52.970321477714460644,
    56.446247697063394804,
    59.347044002602353079,
    60.831778524609809844,
    65.112544048081606660,
    67.079810529494173714,
    69.546401711173979253,
    72.067157674481907582,
    75.704690699083933168,
    77.144840068874805372,
    79.337375020249367923,
    82.910380854086030183,
    84.735492980517050105,
    87.425274613125229407,
    88.809111207634465423,
    92.491899270558484296,
    94.651344040519886967,
    95.870634228245309759,
    98.831194218193692233,
    101.317851005731391,
    103.725538040478339,
    105.446623052326094,
    107.168611184276408,
    111.029535543169674,
    111.874659176992637,
    114.320220915452712,
    116.226680320857554,
    118.790782865976218,
    121.370125002420646,
    122.946829293552589,
    124.256818554345767,
    127.516683879596495,
    129.578704199956050,
    131.087688530932656,
    133.497737202997586,
    134.756509753373872,
    138.116042054533443,
    139.736208952121388,
    141.123707404021123,
    143.111845807620632,
)


@dataclass(frozen=True)
class CesaroPrefixMoments:
    s0: np.ndarray
    s1: np.ndarray
    s2: np.ndarray


@dataclass(frozen=True)
class CesaroSample:
    x: int
    c2: float
    observed_z1: float
    split: str


@dataclass(frozen=True)
class ConvolutionCheck:
    n: int
    direct: float
    fft: float
    absolute_error: float


@dataclass(frozen=True)
class CalibrationMetric:
    zero_height: float
    zero_count: int
    split: str
    model: str
    rmse: float
    mae: float
    max_absolute_error: float


@dataclass(frozen=True)
class CoefficientAudit:
    zero_height: float
    zero_index: int
    ordinate: float
    theoretical_real: float
    theoretical_imag: float
    estimated_real: float
    estimated_imag: float
    amplitude_ratio: float
    phase_error: float


@dataclass(frozen=True)
class CesaroCalibrationExperiment:
    min_x: int
    max_x: int
    log_samples_requested: int
    zero_source: str
    zero_table_max: float
    zero_heights: tuple[float, ...]
    samples: tuple[CesaroSample, ...]
    convolution_checks: tuple[ConvolutionCheck, ...]
    metrics: tuple[CalibrationMetric, ...]
    coefficient_audits: tuple[CoefficientAudit, ...]


def von_mangoldt_values(limit: int) -> np.ndarray:
    if limit < 1:
        raise ValueError("limit must be at least 1")

    is_prime = np.ones(limit + 1, dtype=bool)
    is_prime[:2] = False
    for candidate in range(2, math.isqrt(limit) + 1):
        if is_prime[candidate]:
            is_prime[candidate * candidate : limit + 1 : candidate] = False

    values = np.zeros(limit + 1, dtype=np.float64)
    for prime in np.flatnonzero(is_prime):
        log_prime = math.log(int(prime))
        power = int(prime)
        while power <= limit:
            values[power] = log_prime
            if power > limit // int(prime):
                break
            power *= int(prime)
    return values


def additive_convolution_direct(values: np.ndarray, *, max_n: int | None = None) -> np.ndarray:
    upper = len(values) - 1 if max_n is None else max_n
    if upper >= len(values):
        raise ValueError("max_n must be smaller than len(values)")

    result = np.zeros(upper + 1, dtype=np.float64)
    for n in range(2, upper + 1):
        result[n] = sum(values[m] * values[n - m] for m in range(1, n))
    return result


def additive_convolution_fft(values: np.ndarray, *, max_n: int | None = None) -> np.ndarray:
    upper = len(values) - 1 if max_n is None else max_n
    if upper >= len(values):
        raise ValueError("max_n must be smaller than len(values)")

    active = np.asarray(values[: upper + 1], dtype=np.float64)
    convolution_length = (2 * len(active)) - 1
    fft_length = 1 << (convolution_length - 1).bit_length()
    spectrum = np.fft.rfft(active, fft_length)
    result = np.fft.irfft(spectrum * spectrum, fft_length)[: upper + 1]
    result[np.abs(result) < 1e-12] = 0.0
    return result


def additive_convolution_value(values: np.ndarray, n: int) -> float:
    if n < 2 or n >= len(values):
        raise ValueError("n must satisfy 2 <= n < len(values)")
    return float(sum(values[m] * values[n - m] for m in range(1, n)))


def cesaro_prefix_moments(goldbach_values: np.ndarray) -> CesaroPrefixMoments:
    values = np.asarray(goldbach_values, dtype=np.float64)
    indices = np.arange(len(values), dtype=np.float64)
    return CesaroPrefixMoments(
        s0=np.cumsum(values, dtype=np.float64),
        s1=np.cumsum(indices * values, dtype=np.float64),
        s2=np.cumsum(indices * indices * values, dtype=np.float64),
    )


def cesaro_c2_from_prefix(moments: CesaroPrefixMoments, x: int) -> float:
    if x <= 0 or x >= len(moments.s0):
        raise ValueError("x must index the prefix arrays")
    x_float = float(x)
    return 0.5 * (
        moments.s0[x]
        - (2.0 * moments.s1[x] / x_float)
        + (moments.s2[x] / (x_float * x_float))
    )


def cesaro_c2_direct(goldbach_values: np.ndarray, x: int) -> float:
    if x <= 0 or x >= len(goldbach_values):
        raise ValueError("x must index goldbach_values")
    return 0.5 * sum(
        goldbach_values[n] * ((1.0 - (n / x)) ** 2)
        for n in range(1, x + 1)
    )


def logarithmic_integer_grid(min_x: int, max_x: int, samples: int) -> list[int]:
    if min_x < 1 or max_x < min_x:
        raise ValueError("expected 1 <= min_x <= max_x")
    if samples < 2:
        raise ValueError("samples must be at least 2")

    raw = np.exp(np.linspace(math.log(min_x), math.log(max_x), samples))
    grid = sorted(set(int(round(value)) for value in raw))
    if grid[0] != min_x:
        grid.insert(0, min_x)
    if grid[-1] != max_x:
        grid.append(max_x)
    return grid


def riemann_zeros_up_to(height: float) -> tuple[float, ...]:
    if height <= 0:
        return ()
    if height > RIEMANN_ZERO_ORDINATES[-1]:
        raise ValueError(
            f"height {height} exceeds the certified local table limit "
            f"{RIEMANN_ZERO_ORDINATES[-1]}"
        )
    return tuple(value for value in RIEMANN_ZERO_ORDINATES if value <= height)


_LANCZOS_G = 7
_LANCZOS_COEFFICIENTS = (
    0.99999999999980993,
    676.5203681218851,
    -1259.1392167224028,
    771.32342877765313,
    -176.61502916214059,
    12.507343278686905,
    -0.13857109526572012,
    9.9843695780195716e-6,
    1.5056327351493116e-7,
)


def complex_log_gamma(value: complex) -> complex:
    z = complex(value)
    if z.real < 0.5:
        return cmath.log(math.pi) - cmath.log(cmath.sin(math.pi * z)) - complex_log_gamma(1.0 - z)

    shifted = z - 1.0
    series = complex(_LANCZOS_COEFFICIENTS[0])
    for index, coefficient in enumerate(_LANCZOS_COEFFICIENTS[1:], start=1):
        series += coefficient / (shifted + index)
    t = shifted + _LANCZOS_G + 0.5
    return (
        0.5 * math.log(2.0 * math.pi)
        + (shifted + 0.5) * cmath.log(t)
        - t
        + cmath.log(series)
    )


def linear_zero_coefficient(rho: complex) -> complex:
    return -2.0 / (rho * (rho + 1.0) * (rho + 2.0) * (rho + 3.0))


def explicit_pole_correction_normalized(xs: np.ndarray) -> np.ndarray:
    """Known order-X term for C2, normalized by X**(3/2)."""
    x_values = np.asarray(xs, dtype=np.float64)
    return -(math.log(2.0 * math.pi) / 3.0) / np.sqrt(x_values)


def explicit_linear_normalized(xs: np.ndarray, positive_zero_ordinates: tuple[float, ...]) -> np.ndarray:
    x_values = np.asarray(xs, dtype=np.float64)
    logs = np.log(x_values)
    result = np.zeros(len(x_values), dtype=np.float64)
    for ordinate in positive_zero_ordinates:
        rho = 0.5 + (1j * ordinate)
        coefficient = linear_zero_coefficient(rho)
        result += 2.0 * np.real(coefficient * np.exp(1j * ordinate * logs))
    return result


def explicit_double_normalized(xs: np.ndarray, positive_zero_ordinates: tuple[float, ...]) -> np.ndarray:
    x_values = np.asarray(xs, dtype=np.float64)
    rhos = [0.5 + (1j * ordinate) for ordinate in positive_zero_ordinates]
    rhos.extend(rho.conjugate() for rho in tuple(rhos))

    frequencies: list[float] = []
    coefficients: list[complex] = []
    for rho_1 in rhos:
        for rho_2 in rhos:
            log_coefficient = (
                complex_log_gamma(rho_1)
                + complex_log_gamma(rho_2)
                - complex_log_gamma(rho_1 + rho_2 + 3.0)
            )
            frequencies.append((rho_1 + rho_2).imag)
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
    x_values: np.ndarray,
    observed: np.ndarray,
    positive_zero_ordinates: tuple[float, ...],
    *,
    zero_height: float,
) -> list[CoefficientAudit]:
    if not positive_zero_ordinates:
        return []

    logs = np.log(np.asarray(x_values, dtype=np.float64))
    columns: list[np.ndarray] = []
    for ordinate in positive_zero_ordinates:
        columns.append(np.cos(ordinate * logs))
        columns.append(np.sin(ordinate * logs))
    design = np.column_stack(columns)
    fitted, _, _, _ = np.linalg.lstsq(design, observed, rcond=None)

    audits: list[CoefficientAudit] = []
    for index, ordinate in enumerate(positive_zero_ordinates):
        theoretical = linear_zero_coefficient(0.5 + (1j * ordinate))
        estimated = complex(fitted[2 * index] / 2.0, -fitted[(2 * index) + 1] / 2.0)
        phase_delta = cmath.phase(estimated) - cmath.phase(theoretical)
        phase_error = math.atan2(math.sin(phase_delta), math.cos(phase_delta))
        audits.append(
            CoefficientAudit(
                zero_height=float(zero_height),
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


def build_cesaro_calibration(
    *,
    max_x: int,
    min_x: int = 1_000,
    log_samples: int = 800,
    zero_heights: tuple[float, ...] = (50.0, 100.0, 143.0),
    discovery_fraction: float = 0.65,
) -> CesaroCalibrationExperiment:
    if max_x < min_x:
        raise ValueError("max_x must be at least min_x")
    if not 0.0 < discovery_fraction < 1.0:
        raise ValueError("discovery_fraction must be between 0 and 1")
    if not zero_heights:
        raise ValueError("at least one zero height is required")

    mangoldt = von_mangoldt_values(max_x)
    goldbach = additive_convolution_fft(mangoldt, max_n=max_x)
    moments = cesaro_prefix_moments(goldbach)
    grid = logarithmic_integer_grid(min_x, max_x, log_samples)
    split_index = max(1, min(len(grid) - 1, int(len(grid) * discovery_fraction)))

    c2_values = np.asarray([cesaro_c2_from_prefix(moments, x) for x in grid], dtype=np.float64)
    x_values = np.asarray(grid, dtype=np.float64)
    observed_z1 = (c2_values - ((x_values * x_values) / 24.0)) / np.power(x_values, 1.5)
    samples = tuple(
        CesaroSample(
            x=x,
            c2=float(c2_values[index]),
            observed_z1=float(observed_z1[index]),
            split="discovery" if index < split_index else "validation",
        )
        for index, x in enumerate(grid)
    )

    check_candidates = sorted(
        {
            value
            for value in (4, 5, 6, 10, 20, max_x // 2, max_x)
            if 2 <= value <= max_x
        }
    )
    checks = tuple(
        ConvolutionCheck(
            n=n,
            direct=(direct := additive_convolution_value(mangoldt, n)),
            fft=float(goldbach[n]),
            absolute_error=abs(direct - float(goldbach[n])),
        )
        for n in check_candidates
    )

    metrics: list[CalibrationMetric] = []
    coefficient_audits: list[CoefficientAudit] = []
    split_slices = {
        "discovery": slice(0, split_index),
        "validation": slice(split_index, len(grid)),
    }
    for height in zero_heights:
        zeros = riemann_zeros_up_to(height)
        pole_correction = explicit_pole_correction_normalized(x_values)
        linear = explicit_linear_normalized(x_values, zeros)
        double = explicit_double_normalized(x_values, zeros)
        coefficient_audits.extend(
            _coefficient_audits(
                x_values[:split_index],
                observed_z1[:split_index] - pole_correction[:split_index],
                zeros,
                zero_height=height,
            )
        )
        predictions = {
            "M0_pole_correction": pole_correction,
            "M1_pole_linear": pole_correction + linear,
            "M2_pole_linear_double": pole_correction + linear + double,
        }
        for split_name, split_slice in split_slices.items():
            for model_name, prediction in predictions.items():
                rmse, mae, max_error = _error_metrics(
                    observed_z1[split_slice],
                    prediction[split_slice],
                )
                metrics.append(
                    CalibrationMetric(
                        zero_height=float(height),
                        zero_count=len(zeros),
                        split=split_name,
                        model=model_name,
                        rmse=rmse,
                        mae=mae,
                        max_absolute_error=max_error,
                    )
                )

    return CesaroCalibrationExperiment(
        min_x=min_x,
        max_x=max_x,
        log_samples_requested=log_samples,
        zero_source=RIEMANN_ZERO_SOURCE,
        zero_table_max=RIEMANN_ZERO_ORDINATES[-1],
        zero_heights=tuple(float(height) for height in zero_heights),
        samples=samples,
        convolution_checks=checks,
        metrics=tuple(metrics),
        coefficient_audits=tuple(coefficient_audits),
    )


def write_calibration_artifacts(
    output_dir: Path,
    experiment: CesaroCalibrationExperiment,
) -> dict[str, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    suffix = f"{experiment.min_x}_{experiment.max_x}"
    paths = {
        "samples_csv": output_dir / f"goldbach_005a_samples_{suffix}.csv",
        "metrics_csv": output_dir / f"goldbach_005a_metrics_{suffix}.csv",
        "checks_csv": output_dir / f"goldbach_005a_convolution_checks_{suffix}.csv",
        "coefficient_audits_csv": output_dir / f"goldbach_005a_coefficient_audits_{suffix}.csv",
        "summary_json": output_dir / f"goldbach_005a_summary_{suffix}.json",
    }

    with paths["samples_csv"].open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["x", "c2", "observed_z1", "split"])
        writer.writeheader()
        writer.writerows(asdict(sample) for sample in experiment.samples)

    with paths["metrics_csv"].open("w", newline="", encoding="utf-8") as handle:
        fieldnames = [
            "zero_height",
            "zero_count",
            "split",
            "model",
            "rmse",
            "mae",
            "max_absolute_error",
        ]
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(asdict(metric) for metric in experiment.metrics)

    with paths["checks_csv"].open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["n", "direct", "fft", "absolute_error"])
        writer.writeheader()
        writer.writerows(asdict(check) for check in experiment.convolution_checks)

    with paths["coefficient_audits_csv"].open("w", newline="", encoding="utf-8") as handle:
        fieldnames = [
            "zero_height",
            "zero_index",
            "ordinate",
            "theoretical_real",
            "theoretical_imag",
            "estimated_real",
            "estimated_imag",
            "amplitude_ratio",
            "phase_error",
        ]
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(asdict(audit) for audit in experiment.coefficient_audits)

    validation_metrics = [metric for metric in experiment.metrics if metric.split == "validation"]
    best_validation = min(validation_metrics, key=lambda metric: metric.rmse)
    calibration_height = min(experiment.zero_heights)
    calibration_metrics = {
        metric.model: metric
        for metric in validation_metrics
        if metric.zero_height == calibration_height
    }
    calibration_audits = sorted(
        (
            audit
            for audit in experiment.coefficient_audits
            if audit.zero_height == calibration_height
        ),
        key=lambda audit: audit.zero_index,
    )[:5]
    rmse_improves = (
        calibration_metrics["M1_pole_linear"].rmse
        < calibration_metrics["M0_pole_correction"].rmse
    )
    amplitude_recovered = bool(calibration_audits) and all(
        0.5 <= audit.amplitude_ratio <= 2.0 for audit in calibration_audits
    )
    phase_recovered = bool(calibration_audits) and all(
        abs(audit.phase_error) <= 0.5 for audit in calibration_audits
    )
    calibration_passed = rmse_improves and amplitude_recovered and phase_recovered
    calibration_criteria = {
        "zero_height": calibration_height,
        "audited_zero_count": len(calibration_audits),
        "validation_rmse_m0": calibration_metrics["M0_pole_correction"].rmse,
        "validation_rmse_m1": calibration_metrics["M1_pole_linear"].rmse,
        "requires_m1_rmse_below_m0": rmse_improves,
        "amplitude_ratio_interval": [0.5, 2.0],
        "amplitude_ratios_within_interval": amplitude_recovered,
        "maximum_absolute_phase_error": 0.5,
        "phase_errors_within_limit": phase_recovered,
    }
    summary = {
        "experiment_id": "G5A-005",
        "evidence_level": "Calibracion numerica determinista",
        "formal_proof": False,
        "calibration_passed": calibration_passed,
        "calibration_status": (
            "passed" if calibration_passed else "inconclusive_finite_scale"
        ),
        "calibration_criteria": calibration_criteria,
        "window": {"min": experiment.min_x, "max": experiment.max_x},
        "log_samples_requested": experiment.log_samples_requested,
        "log_samples_realized": len(experiment.samples),
        "zero_source": experiment.zero_source,
        "formula_correction": (
            "Includes -2*(zeta'/zeta)(0)*X/Gamma(k+2); for k=2 this is "
            "-log(2*pi)*X/3."
        ),
        "zero_table_max": experiment.zero_table_max,
        "zero_heights": list(experiment.zero_heights),
        "best_validation_metric": asdict(best_validation),
        "convolution_max_absolute_error": max(
            check.absolute_error for check in experiment.convolution_checks
        ),
        "metrics": [asdict(metric) for metric in experiment.metrics],
        "interpretation": (
            "Calibracion del promedio Cesaro C2 frente a la formula explicita conocida, "
            "incluido el termino de polo de orden X. No constituye evidencia de una "
            "frecuencia nueva."
        ),
    }
    paths["summary_json"].write_text(
        json.dumps(summary, indent=2, ensure_ascii=False, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    return paths
