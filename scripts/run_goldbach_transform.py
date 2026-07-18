from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from athena_azr.goldbach_transform import (  # noqa: E402
    build_goldbach_experiment,
    dft_power_spectrum,
    dominant_frequencies,
    hann_window,
    render_spectrum_svg,
    residual_series,
    write_rows_csv,
    write_spectrum_csv,
    write_summary_json,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Ejecuta la Transformada de Goldbach CED+RAP.")
    parser.add_argument("--max-even", type=int, default=10_000, help="Último número par de la ventana.")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=ROOT / "artifacts" / "goldbach",
        help="Directorio para CSV, JSON y SVG.",
    )
    parser.add_argument("--trend-radius", type=int, default=25, help="Radio de media móvil para residuo.")
    parser.add_argument("--top", type=int, default=10, help="Cantidad de frecuencias dominantes a reportar.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    experiment = build_goldbach_experiment(args.max_even)
    counts = [float(row.partition_count) for row in experiment.rows]
    residual = residual_series(counts, radius=args.trend_radius)
    windowed = hann_window(residual)
    spectrum = dft_power_spectrum(windowed, sample_spacing=2.0)
    top = dominant_frequencies(windowed, sample_spacing=2.0, limit=args.top)

    suffix = f"4_{experiment.max_even}"
    args.output_dir.mkdir(parents=True, exist_ok=True)
    rows_csv = args.output_dir / f"goldbach_partitions_{suffix}.csv"
    spectrum_csv = args.output_dir / f"goldbach_fft_spectrum_{suffix}.csv"
    summary_json = args.output_dir / f"goldbach_summary_{suffix}.json"
    spectrum_svg = args.output_dir / f"goldbach_fft_spectrum_{suffix}.svg"

    write_rows_csv(rows_csv, experiment)
    write_spectrum_csv(spectrum_csv, spectrum)
    write_summary_json(summary_json, experiment, top)
    render_spectrum_svg(spectrum_svg, spectrum)

    print(f"Ventana: 4..{experiment.max_even}")
    print(f"Pares evaluados: {len(experiment.rows)}")
    print(f"Contraejemplos computacionales: {len(experiment.counterexamples)}")
    print(f"CSV particiones: {rows_csv}")
    print(f"CSV espectro: {spectrum_csv}")
    print(f"Resumen JSON: {summary_json}")
    print(f"SVG espectro: {spectrum_svg}")
    print("Frecuencias dominantes:")
    for item in top:
        print(f"  f={item.frequency:.8f} power={item.power:.6f}")

    return 0 if not experiment.counterexamples else 2


if __name__ == "__main__":
    raise SystemExit(main())
