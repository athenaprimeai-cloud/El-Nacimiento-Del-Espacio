"""
PASO 2.5 — Representar investigaciones reales en el kernel sin reglas nuevas.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from athena_core.auditor import AuditVerdict, audit_store
from athena_core.protocol import (
    HypothesisState,
    ProtocolStore,
    create_hypothesis,
    create_question,
    record_result,
)


def run(data_dir: Path) -> dict:
    if data_dir.exists():
        # clean slate for validation run
        for p in data_dir.glob("*"):
            if p.is_file():
                p.unlink()
    store = ProtocolStore(data_dir)
    cases = []

    # --- KV-01 E004.1 H0 ---
    q1 = create_question(
        "¿Los regímenes dinámicos son esencialmente independientes del módulo M "
        "bajo la malla y métricas de E004.1?",
        domain="PEP-D / E004.1",
        store=store,
    )
    h0 = create_hypothesis(
        q1.id,
        "H0-E004.1: independencia esencial del módulo en {5,7,8,11}",
        predicts="Cada m∈{5,7,11} tiene ≥6/8 N almost_identical vs m=8",
        weakens_if="Algunos m fallan almost_identical pero no hay H1_strong",
        dies_if="H1_strong: ≥2 de {5,7,11} con ≥5/8 phase flips vs m=8",
        store=store,
    )
    record_result(
        h0.id,
        control_description=(
            "E004.1 v1.1 CONGELADO: m∈{8,5,7,11}, N malla 8, seeds 0-4, t=1000, "
            "umbrales §7.1; veredicto H1_strong"
        ),
        result_summary="H0: 0/3 módulos almost_identical; H1_strong 3/3; veredicto H1_strong",
        new_state=HypothesisState.MUERTA.value,
        death_reason="Ocurrió dies_if: H1_strong — dependencia de M observada",
        store=store,
    )
    cases.append({"id": "KV-01", "hyp": h0.id, "label": "E004.1 H0", "expect": "MUERTA"})

    # --- KV-02 H-E004-01 ---
    q2 = create_question(
        "¿El régimen depende del módulo M en la batería {5,7,8,11}?",
        domain="PEP-D / E004.1",
        store=store,
    )
    h01 = create_hypothesis(
        q2.id,
        "H-E004-01: el régimen depende de M en {5,7,8,11}",
        predicts="H1_strong bajo protocolo E004.1",
        weakens_if="Solo H1 parcial / PARTIAL_OR_C",
        dies_if="H0: independencia esencial en la batería",
        store=store,
    )
    record_result(
        h01.id,
        control_description="E004.1 v1.1 CONGELADO (mismo marco que KV-01)",
        result_summary="Veredicto H1_strong; hecho apoyado E2 bajo dominio de la batería",
        new_state=HypothesisState.SOPORTADA_BAJO_CONTROL.value,
        store=store,
    )
    cases.append(
        {"id": "KV-02", "hyp": h01.id, "label": "H-E004-01", "expect": "SOPORTADA_BAJO_CONTROL"}
    )

    # --- KV-03 H-E004-03 ---
    q3 = create_question(
        "¿La dependencia de M se explica solo por el tamaño del alfabeto |Σ|?",
        domain="PEP-D / E004.2",
        store=store,
    )
    h03 = create_hypothesis(
        q3.id,
        "H-E004-03: dependencia de M por tamaño del alfabeto (solo cardinal)",
        predicts="A |Σ|=8 fijo, L_mod vs L_alt almost_identical (≥6/8): outcome B",
        weakens_if="Diferencias parciales / outcome C",
        dies_if="n_flip≥5 a |Σ| fijo: outcome A — reorganización material sin cambiar cardinal",
        store=store,
    )
    record_result(
        h03.id,
        control_description=(
            "E004.2 v1.0 CONGELADO: L_mod vs L_alt, |Σ|=8, malla E004.1, "
            "matriz A/B/C/D; REF pass; n_flip=6, n_id=0, n_drift=2 → outcome A"
        ),
        result_summary="Outcome A; H-E004-03 pierde apoyo relativo en este control",
        new_state=HypothesisState.DEBILITADA.value,
        store=store,
    )
    cases.append(
        {"id": "KV-03", "hyp": h03.id, "label": "H-E004-03", "expect": "DEBILITADA"}
    )

    # --- KV-04 H-E004-02 (apoyo relativo, no verdad universal) ---
    q4 = create_question(
        "¿El proyector modular / ley de actualización importa a |Σ| fijo?",
        domain="PEP-D / E004.2",
        store=store,
    )
    h02 = create_hypothesis(
        q4.id,
        "H-E004-02 (núcleo usable): proyector modular importa (hipótesis compuesta)",
        predicts="Outcome A o divergencia material L_mod vs L_alt a |Σ|=8",
        weakens_if="Outcome B (casi-identidad) o C parcial",
        dies_if="Outcome B limpio: n_id≥6 a |Σ| fijo",
        store=store,
    )
    record_result(
        h02.id,
        control_description="E004.2 v1.0 (mismo control que KV-03)",
        result_summary=(
            "Outcome A; apoyo relativo E1 al núcleo proyector — "
            "no demuestra anillo Z/8Z completo; dominio = este control"
        ),
        new_state=HypothesisState.SOPORTADA_BAJO_CONTROL.value,
        store=store,
    )
    cases.append(
        {
            "id": "KV-04",
            "hyp": h02.id,
            "label": "H-E004-02 núcleo",
            "expect": "SOPORTADA_BAJO_CONTROL",
        }
    )

    # --- KV-05 failed generic ---
    q5 = create_question(
        "¿Toy: la métrica M siempre es positiva?",
        domain="validation/toy",
        store=store,
    )
    h_fail = create_hypothesis(
        q5.id,
        "H-toy-fail: M>0 siempre",
        predicts="M>0 en todas las celdas del control toy",
        weakens_if="M=0 en alguna celda",
        dies_if="M≤0 en mayoría de celdas",
        store=store,
    )
    record_result(
        h_fail.id,
        control_description="Toy control: 8 celdas sintéticas",
        result_summary="M≤0 en 7/8 celdas",
        new_state=HypothesisState.MUERTA.value,
        death_reason="dies_if: mayoría no positiva",
        store=store,
    )
    cases.append(
        {"id": "KV-05", "hyp": h_fail.id, "label": "hipótesis fallida toy", "expect": "MUERTA"}
    )

    # --- KV-06 indeterminate ---
    q6 = create_question(
        "¿Toy: el efecto es estable bajo ruido?",
        domain="validation/toy",
        store=store,
    )
    h_ind = create_hypothesis(
        q6.id,
        "H-toy-ind: efecto estable",
        predicts="Signo del efecto idéntico en todas las réplicas",
        weakens_if="Signo mixto en minoría",
        dies_if="Signo invertido en ≥ mitad de réplicas",
        store=store,
    )
    record_result(
        h_ind.id,
        control_description="Toy: 5 réplicas con ruido",
        result_summary="2 réplicas un signo, 2 el otro, 1 nulo — no predeclarado como A/B",
        new_state=HypothesisState.NO_SABEMOS.value,
        store=store,
    )
    cases.append(
        {
            "id": "KV-06",
            "hyp": h_ind.id,
            "label": "hipótesis indeterminada",
            "expect": "NO_SABEMOS",
        }
    )

    # Verify states
    from athena_core.protocol import get_hypothesis

    fit = []
    for c in cases:
        h = get_hypothesis(c["hyp"], store)
        ok = h.state == c["expect"]
        fit.append({**c, "actual": h.state, "fit": ok})

    report = audit_store(store)
    all_fit = all(x["fit"] for x in fit)
    # No new rules: only existing states and protocol API
    new_rules_needed = False
    kernel_pass = all_fit and report.verdict == AuditVerdict.PASS.value

    out = {
        "paso": "2.5",
        "question": "¿Kernel suficiente sin reglas nuevas?",
        "kernel_validation": "PASS" if kernel_pass else "FAIL",
        "all_cases_fit": all_fit,
        "auditor_verdict": report.verdict,
        "cases": fit,
        "auditor_findings": report.to_dict()["findings"],
        "new_protocol_rules_added": new_rules_needed,
        "claim": (
            "Investigaciones reales (E004.1, E004.2) y casos negativo/indeterminado "
            "se representan con CORE+AUDITOR existentes. "
            "No se reclama descubrimiento matemático ni PASO 3."
        ),
    }
    summary_path = data_dir / "KERNEL_VALIDATION_REPORT.json"
    summary_path.write_text(
        json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    return out


def main() -> int:
    data = ROOT / "data" / "athena_kernel_validation"
    out = run(data)
    print(json.dumps(out, indent=2, ensure_ascii=False))
    return 0 if out["kernel_validation"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
