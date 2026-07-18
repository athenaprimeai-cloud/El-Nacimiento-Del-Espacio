"""
T-01 wave-1 analysis — intrinsic properties only.

Does not read Athena domain results / SURVIVORS.
Classifies each reported property as:
  NECESSARY | EMPIRICAL | SEED_DEPENDENT | UNKNOWN
"""

from __future__ import annotations

import argparse
import json
import statistics
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List, Sequence, Tuple

DISCOVERY_DIR = Path(__file__).resolve().parent
ROOT = DISCOVERY_DIR.parent


def gaps(occupied: Sequence[int]) -> List[int]:
    if len(occupied) < 2:
        return []
    s = sorted(occupied)
    return [s[i + 1] - s[i] for i in range(len(s) - 1)]


def load_runs(raw_path: Path) -> List[Dict[str, Any]]:
    runs = []
    with raw_path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                runs.append(json.loads(line))
    return runs


def group_key(params: Dict[str, Any]) -> Tuple:
    return (
        params["N"],
        params["r"],
        params["theta"],
        params["p_birth"],
        params["T"],
    )


def analyze(runs: List[Dict[str, Any]]) -> Dict[str, Any]:
    by_cell: Dict[Tuple, List[Dict[str, Any]]] = defaultdict(list)
    for rec in runs:
        by_cell[group_key(rec["params"])].append(rec)

    cells = []
    for key, recs in sorted(by_cell.items()):
        dens = [r["density"] for r in recs]
        extinct = [1.0 if r["trajectory_summary"]["extinct"] else 0.0 for r in recs]
        mean_gaps = []
        for r in recs:
            g = gaps(r["occupied"])
            mean_gaps.append(statistics.mean(g) if g else 0.0)
        dens_var = statistics.pvariance(dens) if len(dens) > 1 else 0.0
        cells.append(
            {
                "N": key[0],
                "r": key[1],
                "theta": key[2],
                "p_birth": key[3],
                "T": key[4],
                "n_seeds": len(recs),
                "density_mean": statistics.mean(dens),
                "density_std": statistics.pstdev(dens) if len(dens) > 1 else 0.0,
                "density_var": dens_var,
                "extinction_rate": statistics.mean(extinct),
                "mean_gap_mean": statistics.mean(mean_gaps),
                "mean_gap_std": statistics.pstdev(mean_gaps) if len(mean_gaps) > 1 else 0.0,
            }
        )

    # Global empirical patterns (not necessary unless justified)
    # Pattern: higher theta relative to r tends to higher density (weaker exclusion)
    # Pattern: extinction when theta is low and r high may increase

    properties = []

    # --- NECESSARY (rule-derived, not just 20/20 seeds) ---
    properties.append(
        {
            "id": "N1",
            "name": "synchronous_exclusion_bound",
            "statement": (
                "If at time t every site has neighbor-sum >= theta, then at t+1 the configuration "
                "is identically zero (global extinction in one step)."
            ),
            "class": "NECESSARY",
            "justification": (
                "By transition rule: ns >= theta forces x_i^{t+1}=0 for all i, independent of births."
            ),
        }
    )
    properties.append(
        {
            "id": "N2",
            "name": "isolation_preserves_or_birth",
            "statement": (
                "If a site has neighbor-sum < theta and is occupied, it remains occupied "
                "(births irrelevant for that site)."
            ),
            "class": "NECESSARY",
            "justification": (
                "Rule branch: ns < theta and x_i=1 => x_i^{t+1}=1 regardless of U_{t,i}."
            ),
        }
    )
    properties.append(
        {
            "id": "N3",
            "name": "empty_isolated_birth_only",
            "statement": (
                "If a site is empty and neighbor-sum < theta, occupation at t+1 occurs iff U_{t,i} < p_birth."
            ),
            "class": "NECESSARY",
            "justification": "Direct from the second branch of the transition rule.",
        }
    )

    # --- EMPIRICAL from wave (appear across cells; not proven) ---
    # Extinction rate vs (r, theta)
    high_excl = [c for c in cells if c["theta"] == 1 and c["r"] >= 2]
    if high_excl:
        avg_ext = statistics.mean(c["extinction_rate"] for c in high_excl)
        properties.append(
            {
                "id": "E1",
                "name": "high_exclusion_extinction_tendency",
                "statement": (
                    f"Across wave-1 cells with theta=1 and r>=2, mean extinction_rate={avg_ext:.3f} "
                    "(over seeds aggregated per cell)."
                ),
                "class": "EMPIRICAL",
                "justification": "Observed in wave-1 grid; not derived as theorem from the rule alone.",
            }
        )

    # Density increases with T often? check correlation-like
    # Compare T=10 vs T=50 same other params
    pairs = []
    index = {(c["N"], c["r"], c["theta"], c["p_birth"], c["T"]): c for c in cells}
    for c in cells:
        if c["T"] != 10:
            continue
        key50 = (c["N"], c["r"], c["theta"], c["p_birth"], 50)
        if key50 in index:
            pairs.append((c["density_mean"], index[key50]["density_mean"]))
    if pairs:
        up = sum(1 for a, b in pairs if b > a + 1e-9)
        down = sum(1 for a, b in pairs if b < a - 1e-9)
        properties.append(
            {
                "id": "E2",
                "name": "density_T10_vs_T50",
                "statement": (
                    f"Among matched param cells, density_mean T=50 > T=10 in {up}/{len(pairs)} cells; "
                    f"lower in {down}/{len(pairs)}."
                ),
                "class": "EMPIRICAL",
                "justification": "Wave-1 comparison only; not a necessary consequence of the rule.",
            }
        )

    # --- SEED_DEPENDENT ---
    # cells with high density_std relative to mean
    volatile = [c for c in cells if c["density_std"] > 0.05]
    properties.append(
        {
            "id": "S1",
            "name": "seed_volatility",
            "statement": (
                f"{len(volatile)}/{len(cells)} param-cells have density_std > 0.05 across 20 seeds "
                "(non-negligible seed dependence of density)."
            ),
            "class": "SEED_DEPENDENT",
            "justification": "Empirical spread across seeds; magnitude depends on (N,r,theta,p_birth,T).",
        }
    )

    # --- UNKNOWN ---
    properties.append(
        {
            "id": "U1",
            "name": "long_run_invariant_measure",
            "statement": "Whether a unique stationary distribution exists for all params in the grid.",
            "class": "UNKNOWN",
            "justification": "Not addressed by finite-T wave-1.",
        }
    )

    return {
        "family": "T-01",
        "spec_version": "1.0",
        "n_runs": len(runs),
        "n_param_cells": len(cells),
        "cells_summary": cells,
        "properties": properties,
        "classification_legend": {
            "NECESSARY": "Derived from the transition rule (proof sketch in justification).",
            "EMPIRICAL": "Seen in wave-1 aggregates; not proven necessary.",
            "SEED_DEPENDENT": "Varies materially with seed.",
            "UNKNOWN": "Open; not settled by this wave.",
        },
        "note": (
            "No Athena domain comparison. No P* sealed. "
            "Necessary consequences listed are rule-level; empirical are observational."
        ),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--raw",
        type=Path,
        default=ROOT / "results" / "T01_REFERENCE_WAVE1" / "raw_runs.jsonl",
    )
    ap.add_argument(
        "--out",
        type=Path,
        default=ROOT / "results" / "T01_REFERENCE_WAVE1" / "analysis_wave1.json",
    )
    args = ap.parse_args()
    runs = load_runs(args.raw)
    report = analyze(runs)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    # compact print
    print(json.dumps({
        "n_runs": report["n_runs"],
        "n_param_cells": report["n_param_cells"],
        "properties": [
            {"id": p["id"], "class": p["class"], "name": p["name"]}
            for p in report["properties"]
        ],
        "wrote": str(args.out),
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
