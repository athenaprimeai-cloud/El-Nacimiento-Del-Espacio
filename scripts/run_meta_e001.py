"""META-E001 campaign — multi-seed, try to falsify pipeline benefit."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from athena_core.meta_eval import run_meta_e001_campaign


def main() -> int:
    n_rep = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    n_cand = int(sys.argv[2]) if len(sys.argv) > 2 else 100
    out = run_meta_e001_campaign(n_rep=n_rep, n_candidates=n_cand)
    dest = ROOT / "META-E001" / "resultados"
    dest.mkdir(parents=True, exist_ok=True)
    path = dest / "classification.json"
    path.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(out, indent=2, ensure_ascii=False))
    print(f"\nWrote {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
