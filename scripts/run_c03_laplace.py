from __future__ import annotations

import argparse
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from athena_azr.c03_laplace_chi3 import (  # noqa: E402
    build_c03_experiment,
    write_c03_artifacts,
)


def _heights(value: str) -> tuple[float, ...]:
    result = tuple(float(item.strip()) for item in value.split(",") if item.strip())
    if not result:
        raise argparse.ArgumentTypeError("at least one height is required")
    return result


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Experimento 005B: calibracion mixta C03 por series de Laplace."
    )
    parser.add_argument("--max-x", type=int, default=1_000_000)
    parser.add_argument("--min-x", type=int, default=1_000)
    parser.add_argument("--log-samples", type=int, default=800)
    parser.add_argument(
        "--chi3-zero-heights",
        type=_heights,
        default=(50.0, 100.0, 143.0),
    )
    parser.add_argument("--zeta-zero-height", type=float, default=143.0)
    parser.add_argument("--discovery-fraction", type=float, default=0.65)
    parser.add_argument("--output-dir", type=Path, default=Path("artifacts"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    experiment = build_c03_experiment(
        max_x=args.max_x,
        min_x=args.min_x,
        log_samples=args.log_samples,
        chi3_zero_heights=args.chi3_zero_heights,
        zeta_zero_height=args.zeta_zero_height,
        discovery_fraction=args.discovery_fraction,
    )
    paths = write_c03_artifacts(args.output_dir, experiment)

    print("Experimento 005B: canal mixto C03")
    print(f"Ventana: {experiment.min_x}..{experiment.max_x}")
    print(f"Muestras logaritmicas: {len(experiment.samples)}")
    print(
        "Error maximo de convolucion: "
        f"{max(check.absolute_error for check in experiment.convolution_checks):.6e}"
    )
    for metric in experiment.metrics:
        if metric.split == "validation":
            print(
                f"Tchi={metric.chi3_zero_height:g} "
                f"Lzeros={metric.chi3_zero_count} "
                f"Zzeros={metric.zeta_zero_count} "
                f"{metric.model:<25} rmse={metric.rmse:.6e}"
            )
    for name, path in paths.items():
        print(f"{name}: {path}")


if __name__ == "__main__":
    main()
