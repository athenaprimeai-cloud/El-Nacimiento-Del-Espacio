from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from athena_azr.c05_laplace_chi5 import (  # noqa: E402
    C05_IMPLEMENTATION_STATUS,
    build_c05_experiment,
    protected_c05_baseline_paths,
    validate_c05_output_dir,
    validate_c05_execution_authorization,
    validate_c05_rerun_protocol,
    write_c05_artifacts,
)


def _heights(value: str) -> tuple[float, ...]:
    result = tuple(float(item.strip()) for item in value.split(",") if item.strip())
    if not result:
        raise argparse.ArgumentTypeError("at least one height is required")
    return result


def _hash_files(paths: tuple[Path, ...]) -> dict[str, str]:
    result: dict[str, str] = {}
    for path in paths:
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        result[str(path)] = digest
    return result


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Experimento 005E: calibracion mixta C05 por series de Laplace."
    )
    parser.add_argument("--max-x", type=int, default=1_000_000)
    parser.add_argument("--min-x", type=int, default=1_000)
    parser.add_argument("--log-samples", type=int, default=800)
    parser.add_argument(
        "--chi5-zero-heights",
        type=_heights,
        default=(50.0, 100.0, 143.0),
    )
    parser.add_argument("--zeta-zero-height", type=float, default=143.0)
    parser.add_argument("--discovery-fraction", type=float, default=0.65)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("artifacts/goldbach_cesaro/c05_rerun_clean"),
    )
    parser.add_argument(
        "--sealed-protocol",
        type=Path,
        help="JSON aprobado y sellado antes del rerun limpio G5B-005E-R.",
    )
    parser.add_argument(
        "--execution-authorization",
        type=Path,
        help="Autorizacion posterior que referencia el hash del protocolo sellado.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    try:
        protocol = validate_c05_rerun_protocol(args.sealed_protocol)
        validate_c05_execution_authorization(
            args.execution_authorization,
            str(protocol["protocol_sha256"]),
        )
        output_dir = validate_c05_output_dir(args.output_dir, PROJECT_ROOT)
    except RuntimeError as error:
        raise SystemExit(str(error)) from error
    protected = protected_c05_baseline_paths(PROJECT_ROOT)
    hashes_before = _hash_files(protected)
    experiment = build_c05_experiment(
        max_x=args.max_x,
        min_x=args.min_x,
        log_samples=args.log_samples,
        chi5_zero_heights=args.chi5_zero_heights,
        zeta_zero_height=args.zeta_zero_height,
        discovery_fraction=args.discovery_fraction,
    )
    paths = write_c05_artifacts(output_dir, experiment, hashes_before)
    summary = json.loads(paths["summary_json"].read_text(encoding="utf-8"))

    print("Experimento 005E: canal mixto C05")
    print(f"Ventana: {experiment.min_x}..{experiment.max_x}")
    print(f"Muestras logaritmicas: {len(experiment.samples)}")
    print(f"Estado de implementacion: {C05_IMPLEMENTATION_STATUS}")
    print(f"Criterios numericos superados: {summary['numerical_calibration_passed']}")
    print(f"Aceptacion oficial: {summary['calibration_passed']}")
    print(f"Inmutabilidad superada: {summary['immutability_passed']}")
    for metric in experiment.metrics:
        if metric.split == "validation":
            print(
                f"Tchi={metric.chi5_zero_height:g} "
                f"Lzeros={metric.chi5_zero_count} "
                f"Zzeros={metric.zeta_zero_count} "
                f"{metric.model:<25} rmse={metric.rmse:.6e}"
            )
    for name, path in paths.items():
        print(f"{name}: {path}")


if __name__ == "__main__":
    main()
