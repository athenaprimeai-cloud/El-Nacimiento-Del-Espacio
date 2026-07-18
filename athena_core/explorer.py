"""
PASO 3 — Explorador: presión exploratoria, no conocimiento.

Genera candidatos sintéticos (sin LLM). No decide, no archiva estados terminales.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from .protocol import (
    Hypothesis,
    ProtocolError,
    ProtocolStore,
    create_hypothesis,
    create_question,
)


@dataclass
class CandidateAttempt:
    index: int
    accepted: bool
    hypothesis_id: Optional[str] = None
    error_code: Optional[str] = None
    error_message: Optional[str] = None
    statement: str = ""
    latent_class: str = "noise"


@dataclass
class ExplorerReport:
    question_id: str
    n_requested: int
    n_accepted: int
    n_rejected: int
    attempts: List[CandidateAttempt] = field(default_factory=list)
    # meta-only map hyp_id -> latent_class (Selector must not use)
    latent_by_hyp: Dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "question_id": self.question_id,
            "n_requested": self.n_requested,
            "n_accepted": self.n_accepted,
            "n_rejected": self.n_rejected,
            "rejection_rate": (
                self.n_rejected / self.n_requested if self.n_requested else 0.0
            ),
            "attempts": [
                {
                    "index": a.index,
                    "accepted": a.accepted,
                    "hypothesis_id": a.hypothesis_id,
                    "error_code": a.error_code,
                    "statement": a.statement[:80],
                    "latent_class": a.latent_class,
                }
                for a in self.attempts
            ],
            "latent_by_hyp": self.latent_by_hyp,
            "success_criterion": (
                "Kernel absorbed pressure without redefining method; "
                "success ≠ brilliant hypothesis"
            ),
        }


def _synthetic_payload(i: int, n: int, seed: int = 0) -> Dict[str, str]:
    """
    Mix of valid fichas and deliberate incomplete/noise payloads.
    ~80% noisy/incomplete, ~20% well-formed — pressure test.
    seed shifts which indices are well-formed (replica variation).

    latent_class (meta only; Selector must not use):
      noise | common_ok | rare_valuable
    """
    j = (i + seed * 7) % max(1, n)
    # Incomplete / noise (should be rejected by CORE)
    if j % 5 != 0:
        kind = j % 4
        if kind == 0:
            return {
                "statement": f"candidato ruido {i}",
                "predicts": "",  # incomplete
                "weakens_if": "x",
                "dies_if": "y",
                "latent_class": "noise",
            }
        if kind == 1:
            return {
                "statement": "",
                "predicts": "algo",
                "weakens_if": "w",
                "dies_if": "d",
                "latent_class": "noise",
            }
        if kind == 2:
            return {
                "statement": f"patrón interesante {i}",
                "predicts": "se ve en el plot",
                "weakens_if": "",  # incomplete
                "dies_if": "no se ve",
                "latent_class": "noise",
            }
        return {
            "statement": f"teoría bonita {i}",
            "predicts": "siempre",
            "weakens_if": "a veces",
            "dies_if": "",  # incomplete
            "latent_class": "noise",
        }
    # Well-formed: mix common_ok and rare_valuable (rare = unusual metrics / long path)
    # rare_valuable: deliberately "hard" / less flashy falsifiability style
    rare = ((i + seed * 3) % 5 == 0)
    if rare:
        return {
            "statement": (
                f"H-rare-{i}: estructura poco frecuente en región R_{(i+seed)%11} "
                f"(baja señal local, posible profundidad)"
            ),
            "predicts": (
                f"Si H-rare, efecto solo en cola de malla N≥{(i%3)+2}00 "
                f"con |Δ| > 0.05 tras t largo"
            ),
            "weakens_if": f"efecto solo en un seed o N medio",
            "dies_if": f"efecto nulo en toda la malla alta",
            "latent_class": "rare_valuable",
        }
    return {
        "statement": f"H-cand-{i}: diferencia medible en métrica M_{(i + seed) % 7}",
        "predicts": f"Si H, |ΔM| > 0.1 en control C_{(i + seed) % 3}",
        "weakens_if": f"0 < |ΔM| ≤ 0.1 en C_{(i + seed) % 3}",
        "dies_if": f"|ΔM| ≈ 0 en C_{(i + seed) % 3}",
        "latent_class": "common_ok",
    }


def explore_pressure(
    question_text: str,
    n_candidates: int = 100,
    domain: str = "explorer/pressure",
    store: Optional[ProtocolStore] = None,
    seed: int = 0,
) -> ExplorerReport:
    """
    Genera N candidatos sintéticos y los empuja al kernel.
    No interpreta; no cierra estados terminales.
    """
    store = store or ProtocolStore()
    q = create_question(question_text, domain=domain, store=store)
    attempts: List[CandidateAttempt] = []
    accepted = 0
    rejected = 0

    latent_by_hyp: Dict[str, str] = {}
    for i in range(n_candidates):
        payload = _synthetic_payload(i, n_candidates, seed=seed)
        lat = payload.get("latent_class", "noise")
        try:
            h: Hypothesis = create_hypothesis(
                q.id,
                payload["statement"],
                payload["predicts"],
                payload["weakens_if"],
                payload["dies_if"],
                store=store,
            )
            accepted += 1
            latent_by_hyp[h.id] = lat
            attempts.append(
                CandidateAttempt(
                    index=i,
                    accepted=True,
                    hypothesis_id=h.id,
                    statement=payload["statement"],
                    latent_class=lat,
                )
            )
        except ProtocolError as e:
            rejected += 1
            attempts.append(
                CandidateAttempt(
                    index=i,
                    accepted=False,
                    error_code=e.code,
                    error_message=str(e),
                    statement=payload.get("statement", ""),
                    latent_class=lat,
                )
            )

    return ExplorerReport(
        question_id=q.id,
        n_requested=n_candidates,
        n_accepted=accepted,
        n_rejected=rejected,
        attempts=attempts,
        latent_by_hyp=latent_by_hyp,
    )
