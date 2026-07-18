"""
T-05 reference generator — Unif points in [0,1]^d + sequential metric hard-core.

Spec: ATHENA_T05_REFERENCE_GENERATOR.md 1.0
Blind: no Athena, SURVIVORS, E00x, T-01/T-03/T-04 I/O.
Does not analyze or invent P*.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import random
from pathlib import Path
from typing import Any, Dict, List, Sequence, Tuple

DISCOVERY_DIR = Path(__file__).resolve().parent
ROOT = DISCOVERY_DIR.parent


def _refuse_forbidden(path: Path) -> None:
    s = str(path).replace("\\", "/")
    for frag in (
        "ATHENA_SURVIVORS",
        "ATHENA_DOMAIN_",
        "classification.json",
        "T01_REFERENCE",
        "T03_REFERENCE",
        "T04_REFERENCE",
        "t01_wave",
        "t03_wave",
        "t04_wave",
    ):
        if frag in s:
            raise RuntimeError(f"T-05 generator refuses path: {path}")


def euclid(a: Sequence[float], b: Sequence[float]) -> float:
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))


def generate_t05(n: int, d: int, epsilon: float, seed: int) -> Dict[str, Any]:
    rng_pts = random.Random(seed)
    points: List[List[float]] = [
        [rng_pts.random() for _ in range(d)] for _ in range(n)
    ]
    # permutation with independent stream
    rng_perm = random.Random(seed + 1)
    order = list(range(n))
    rng_perm.shuffle(order)

    accepted: List[int] = []
    accepted_coords: List[List[float]] = []
    for i in order:
        ok = True
        for j in accepted:
            if euclid(points[i], points[j]) < epsilon:
                ok = False
                break
        if ok:
            accepted.append(i)
            accepted_coords.append(points[i][:])

    # labels 1..n for archive consistency with other families
    occupied = sorted(i + 1 for i in accepted)
    card = len(occupied)

    # mean nearest-neighbor among accepted (if >=2)
    mean_nn = 0.0
    if card >= 2:
        nns = []
        for a in range(card):
            best = float("inf")
            for b in range(card):
                if a == b:
                    continue
                best = min(best, euclid(accepted_coords[a], accepted_coords[b]))
            nns.append(best)
        mean_nn = sum(nns) / len(nns)

    return {
        "family": "T-05",
        "spec_version": "1.0",
        "params": {
            "n": n,
            "d": d,
            "epsilon": epsilon,
            "seed": seed,
            "selection": "sequential_hard_core_metric",
            "point_process": "iid_uniform_unit_cube",
        },
        "occupied": occupied,
        "coordinates_accepted": accepted_coords,
        "cardinality": card,
        "density": card / n if n else 0.0,
        "mean_nn_distance_accepted": mean_nn,
        "min_distance_accepted": (
            min(
                euclid(accepted_coords[a], accepted_coords[b])
                for a in range(card)
                for b in range(a + 1, card)
            )
            if card >= 2
            else None
        ),
    }


def expand_wave(config: Dict[str, Any]) -> List[Dict[str, Any]]:
    d = int(config["d"])
    jobs = []
    for n in config["n_list"]:
        for eps in config["epsilon_list"]:
            for seed in config["seeds"]:
                jobs.append(
                    {
                        "n": int(n),
                        "d": d,
                        "epsilon": float(eps),
                        "seed": int(seed),
                    }
                )
    return jobs


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def run_wave(config_path: Path, out_dir: Path) -> Dict[str, Any]:
    _refuse_forbidden(config_path)
    config = json.loads(config_path.read_text(encoding="utf-8"))
    out_dir.mkdir(parents=True, exist_ok=True)
    raw_path = out_dir / "raw_runs.jsonl"
    jobs = expand_wave(config)

    with raw_path.open("w", encoding="utf-8", newline="\n") as f:
        for j, job in enumerate(jobs):
            rec = generate_t05(**job)
            rec["run_index"] = j
            f.write(json.dumps(rec, ensure_ascii=False, separators=(",", ":")) + "\n")

    raw_hash = sha256_file(raw_path)
    manifest = {
        "wave": config.get("wave", "T05_REFERENCE_WAVE1"),
        "family": "T-05",
        "spec_version": "1.0",
        "config_path": str(config_path.as_posix()),
        "n_jobs": len(jobs),
        "raw_runs": raw_path.name,
        "raw_runs_sha256": raw_hash,
        "blind": True,
        "athena_io": "forbidden",
        "t01_t03_t04_io": "forbidden",
        "representation": "metric_embedding_R^d",
    }
    man_path = out_dir / "wave_manifest.json"
    man_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (out_dir / "sha256.txt").write_text(
        "\n".join(
            [
                f"{raw_hash}  {raw_path.name}",
                f"{sha256_file(man_path)}  {man_path.name}",
                f"{sha256_file(config_path)}  config:{config_path.name}",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    return manifest


def main(argv: Sequence[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="T-05 blind metric hard-core generator")
    p.add_argument("--config", type=Path, default=DISCOVERY_DIR / "t05_wave1_config.json")
    p.add_argument("--out", type=Path, default=ROOT / "results" / "T05_REFERENCE_WAVE1")
    p.add_argument("--smoke", action="store_true")
    args = p.parse_args(list(argv) if argv is not None else None)

    if args.smoke:
        r1 = generate_t05(n=200, d=2, epsilon=0.05, seed=0)
        r2 = generate_t05(n=200, d=2, epsilon=0.05, seed=0)
        assert r1["occupied"] == r2["occupied"]
        assert r1["min_distance_accepted"] is None or r1["min_distance_accepted"] >= 0.05 - 1e-12
        print(
            json.dumps(
                {
                    "params": r1["params"],
                    "cardinality": r1["cardinality"],
                    "density": r1["density"],
                    "min_distance_accepted": r1["min_distance_accepted"],
                    "reproducibility_ok": True,
                    "hard_core_ok": True,
                },
                indent=2,
            )
        )
        return 0

    man = run_wave(args.config.resolve(), args.out.resolve())
    print(json.dumps(man, indent=2))
    print(f"Wrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
