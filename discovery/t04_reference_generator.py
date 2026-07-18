"""
T-04 reference generator — geometric gap renewal (point process on 1..N).

Spec: ATHENA_T04_REFERENCE_GENERATOR.md 1.0
Blind: no T-01/T-03 results, no Athena domain I/O.
Does not analyze or invent P*.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import random
from pathlib import Path
from typing import Any, Dict, List, Sequence

DISCOVERY_DIR = Path(__file__).resolve().parent
ROOT = DISCOVERY_DIR.parent


def _assert_config_ok(path: Path) -> None:
    s = str(path).replace("\\", "/")
    for frag in (
        "ATHENA_SURVIVORS",
        "ATHENA_DOMAIN_",
        "classification.json",
        "T01_REFERENCE",
        "T03_REFERENCE",
        "t01_wave",
        "t03_wave",
    ):
        if frag in s and "t04" not in s.lower():
            # allow only if it's clearly t04 path; config is t04
            if "t04" not in Path(s).name.lower() and "T04" not in s:
                raise RuntimeError(f"T-04 refuses path: {path}")


def draw_geometric_gap(rng: random.Random, q: float) -> int:
    """Gap G >= 1: trials until success with probability q."""
    if not (0.0 < q <= 1.0):
        raise ValueError("q must be in (0,1]")
    g = 0
    while True:
        g += 1
        if rng.random() < q:
            return g


def generate_t04(N: int, q: float, seed: int) -> Dict[str, Any]:
    rng = random.Random(seed)
    occupied: List[int] = []
    p = 0
    n_gaps = 0
    gap_sum = 0
    while p < N:
        G = draw_geometric_gap(rng, q)
        n_gaps += 1
        gap_sum += G
        p = p + G
        if 1 <= p <= N:
            occupied.append(p)
        # if p > N: stop without adding
    card = len(occupied)
    return {
        "family": "T-04",
        "spec_version": "1.0",
        "params": {
            "N": N,
            "q": q,
            "seed": seed,
            "gap_law": "geometric",
        },
        "occupied": occupied,
        "cardinality": card,
        "density": card / N if N else 0.0,
        "n_gaps_drawn": n_gaps,
        "mean_gap_realized": (gap_sum / n_gaps) if n_gaps else 0.0,
        "expected_gap": 1.0 / q,
        "expected_density_approx": q,
    }


def expand_wave(config: Dict[str, Any]) -> List[Dict[str, Any]]:
    jobs = []
    for N in config["N_list"]:
        for q in config["q_list"]:
            for seed in config["seeds"]:
                jobs.append({"N": int(N), "q": float(q), "seed": int(seed)})
    return jobs


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def run_wave(config_path: Path, out_dir: Path) -> Dict[str, Any]:
    _assert_config_ok(config_path)
    config = json.loads(config_path.read_text(encoding="utf-8"))
    out_dir.mkdir(parents=True, exist_ok=True)
    raw_path = out_dir / "raw_runs.jsonl"
    jobs = expand_wave(config)

    with raw_path.open("w", encoding="utf-8", newline="\n") as f:
        for j, job in enumerate(jobs):
            rec = generate_t04(**job)
            rec["run_index"] = j
            f.write(json.dumps(rec, ensure_ascii=False, separators=(",", ":")) + "\n")

    raw_hash = sha256_file(raw_path)
    manifest = {
        "wave": config.get("wave", "T04_REFERENCE_WAVE1"),
        "family": "T-04",
        "spec_version": "1.0",
        "config_path": str(config_path.as_posix()),
        "n_jobs": len(jobs),
        "raw_runs": raw_path.name,
        "raw_runs_sha256": raw_hash,
        "blind": True,
        "athena_io": "forbidden",
        "t01_io": "forbidden",
        "t03_io": "forbidden",
        "generation": "gap_renewal_geometric",
    }
    man_path = out_dir / "wave_manifest.json"
    man_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    sums = out_dir / "sha256.txt"
    sums.write_text(
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
    p = argparse.ArgumentParser(description="T-04 blind geometric renewal generator")
    p.add_argument("--config", type=Path, default=DISCOVERY_DIR / "t04_wave1_config.json")
    p.add_argument("--out", type=Path, default=ROOT / "results" / "T04_REFERENCE_WAVE1")
    p.add_argument("--smoke", action="store_true")
    args = p.parse_args(list(argv) if argv is not None else None)

    if args.smoke:
        rec = generate_t04(N=100, q=0.2, seed=0)
        rec2 = generate_t04(N=100, q=0.2, seed=0)
        assert rec["occupied"] == rec2["occupied"]
        print(
            json.dumps(
                {
                    "params": rec["params"],
                    "cardinality": rec["cardinality"],
                    "density": rec["density"],
                    "mean_gap_realized": rec["mean_gap_realized"],
                    "expected_gap": rec["expected_gap"],
                    "reproducibility_ok": True,
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
