"""
T-03 reference generator — elementary CA (Wolfram r=1), deterministic sync.

Implements ATHENA_T03_REFERENCE_GENERATOR.md spec 1.0 only.
Blind: no T-01 raw/analysis, no SURVIVORS, no DOMAIN E00x, no classification.json.
Does not analyze, compare, or invent P*.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import random
import sys
from pathlib import Path
from typing import Any, Dict, List, Sequence

DISCOVERY_DIR = Path(__file__).resolve().parent
ROOT = DISCOVERY_DIR.parent

_FORBIDDEN_NAME_FRAGMENTS = (
    "ATHENA_SURVIVORS",
    "ATHENA_DOMAIN_",
    "classification.json",
    "META_DECISION_LOG",
    "T01_REFERENCE",
    "t01_reference",
    "T01_NECESSARY",
    "raw_runs.jsonl",  # only if path is under T01 — checked more carefully
)


def _assert_not_forbidden(path: Path) -> None:
    s = str(path).replace("\\", "/")
    # Allow writing T03 paths; forbid reading Athena / T01 result trees as config
    if "T01_REFERENCE" in s or "t01_wave" in s.lower():
        raise RuntimeError(f"T-03 generator refuses T-01 path: {path}")
    for frag in (
        "ATHENA_SURVIVORS",
        "ATHENA_DOMAIN_",
        "classification.json",
        "META_DECISION_LOG",
    ):
        if frag in s:
            raise RuntimeError(f"T-03 generator refuses forbidden path: {path}")


def wolfram_next(x: Sequence[int], W: int) -> List[int]:
    """
    Synchronous elementary CA, r=1, null boundary (outside = 0).
    LSB of W = f(000). Neighborhood code = 4*left + 2*center + right.
    """
    N = len(x)
    x_next = [0] * N
    for i in range(N):
        left = x[i - 1] if i > 0 else 0
        center = x[i]
        right = x[i + 1] if i + 1 < N else 0
        code = (left << 2) | (center << 1) | right
        x_next[i] = (W >> code) & 1
    return x_next


def generate_initial_state(N: int, p_init: float, seed: int) -> List[int]:
    rng = random.Random(seed)
    return [1 if rng.random() < p_init else 0 for _ in range(N)]


def run_once(
    N: int,
    W: int,
    p_init: float,
    T: int,
    seed: int,
) -> Dict[str, Any]:
    x = generate_initial_state(N, p_init, seed)
    initial_occupied = [i + 1 for i, v in enumerate(x) if v == 1]
    dens_hist = [sum(x) / N]
    for _ in range(T):
        x = wolfram_next(x, W)
        dens_hist.append(sum(x) / N)
    occupied = [i + 1 for i, v in enumerate(x) if v == 1]
    card = len(occupied)
    return {
        "family": "T-03",
        "spec_version": "1.0",
        "params": {
            "N": N,
            "r": 1,
            "W": W,
            "p_init": p_init,
            "T": T,
            "seed": seed,
            "boundary": "null",
        },
        "initial_occupied_count": len(initial_occupied),
        "initial_density": len(initial_occupied) / N,
        "occupied": occupied,
        "cardinality": card,
        "density": card / N,
        "trajectory_summary": {
            "density_by_t": dens_hist,
            "final_density": card / N,
            "extinct": card == 0,
            "full": card == N,
        },
    }


def expand_wave(config: Dict[str, Any]) -> List[Dict[str, Any]]:
    jobs = []
    p_init = float(config["p_init"])
    r = int(config.get("r", 1))
    if r != 1:
        raise ValueError("spec 1.0 wave1 requires r=1")
    for N in config["N_list"]:
        for W in config["W_list"]:
            for T in config["T_list"]:
                for seed in config["seeds"]:
                    jobs.append(
                        {
                            "N": int(N),
                            "W": int(W),
                            "p_init": p_init,
                            "T": int(T),
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
    _assert_not_forbidden(config_path)
    config = json.loads(config_path.read_text(encoding="utf-8"))
    out_dir.mkdir(parents=True, exist_ok=True)
    raw_path = out_dir / "raw_runs.jsonl"
    jobs = expand_wave(config)

    with raw_path.open("w", encoding="utf-8", newline="\n") as f:
        for j, job in enumerate(jobs):
            rec = run_once(**job)
            rec["run_index"] = j
            f.write(json.dumps(rec, ensure_ascii=False, separators=(",", ":")) + "\n")

    raw_hash = sha256_file(raw_path)
    manifest = {
        "wave": config.get("wave", "T03_REFERENCE_WAVE1"),
        "family": "T-03",
        "spec_version": "1.0",
        "config_path": str(config_path.as_posix()),
        "n_jobs": len(jobs),
        "raw_runs": raw_path.name,
        "raw_runs_sha256": raw_hash,
        "blind": True,
        "athena_io": "forbidden",
        "t01_io": "forbidden",
        "synchronous_update": True,
        "deterministic_transition": True,
    }
    man_path = out_dir / "wave_manifest.json"
    man_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    sums_path = out_dir / "sha256.txt"
    lines = [
        f"{raw_hash}  {raw_path.name}",
        f"{sha256_file(man_path)}  {man_path.name}",
        f"{sha256_file(config_path)}  config:{config_path.name}",
    ]
    sums_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return manifest


def main(argv: Sequence[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="T-03 blind elementary CA generator")
    p.add_argument(
        "--config",
        type=Path,
        default=DISCOVERY_DIR / "t03_wave1_config.json",
    )
    p.add_argument(
        "--out",
        type=Path,
        default=ROOT / "results" / "T03_REFERENCE_WAVE1",
    )
    p.add_argument("--smoke", action="store_true")
    args = p.parse_args(list(argv) if argv is not None else None)

    if args.smoke:
        rec = run_once(N=64, W=30, p_init=0.5, T=10, seed=0)
        print(
            json.dumps(
                {
                    "params": rec["params"],
                    "cardinality": rec["cardinality"],
                    "density": rec["density"],
                    "trajectory_summary": rec["trajectory_summary"],
                },
                indent=2,
            )
        )
        # reproducibility check
        rec2 = run_once(N=64, W=30, p_init=0.5, T=10, seed=0)
        assert rec["occupied"] == rec2["occupied"], "deterministic trajectory failed"
        print("reproducibility_ok: true")
        return 0

    man = run_wave(args.config.resolve(), args.out.resolve())
    print(json.dumps(man, indent=2))
    print(f"Wrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
