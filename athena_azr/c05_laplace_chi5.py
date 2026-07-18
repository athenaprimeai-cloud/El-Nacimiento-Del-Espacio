"""Provisional, quarantined implementation of the mixed Goldbach channel C05."""

from __future__ import annotations

import cmath
import csv
import hashlib
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np

from athena_azr.c03_laplace_chi3 import (
    c03_cross_normalized,
    c03_linear_coefficient,
    c03_linear_normalized,
    hurwitz_zeta_euler_maclaurin,
    mixed_cesaro_c2_direct,
    mixed_cesaro_c2_from_prefix,
    mixed_convolution_direct,
    mixed_convolution_fft,
)
from athena_azr.cesaro_calibration import (
    CesaroPrefixMoments,
    cesaro_prefix_moments,
    logarithmic_integer_grid,
    riemann_zeros_up_to,
    von_mangoldt_values,
)


CHI5_B0 = -0.02202465783872691842463476000992951686
CHI5_L_DERIVATIVE_AT_ZERO = 0.4812118250596034474977589134243601475
C05_IMPLEMENTATION_STATUS = "provisional_quarantined"
C05_OFFICIAL_STATUS = "not_accepted"
C05_RETROSPECTIVE_APPROVAL = "rejected_for_now"
C05_FINAL_REVIEW_STATUS = "pending_clean_rerun"
C05_RERUN_EXPERIMENT_ID = "G5B-005E-R"
C05_QUARANTINE_ARCHIVE = Path("artifacts/goldbach_cesaro/c05_controlled")
C05_ALLOWED_RERUN_CONTROL_FILES = frozenset(
    {"C05_SEALED_PROTOCOL.json", "C05_EXECUTION_AUTHORIZATION.json"}
)
C05_ALLOWED_MODELS = (
    "M0_local",
    "M1_local_lzeros",
    "M2_local_lzeros_cross",
)
CHI5_ZERO_SOURCE = (
    "Primitive quadratic Dirichlet character modulo 5; local completed-L "
    "sign changes with direct Hurwitz-zeta residual checks"
)

# Positive ordinates of L(s, chi_5), evaluated from the Hurwitz representation.
CHI5_ZERO_ORDINATES = (
    6.648453344727717,
    9.831444432886670,
    11.958845626083516,
    16.033821128384233,
    17.566994292325553,
    19.540732622784752,
    22.227405454459415,
    24.588466217408190,
    26.776095948004141,
    28.461035100177526,
    29.707909350480968,
    33.000456006870522,
    34.728812978904813,
    35.868638371812281,
    38.129184721436530,
    39.560572946403184,
    41.842438545791694,
    44.031290061441695,
    45.427300082782295,
    46.492727159491409,
    48.345661821067850,
    51.087751926746492,
    52.125902231316971,
    53.830445195442167,
    55.589280335404808,
    56.838865942890990,
    58.386117485358383,
    61.138864751921744,
    62.132904720233881,
    63.709543060981147,
    64.637359665374589,
    66.747641845937807,
    68.590727924825018,
    70.115837159193489,
    71.605959479243012,
    73.350105431468251,
    74.293688438016574,
    75.534904117228109,
    78.072170864382343,
    79.786062490097947,
    80.567300856410696,
    81.923380893154103,
    83.699157001874113,
    84.952507103754982,
    86.809996679338781,
    88.281776599709843,
    90.376573182128169,
    90.715525933147006,
    92.450243253774403,
    93.394423937828037,
    95.970001646037701,
    97.331588252898086,
    98.227457869901087,
    99.838050807536547,
    101.187717096918590,
    102.605287941050022,
    103.666131079767780,
    105.973193797758796,
    107.297103637525964,
    108.498106624261624,
    109.550258607184134,
    110.636197672627873,
    112.615769945049465,
    114.230639872381943,
    115.578413982377072,
    116.635671759783804,
    118.371162306355245,
    119.561491625879995,
    120.281734191852763,
    122.061632283894141,
    124.242837148950343,
    125.281536169054476,
    126.398699378424567,
    127.320634828115232,
    129.048300094320894,
    130.197038266857760,
    132.086005303117531,
    133.030228388331921,
    134.924963894111556,
    135.874497690098394,
    137.201083466840657,
    138.035699031304887,
    139.410599595145754,
    141.946240551604944,
    142.524512432987763,
    143.961591123287349,
)


def canonical_c05_protocol_hash(payload: object) -> str:
    """Hash a protocol payload using a deterministic JSON representation."""
    canonical = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")
    return hashlib.sha256(canonical).hexdigest()


def validate_c05_rerun_protocol(protocol_path: Path | None) -> dict[str, object]:
    """Verify the sealed protocol without treating it as run authorization."""
    if protocol_path is None or not Path(protocol_path).is_file():
        raise RuntimeError(
            "C05 is quarantined: a sealed protocol file is required before rerun."
        )
    try:
        protocol = json.loads(Path(protocol_path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise RuntimeError("C05 rerun protocol is not approved and sealed.") from error

    required_text = ("approved_by", "sealed_at", "protocol_sha256")
    sealed_payload = protocol.get("sealed_payload")
    approved = (
        protocol.get("experiment_id") == C05_RERUN_EXPERIMENT_ID
        and protocol.get("status") == "sealed_pending_execution_authorization"
        and protocol.get("approved") is True
        and protocol.get("hash_definition")
        == "sha256_canonical_json_of_sealed_payload"
        and isinstance(sealed_payload, dict)
        and all(isinstance(protocol.get(key), str) and protocol[key] for key in required_text)
    )
    if not approved:
        raise RuntimeError("C05 rerun protocol is not approved and sealed.")
    if canonical_c05_protocol_hash(sealed_payload) != protocol["protocol_sha256"]:
        raise RuntimeError("C05 sealed protocol hash mismatch.")
    return protocol


def validate_c05_execution_authorization(
    authorization_path: Path | None,
    protocol_sha256: str,
) -> dict[str, object]:
    """Require a separately hashed authorization referencing the sealed protocol."""
    if authorization_path is None or not Path(authorization_path).is_file():
        raise RuntimeError("C05 execution authorization is required after protocol sealing.")
    try:
        authorization = json.loads(Path(authorization_path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise RuntimeError("C05 execution authorization is invalid.") from error

    payload = authorization.get("authorization_payload")
    valid = (
        authorization.get("experiment_id") == C05_RERUN_EXPERIMENT_ID
        and authorization.get("status") == "execution_authorized"
        and authorization.get("approved") is True
        and authorization.get("hash_definition")
        == "sha256_canonical_json_of_authorization_payload"
        and isinstance(payload, dict)
        and payload.get("protocol_sha256") == protocol_sha256
        and isinstance(payload.get("authorized_by"), str)
        and bool(payload.get("authorized_by"))
        and isinstance(payload.get("authorized_at"), str)
        and bool(payload.get("authorized_at"))
        and isinstance(authorization.get("authorization_sha256"), str)
    )
    if not valid:
        raise RuntimeError("C05 execution authorization is invalid.")
    if canonical_c05_protocol_hash(payload) != authorization["authorization_sha256"]:
        raise RuntimeError("C05 execution authorization hash mismatch.")
    return authorization


def validate_c05_output_dir(output_dir: Path, project_root: Path) -> Path:
    """Keep every future rerun separate from the preserved quarantine archive."""
    root = Path(project_root).resolve()
    output = Path(output_dir)
    if not output.is_absolute():
        output = root / output
    output = output.resolve()
    archive = (root / C05_QUARANTINE_ARCHIVE).resolve()
    if output == archive or archive in output.parents:
        raise RuntimeError("C05 clean rerun cannot overwrite the quarantine archive.")
    if output.is_dir():
        unexpected = {
            path.name
            for path in output.iterdir()
            if path.name not in C05_ALLOWED_RERUN_CONTROL_FILES
        }
        if unexpected:
            raise RuntimeError("C05 clean rerun output directory contains unexpected files.")
    return output


@dataclass(frozen=True)
class C05Sample:
    x: int
    c05: float
    observed_z05: float
    m0_local: float
    m1_local_lzeros: float
    m2_local_lzeros_cross: float
    split: str


@dataclass(frozen=True)
class C05ConvolutionCheck:
    n: int
    direct: float
    fft: float
    absolute_error: float


@dataclass(frozen=True)
class C05Metric:
    chi5_zero_height: float
    chi5_zero_count: int
    zeta_zero_height: float
    zeta_zero_count: int
    split: str
    model: str
    rmse: float
    mae: float
    max_absolute_error: float


@dataclass(frozen=True)
class C05CoefficientAudit:
    chi5_zero_height: float
    zero_index: int
    ordinate: float
    theoretical_real: float
    theoretical_imag: float
    estimated_real: float
    estimated_imag: float
    amplitude_ratio: float
    phase_error: float


@dataclass(frozen=True)
class C05Experiment:
    min_x: int
    max_x: int
    log_samples_requested: int
    discovery_fraction: float
    chi5_zero_source: str
    chi5_zero_table_max: float
    chi5_zero_heights: tuple[float, ...]
    zeta_zero_height: float
    frozen_channels: tuple[str, ...]
    explicit_formula_complete: bool
    samples: tuple[C05Sample, ...]
    convolution_checks: tuple[C05ConvolutionCheck, ...]
    metrics: tuple[C05Metric, ...]
    coefficient_audits: tuple[C05CoefficientAudit, ...]


def chi5_values(limit: int) -> np.ndarray:
    if limit < 0:
        raise ValueError("limit must be non-negative")
    indices = np.arange(limit + 1, dtype=np.int64)
    residues = indices % 5
    values = np.zeros(limit + 1, dtype=np.int8)
    values[(residues == 1) | (residues == 4)] = 1
    values[(residues == 2) | (residues == 3)] = -1
    return values


def dirichlet_l_chi5(value: complex) -> complex:
    s = complex(value)
    if abs(s) < 1e-4:
        first = complex(CHI5_L_DERIVATIVE_AT_ZERO)
        second = first * CHI5_B0
        return (first * s) + (second * s * s)
    return cmath.exp(-s * math.log(5.0)) * (
        hurwitz_zeta_euler_maclaurin(s, 1.0 / 5.0)
        - hurwitz_zeta_euler_maclaurin(s, 2.0 / 5.0)
        - hurwitz_zeta_euler_maclaurin(s, 3.0 / 5.0)
        + hurwitz_zeta_euler_maclaurin(s, 4.0 / 5.0)
    )


def chi5_zeros_up_to(height: float) -> tuple[float, ...]:
    if height <= 0.0:
        return ()
    if height > CHI5_ZERO_ORDINATES[-1]:
        raise ValueError(
            f"height {height} exceeds the local chi5 table limit "
            f"{CHI5_ZERO_ORDINATES[-1]}"
        )
    return tuple(value for value in CHI5_ZERO_ORDINATES if value <= height)


def c05_pole_normalized(xs: np.ndarray) -> np.ndarray:
    x_values = np.asarray(xs, dtype=np.float64)
    return (
        ((11.0 / 6.0) - CHI5_B0 - np.log(x_values))
        / (6.0 * np.sqrt(x_values))
    )


def c05_linear_coefficient(rho: complex) -> complex:
    return c03_linear_coefficient(rho)


def c05_linear_normalized(
    xs: np.ndarray,
    positive_chi5_zero_ordinates: tuple[float, ...],
) -> np.ndarray:
    return c03_linear_normalized(xs, positive_chi5_zero_ordinates)


def c05_cross_normalized(
    xs: np.ndarray,
    positive_zeta_zero_ordinates: tuple[float, ...],
    positive_chi5_zero_ordinates: tuple[float, ...],
) -> np.ndarray:
    return c03_cross_normalized(
        xs,
        positive_zeta_zero_ordinates,
        positive_chi5_zero_ordinates,
    )


def _error_metrics(observed: np.ndarray, predicted: np.ndarray) -> tuple[float, float, float]:
    errors = np.asarray(observed, dtype=np.float64) - np.asarray(predicted, dtype=np.float64)
    return (
        float(np.sqrt(np.mean(errors * errors))),
        float(np.mean(np.abs(errors))),
        float(np.max(np.abs(errors))),
    )


def _coefficient_audits(
    xs: np.ndarray,
    observed_without_local_and_cross: np.ndarray,
    positive_chi5_zero_ordinates: tuple[float, ...],
    *,
    chi5_zero_height: float,
) -> list[C05CoefficientAudit]:
    if not positive_chi5_zero_ordinates:
        return []
    logs = np.log(np.asarray(xs, dtype=np.float64))
    columns: list[np.ndarray] = []
    for ordinate in positive_chi5_zero_ordinates:
        columns.append(np.cos(ordinate * logs))
        columns.append(np.sin(ordinate * logs))
    design = np.column_stack(columns)
    fitted, _, _, _ = np.linalg.lstsq(
        design,
        observed_without_local_and_cross,
        rcond=None,
    )

    audits: list[C05CoefficientAudit] = []
    for index, ordinate in enumerate(positive_chi5_zero_ordinates):
        theoretical = c05_linear_coefficient(0.5 + (1j * ordinate))
        estimated = complex(fitted[2 * index] / 2.0, -fitted[(2 * index) + 1] / 2.0)
        phase_delta = cmath.phase(estimated) - cmath.phase(theoretical)
        phase_error = math.atan2(math.sin(phase_delta), math.cos(phase_delta))
        audits.append(
            C05CoefficientAudit(
                chi5_zero_height=float(chi5_zero_height),
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


def build_c05_experiment(
    *,
    max_x: int,
    min_x: int,
    log_samples: int,
    chi5_zero_heights: tuple[float, ...],
    zeta_zero_height: float,
    discovery_fraction: float = 0.65,
) -> C05Experiment:
    if max_x < min_x:
        raise ValueError("max_x must be at least min_x")
    if not 0.0 < discovery_fraction < 1.0:
        raise ValueError("discovery_fraction must be between zero and one")
    if not chi5_zero_heights:
        raise ValueError("at least one chi5 zero height is required")

    mangoldt = von_mangoldt_values(max_x)
    twisted = mangoldt * chi5_values(max_x)
    mixed = mixed_convolution_fft(mangoldt, twisted, max_n=max_x)
    moments: CesaroPrefixMoments = cesaro_prefix_moments(mixed)
    grid = logarithmic_integer_grid(min_x, max_x, log_samples)
    split_index = max(1, min(len(grid) - 1, int(len(grid) * discovery_fraction)))
    x_values = np.asarray(grid, dtype=np.float64)
    c05_values = np.asarray(
        [mixed_cesaro_c2_from_prefix(moments, x) for x in grid],
        dtype=np.float64,
    )
    observed = c05_values / np.power(x_values, 1.5)
    local = c05_pole_normalized(x_values)
    zeta_zeros = riemann_zeros_up_to(zeta_zero_height)

    checks = tuple(
        C05ConvolutionCheck(
            n=n,
            direct=(direct := float(sum(mangoldt[m] * twisted[n - m] for m in range(1, n)))),
            fft=float(mixed[n]),
            absolute_error=abs(direct - float(mixed[n])),
        )
        for n in sorted(
            value
            for value in {4, 5, 6, 10, 20, max_x // 2, max_x}
            if 2 <= value <= max_x
        )
    )

    split_slices = {
        "discovery": slice(0, split_index),
        "validation": slice(split_index, len(grid)),
    }
    metrics: list[C05Metric] = []
    audits: list[C05CoefficientAudit] = []
    predictions_by_height: dict[float, dict[str, np.ndarray]] = {}
    for height in chi5_zero_heights:
        chi5_zeros = chi5_zeros_up_to(height)
        linear = c05_linear_normalized(x_values, chi5_zeros)
        cross = c05_cross_normalized(x_values, zeta_zeros, chi5_zeros)
        predictions = {
            "M0_local": local,
            "M1_local_lzeros": local + linear,
            "M2_local_lzeros_cross": local + linear + cross,
        }
        predictions_by_height[float(height)] = predictions
        audits.extend(
            _coefficient_audits(
                x_values[:split_index],
                observed[:split_index] - local[:split_index] - cross[:split_index],
                chi5_zeros,
                chi5_zero_height=height,
            )
        )
        for split_name, split_slice in split_slices.items():
            for model_name, prediction in predictions.items():
                rmse, mae, max_error = _error_metrics(
                    observed[split_slice],
                    prediction[split_slice],
                )
                metrics.append(
                    C05Metric(
                        chi5_zero_height=float(height),
                        chi5_zero_count=len(chi5_zeros),
                        zeta_zero_height=float(zeta_zero_height),
                        zeta_zero_count=len(zeta_zeros),
                        split=split_name,
                        model=model_name,
                        rmse=rmse,
                        mae=mae,
                        max_absolute_error=max_error,
                    )
                )

    reporting_height = max(float(height) for height in chi5_zero_heights)
    reporting_predictions = predictions_by_height[reporting_height]
    samples = tuple(
        C05Sample(
            x=x,
            c05=float(c05_values[index]),
            observed_z05=float(observed[index]),
            m0_local=float(reporting_predictions["M0_local"][index]),
            m1_local_lzeros=float(reporting_predictions["M1_local_lzeros"][index]),
            m2_local_lzeros_cross=float(
                reporting_predictions["M2_local_lzeros_cross"][index]
            ),
            split="discovery" if index < split_index else "validation",
        )
        for index, x in enumerate(grid)
    )

    return C05Experiment(
        min_x=min_x,
        max_x=max_x,
        log_samples_requested=log_samples,
        discovery_fraction=discovery_fraction,
        chi5_zero_source=CHI5_ZERO_SOURCE,
        chi5_zero_table_max=CHI5_ZERO_ORDINATES[-1],
        chi5_zero_heights=tuple(float(height) for height in chi5_zero_heights),
        zeta_zero_height=float(zeta_zero_height),
        frozen_channels=("C00", "C03", "C03-B", "C35", "C15"),
        explicit_formula_complete=False,
        samples=samples,
        convolution_checks=checks,
        metrics=tuple(metrics),
        coefficient_audits=tuple(audits),
    )


def _artifact_label(max_x: int) -> str:
    exponent = round(math.log10(max_x)) if max_x > 0 else 0
    if max_x > 0 and 10**exponent == max_x:
        return f"X1e{exponent}"
    return f"X{max_x}"


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def protected_c05_baseline_paths(project_root: Path) -> tuple[Path, ...]:
    artifacts = Path(project_root) / "artifacts"
    if not artifacts.is_dir():
        return ()
    protected: list[Path] = []
    for path in artifacts.rglob("*"):
        if not path.is_file() or "c05_controlled" in path.parts:
            continue
        name = path.name.lower()
        if (
            name.startswith("c03_")
            or name.startswith("c03b_")
            or name.startswith("goldbach_005a_")
            or "c35" in name
            or "c15" in name
        ):
            protected.append(path)
    return tuple(sorted(protected, key=lambda item: str(item).lower()))


def write_c05_artifacts(
    output_dir: Path,
    experiment: C05Experiment,
    protected_hashes_before: dict[str, str],
) -> dict[str, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    label = _artifact_label(experiment.max_x)
    paths = {
        "series_csv": output_dir / f"c05_series_{label}.csv",
        "metrics_csv": output_dir / f"c05_metrics_{label}.csv",
        "checks_csv": output_dir / f"c05_convolution_checks_{label}.csv",
        "audits_csv": output_dir / f"c05_coefficient_audits_{label}.csv",
        "immutability_csv": output_dir / f"c05_immutability_{label}.csv",
        "summary_json": output_dir / f"c05_summary_{label}.json",
    }

    for key, rows in (
        ("series_csv", experiment.samples),
        ("metrics_csv", experiment.metrics),
        ("checks_csv", experiment.convolution_checks),
        ("audits_csv", experiment.coefficient_audits),
    ):
        dictionaries = [asdict(row) for row in rows]
        with paths[key].open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(dictionaries[0].keys()))
            writer.writeheader()
            writer.writerows(dictionaries)

    immutable = True
    with paths["immutability_csv"].open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["path", "sha256_before", "sha256_after", "unchanged"],
        )
        writer.writeheader()
        for path_text, before in sorted(protected_hashes_before.items()):
            protected = Path(path_text)
            after = _sha256(protected) if protected.is_file() else "__missing__"
            unchanged = before == after
            immutable = immutable and unchanged
            writer.writerow(
                {
                    "path": path_text,
                    "sha256_before": before,
                    "sha256_after": after,
                    "unchanged": unchanged,
                }
            )

    validation = [metric for metric in experiment.metrics if metric.split == "validation"]
    calibration_height = max(experiment.chi5_zero_heights)
    calibration_metrics = {
        metric.model: metric
        for metric in validation
        if metric.chi5_zero_height == calibration_height
    }
    first_audit = next(
        audit
        for audit in experiment.coefficient_audits
        if audit.chi5_zero_height == calibration_height and audit.zero_index == 1
    )
    m1_improves = calibration_metrics["M1_local_lzeros"].rmse < calibration_metrics["M0_local"].rmse
    m2_improves = calibration_metrics["M2_local_lzeros_cross"].rmse < calibration_metrics["M1_local_lzeros"].rmse
    first_zero_recovered = (
        0.9 <= first_audit.amplitude_ratio <= 1.1
        and abs(first_audit.phase_error) <= 0.1
    )
    numerical_calibration_passed = (
        m1_improves and m2_improves and first_zero_recovered and immutable
    )

    summary = {
        "experiment_id": "G5B-005E",
        "channel": "C05",
        "evidence_level": "Resultado numerico provisional en cuarentena",
        "formal_proof": False,
        "novelty_claim": False,
        "explicit_formula_complete": experiment.explicit_formula_complete,
        "expansion_status": "controlled_truncation",
        "local_background": "X/6 * (H3 - b0 - log X)",
        "b0": CHI5_B0,
        "double_terms": "zeta-L5 crosses only",
        "numerical_calibration_passed": numerical_calibration_passed,
        "calibration_passed": False,
        "calibration_status": C05_IMPLEMENTATION_STATUS,
        "implementation_status": C05_IMPLEMENTATION_STATUS,
        "official_status": C05_OFFICIAL_STATUS,
        "retrospective_approval": C05_RETROSPECTIVE_APPROVAL,
        "final_review": C05_FINAL_REVIEW_STATUS,
        "eligible_for_downstream_use": False,
        "temporal_contamination": "protocol_finalized_after_observing_C05_results",
        "calibration_criteria": {
            "chi5_zero_height": calibration_height,
            "validation_rmse_m0": calibration_metrics["M0_local"].rmse,
            "validation_rmse_m1": calibration_metrics["M1_local_lzeros"].rmse,
            "validation_rmse_m2": calibration_metrics["M2_local_lzeros_cross"].rmse,
            "requires_m1_below_m0": m1_improves,
            "requires_m2_below_m1": m2_improves,
            "first_zero_amplitude_ratio": first_audit.amplitude_ratio,
            "first_zero_phase_error": first_audit.phase_error,
            "first_zero_amplitude_interval": [0.9, 1.1],
            "first_zero_maximum_absolute_phase_error": 0.1,
            "first_zero_recovered": first_zero_recovered,
        },
        "window": {"min": experiment.min_x, "max": experiment.max_x},
        "log_samples_requested": experiment.log_samples_requested,
        "log_samples_realized": len(experiment.samples),
        "discovery_fraction": experiment.discovery_fraction,
        "chi5_zero_source": experiment.chi5_zero_source,
        "chi5_zero_table_max": experiment.chi5_zero_table_max,
        "chi5_zero_heights": list(experiment.chi5_zero_heights),
        "zeta_zero_height": experiment.zeta_zero_height,
        "first_chi5_zero": CHI5_ZERO_ORDINATES[0],
        "rejected_foreign_frequencies": [6.0206, 9.810574],
        "frozen_channels": list(experiment.frozen_channels),
        "immutability_passed": immutable,
        "protected_file_count": len(protected_hashes_before),
        "convolution_max_absolute_error": max(
            check.absolute_error for check in experiment.convolution_checks
        ),
        "metrics": [asdict(metric) for metric in experiment.metrics],
        "interpretation": (
            "Implementacion provisional conservada como evidencia exploratoria en cuarentena. "
            "No pertenece al linaje oficial, no puede justificar C35 o C15 y no constituye "
            "evidencia de una frecuencia nueva ni una formula explicita completa."
        ),
    }
    paths["summary_json"].write_text(
        json.dumps(summary, indent=2, ensure_ascii=False, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    return paths
