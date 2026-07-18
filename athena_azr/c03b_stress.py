"""Falsification and robustness audits for the calibrated C03 channel."""

from __future__ import annotations

import hashlib
import csv
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np

from athena_azr.c03_laplace_chi3 import (
    CHI3_ZERO_ORDINATES,
    c03_cross_normalized,
    c03_linear_coefficient,
    c03_linear_normalized,
    c03_pole_normalized,
    chi3_values,
    chi3_zeros_up_to,
    mixed_cesaro_c2_from_prefix,
    mixed_convolution_fft,
)
from athena_azr.cesaro_calibration import (
    cesaro_prefix_moments,
    logarithmic_integer_grid,
    riemann_zeros_up_to,
    von_mangoldt_values,
)


@dataclass(frozen=True)
class MaxTResult:
    real_maximum: float
    real_peak_frequency: float
    rayleigh_resolution: float
    p_fwer: float
    control_maxima: np.ndarray


@dataclass(frozen=True)
class FrequencyFit:
    frequency: float
    estimated_real: float
    estimated_imag: float
    discovery_rmse: float
    validation_rmse: float


@dataclass(frozen=True)
class AblationRecord:
    window_max: int
    zero_count: int
    model: str
    split: str
    rmse: float


@dataclass(frozen=True)
class WindowRecord:
    window_max: int
    zero_count: int
    first_zero_amplitude_ratio: float
    first_zero_phase_error: float
    fitted_validation_rmse: float
    correct_pole_validation_rmse: float
    flipped_pole_validation_rmse: float
    pole_flip_degradation_ratio: float


@dataclass(frozen=True)
class WrongFrequencyRecord:
    frequency: float
    control_type: str
    estimated_amplitude: float
    discovery_rmse: float
    validation_rmse: float


@dataclass(frozen=True)
class C03BAudit:
    min_x: int
    max_x: int
    log_samples: int
    discovery_fraction: float
    window_maxima: tuple[int, ...]
    ablation_counts: tuple[int, ...]
    full_chi3_zero_height: float
    zeta_zero_height: float
    random_frequency_controls: int
    seed: int
    experiment_status: str
    novelty_claim: bool
    frozen_channels: tuple[str, ...]
    ablations: tuple[AblationRecord, ...]
    windows: tuple[WindowRecord, ...]
    wrong_frequencies: tuple[WrongFrequencyRecord, ...]
    max_t: MaxTResult


def permute_within_classes(
    values: np.ndarray,
    classes: np.ndarray,
    rng: np.random.Generator,
) -> np.ndarray:
    """Permute values independently inside each observed class."""
    source = np.asarray(values)
    labels = np.asarray(classes)
    if source.ndim != 1 or labels.ndim != 1 or len(source) != len(labels):
        raise ValueError("values and classes must be one-dimensional and equally sized")

    result = source.copy()
    for label in np.unique(labels):
        indices = np.flatnonzero(labels == label)
        result[indices] = source[rng.permutation(indices)]
    return result


def _spectral_projection(
    log_x: np.ndarray,
    residual: np.ndarray,
    frequencies: np.ndarray,
) -> tuple[np.ndarray, float]:
    coordinates = np.asarray(log_x, dtype=np.float64)
    signal = np.asarray(residual, dtype=np.float64)
    omega = np.asarray(frequencies, dtype=np.float64)
    if coordinates.ndim != 1 or signal.ndim != 1 or len(coordinates) != len(signal):
        raise ValueError("log_x and residual must be one-dimensional and equally sized")
    if omega.ndim != 1 or not len(omega):
        raise ValueError("frequencies must be a non-empty one-dimensional array")

    centered = signal - np.mean(signal)
    window = np.hanning(len(signal)) if len(signal) > 2 else np.ones(len(signal))
    weighted = centered * window
    scale = float(np.dot(weighted, weighted))
    phase = np.exp(-1j * np.outer(omega, coordinates))
    return phase @ weighted, scale


def spectral_power(
    log_x: np.ndarray,
    residual: np.ndarray,
    frequencies: np.ndarray,
) -> np.ndarray:
    projection, scale = _spectral_projection(log_x, residual, frequencies)
    if scale == 0.0:
        return np.zeros(len(np.asarray(frequencies)), dtype=np.float64)
    return np.abs(projection) ** 2 / scale


def max_t_permutation_test(
    log_x: np.ndarray,
    residual: np.ndarray,
    classes: np.ndarray,
    frequencies: np.ndarray,
    *,
    controls: int,
    seed: int,
) -> MaxTResult:
    if controls < 1:
        raise ValueError("controls must be positive")
    coordinates = np.asarray(log_x, dtype=np.float64)
    signal = np.asarray(residual, dtype=np.float64)
    omega = np.asarray(frequencies, dtype=np.float64)
    centered = signal - np.mean(signal)
    window = np.hanning(len(signal)) if len(signal) > 2 else np.ones(len(signal))
    phase = np.exp(-1j * np.outer(omega, coordinates))
    real_weighted = centered * window
    real_scale = float(np.dot(real_weighted, real_weighted))
    real_powers = (
        np.abs(phase @ real_weighted) ** 2 / real_scale
        if real_scale
        else np.zeros(len(omega), dtype=np.float64)
    )
    real_index = int(np.argmax(real_powers))
    rng = np.random.default_rng(seed)
    maxima = np.empty(controls, dtype=np.float64)
    batch_size = 128
    for start in range(0, controls, batch_size):
        stop = min(start + batch_size, controls)
        weighted_controls = np.empty((stop - start, len(signal)), dtype=np.float64)
        for local_index in range(stop - start):
            control = permute_within_classes(centered, classes, rng)
            weighted_controls[local_index] = control * window
        scales = np.sum(weighted_controls * weighted_controls, axis=1)
        projections = weighted_controls @ phase.T
        powers = np.abs(projections) ** 2
        powers = np.divide(
            powers,
            scales[:, np.newaxis],
            out=np.zeros_like(powers, dtype=np.float64),
            where=scales[:, np.newaxis] != 0.0,
        )
        maxima[start:stop] = np.max(powers, axis=1)
    real_maximum = float(real_powers[real_index])
    p_fwer = float((1 + np.count_nonzero(maxima >= real_maximum)) / (controls + 1))
    log_span = float(np.ptp(coordinates))
    return MaxTResult(
        real_maximum=real_maximum,
        real_peak_frequency=float(np.asarray(frequencies)[real_index]),
        rayleigh_resolution=float((2.0 * math.pi / log_span) if log_span else math.inf),
        p_fwer=p_fwer,
        control_maxima=maxima,
    )


def fit_log_frequency(
    discovery_log_x: np.ndarray,
    discovery_target: np.ndarray,
    validation_log_x: np.ndarray,
    validation_target: np.ndarray,
    frequency: float,
) -> FrequencyFit:
    discovery_coordinates = np.asarray(discovery_log_x, dtype=np.float64)
    discovery_values = np.asarray(discovery_target, dtype=np.float64)
    validation_coordinates = np.asarray(validation_log_x, dtype=np.float64)
    validation_values = np.asarray(validation_target, dtype=np.float64)
    design = np.column_stack(
        (
            np.cos(frequency * discovery_coordinates),
            np.sin(frequency * discovery_coordinates),
        )
    )
    fitted, _, _, _ = np.linalg.lstsq(design, discovery_values, rcond=None)
    validation_design = np.column_stack(
        (
            np.cos(frequency * validation_coordinates),
            np.sin(frequency * validation_coordinates),
        )
    )
    discovery_error = discovery_values - (design @ fitted)
    validation_error = validation_values - (validation_design @ fitted)
    return FrequencyFit(
        frequency=float(frequency),
        estimated_real=float(fitted[0] / 2.0),
        estimated_imag=float(-fitted[1] / 2.0),
        discovery_rmse=float(np.sqrt(np.mean(discovery_error * discovery_error))),
        validation_rmse=float(np.sqrt(np.mean(validation_error * validation_error))),
    )


def hash_files(paths: tuple[Path, ...] | list[Path]) -> dict[str, str]:
    result: dict[str, str] = {}
    for path in paths:
        file_path = Path(path)
        digest = hashlib.sha256()
        with file_path.open("rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(chunk)
        result[str(file_path)] = digest.hexdigest()
    return result


def protected_baseline_paths(project_root: Path) -> tuple[Path, ...]:
    artifacts = Path(project_root) / "artifacts"
    if not artifacts.is_dir():
        return ()
    protected: list[Path] = []
    for path in artifacts.rglob("*"):
        if not path.is_file() or "c03b_stress_tests" in path.parts:
            continue
        name = path.name.lower()
        if (
            name.startswith("c03_")
            or name.startswith("goldbach_005a_")
            or any(channel in name for channel in ("c05", "c35", "c15"))
        ):
            protected.append(path)
    return tuple(sorted(protected, key=lambda path: str(path).lower()))


def _rmse(observed: np.ndarray, predicted: np.ndarray) -> float:
    error = np.asarray(observed, dtype=np.float64) - np.asarray(predicted, dtype=np.float64)
    return float(np.sqrt(np.mean(error * error)))


def _fit_log_frequencies(
    discovery_log_x: np.ndarray,
    discovery_target: np.ndarray,
    validation_log_x: np.ndarray,
    validation_target: np.ndarray,
    frequencies: tuple[float, ...],
) -> tuple[np.ndarray, float]:
    columns: list[np.ndarray] = []
    validation_columns: list[np.ndarray] = []
    for frequency in frequencies:
        columns.extend(
            (
                np.cos(frequency * discovery_log_x),
                np.sin(frequency * discovery_log_x),
            )
        )
        validation_columns.extend(
            (
                np.cos(frequency * validation_log_x),
                np.sin(frequency * validation_log_x),
            )
        )
    design = np.column_stack(columns)
    validation_design = np.column_stack(validation_columns)
    fitted, _, _, _ = np.linalg.lstsq(design, discovery_target, rcond=None)
    validation_rmse = _rmse(validation_target, validation_design @ fitted)
    coefficients = np.asarray(
        [complex(fitted[2 * index] / 2.0, -fitted[(2 * index) + 1] / 2.0)
         for index in range(len(frequencies))],
        dtype=np.complex128,
    )
    return coefficients, validation_rmse


def _split_index(length: int, fraction: float) -> int:
    return max(1, min(length - 1, int(length * fraction)))


def _random_control_frequencies(
    rng: np.random.Generator,
    count: int,
    minimum: float,
    maximum: float,
    excluded: tuple[float, ...],
) -> tuple[float, ...]:
    result: list[float] = []
    while len(result) < count:
        candidate = float(rng.uniform(minimum, maximum))
        if all(abs(candidate - value) >= 0.25 for value in (*excluded, *result)):
            result.append(candidate)
    return tuple(result)


def build_c03b_audit(
    *,
    max_x: int,
    min_x: int,
    log_samples: int,
    window_maxima: tuple[int, ...],
    ablation_counts: tuple[int, ...],
    full_chi3_zero_height: float,
    zeta_zero_height: float,
    random_frequency_controls: int,
    max_t_controls: int,
    max_t_frequency_min: float,
    max_t_frequency_max: float,
    max_t_frequency_step: float,
    seed: int,
    discovery_fraction: float = 0.65,
) -> C03BAudit:
    if max_x != max(window_maxima):
        raise ValueError("max_x must equal the largest window maximum")
    if min(window_maxima) < min_x:
        raise ValueError("all windows must end at or above min_x")
    if not 0.0 < discovery_fraction < 1.0:
        raise ValueError("discovery_fraction must be between zero and one")
    if max_t_frequency_step <= 0.0:
        raise ValueError("max_t_frequency_step must be positive")

    chi3_zeros = chi3_zeros_up_to(full_chi3_zero_height)
    if not chi3_zeros or max(ablation_counts) > len(chi3_zeros):
        raise ValueError("the zero table does not cover the requested ablations")
    zeta_zeros = riemann_zeros_up_to(zeta_zero_height)
    mangoldt = von_mangoldt_values(max_x)
    twisted = mangoldt * chi3_values(max_x)
    convolution = mixed_convolution_fft(mangoldt, twisted, max_n=max_x)
    moments = cesaro_prefix_moments(convolution)

    ablations: list[AblationRecord] = []
    windows: list[WindowRecord] = []
    largest_context: dict[str, np.ndarray | int] = {}
    audit_count = max(ablation_counts)

    for window_max in window_maxima:
        grid = logarithmic_integer_grid(min_x, window_max, log_samples)
        xs = np.asarray(grid, dtype=np.float64)
        log_x = np.log(xs)
        split_at = _split_index(len(grid), discovery_fraction)
        observed = np.asarray(
            [mixed_cesaro_c2_from_prefix(moments, x) for x in grid],
            dtype=np.float64,
        ) / np.power(xs, 1.5)
        pole = c03_pole_normalized(xs)

        for zero_count in ablation_counts:
            selected = chi3_zeros[:zero_count]
            linear = c03_linear_normalized(xs, selected)
            cross = c03_cross_normalized(xs, zeta_zeros, selected)
            predictions = {
                "M1_pole_lzeros": pole + linear,
                "M2_pole_lzeros_cross": pole + linear + cross,
            }
            for split_name, split_slice in (
                ("discovery", slice(0, split_at)),
                ("validation", slice(split_at, len(grid))),
            ):
                for model, prediction in predictions.items():
                    ablations.append(
                        AblationRecord(
                            window_max=window_max,
                            zero_count=zero_count,
                            model=model,
                            split=split_name,
                            rmse=_rmse(observed[split_slice], prediction[split_slice]),
                        )
                    )

        audit_zeros = chi3_zeros[:audit_count]
        audit_linear = c03_linear_normalized(xs, audit_zeros)
        audit_cross = c03_cross_normalized(xs, zeta_zeros, audit_zeros)
        coefficients, fitted_validation_rmse = _fit_log_frequencies(
            log_x[:split_at],
            observed[:split_at] - pole[:split_at] - audit_cross[:split_at],
            log_x[split_at:],
            observed[split_at:] - pole[split_at:] - audit_cross[split_at:],
            audit_zeros,
        )
        theoretical = c03_linear_coefficient(0.5 + (1j * audit_zeros[0]))
        estimated = coefficients[0]
        phase_delta = math.atan2(
            math.sin(np.angle(estimated) - np.angle(theoretical)),
            math.cos(np.angle(estimated) - np.angle(theoretical)),
        )
        correct_prediction = pole + audit_linear + audit_cross
        flipped_prediction = -pole + audit_linear + audit_cross
        correct_rmse = _rmse(observed[split_at:], correct_prediction[split_at:])
        flipped_rmse = _rmse(observed[split_at:], flipped_prediction[split_at:])
        windows.append(
            WindowRecord(
                window_max=window_max,
                zero_count=audit_count,
                first_zero_amplitude_ratio=float(abs(estimated) / abs(theoretical)),
                first_zero_phase_error=float(phase_delta),
                fitted_validation_rmse=fitted_validation_rmse,
                correct_pole_validation_rmse=correct_rmse,
                flipped_pole_validation_rmse=flipped_rmse,
                pole_flip_degradation_ratio=float(flipped_rmse / correct_rmse),
            )
        )
        if window_max == max_x:
            largest_context = {
                "xs": xs,
                "log_x": log_x,
                "observed": observed,
                "pole": pole,
                "split_at": split_at,
            }

    xs = np.asarray(largest_context["xs"])
    log_x = np.asarray(largest_context["log_x"])
    observed = np.asarray(largest_context["observed"])
    pole = np.asarray(largest_context["pole"])
    split_at = int(largest_context["split_at"])
    single_frequency_target = observed - pole
    rng = np.random.default_rng(seed)
    fixed_wrong = (4.5324, 7.8096)
    random_wrong = _random_control_frequencies(
        rng,
        random_frequency_controls,
        max_t_frequency_min,
        max_t_frequency_max,
        (CHI3_ZERO_ORDINATES[0], *fixed_wrong, *chi3_zeros),
    )
    wrong_frequencies: list[WrongFrequencyRecord] = []
    for frequency, control_type in (
        (CHI3_ZERO_ORDINATES[0], "correct_chi3_zero"),
        *((frequency, "fixed_wrong") for frequency in fixed_wrong),
        *((frequency, "random_wrong") for frequency in random_wrong),
    ):
        fit = fit_log_frequency(
            log_x[:split_at],
            single_frequency_target[:split_at],
            log_x[split_at:],
            single_frequency_target[split_at:],
            frequency,
        )
        wrong_frequencies.append(
            WrongFrequencyRecord(
                frequency=float(frequency),
                control_type=control_type,
                estimated_amplitude=float(abs(complex(fit.estimated_real, fit.estimated_imag))),
                discovery_rmse=fit.discovery_rmse,
                validation_rmse=fit.validation_rmse,
            )
        )

    full_linear = c03_linear_normalized(xs, chi3_zeros)
    full_cross = c03_cross_normalized(xs, zeta_zeros, chi3_zeros)
    full_residual = observed - pole - full_linear - full_cross
    validation_log_x = log_x[split_at:]
    validation_residual = full_residual[split_at:]
    validation_classes = np.asarray(xs[split_at:], dtype=np.int64) % 3
    scan_frequencies = np.arange(
        max_t_frequency_min,
        max_t_frequency_max + (0.5 * max_t_frequency_step),
        max_t_frequency_step,
        dtype=np.float64,
    )
    max_t = max_t_permutation_test(
        validation_log_x,
        validation_residual,
        validation_classes,
        scan_frequencies,
        controls=max_t_controls,
        seed=seed + 1,
    )

    return C03BAudit(
        min_x=min_x,
        max_x=max_x,
        log_samples=log_samples,
        discovery_fraction=discovery_fraction,
        window_maxima=tuple(window_maxima),
        ablation_counts=tuple(ablation_counts),
        full_chi3_zero_height=float(full_chi3_zero_height),
        zeta_zero_height=float(zeta_zero_height),
        random_frequency_controls=random_frequency_controls,
        seed=seed,
        experiment_status="falsification_audit",
        novelty_claim=False,
        frozen_channels=("C00", "C03", "C05", "C35", "C15"),
        ablations=tuple(ablations),
        windows=tuple(windows),
        wrong_frequencies=tuple(wrong_frequencies),
        max_t=max_t,
    )


def _artifact_label(max_x: int) -> str:
    exponent = round(math.log10(max_x)) if max_x > 0 else 0
    if max_x > 0 and 10**exponent == max_x:
        return f"X1e{exponent}"
    return f"X{max_x}"


def _write_dataclass_csv(path: Path, rows: tuple[object, ...]) -> None:
    if not rows:
        raise ValueError(f"cannot write an empty artifact: {path.name}")
    dictionaries = [asdict(row) for row in rows]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(dictionaries[0].keys()))
        writer.writeheader()
        writer.writerows(dictionaries)


def write_c03b_artifacts(
    output_dir: Path,
    audit: C03BAudit,
    protected_hashes_before: dict[str, str],
) -> dict[str, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    label = _artifact_label(audit.max_x)
    paths = {
        "ablation_csv": output_dir / f"c03b_ablation_{label}.csv",
        "windows_csv": output_dir / f"c03b_windows_{label}.csv",
        "wrong_frequencies_csv": output_dir / f"c03b_wrong_frequencies_{label}.csv",
        "max_t_csv": output_dir / f"c03b_max_t_{label}.csv",
        "immutability_csv": output_dir / f"c03b_immutability_{label}.csv",
        "summary_json": output_dir / f"c03b_summary_{label}.json",
    }
    _write_dataclass_csv(paths["ablation_csv"], audit.ablations)
    _write_dataclass_csv(paths["windows_csv"], audit.windows)
    _write_dataclass_csv(paths["wrong_frequencies_csv"], audit.wrong_frequencies)

    with paths["max_t_csv"].open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["control_index", "maximum_power"])
        writer.writeheader()
        writer.writerows(
            {"control_index": index + 1, "maximum_power": float(value)}
            for index, value in enumerate(audit.max_t.control_maxima)
        )

    immutability_rows: list[dict[str, object]] = []
    for path_text, before_digest in sorted(protected_hashes_before.items()):
        protected_path = Path(path_text)
        after_digest = (
            hash_files((protected_path,))[path_text]
            if protected_path.is_file()
            else "__missing__"
        )
        immutability_rows.append(
            {
                "path": path_text,
                "sha256_before": before_digest,
                "sha256_after": after_digest,
                "unchanged": before_digest == after_digest,
            }
        )
    with paths["immutability_csv"].open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["path", "sha256_before", "sha256_after", "unchanged"],
        )
        writer.writeheader()
        writer.writerows(immutability_rows)

    validation_m2 = [
        row
        for row in audit.ablations
        if row.split == "validation" and row.model == "M2_pole_lzeros_cross"
    ]
    ablation_monotone = True
    for window_max in audit.window_maxima:
        rows = sorted(
            (row for row in validation_m2 if row.window_max == window_max),
            key=lambda row: row.zero_count,
        )
        ablation_monotone = ablation_monotone and all(
            right.rmse < left.rmse for left, right in zip(rows, rows[1:])
        )

    correct_frequency = next(
        row for row in audit.wrong_frequencies if row.control_type == "correct_chi3_zero"
    )
    false_frequencies = [
        row for row in audit.wrong_frequencies if row.control_type != "correct_chi3_zero"
    ]
    wrong_frequencies_rejected = all(
        correct_frequency.validation_rmse < row.validation_rmse for row in false_frequencies
    )
    pole_sign_required = all(
        row.flipped_pole_validation_rmse > row.correct_pole_validation_rmse
        for row in audit.windows
    )
    persistence_rows = audit.windows[-min(3, len(audit.windows)):]
    phase_persistent = all(
        0.9 <= row.first_zero_amplitude_ratio <= 1.1
        and abs(row.first_zero_phase_error) <= 0.1
        for row in persistence_rows
    )
    residual_whiteness_not_rejected = audit.max_t.p_fwer >= 0.05
    immutability_passed = all(bool(row["unchanged"]) for row in immutability_rows)
    robustness_passed = all(
        (
            ablation_monotone,
            wrong_frequencies_rejected,
            pole_sign_required,
            phase_persistent,
            residual_whiteness_not_rejected,
            immutability_passed,
        )
    )
    peak_classification = (
        "unresolved_low_frequency_drift"
        if audit.max_t.real_peak_frequency < audit.max_t.rayleigh_resolution
        else "resolved_residual_peak_requires_theoretical_audit"
    )

    summary = {
        "experiment_id": "G5B-005-C03B",
        "channel": "C03-B",
        "experiment_status": audit.experiment_status,
        "expansion_status": "controlled_truncation_audit",
        "formal_proof": False,
        "novelty_claim": audit.novelty_claim,
        "novelty_status": "not_established",
        "robustness_passed": robustness_passed,
        "criteria": {
            "ablation_strictly_monotone": ablation_monotone,
            "wrong_frequencies_rejected_out_of_sample": wrong_frequencies_rejected,
            "correct_pole_sign_required": pole_sign_required,
            "first_zero_phase_and_amplitude_persistent": phase_persistent,
            "residual_whiteness_not_rejected_at_0_05": residual_whiteness_not_rejected,
        },
        "window": {"min": audit.min_x, "max": audit.max_x},
        "window_maxima": list(audit.window_maxima),
        "ablation_counts": list(audit.ablation_counts),
        "log_samples_per_window": audit.log_samples,
        "discovery_fraction": audit.discovery_fraction,
        "full_chi3_zero_height": audit.full_chi3_zero_height,
        "zeta_zero_height": audit.zeta_zero_height,
        "random_frequency_controls": audit.random_frequency_controls,
        "max_t": {
            "controls": len(audit.max_t.control_maxima),
            "real_maximum": audit.max_t.real_maximum,
            "real_peak_frequency": audit.max_t.real_peak_frequency,
            "rayleigh_resolution": audit.max_t.rayleigh_resolution,
            "peak_classification": peak_classification,
            "structural_origin": "finite_scale_or_known_component_leakage_candidate",
            "p_fwer": audit.max_t.p_fwer,
            "control_maximum_q95": float(np.quantile(audit.max_t.control_maxima, 0.95)),
        },
        "immutability_passed": immutability_passed,
        "protected_file_count": len(immutability_rows),
        "frozen_channels": list(audit.frozen_channels),
        "interpretation": (
            "Esta auditoria no descubre una frecuencia nueva; intenta falsificar la "
            "robustez de una calibracion existente mediante controles negativos, "
            "ablacion, escalado, inversion de signo y correccion max-T."
        ),
    }
    paths["summary_json"].write_text(
        json.dumps(summary, indent=2, ensure_ascii=False, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    return paths
