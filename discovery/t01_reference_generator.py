"""
T-01 reference generator — blind to Athena historical results.

Implements ATHENA_T01_REFERENCE_GENERATOR.md spec 1.0 only.
No imports/paths of SURVIVORS, DOMAIN E00x, or classification.json.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import random
import sys
from pathlib import Path
from typing import Any, Dict, List, Sequence

# Discovery root = parent of this file's directory's parent when run as script
DISCOVERY_DIR = Path(__file__).resolve().parent
ROOT = DISCOVERY_DIR.parent

# Hard ban: refuse to open forbidden names if someone passes them as config
_FORBIDDEN_NAME_FRAGMENTS = (
    "ATHENA_SURVIVORS",
    "ATHENA_DOMAIN_",
    "classification.json",
    "META_DECISION_LOG",
)


def _assert_not_forbidden(path: Path) -> None:
    s = str(path).replace("\\", "/")
    for frag in _FORBIDDEN_NAME_FRAGMENTS:
        if frag in s:
            raise RuntimeError(f"T-01 generator refuses forbidden path: {path}")


def generate_initial_state(N: int, p_init: float, seed: int) -> List[int]:
    rng = random.Random(seed)
    return [1 if rng.random() < p_init else 0 for _ in range(N)]


def neighbor_sum(x: Sequence[int], i: int, r: int) -> int:
    """0-based index i; neighbors j with 0 < |j-i| <= r."""
    N = len(x)
    s = 0
    lo = max(0, i - r)
    hi = min(N - 1, i + r)
    for j in range(lo, hi + 1):
        if j != i:
            s += x[j]
    return s


def synchronous_update(
    x: Sequence[int],
    r: int,
    theta: int,
    p_birth: float,
    rng: random.Random,
) -> List[int]:
    """
    Fully synchronous: all decisions from x(t), then apply together.
    Never use already-updated cells when deciding neighbors.
    """
    N = len(x)
    # Precompute all U_i for births in order i=0..N-1
    U = [rng.random() for _ in range(N)]
    x_next = [0] * N
    for i in range(N):
        ns = neighbor_sum(x, i, r)
        if ns >= theta:
            x_next[i] = 0
        elif x[i] == 1 or U[i] < p_birth:
            x_next[i] = 1
        else:
            x_next[i] = 0
    return x_next


def run_once(
    N: int,
    r: int,
    theta: int,
    p_init: float,
    p_birth: float,
    T: int,
    seed: int,
) -> Dict[str, Any]:
    x = generate_initial_state(N, p_init, seed)
    initial_occupied = [i + 1 for i, v in enumerate(x) if v == 1]
    dens_hist = [sum(x) / N]
    for t in range(T):
        # Spec: Random(s + 1 + t)
        rng = random.Random(seed + 1 + t)
        x = synchronous_update(x, r, theta, p_birth, rng)
        dens_hist.append(sum(x) / N)
    occupied = [i + 1 for i, v in enumerate(x) if v == 1]
    card = len(occupied)
    return {
        "family": "T-01",
        "spec_version": "1.0",
        "params": {
            "N": N,
            "r": r,
            "theta": theta,
            "p_init": p_init,
            "p_birth": p_birth,
            "T": T,
            "seed": seed,
        },
        "initial_cardinality": len(initial_occupied),
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
    for N in config["N_list"]:
        for r in config["r_list"]:
            for theta in config["theta_list"]:
                if theta > 2 * r:
                    continue
                for p_birth in config["p_birth_list"]:
                    for T in config["T_list"]:
                        for seed in config["seeds"]:
                            jobs.append(
                                {
                                    "N": int(N),
                                    "r": int(r),
                                    "theta": int(theta),
                                    "p_init": p_init,
                                    "p_birth": float(p_birth),
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
        "wave": config.get("wave", "T01_REFERENCE_WAVE1"),
        "family": "T-01",
        "spec_version": "1.0",
        "config_path": str(config_path.as_posix()),
        "n_jobs": len(jobs),
        "raw_runs": raw_path.name,
        "raw_runs_sha256": raw_hash,
        "blind": True,
        "athena_io": "forbidden",
        "synchronous_update": True,
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
    p = argparse.ArgumentParser(description="T-01 blind reference generator")
    p.add_argument(
        "--config",
        type=Path,
        default=DISCOVERY_DIR / "t01_wave1_config.json",
        help="Wave parameter config (not the family rule)",
    )
    p.add_argument(
        "--out",
        type=Path,
        default=ROOT / "results" / "T01_REFERENCE_WAVE1",
        help="Output directory for raw_runs + manifest",
    )
    p.add_argument(
        "--smoke",
        action="store_true",
        help="Single tiny run for sanity (N=100, 1 seed) without full wave",
    )
    args = p.parse_args(list(argv) if argv is not None else None)

    if args.smoke:
        rec = run_once(N=100, r=2, theta=2, p_init=0.5, p_birth=0.2, T=5, seed=0)
        print(json.dumps({k: rec[k] for k in ("params", "cardinality", "density", "trajectory_summary")}, indent=2))
        return 0

    man = run_wave(args.config.resolve(), args.out.resolve())
    print(json.dumps(man, indent=2))
    print(f"Wrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
