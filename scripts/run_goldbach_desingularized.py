from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from athena_azr.goldbach_transform import (  # noqa: E402
    build_multispectrum_experiment,
    dft_power_spectrum,
    hann_window,
    render_spectrum_svg,
    write_channel_values_csv,
    write_multispectrum_peaks_csv,
    write_multispectrum_summary_json,
    write_spectrum_csv,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Ejecuta el Experimento 002 de Goldbach desingularizado.")
    parser.add_argument("--max-even", type=int, default=10_000, help="Último número par de la ventana.")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=ROOT / "artifacts" / "goldbach_desingularized",
        help="Directorio para CSV, JSON y SVG.",
    )
    parser.add_argument("--trend-radius", type=int, default=25, help="Radio de media móvil para residuo.")
    parser.add_argument("--top", type=int, default=12, help="Cantidad de picos dominantes por canal.")
    parser.add_argument("--seed", type=int, default=1436, help="Semilla del control aleatorio reproducible.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    experiment = build_multispectrum_experiment(
        args.max_even,
        random_seed=args.seed,
        peak_limit=args.top,
        trend_radius=args.trend_radius,
    )

    suffix = f"4_{experiment.max_even}"
    args.output_dir.mkdir(parents=True, exist_ok=True)

    values_csv = args.output_dir / f"goldbach_002_channel_values_{suffix}.csv"
    peaks_csv = args.output_dir / f"goldbach_002_peaks_{suffix}.csv"
    summary_json = args.output_dir / f"goldbach_002_summary_{suffix}.json"

    write_channel_values_csv(values_csv, experiment)
    write_multispectrum_peaks_csv(peaks_csv, experiment)
    write_multispectrum_summary_json(summary_json, experiment)

    for channel in experiment.channels:
        windowed = hann_window(list(channel.values))
        spectrum = dft_power_spectrum(windowed, sample_spacing=2.0)
        spectrum_csv = args.output_dir / f"goldbach_002_{channel.name}_spectrum_{suffix}.csv"
        spectrum_svg = args.output_dir / f"goldbach_002_{channel.name}_spectrum_{suffix}.svg"
        write_spectrum_csv(spectrum_csv, spectrum)
        render_spectrum_svg(spectrum_svg, spectrum)

    print(f"Experimento 002: 4..{experiment.max_even}")
    print(f"Pares evaluados: {len(experiment.rows)}")
    print(f"Contraejemplos computacionales: {len(experiment.counterexamples)}")
    print(f"Valores por canal: {values_csv}")
    print(f"Picos enriquecidos: {peaks_csv}")
    print(f"Resumen JSON: {summary_json}")
    for channel in experiment.channels:
        print(f"Canal: {channel.name}")
        for peak in channel.peaks[:5]:
            print(
                "  "
                f"f={peak.frequency:.8f} "
                f"period={peak.period:.4f} "
                f"nearest={peak.nearest_rational} "
                f"mod={peak.candidate_modulus} "
                f"norm={peak.normalized_power:.6f}"
            )

    return 0 if not experiment.counterexamples else 2


if __name__ == "__main__":
    raise SystemExit(main())
