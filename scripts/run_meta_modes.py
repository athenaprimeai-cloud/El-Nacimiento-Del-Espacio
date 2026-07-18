"""Programa meta: comparar M1 vs M2 (proceso, no matemáticas de dominio)."""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from athena_core.meta_eval import compare_modes
from athena_core.protocol import ProtocolStore


def main() -> int:
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 100
    dirs: list[Path] = []

    def factory() -> ProtocolStore:
        d = Path(tempfile.mkdtemp(prefix="athena_meta_"))
        dirs.append(d)
        return ProtocolStore(d)

    out = compare_modes(n_candidates=n, store_factory=factory)
    out_path = ROOT / "data" / "athena_meta"
    out_path.mkdir(parents=True, exist_ok=True)
    report = out_path / "META_MODES_REPORT.json"
    report.write_text(
        json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(json.dumps(out, indent=2, ensure_ascii=False))
    print(f"\nWrote {report}")
    ok = out["comparison"]["posthoc_clean"]
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
