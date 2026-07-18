"""
CHALLENGE SELECTOR — prioriza qué atacar primero.
No decide verdad. Determinista, auditable.
"""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional, Sequence, Set

from .protocol import Hypothesis, HypothesisState, ProtocolStore, get_hypothesis


def _tokens(text: str) -> Set[str]:
    return {t for t in re.findall(r"[a-zA-Z0-9_Δ]+", (text or "").lower()) if len(t) > 1}


def _jaccard(a: Set[str], b: Set[str]) -> float:
    if not a and not b:
        return 1.0
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def _has_numeric_anchor(text: str) -> bool:
    return bool(re.search(r"\d", text or ""))


@dataclass
class ScoredCandidate:
    hypothesis_id: str
    group: str  # A | B | C
    rank: int
    score: float
    novelty: float
    falsifiability: float
    redundancy: float
    cost: float
    completeness: float
    selector_confidence: float  # 0..1 — how decisive the ranking signal is
    reasons: List[str] = field(default_factory=list)
    # Explicit priority rationale (auditable; heuristics are methodological hypotheses)
    priority_rationale: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class SelectionReport:
    n_input: int
    n_group_a: int
    n_group_b: int
    n_group_c: int
    ranked: List[ScoredCandidate]
    selector_version: str = "v0.1-deterministic"
    # Methodological caveat: scoring rules are hypotheses, not truths
    heuristic_status: str = (
        "methodological_hypothesis — may bias against hard-but-important work; "
        "must be retrospectively auditable"
    )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "n_input": self.n_input,
            "n_group_a": self.n_group_a,
            "n_group_b": self.n_group_b,
            "n_group_c": self.n_group_c,
            "selector_version": self.selector_version,
            "heuristic_status": self.heuristic_status,
            "scarce_resource": "experiments (not hypotheses)",
            "ranked": [r.to_dict() for r in self.ranked],
            "claim": (
                "Priority for experimental budget only; "
                "not truth; selector can be wrong and must be audited later"
            ),
        }


def _score_one(
    h: Hypothesis,
    others: Sequence[Hypothesis],
) -> ScoredCandidate:
    reasons: List[str] = []
    pred = h.predicts or ""
    weak = h.weakens_if or ""
    dies = h.dies_if or ""
    stmt = h.statement or ""

    # Completeness 0..1
    fields = [stmt, pred, weak, dies]
    filled = sum(1 for f in fields if f.strip())
    completeness = filled / 4.0
    if completeness < 1.0:
        reasons.append("ficha incompleta o débil")

    # Falsifiability 0..1
    fals = 0.0
    if dies.strip():
        fals += 0.45
    if weak.strip():
        fals += 0.25
    if _has_numeric_anchor(dies) or _has_numeric_anchor(pred):
        fals += 0.20
        reasons.append("anclas numéricas en predicción/muerte")
    if len(dies.strip()) >= 12 and len(pred.strip()) >= 12:
        fals += 0.10
    fals = min(1.0, fals)
    if fals >= 0.7:
        reasons.append("alta falsabilidad relativa")
    elif fals < 0.4:
        reasons.append("baja falsabilidad")

    # Novelty vs others (1 - max jaccard on statement+predicts)
    self_tok = _tokens(stmt + " " + pred)
    max_sim = 0.0
    for o in others:
        if o.id == h.id:
            continue
        sim = _jaccard(self_tok, _tokens((o.statement or "") + " " + (o.predicts or "")))
        if sim > max_sim:
            max_sim = sim
    novelty = 1.0 - max_sim
    redundancy = max_sim
    if redundancy >= 0.5:
        reasons.append(f"redundante (similitud≈{redundancy:.2f})")
    if novelty >= 0.7:
        reasons.append("novedad relativa alta")

    # Cost: vaguer / longer = higher cost (worse)
    length_pen = min(1.0, (len(stmt) + len(pred)) / 400.0)
    vague = 0.0
    for bad in ("interesante", "bonita", "siempre", "se ve", "plot", "teoría"):
        if bad in (stmt + pred).lower():
            vague += 0.15
    cost = min(1.0, 0.3 + 0.4 * length_pen + vague)
    if cost >= 0.7:
        reasons.append("coste experimental heurístico alto")

    # Combined: high fals + novelty, low redundancy + cost
    score = (
        0.35 * fals
        + 0.25 * novelty
        + 0.15 * completeness
        + 0.15 * (1.0 - redundancy)
        + 0.10 * (1.0 - cost)
    )

    # Confidence: high when signals agree (high fals + novelty, low redun/cost)
    agreement = (
        fals
        + novelty
        + (1.0 - redundancy)
        + (1.0 - cost)
        + completeness
    ) / 5.0
    # Penalize mid-range ambiguity
    confidence = abs(agreement - 0.5) * 2.0 * min(1.0, fals + 0.3)
    confidence = round(min(1.0, max(0.05, confidence * agreement)), 2)

    rationale = {
        "falsifiability": round(fals, 2),
        "cost": round(cost, 2),
        "redundancy": round(redundancy, 2),
        "novelty": round(novelty, 2),
        "completeness": round(completeness, 2),
        "score": round(score, 4),
        "selector_confidence": confidence,
        "note": "Heuristics are methodological hypotheses, not truths",
    }

    return ScoredCandidate(
        hypothesis_id=h.id,
        group="",  # fill later
        rank=0,
        score=round(score, 4),
        novelty=round(novelty, 4),
        falsifiability=round(fals, 4),
        redundancy=round(redundancy, 4),
        cost=round(cost, 4),
        completeness=round(completeness, 4),
        selector_confidence=confidence,
        reasons=reasons or ["puntuación por defecto"],
        priority_rationale=rationale,
    )


def select_challenges(
    hypothesis_ids: Optional[Sequence[str]] = None,
    store: Optional[ProtocolStore] = None,
    only_open: bool = True,
    top_a_fraction: float = 0.15,
    top_a_min: int = 1,
    top_a_max: int = 15,
) -> SelectionReport:
    """
    Ordena candidatos para presupuesto de ataque.
    Por defecto solo hipótesis OPEN.
    """
    store = store or ProtocolStore()
    if hypothesis_ids is None:
        hyps = store.all_hypotheses()
    else:
        hyps = [get_hypothesis(hid, store) for hid in hypothesis_ids]

    if only_open:
        hyps = [h for h in hyps if h.state == HypothesisState.OPEN.value]

    if not hyps:
        return SelectionReport(0, 0, 0, 0, [])

    scored: List[ScoredCandidate] = []
    for h in hyps:
        scored.append(_score_one(h, hyps))

    # Soft-penalize redundancy in ranking without burying all similar candidates as C
    for s in scored:
        s.score = round(s.score - 0.08 * s.redundancy, 4)

    scored.sort(key=lambda s: (-s.score, s.hypothesis_id))

    n = len(scored)
    n_a = max(top_a_min, min(top_a_max, int(round(n * top_a_fraction))))
    n_a = min(n_a, n)
    # Bottom third by score → C; incomplete fichas always C
    n_c_floor = max(0, n // 3)

    for i, s in enumerate(scored):
        s.rank = i + 1
        if s.completeness < 1.0 or s.falsifiability < 0.3:
            s.group = "C"
            s.reasons.append("grupo C: ficha débil / poco falsable")
        elif s.rank <= n_a:
            s.group = "A"
            s.reasons.append("grupo A: priorizar ataque (presupuesto experimental)")
        elif s.rank > n - n_c_floor:
            s.group = "C"
            s.reasons.append("grupo C: cola de prioridad / bajo score")
        else:
            s.group = "B"
            s.reasons.append("grupo B: valor medio")
        s.priority_rationale["priority_final"] = s.group
        s.priority_rationale["rank"] = s.rank

    na = sum(1 for s in scored if s.group == "A")
    nb = sum(1 for s in scored if s.group == "B")
    nc = sum(1 for s in scored if s.group == "C")

    return SelectionReport(
        n_input=n,
        n_group_a=na,
        n_group_b=nb,
        n_group_c=nc,
        ranked=scored,
    )


def build_selector_retrospective_stub(
    selection: SelectionReport,
) -> Dict[str, Any]:
    """
    Plantilla para auditoría futura del Selector (meses después):
    ¿las A sobrevivieron más? ¿las C escondían mejores hallazgos?
    Las heurísticas deben poder fallar y documentarse.
    """
    return {
        "selector_version": selection.selector_version,
        "heuristic_status": selection.heuristic_status,
        "questions_for_later": [
            "¿Las hipótesis grupo A sobrevivieron más a controles que B/C?",
            "¿Las C escondían descubrimientos mejores cuando se atacaron?",
            "¿El sesgo a barato/falsable/novedoso dejó fuera trabajo difícil e importante?",
        ],
        "assignments": [
            {
                "hypothesis_id": s.hypothesis_id,
                "group": s.group,
                "score": s.score,
                "selector_confidence": s.selector_confidence,
                "priority_rationale": s.priority_rationale,
                # Fill later after controls:
                "outcome_after_attack": None,
                "selector_was_useful": None,
            }
            for s in selection.ranked
        ],
        "note": (
            "Selector is also a methodological object of study; "
            "not a permanent unexamined bias"
        ),
    }
