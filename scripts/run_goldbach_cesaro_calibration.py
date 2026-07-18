from __future__ import annotations

import argparse
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from athena_azr.cesaro_calibration import (  # noqa: E402
    build_cesaro_calibration,
    write_calibration_artifacts,
)


def parse_zero_heights(value: str) -> tuple[float, ...]:
    heights = tuple(float(item.strip()) for item in value.split(",") if item.strip())
    if not heights:
        raise argparse.ArgumentTypeError("zero-heights must contain at least one value")
    return heights


def main() -> None:
    parser = argparse.ArgumentParser(description="Ejecuta la calibracion Cesaro C2 de Goldbach.")
    parser.add_argument("--max-x", type=int, default=1_000_000)
    parser.add_argument("--min-x", type=int, default=1_000)
    parser.add_argument("--log-samples", type=int, default=800)
    parser.add_argument(
        "--zero-heights",
        type=parse_zero_heights,
        default=(50.0, 100.0, 143.0),
        help="Alturas separadas por coma; la tabla local llega hasta 143.1118.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=ROOT / "artifacts" / "goldbach_cesaro",
    )
    args = parser.parse_args()

    experiment = build_cesaro_calibration(
        max_x=args.max_x,
        min_x=args.min_x,
        log_samples=args.log_samples,
        zero_heights=args.zero_heights,
    )
    paths = write_calibration_artifacts(args.output_dir, experiment)

    print("Experimento 005A: calibracion Cesaro C2")
    print(f"Ventana: {experiment.min_x}..{experiment.max_x}")
    print(f"Muestras logaritmicas: {len(experiment.samples)}")
    print(
        "Error maximo de convolucion: "
        f"{max(check.absolute_error for check in experiment.convolution_checks):.6e}"
    )
    for metric in experiment.metrics:
        if metric.split == "validation":
            print(
                f"T={metric.zero_height:g} zeros={metric.zero_count:2d} "
                f"{metric.model:16s} rmse={metric.rmse:.6e}"
            )
    for name, path in paths.items():
        print(f"{name}: {path}")


if __name__ == "__main__":
    main()
