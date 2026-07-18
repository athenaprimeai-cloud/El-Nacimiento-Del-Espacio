from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from athena_azr.goldbach_transform import (  # noqa: E402
    build_extraction_experiment,
    write_extraction_peaks_csv,
    write_extraction_summary_json,
    write_extraction_values_csv,
)


DEFAULT_PRIMES = (3, 5, 7, 11, 13)
DEFAULT_SEEDS = [1436, 2718, 3141, 5772, 16180]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Ejecuta el Experimento 004 de extracción modular.")
    parser.add_argument("--max-even", type=int, default=10_000, help="Último número par de la ventana.")
    parser.add_argument("--min-even", type=int, default=4, help="Primer número par de la ventana.")
    parser.add_argument("--top", type=int, default=12, help="Cantidad de picos por etapa.")
    parser.add_argument("--prime", action="append", type=int, help="Primo modular a proyectar. Puede repetirse.")
    parser.add_argument("--seed", action="append", type=int, help="Semilla de control. Puede repetirse.")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=ROOT / "artifacts" / "goldbach_extraction",
        help="Directorio para resultados.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    modular_primes = tuple(args.prime) if args.prime else DEFAULT_PRIMES
    seeds = args.seed if args.seed else DEFAULT_SEEDS

    experiment = build_extraction_experiment(
        args.max_even,
        min_even=args.min_even,
        modular_primes=modular_primes,
        control_seeds=seeds,
        peak_limit=args.top,
    )

    args.output_dir.mkdir(parents=True, exist_ok=True)
    suffix = f"{args.min_even}_{experiment.max_even}_{'-'.join(str(prime) for prime in modular_primes)}"
    values_csv = args.output_dir / f"goldbach_004_values_{suffix}.csv"
    peaks_csv = args.output_dir / f"goldbach_004_peaks_{suffix}.csv"
    summary_json = args.output_dir / f"goldbach_004_summary_{suffix}.json"

    write_extraction_values_csv(values_csv, experiment)
    write_extraction_peaks_csv(peaks_csv, experiment)
    write_extraction_summary_json(summary_json, experiment)

    print("Experimento 004: extracción de deriva y ruedas modulares")
    print(f"Ventana: {args.min_even}..{experiment.max_even}")
    print(f"Primos proyectados: {','.join(str(prime) for prime in experiment.modular_primes)}")
    print(f"Valores: {values_csv}")
    print(f"Picos: {peaks_csv}")
    print(f"Resumen: {summary_json}")
    for stage in experiment.stages:
        print(f"Etapa: {stage.name} energy={stage.total_spectral_energy:.10f}")
        for peak in stage.peaks[:5]:
            print(
                "  "
                f"f={peak.frequency:.8f} "
                f"nearest={peak.nearest_rational} "
                f"frac={peak.fraction_of_total_energy:.8f} "
                f"p_global={peak.global_empirical_p:.6f}"
            )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
