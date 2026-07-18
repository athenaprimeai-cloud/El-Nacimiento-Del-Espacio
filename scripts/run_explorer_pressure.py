"""PASO 3 — presión exploratoria: N candidatos, kernel no debe romperse."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from athena_core.auditor import audit_store
from athena_core.explorer import explore_pressure
from athena_core.protocol import ProtocolStore


def main() -> int:
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 100
    data = ROOT / "data" / "athena_explorer_pressure"
    if data.exists():
        for p in data.glob("*"):
            if p.is_file():
                p.unlink()
    store = ProtocolStore(data)
    report = explore_pressure(
        "¿Existe alguna diferencia medible en un sistema toy bajo control C?",
        n_candidates=n,
        store=store,
    )
    audit = audit_store(store)
    out = {
        **report.to_dict(),
        "auditor_verdict": audit.verdict,
        "auditor_findings": audit.to_dict()["findings"],
        "paso3_success": (
            report.n_rejected > report.n_accepted
            and audit.verdict == "PASS"
            and report.n_requested == n
        ),
        "claim": (
            "Éxito = kernel absorbió ruido sin romperse; "
            "no se reclama hipótesis brillante ni descubrimiento."
        ),
    }
    (data / "EXPLORER_PRESSURE_REPORT.json").write_text(
        json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(json.dumps(out, indent=2, ensure_ascii=False))
    return 0 if out["paso3_success"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
