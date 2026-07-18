"""Explorador → Selector: presión luego priorización de ataque."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from athena_core.auditor import audit_store
from athena_core.explorer import explore_pressure
from athena_core.protocol import ProtocolStore
from athena_core.selector import (
    build_selector_retrospective_stub,
    select_challenges,
)


def main() -> int:
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 100
    data = ROOT / "data" / "athena_selector_run"
    if data.exists():
        for p in data.glob("*"):
            if p.is_file():
                p.unlink()
    store = ProtocolStore(data)
    explore_pressure(
        "¿Hay diferencia medible bajo control C? (presión + selección)",
        n_candidates=n,
        store=store,
    )
    selection = select_challenges(store=store, only_open=True)
    audit = audit_store(store)
    out = {
        "explorer_n": n,
        "selection": selection.to_dict(),
        "top_a": [
            r.to_dict()
            for r in selection.ranked
            if r.group == "A"
        ][:10],
        "retrospective_stub": build_selector_retrospective_stub(selection),
        "auditor_verdict": audit.verdict,
        "bottleneck": "research economy — what to attack first",
        "scarce_resource": "experiments",
        "claim": "Priority only; not truth; selector heuristics are methodological hypotheses",
    }
    (data / "SELECTOR_REPORT.json").write_text(
        json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(json.dumps(out, indent=2, ensure_ascii=False)[:4000])
    print("...")
    print(
        json.dumps(
            {
                "n_input": selection.n_input,
                "A": selection.n_group_a,
                "B": selection.n_group_b,
                "C": selection.n_group_c,
                "auditor": audit.verdict,
            },
            indent=2,
        )
    )
    return 0 if audit.verdict == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
