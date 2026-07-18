from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from athena_azr.c03b_stress import (  # noqa: E402
    build_c03b_audit,
    hash_files,
    protected_baseline_paths,
    write_c03b_artifacts,
)


def _integer_tuple(value: str) -> tuple[int, ...]:
    result = tuple(int(item.strip()) for item in value.split(",") if item.strip())
    if not result:
        raise argparse.ArgumentTypeError("at least one integer is required")
    return result


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Experimento 005C: falsificacion espectral C03-B."
    )
    parser.add_argument("--max-x", type=int, default=1_000_000)
    parser.add_argument("--min-x", type=int, default=1_000)
    parser.add_argument("--log-samples", type=int, default=800)
    parser.add_argument(
        "--windows",
        type=_integer_tuple,
        default=(10_000, 30_000, 100_000, 300_000, 1_000_000),
    )
    parser.add_argument("--ablation-counts", type=_integer_tuple, default=(0, 1, 2, 4, 8))
    parser.add_argument("--chi3-zero-height", type=float, default=143.0)
    parser.add_argument("--zeta-zero-height", type=float, default=143.0)
    parser.add_argument("--random-frequency-controls", type=int, default=24)
    parser.add_argument("--max-t-controls", type=int, default=999)
    parser.add_argument("--max-t-frequency-min", type=float, default=0.5)
    parser.add_argument("--max-t-frequency-max", type=float, default=143.0)
    parser.add_argument("--max-t-frequency-step", type=float, default=0.05)
    parser.add_argument("--seed", type=int, default=20260610)
    parser.add_argument("--discovery-fraction", type=float, default=0.65)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("artifacts/goldbach_cesaro/c03b_stress_tests"),
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    protected = protected_baseline_paths(PROJECT_ROOT)
    hashes_before = hash_files(protected)
    audit = build_c03b_audit(
        max_x=args.max_x,
        min_x=args.min_x,
        log_samples=args.log_samples,
        window_maxima=args.windows,
        ablation_counts=args.ablation_counts,
        full_chi3_zero_height=args.chi3_zero_height,
        zeta_zero_height=args.zeta_zero_height,
        random_frequency_controls=args.random_frequency_controls,
        max_t_controls=args.max_t_controls,
        max_t_frequency_min=args.max_t_frequency_min,
        max_t_frequency_max=args.max_t_frequency_max,
        max_t_frequency_step=args.max_t_frequency_step,
        seed=args.seed,
        discovery_fraction=args.discovery_fraction,
    )
    paths = write_c03b_artifacts(args.output_dir, audit, hashes_before)
    summary = json.loads(paths["summary_json"].read_text(encoding="utf-8"))

    print("Experimento 005C: C03-B falsificacion espectral")
    print(f"Ventanas: {', '.join(str(value) for value in audit.window_maxima)}")
    print(f"Controles max-T: {len(audit.max_t.control_maxima)}")
    print(f"p_FWER residual: {audit.max_t.p_fwer:.6g}")
    print(f"Robustez superada: {summary['robustness_passed']}")
    print(f"Inmutabilidad superada: {summary['immutability_passed']}")
    for name, path in paths.items():
        print(f"{name}: {path}")


if __name__ == "__main__":
    main()
