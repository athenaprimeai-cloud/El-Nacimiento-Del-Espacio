"""
T-05 wave-1 analysis — intrinsic properties of metric hard-core only.
No Athena / T-01 / T-03 / T-04 comparison. No P*.
"""

from __future__ import annotations

import argparse
import json
import math
import statistics
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parent.parent


def load_runs(path: Path) -> List[Dict[str, Any]]:
    out = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            if line.strip():
                out.append(json.loads(line))
    return out


def gkey(p: Dict[str, Any]) -> Tuple:
    return (p["n"], p["d"], p["epsilon"])


def analyze(runs: List[Dict[str, Any]]) -> Dict[str, Any]:
    by: Dict[Tuple, List[Dict[str, Any]]] = defaultdict(list)
    for r in runs:
        by[gkey(r["params"])].append(r)

    cells = []
    hard_core_violations = 0
    for key, recs in sorted(by.items()):
        dens = [r["density"] for r in recs]
        cards = [r["cardinality"] for r in recs]
        mins = [r["min_distance_accepted"] for r in recs if r["min_distance_accepted"] is not None]
        eps = key[2]
        for r in recs:
            md = r["min_distance_accepted"]
            if md is not None and md < eps - 1e-9:
                hard_core_violations += 1
        cells.append(
            {
                "n": key[0],
                "d": key[1],
                "epsilon": eps,
                "n_seeds": len(recs),
                "density_mean": statistics.mean(dens),
                "density_std": statistics.pstdev(dens) if len(dens) > 1 else 0.0,
                "cardinality_mean": statistics.mean(cards),
                "min_dist_mean": statistics.mean(mins) if mins else None,
            }
        )

    # packing upper bound rough: area of disks radius eps/2
    properties = [
        {
            "id": "N1",
            "name": "hard_core_min_distance",
            "statement": (
                "By construction of sequential hard-core acceptance, any two accepted points "
                "satisfy Euclidean distance >= epsilon (up to floating-point error)."
            ),
            "class": "NECESSARY",
            "justification": "Acceptance condition forbids adding a point within epsilon of an accepted one.",
        },
        {
            "id": "N2",
            "name": "diameter_bound_single_point",
            "statement": (
                "If epsilon > sqrt(d) (diameter of [0,1]^d), at most one point can be accepted."
            ),
            "class": "NECESSARY",
            "justification": "Any two points in the unit cube are at distance <= sqrt(d).",
        },
        {
            "id": "N3",
            "name": "metric_not_ordinal",
            "statement": (
                "Selection depends only on Euclidean positions and epsilon, not on integer "
                "adjacency |i-j|; permuting labels without moving points leaves the geometry rule invariant."
            ),
            "class": "NECESSARY",
            "justification": "Rule uses only X_i and ||·||_2; indices are tags.",
        },
        {
            "id": "N4",
            "name": "packing_cardinality_bound",
            "statement": (
                "Accepted set is an epsilon-packing of [0,1]^d; cardinality is O(epsilon^{-d}) "
                "(e.g. area argument with disjoint balls of radius epsilon/2 intersected with a slightly enlarged cube)."
            ),
            "class": "NECESSARY",
            "justification": "Standard packing bound for hard-core point sets in a bounded domain.",
        },
    ]

    # EMPIRICAL: density decreases with epsilon
    mono = 0
    mono_n = 0
    for n in sorted({c["n"] for c in cells}):
        row = sorted([c for c in cells if c["n"] == n], key=lambda c: c["epsilon"])
        mono_n += 1
        if all(
            row[i]["density_mean"] > row[i + 1]["density_mean"] + 1e-12
            for i in range(len(row) - 1)
        ):
            mono += 1
    properties.append(
        {
            "id": "E1",
            "name": "density_decreases_with_epsilon",
            "statement": f"For {mono}/{mono_n} values of n, mean density strictly decreases as epsilon increases.",
            "class": "EMPIRICAL",
            "justification": "Wave-1 observation; consistent with packing but finite-n/seed.",
        }
    )

    properties.append(
        {
            "id": "E2",
            "name": "hard_core_numerical_check",
            "statement": f"Hard-core violations in raw min_distance < epsilon: {hard_core_violations} (expect 0).",
            "class": "EMPIRICAL",
            "justification": "Numerical support of N1.",
        }
    )

    volatile = [c for c in cells if c["density_std"] > 0.02]
    properties.append(
        {
            "id": "S1",
            "name": "seed_sensitivity",
            "statement": f"{len(volatile)}/{len(cells)} cells have density_std > 0.02 across seeds.",
            "class": "SEED_DEPENDENT",
            "justification": "Random points + random order.",
        }
    )

    properties.append(
        {
            "id": "U1",
            "name": "matérn_intensity_limit",
            "statement": "Exact limiting intensity of this sequential thinning vs classical Matérn hard-core processes.",
            "class": "UNKNOWN",
            "justification": "Not derived in wave-1; literature exists but not claimed here.",
        }
    )

    return {
        "family": "T-05",
        "spec_version": "1.0",
        "n_runs": len(runs),
        "n_param_cells": len(cells),
        "cells_summary": cells,
        "properties": properties,
        "hard_core_violations": hard_core_violations,
        "note": (
            "Intrinsic geometry only. Question: what MUST happen given this machine? "
            "Not: does it look like primes? No P* sealed."
        ),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw", type=Path, default=ROOT / "results" / "T05_REFERENCE_WAVE1" / "raw_runs.jsonl")
    ap.add_argument("--out", type=Path, default=ROOT / "results" / "T05_REFERENCE_WAVE1" / "analysis_wave1.json")
    args = ap.parse_args()
    report = analyze(load_runs(args.raw))
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "n_runs": report["n_runs"],
                "n_param_cells": report["n_param_cells"],
                "hard_core_violations": report["hard_core_violations"],
                "properties": [
                    {"id": p["id"], "class": p["class"], "name": p["name"]} for p in report["properties"]
                ],
                "wrote": str(args.out),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
