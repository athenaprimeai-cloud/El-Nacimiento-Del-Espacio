from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from athena_azr.goldbach_transform import (  # noqa: E402
    build_persistence_experiment,
    write_persistence_candidates_csv,
    write_persistence_summary_json,
)


DEFAULT_WINDOWS = [
    (4, 2500),
    (4, 5000),
    (4, 7500),
    (4, 10000),
    (1000, 4000),
    (3000, 6000),
    (5000, 8000),
    (7000, 10000),
]

DEFAULT_SEEDS = [1436, 2718, 3141, 5772, 16180]


def parse_window(value: str) -> tuple[int, int]:
    try:
        start_text, end_text = value.split(":", 1)
        return int(start_text), int(end_text)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("Use window format START:END, for example 4:10000.") from exc


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Ejecuta el Experimento 003 de persistencia multiescala.")
    parser.add_argument(
        "--window",
        action="append",
        type=parse_window,
        help="Ventana START:END. Puede repetirse. Si se omite, usa las ventanas del Libro Uno.",
    )
    parser.add_argument(
        "--seed",
        action="append",
        type=int,
        help="Semilla de control. Puede repetirse. Si se omite, usa 1436,2718,3141,5772,16180.",
    )
    parser.add_argument("--channel", default="desingularized_ratio", help="Canal real que se evalúa.")
    parser.add_argument("--top", type=int, default=12, help="Cantidad de picos por ventana.")
    parser.add_argument("--trend-radius", type=int, default=25, help="Radio de media móvil.")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=ROOT / "artifacts" / "goldbach_persistence",
        help="Directorio para resultados.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    windows = args.window if args.window else DEFAULT_WINDOWS
    seeds = args.seed if args.seed else DEFAULT_SEEDS

    experiment = build_persistence_experiment(
        windows=windows,
        control_seeds=seeds,
        channel_name=args.channel,
        peak_limit=args.top,
        trend_radius=args.trend_radius,
    )

    args.output_dir.mkdir(parents=True, exist_ok=True)
    suffix = f"{experiment.channel_name}_{len(experiment.windows)}w_{len(experiment.control_seeds)}s"
    candidates_csv = args.output_dir / f"goldbach_003_candidates_{suffix}.csv"
    summary_json = args.output_dir / f"goldbach_003_summary_{suffix}.json"

    write_persistence_candidates_csv(candidates_csv, experiment)
    write_persistence_summary_json(summary_json, experiment)

    print("Experimento 003: Persistencia multiescala")
    print(f"Canal: {experiment.channel_name}")
    print(f"Ventanas: {len(experiment.windows)}")
    print(f"Semillas de control: {','.join(str(seed) for seed in experiment.control_seeds)}")
    print(f"Candidatos: {len(experiment.candidates)}")
    print(f"CSV candidatos: {candidates_csv}")
    print(f"Resumen JSON: {summary_json}")
    print("Primeros candidatos:")
    for candidate in experiment.candidates[:10]:
        print(
            "  "
            f"{candidate.nearest_rational} "
            f"coverage={candidate.coverage:.3f} "
            f"mean_f={candidate.mean_frequency:.8f} "
            f"power_frac={candidate.mean_power_fraction:.6f} "
            f"control_pct={candidate.control_percentile:.3f} "
            f"class={candidate.classification}"
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
