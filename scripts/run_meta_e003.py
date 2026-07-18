"""
META-E003 — ¿el Auditor solo ve forma o también daño epistemológico?
"""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path
from typing import Any, Callable, Dict, List, Tuple

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from athena_core.auditor import AuditVerdict, audit_store
from athena_core.protocol import (
    HypothesisState,
    ProtocolError,
    ProtocolStore,
    create_hypothesis,
    create_question,
    force_corrupt_predicts_for_audit,
    force_delete_hypothesis_for_audit,
    record_result,
)


def _fresh() -> ProtocolStore:
    return ProtocolStore(Path(tempfile.mkdtemp(prefix="e003_")))


def _base_hyp(store: ProtocolStore, tag: str = ""):
    q = create_question(f"META-E003 {tag}", domain="meta-e003", store=store)
    return create_hypothesis(
        q.id,
        f"H {tag}: diferencia medible",
        predicts="Si H, |Δ| > 0.1 bajo control C",
        weakens_if="0 < |Δ| ≤ 0.1",
        dies_if="|Δ| ≈ 0",
        store=store,
    )


AttackFn = Callable[[], Tuple[str, str, str]]
# returns (attack_id, expected_verdict, notes)


def attack_a1() -> Tuple[str, str, Dict[str, Any]]:
    store = _fresh()
    h = _base_hyp(store, "A1")
    record_result(
        h.id, "Control C", "murió", HypothesisState.DEBILITADA.value, store=store
    )
    force_corrupt_predicts_for_audit(h.id, "predicción reescrita post-hoc", store=store)
    rep = audit_store(store)
    return "A1", rep.verdict, {"findings": [f.code for f in rep.findings]}


def attack_a2() -> Tuple[str, str, Dict[str, Any]]:
    store = _fresh()
    h = _base_hyp(store, "A2")
    record_result(
        h.id,
        "Control C",
        "muerta",
        HypothesisState.MUERTA.value,
        death_reason="dies_if",
        store=store,
    )
    force_delete_hypothesis_for_audit(h.id, store=store)
    rep = audit_store(store)
    return "A2", rep.verdict, {"findings": [f.code for f in rep.findings]}


def attack_a3() -> Tuple[str, str, Dict[str, Any]]:
    """Try close MUERTA without reason — Core should block; if forced, Auditor fails."""
    store = _fresh()
    h = _base_hyp(store, "A3")
    blocked = False
    try:
        record_result(
            h.id, "Control C", "x", HypothesisState.MUERTA.value, store=store
        )
    except ProtocolError as e:
        blocked = e.code == "DEATH_REASON_REQUIRED"
    # Also plant invalid terminal via direct corruption
    h2 = _base_hyp(store, "A3b")
    from athena_core.protocol import get_hypothesis

    hh = get_hypothesis(h2.id, store)
    hh.state = HypothesisState.MUERTA.value
    hh.control_id = "C-fake"
    hh.result_summary = "x"
    hh.death_reason = None
    store.save_hypothesis(hh)
    rep = audit_store(store)
    return (
        "A3",
        rep.verdict,
        {"core_blocked_clean_path": blocked, "findings": [f.code for f in rep.findings]},
    )


def attack_a4() -> Tuple[str, str, Dict[str, Any]]:
    """Scale: many OPEN + one buried corruption."""
    store = _fresh()
    for i in range(50):
        _base_hyp(store, f"scale-{i}")
    h = _base_hyp(store, "A4-corrupt")
    record_result(
        h.id, "Control C", "ok", HypothesisState.DEBILITADA.value, store=store
    )
    force_corrupt_predicts_for_audit(h.id, "buried rewrite", store=store)
    rep = audit_store(store)
    return "A4", rep.verdict, {
        "n_hypotheses": len(store.all_hypotheses()),
        "findings": [f.code for f in rep.findings],
    }


def attack_a5() -> Tuple[str, str, Dict[str, Any]]:
    """Semantic shift: formal OK, meaning displaced — Auditor expected PASS."""
    store = _fresh()
    h = _base_hyp(store, "A5")
    # Formally valid close; summary misrepresents (still "a string")
    record_result(
        h.id,
        "Control C: malla completa",
        "resultado favorece hipótesis",  # misleading vs actual conditionality
        HypothesisState.SOPORTADA_BAJO_CONTROL.value,
        store=store,
    )
    rep = audit_store(store)
    return "A5", rep.verdict, {
        "note": "semantic corruption; format valid",
        "findings": [f.code for f in rep.findings],
    }


def attack_a6() -> Tuple[str, str, Dict[str, Any]]:
    """Misleading metric campaign: only ECO reported in summary; form OK."""
    store = _fresh()
    h = _base_hyp(store, "A6")
    record_result(
        h.id,
        "Control: presupuesto",
        "ECO=0.85; (no se reportó cobertura/diversidad)",
        HypothesisState.SOPORTADA_BAJO_CONTROL.value,
        store=store,
    )
    rep = audit_store(store)
    return "A6", rep.verdict, {
        "note": "metric omission not checked by Auditor v0.1",
        "findings": [f.code for f in rep.findings],
    }


def attack_a7() -> Tuple[str, str, Dict[str, Any]]:
    """Formal compliance; result does not address prediction."""
    store = _fresh()
    h = _base_hyp(store, "A7")
    record_result(
        h.id,
        "Control C",
        "el experimento terminó sin errores de sistema",  # never answers |Δ|>0.1
        HypothesisState.SOPORTADA_BAJO_CONTROL.value,
        store=store,
    )
    rep = audit_store(store)
    return "A7", rep.verdict, {
        "note": "result does not speak to prediction",
        "findings": [f.code for f in rep.findings],
    }


def control_nosabe() -> Tuple[str, str, Dict[str, Any]]:
    store = _fresh()
    h = _base_hyp(store, "NOSABE")
    record_result(
        h.id,
        "Control C",
        "señal mixta",
        HypothesisState.NO_SABEMOS.value,
        store=store,
    )
    rep = audit_store(store)
    return "CTRL_NOSABE", rep.verdict, {"findings": [f.code for f in rep.findings]}


def main() -> int:
    structural = [attack_a1, attack_a2, attack_a3, attack_a4]
    semantic = [attack_a5, attack_a6, attack_a7]
    results = []

    for fn in structural + semantic + [control_nosabe]:
        aid, verdict, detail = fn()
        results.append({"attack": aid, "auditor_verdict": verdict, **detail})

    struct = [r for r in results if r["attack"].startswith("A") and r["attack"] <= "A4"]
    # fix: A1-A4 by name
    struct = [r for r in results if r["attack"] in ("A1", "A2", "A3", "A4")]
    sem = [r for r in results if r["attack"] in ("A5", "A6", "A7")]
    nosabe = next(r for r in results if r["attack"] == "CTRL_NOSABE")

    det_struct = sum(1 for r in struct if r["auditor_verdict"] == "FAIL") / len(struct)
    pass_sem = sum(1 for r in sem if r["auditor_verdict"] == "PASS") / len(sem)
    fp_nosabe = nosabe["auditor_verdict"] == "FAIL"

    # Verdict per protocol
    if det_struct < 1.0:
        h01, h00 = "DEBILITADA", "SOPORTADA_BAJO_CONTROL"
        verdict = "STRUCTURAL_GAP"
    elif pass_sem >= 2 / 3 and not fp_nosabe:
        h01, h00 = "SOPORTADA_BAJO_CONTROL", "SOPORTADA_BAJO_CONTROL"
        # both: H01 on structural, H00 on semantic limits — dual support
        verdict = "DUAL_H01_STRUCT_H00_SEMANTIC_LIMITS"
    else:
        h01, h00 = "NO_SABEMOS", "NO_SABEMOS"
        verdict = "NO_SABEMOS"

    area_map = {
        "integridad_documental": "fuerte" if det_struct == 1.0 else "debil",
        "contratos_explicitos": "fuerte" if det_struct == 1.0 else "debil",
        "interpretacion_semantica": "limitada" if pass_sem >= 2 / 3 else "inesperada_deteccion",
        "supuestos_ocultos_metricas": "abierta" if pass_sem >= 2 / 3 else "parcial",
        "no_sabemos_legitimo": "ok" if not fp_nosabe else "falso_positivo",
    }

    out = {
        "campaign": "META-E003",
        "protocol": "v1.0 CONGELADO",
        "results": results,
        "metrics": {
            "DET_STRUCT": det_struct,
            "PASS_SEM": pass_sem,
            "FP_NOSABE": fp_nosabe,
        },
        "hypotheses": {
            "H-META-E003-01": h01,
            "H-META-E003-00": h00,
        },
        "verdict": verdict,
        "area_map": area_map,
        "evidence_profile": {
            "E-M1": "fuerte" if det_struct == 1.0 else "contraria",
            "E-M2": "no evaluada",
            "E-M3": "parcial — forma vs semántica",
            "E-M4": "no evaluada",
            "E-M5": "no evaluada",
        },
        "reading": (
            "Auditor v0.1 is strong on structural/protocol form; "
            "semantic and metric-choice damage can PASS — "
            "shared-assumption blind spot (H-00 on semantics)."
        ),
        "legislation_hint": (
            "Do not destroy Auditor; document boundary: automatic form + human/semantic review"
        ),
        "claim_limit": "Attack suite is predeclared; not an exhaustive adversary.",
    }
    dest = ROOT / "META-E003" / "resultados"
    dest.mkdir(parents=True, exist_ok=True)
    path = dest / "classification.json"
    path.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(out, indent=2, ensure_ascii=False))
    print(f"\nWrote {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
