"""
Programa meta: ¿el conjunto es mejor que las partes?
Métricas de proceso, no de matemáticas de dominio.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional

from .auditor import audit_store
from .explorer import explore_pressure
from .protocol import HypothesisState, ProtocolStore
from .selector import select_challenges


@dataclass
class ModeMetrics:
    mode: str
    n_candidates_generated: int
    n_open_accepted: int
    n_rejected_by_core: int
    n_group_a: int = 0
    n_group_b: int = 0
    n_group_c: int = 0
    posthoc_violations: int = 0
    auditor_verdict: str = "PASS"
    # Proxies for "knowledge retained / process quality"
    elimination_ready: int = 0  # terminal with control (none in pure explore)
    no_sabemos_count: int = 0
    # Budget: if selector used, experiments "planned" = |A| not |all|
    budget_units: int = 0
    cost_proxy: float = 0.0  # budget_units / max(1, open)  or 1/open
    notes: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def _run_m1(store: ProtocolStore, question: str, n: int, seed: int = 0) -> ModeMetrics:
    rep = explore_pressure(question, n_candidates=n, store=store, seed=seed)
    audit = audit_store(store)
    open_n = rep.n_accepted
    # Without selector, budget = all open (must attack everything)
    budget = open_n
    return ModeMetrics(
        mode="M1_explorer_only",
        n_candidates_generated=rep.n_requested,
        n_open_accepted=open_n,
        n_rejected_by_core=rep.n_rejected,
        posthoc_violations=sum(
            1 for f in audit.findings if f.severity == "FAIL"
        ),
        auditor_verdict=audit.verdict,
        budget_units=budget,
        cost_proxy=round(budget / max(1, open_n), 4) if open_n else 0.0,
        notes=[
            "Budget = all OPEN; no prioritization",
            "No Critic/Designer yet — elimination_ready stays 0",
        ],
    )


def _run_m2(store: ProtocolStore, question: str, n: int, seed: int = 0) -> ModeMetrics:
    rep = explore_pressure(question, n_candidates=n, store=store, seed=seed)
    sel = select_challenges(store=store, only_open=True)
    audit = audit_store(store)
    open_n = rep.n_accepted
    budget = sel.n_group_a  # only A would be attacked first
    return ModeMetrics(
        mode="M2_explorer_selector",
        n_candidates_generated=rep.n_requested,
        n_open_accepted=open_n,
        n_rejected_by_core=rep.n_rejected,
        n_group_a=sel.n_group_a,
        n_group_b=sel.n_group_b,
        n_group_c=sel.n_group_c,
        posthoc_violations=sum(
            1 for f in audit.findings if f.severity == "FAIL"
        ),
        auditor_verdict=audit.verdict,
        budget_units=budget,
        cost_proxy=round(budget / max(1, open_n), 4) if open_n else 0.0,
        notes=[
            "Budget = |A| (priority attacks only)",
            "If cost_proxy < M1, selector reduces experiments per open hypothesis",
            "Selector heuristics = methodological hypothesis",
        ],
    )


def compare_modes(
    question: str = "¿Meta: hay diferencia medible bajo C?",
    n_candidates: int = 100,
    store_factory=None,
    seed: int = 0,
) -> Dict[str, Any]:
    """
    Compara M1 vs M2 (M3/M4 N/A hasta Crítico/Diseñador).
    store_factory: callable () -> ProtocolStore for isolation.
    """

    def fresh() -> ProtocolStore:
        if store_factory:
            return store_factory()
        raise ValueError("store_factory required for isolated modes")

    m1_store = fresh()
    m1 = _run_m1(m1_store, question + " [M1]", n_candidates, seed=seed)

    m2_store = fresh()
    m2 = _run_m2(m2_store, question + " [M2]", n_candidates, seed=seed)

    # Emergent value proxies (methodological, not domain math)
    budget_reduction = None
    if m1.budget_units > 0:
        budget_reduction = round(
            1.0 - (m2.budget_units / m1.budget_units), 4
        )

    posthoc_ok = (
        m1.posthoc_violations == 0
        and m2.posthoc_violations == 0
        and m1.auditor_verdict == "PASS"
        and m2.auditor_verdict == "PASS"
    )

    return {
        "seed": seed,
        "question_systemic": "¿El conjunto es mejor que la suma de las partes?",
        "modes": {
            "M1": m1.to_dict(),
            "M2": m2.to_dict(),
            "M3": {"status": "N/A", "reason": "Crítico not implemented"},
            "M4": {"status": "N/A", "reason": "Full pipeline not implemented"},
        },
        "comparison": {
            "budget_reduction_M2_vs_M1": budget_reduction,
            "posthoc_clean": posthoc_ok,
            "m2_budget_lt_m1": bool(m2.budget_units < m1.budget_units),
            "m2_improves_experiment_economy": bool(
                m2.budget_units < m1.budget_units and posthoc_ok
            ),
        },
        "claim_limit": (
            "Process metrics only. Scope: MONOLITO=no selector vs PIPELINE=selector. "
            "Not full monolith without Core. Not M4. Selector bias open."
        ),
    }


def run_meta_e001_campaign(
    n_rep: int = 10,
    n_candidates: int = 100,
    budget_reduction_threshold: float = 0.50,
    store_factory=None,
) -> Dict[str, Any]:
    """
    META-E001 multi-seed campaign per frozen protocol.
    Tries to falsify H-META-E001-01 as hard as the design allows.
    """
    import tempfile
    from pathlib import Path

    def fresh() -> ProtocolStore:
        if store_factory:
            return store_factory()
        d = Path(tempfile.mkdtemp(prefix="meta_e001_"))
        return ProtocolStore(d)

    replicas = []
    for seed in range(n_rep):
        r = compare_modes(
            question="META-E001: ¿pipeline separado vs monolito de presupuesto?",
            n_candidates=n_candidates,
            store_factory=fresh,
            seed=seed,
        )
        replicas.append(r)

    reductions = [
        r["comparison"]["budget_reduction_M2_vs_M1"]
        for r in replicas
        if r["comparison"]["budget_reduction_M2_vs_M1"] is not None
    ]
    posthoc_all = all(r["comparison"]["posthoc_clean"] for r in replicas)
    m2_lt_all = all(r["comparison"]["m2_budget_lt_m1"] for r in replicas)
    mean_red = sum(reductions) / len(reductions) if reductions else 0.0
    min_red = min(reductions) if reductions else 0.0
    n_meet_threshold = sum(1 for x in reductions if x >= budget_reduction_threshold)

    # Protocol rules (frozen):
    # H-01 dies if: pipeline more posthoc OR integrity fail OR budget not lower
    # H-00 dies if: reduction >= 50% with POSTHOC=0 and INTEGRITY PASS in all N_rep
    h01_dies = (not posthoc_all) or (not m2_lt_all)
    h00_dies = posthoc_all and m2_lt_all and n_meet_threshold == n_rep
    # If economy improves strongly: H-01 supported on E-M2; H-00 dies
    # If mixed: NO_SABEMOS

    if h01_dies and not h00_dies:
        verdict = "H-META-E001-00_WINS"  # separation does not help / hurts integrity
        h01_state = "MUERTA"
        h00_state = "SOPORTADA_BAJO_CONTROL"
    elif h00_dies and not h01_dies:
        verdict = "H-META-E001-01_WINS_E-M2"  # economy with integrity
        h01_state = "SOPORTADA_BAJO_CONTROL"
        h00_state = "MUERTA"
    elif h00_dies and h01_dies:
        verdict = "NO_SABEMOS_CONFLICT"
        h01_state = "NO_SABEMOS"
        h00_state = "NO_SABEMOS"
    else:
        # budget lower but threshold not met in all seeds, or mixed
        if m2_lt_all and posthoc_all and mean_red > 0:
            verdict = "H-META-E001-01_PARTIAL_E-M2"
            h01_state = "DEBILITADA" if mean_red < budget_reduction_threshold else "SOPORTADA_BAJO_CONTROL"
            h00_state = "DEBILITADA"
            if mean_red >= budget_reduction_threshold and n_meet_threshold < n_rep:
                h01_state = "DEBILITADA"  # not all replicas
                verdict = "NO_SABEMOS_THRESHOLD"
                h00_state = "NO_SABEMOS"
        else:
            verdict = "NO_SABEMOS"
            h01_state = "NO_SABEMOS"
            h00_state = "NO_SABEMOS"

    # Evidence profile
    e_m1 = "fuerte" if posthoc_all else "contraria"
    if m2_lt_all and mean_red >= budget_reduction_threshold and n_meet_threshold == n_rep:
        e_m2 = "fuerte"
    elif m2_lt_all and mean_red > 0:
        e_m2 = "moderada"
    elif not m2_lt_all:
        e_m2 = "contraria"
    else:
        e_m2 = "insuficiente"
    e_m3 = "insuficiente"  # no Critic; POSTHOC alone is weak for "errors"
    if not posthoc_all:
        e_m3 = "contraria"

    return {
        "campaign": "META-E001",
        "protocol": "v1.0 CONGELADO",
        "n_rep": n_rep,
        "n_candidates": n_candidates,
        "budget_reduction_threshold": budget_reduction_threshold,
        "replicas_summary": [
            {
                "seed": r["seed"],
                "budget_m1": r["modes"]["M1"]["budget_units"],
                "budget_m2": r["modes"]["M2"]["budget_units"],
                "reduction": r["comparison"]["budget_reduction_M2_vs_M1"],
                "posthoc_clean": r["comparison"]["posthoc_clean"],
            }
            for r in replicas
        ],
        "aggregate": {
            "mean_budget_reduction": round(mean_red, 4),
            "min_budget_reduction": round(min_red, 4),
            "n_replicas_meet_50pct": n_meet_threshold,
            "all_posthoc_clean": posthoc_all,
            "all_m2_budget_lt_m1": m2_lt_all,
        },
        "verdict": verdict,
        "hypotheses": {
            "H-META-E001-01": h01_state,
            "H-META-E001-00": h00_state,
        },
        "evidence_profile": {
            "E-M1": e_m1,
            "E-M2": e_m2,
            "E-M3": e_m3,
            "E-M4": "no evaluada",
            "E-M5": "no evaluada",
        },
        "local_vs_global": (
            "E-M2 local economy improvement does not prove global scientific quality; "
            "Selector bias (hard-but-important hypotheses) remains open"
        ),
        "scope_limit": (
            "MONOLITO = without Selector only; Core+Auditor present in both arms. "
            "Not a pure unstructured process without Core."
        ),
    }
