"""
T-03 wave-1 analysis — intrinsic only. No Athena / T-01 comparison.
Classes: NECESSARY | EMPIRICAL | SEED_DEPENDENT | UNKNOWN
"""

from __future__ import annotations

import argparse
import json
import statistics
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List, Sequence, Tuple

ROOT = Path(__file__).resolve().parent.parent


def gaps(occupied: Sequence[int]) -> List[int]:
    if len(occupied) < 2:
        return []
    s = sorted(occupied)
    return [s[i + 1] - s[i] for i in range(len(s) - 1)]


def load_runs(path: Path) -> List[Dict[str, Any]]:
    out = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                out.append(json.loads(line))
    return out


def gkey(p: Dict[str, Any]) -> Tuple:
    return (p["N"], p["W"], p["T"])


def analyze(runs: List[Dict[str, Any]]) -> Dict[str, Any]:
    by: Dict[Tuple, List[Dict[str, Any]]] = defaultdict(list)
    for r in runs:
        by[gkey(r["params"])].append(r)

    cells = []
    for key, recs in sorted(by.items()):
        dens = [r["density"] for r in recs]
        extinct = [1.0 if r["trajectory_summary"]["extinct"] else 0.0 for r in recs]
        full = [1.0 if r["trajectory_summary"]["full"] else 0.0 for r in recs]
        # seed agreement on final density
        cells.append(
            {
                "N": key[0],
                "W": key[1],
                "T": key[2],
                "n_seeds": len(recs),
                "density_mean": statistics.mean(dens),
                "density_std": statistics.pstdev(dens) if len(dens) > 1 else 0.0,
                "extinction_rate": statistics.mean(extinct),
                "full_rate": statistics.mean(full),
            }
        )

    properties = []

    # NECESSARY from rule algebra (Wolfram elementary)
    properties.append(
        {
            "id": "N1",
            "name": "rule0_global_zero",
            "statement": "For W=0, f≡0, so for all t>=1 the configuration is identically zero (null boundary irrelevant).",
            "class": "NECESSARY",
            "justification": "Every neighborhood maps to 0; synchronous step forces x^{t+1}=0 regardless of x^t (including after first step from any init).",
        }
    )
    properties.append(
        {
            "id": "N2",
            "name": "deterministic_trajectory",
            "statement": "Given (N,W,p_init,T,seed), the trajectory is unique: same seed => identical occupied list.",
            "class": "NECESSARY",
            "justification": "Init is a function of seed; transition f is deterministic and synchronous.",
        }
    )
    properties.append(
        {
            "id": "N3",
            "name": "additive_mod2_linearity",
            "statement": (
                "For additive rules (W in a known additive set, e.g. 90, 150), "
                "evolution is linear over GF(2) under XOR of initial conditions "
                "(with fixed null boundary the linear structure holds on the finite vector space)."
            ),
            "class": "NECESSARY",
            "justification": (
                "Elementary CA 90 and 150 are linear: f is XOR of selected neighbors. "
                "Superposition of configs evolves as XOR of evolutions."
            ),
        }
    )

    # EMPIRICAL from wave
    w0 = [c for c in cells if c["W"] == 0]
    if w0:
        # after T>=1 should be extinct — check T=10,50,100
        rate = statistics.mean(c["extinction_rate"] for c in w0)
        properties.append(
            {
                "id": "E1",
                "name": "rule0_extinction_observed",
                "statement": f"Wave-1: W=0 mean extinction_rate={rate:.3f} across cells (supports N1 numerically).",
                "class": "EMPIRICAL",
                "justification": "Numerical check of N1 on the grid; not a new theorem.",
            }
        )

    # density by W aggregated
    by_w: Dict[int, List[float]] = defaultdict(list)
    for c in cells:
        by_w[c["W"]].append(c["density_mean"])
    w_means = {w: statistics.mean(v) for w, v in by_w.items()}
    properties.append(
        {
            "id": "E2",
            "name": "density_depends_on_W",
            "statement": (
                "Mean final density (over N,T,seeds) varies strongly with W: "
                + ", ".join(f"W{w}={w_means[w]:.3f}" for w in sorted(w_means))
            ),
            "class": "EMPIRICAL",
            "justification": "Observed aggregation on wave-1; not derived as closed form for all W.",
        }
    )

    # SEED_DEPENDENT: high density_std
    volatile = [c for c in cells if c["density_std"] > 0.05]
    properties.append(
        {
            "id": "S1",
            "name": "seed_sensitivity",
            "statement": (
                f"{len(volatile)}/{len(cells)} cells have density_std>0.05 across seeds "
                "(init Bernoulli sensitivity under deterministic flow)."
            ),
            "class": "SEED_DEPENDENT",
            "justification": "Spread across seeds for fixed (N,W,T).",
        }
    )

    properties.append(
        {
            "id": "U1",
            "name": "class_iv_long_horizon",
            "statement": "Long-horizon classification (Wolfram class) for complex rules (e.g. 110) on finite N with null boundary.",
            "class": "UNKNOWN",
            "justification": "Finite T in {10,50,100} does not settle asymptotic class.",
        }
    )

    return {
        "family": "T-03",
        "spec_version": "1.0",
        "n_runs": len(runs),
        "n_param_cells": len(cells),
        "cells_summary": cells,
        "properties": properties,
        "classification_legend": {
            "NECESSARY": "From the CA rule / determinism (justified).",
            "EMPIRICAL": "Wave-1 aggregate observation.",
            "SEED_DEPENDENT": "Varies with initial seed.",
            "UNKNOWN": "Open under this wave.",
        },
        "note": "No Athena bridge. No T-01 comparison. No P* sealed.",
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--raw",
        type=Path,
        default=ROOT / "results" / "T03_REFERENCE_WAVE1" / "raw_runs.jsonl",
    )
    ap.add_argument(
        "--out",
        type=Path,
        default=ROOT / "results" / "T03_REFERENCE_WAVE1" / "analysis_wave1.json",
    )
    args = ap.parse_args()
    runs = load_runs(args.raw)
    report = analyze(runs)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "n_runs": report["n_runs"],
                "n_param_cells": report["n_param_cells"],
                "properties": [
                    {"id": p["id"], "class": p["class"], "name": p["name"]}
                    for p in report["properties"]
                ],
                "wrote": str(args.out),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
