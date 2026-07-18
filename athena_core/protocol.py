"""
Núcleo ejecutable del protocolo Athena (PASO 1).

Impone disciplina. No investiga matemáticas. No usa IA.
"""

from __future__ import annotations

import json
import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional


class HypothesisState(str, Enum):
    """Estados de primera clase — incluyen NO_SABEMOS."""

    OPEN = "OPEN"  # ficha creada, sin resultado de control
    SOPORTADA_BAJO_CONTROL = "SOPORTADA_BAJO_CONTROL"
    DEBILITADA = "DEBILITADA"
    MUERTA = "MUERTA"
    INDETERMINADA = "INDETERMINADA"
    NO_SABEMOS = "NO_SABEMOS"


# Terminal states: no more result registration that rewrites history lightly
_TERMINAL = frozenset(
    {
        HypothesisState.SOPORTADA_BAJO_CONTROL,
        HypothesisState.DEBILITADA,
        HypothesisState.MUERTA,
        HypothesisState.INDETERMINADA,
        HypothesisState.NO_SABEMOS,
    }
)

_CLOSED_WITH_RESULT = _TERMINAL  # all require a recorded control except OPEN


class ProtocolError(Exception):
    """Violación de disciplina del núcleo."""

    def __init__(self, code: str, message: str) -> None:
        self.code = code
        super().__init__(f"[{code}] {message}")


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _new_id(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4().hex[:8]}"


@dataclass
class Question:
    id: str
    text: str
    domain: str
    created_at: str


@dataclass
class Hypothesis:
    id: str
    question_id: str
    statement: str
    predicts: str  # Z — frozen after result
    weakens_if: str
    dies_if: str  # W
    state: str
    control_id: Optional[str] = None
    result_summary: Optional[str] = None
    death_reason: Optional[str] = None
    created_at: str = field(default_factory=_now)
    finalized_at: Optional[str] = None
    history: List[Dict[str, Any]] = field(default_factory=list)

    def is_terminal(self) -> bool:
        return HypothesisState(self.state) in _TERMINAL

    def has_result(self) -> bool:
        return self.result_summary is not None and self.control_id is not None


@dataclass
class ControlRecord:
    id: str
    hypothesis_id: str
    description: str
    created_at: str


class ProtocolStore:
    """Persistencia JSON simple (registro permanente del núcleo)."""

    def __init__(self, root: Optional[Path] = None) -> None:
        if root is None:
            root = Path(__file__).resolve().parent.parent / "data" / "athena_core"
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)
        self._questions = self.root / "questions.json"
        self._hypotheses = self.root / "hypotheses.json"
        self._controls = self.root / "controls.json"
        self._audit = self.root / "audit_log.jsonl"
        for p in (self._questions, self._hypotheses, self._controls):
            if not p.exists():
                p.write_text("{}", encoding="utf-8")

    def _load(self, path: Path) -> Dict[str, Any]:
        return json.loads(path.read_text(encoding="utf-8"))

    def _save(self, path: Path, data: Dict[str, Any]) -> None:
        path.write_text(
            json.dumps(data, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )

    def audit(self, event: str, detail: Dict[str, Any]) -> None:
        line = json.dumps(
            {"ts": _now(), "event": event, **detail}, ensure_ascii=False
        )
        with self._audit.open("a", encoding="utf-8") as f:
            f.write(line + "\n")

    def save_question(self, q: Question) -> None:
        data = self._load(self._questions)
        data[q.id] = asdict(q)
        self._save(self._questions, data)

    def get_question(self, qid: str) -> Optional[Dict[str, Any]]:
        return self._load(self._questions).get(qid)

    def save_hypothesis(self, h: Hypothesis) -> None:
        data = self._load(self._hypotheses)
        data[h.id] = asdict(h)
        self._save(self._hypotheses, data)

    def get_hypothesis(self, hid: str) -> Optional[Hypothesis]:
        raw = self._load(self._hypotheses).get(hid)
        if raw is None:
            return None
        return Hypothesis(**raw)

    def all_hypotheses(self) -> List[Hypothesis]:
        data = self._load(self._hypotheses)
        return [Hypothesis(**v) for v in data.values()]

    def save_control(self, c: ControlRecord) -> None:
        data = self._load(self._controls)
        data[c.id] = asdict(c)
        self._save(self._controls, data)

    def delete_hypothesis_attempt(self, hid: str) -> None:
        """Always raises if hypothesis exists — especially if MUERTA."""
        h = self.get_hypothesis(hid)
        if h is None:
            raise ProtocolError("NOT_FOUND", f"Hipótesis {hid} no existe")
        if HypothesisState(h.state) == HypothesisState.MUERTA:
            self.audit(
                "REJECT_DELETE_DEAD",
                {"hypothesis_id": hid, "state": h.state},
            )
            raise ProtocolError(
                "FT-CORE-02",
                "No se puede borrar una hipótesis MUERTA (memoria negativa)",
            )
        self.audit(
            "REJECT_DELETE",
            {"hypothesis_id": hid, "state": h.state},
        )
        raise ProtocolError(
            "DELETE_FORBIDDEN",
            "El núcleo no borra hipótesis; solo archiva estados",
        )


def create_question(
    text: str,
    domain: str = "unspecified",
    store: Optional[ProtocolStore] = None,
) -> Question:
    store = store or ProtocolStore()
    q = Question(id=_new_id("Q"), text=text.strip(), domain=domain, created_at=_now())
    if not q.text:
        raise ProtocolError("EMPTY", "La pregunta no puede estar vacía")
    store.save_question(q)
    store.audit("CREATE_QUESTION", {"id": q.id, "text": q.text})
    return q


def create_hypothesis(
    question_id: str,
    statement: str,
    predicts: str,
    weakens_if: str,
    dies_if: str,
    store: Optional[ProtocolStore] = None,
) -> Hypothesis:
    store = store or ProtocolStore()
    if store.get_question(question_id) is None:
        raise ProtocolError("NO_QUESTION", f"Pregunta {question_id} no existe")
    if not all(
        s.strip() for s in (statement, predicts, weakens_if, dies_if)
    ):
        raise ProtocolError(
            "INCOMPLETE_FICHA",
            "Se requieren statement, predicts, weakens_if y dies_if",
        )
    h = Hypothesis(
        id=_new_id("H"),
        question_id=question_id,
        statement=statement.strip(),
        predicts=predicts.strip(),
        weakens_if=weakens_if.strip(),
        dies_if=dies_if.strip(),
        state=HypothesisState.OPEN.value,
        history=[{"ts": _now(), "event": "created"}],
    )
    store.save_hypothesis(h)
    store.audit("CREATE_HYPOTHESIS", {"id": h.id, "question_id": question_id})
    return h


def get_hypothesis(
    hypothesis_id: str, store: Optional[ProtocolStore] = None
) -> Hypothesis:
    store = store or ProtocolStore()
    h = store.get_hypothesis(hypothesis_id)
    if h is None:
        raise ProtocolError("NOT_FOUND", f"Hipótesis {hypothesis_id} no existe")
    return h


def list_hypotheses(store: Optional[ProtocolStore] = None) -> List[Hypothesis]:
    store = store or ProtocolStore()
    return store.all_hypotheses()


def record_result(
    hypothesis_id: str,
    control_description: str,
    result_summary: str,
    new_state: str,
    death_reason: Optional[str] = None,
    store: Optional[ProtocolStore] = None,
) -> Hypothesis:
    """
    Registra resultado bajo un control y cierra estado.
    Requiere control_description no vacío (FT-CORE-03).
    """
    store = store or ProtocolStore()
    h = get_hypothesis(hypothesis_id, store)

    if h.is_terminal():
        raise ProtocolError(
            "ALREADY_FINAL",
            f"Hipótesis {hypothesis_id} ya está en estado terminal {h.state}",
        )

    if not control_description or not control_description.strip():
        store.audit(
            "BLOCK_NO_CONTROL",
            {"hypothesis_id": hypothesis_id},
        )
        raise ProtocolError(
            "FT-CORE-03",
            "No se puede cerrar hipótesis sin control declarado",
        )

    try:
        state = HypothesisState(new_state)
    except ValueError as e:
        raise ProtocolError(
            "INVALID_STATE",
            f"Estado no permitido: {new_state}. "
            f"Use: {[s.value for s in HypothesisState if s != HypothesisState.OPEN]}",
        ) from e

    if state == HypothesisState.OPEN:
        raise ProtocolError(
            "INVALID_STATE",
            "No se puede 'cerrar' en OPEN; use un estado de resultado",
        )

    if state == HypothesisState.MUERTA and not (
        death_reason and death_reason.strip()
    ):
        raise ProtocolError(
            "DEATH_REASON_REQUIRED",
            "MUERTA requiere death_reason (memoria negativa)",
        )

    ctrl = ControlRecord(
        id=_new_id("C"),
        hypothesis_id=h.id,
        description=control_description.strip(),
        created_at=_now(),
    )
    store.save_control(ctrl)

    h.control_id = ctrl.id
    h.result_summary = result_summary.strip()
    h.state = state.value
    h.finalized_at = _now()
    if death_reason:
        h.death_reason = death_reason.strip()
    h.history.append(
        {
            "ts": h.finalized_at,
            "event": "result_recorded",
            "control_id": ctrl.id,
            "state": h.state,
        }
    )
    store.save_hypothesis(h)
    store.audit(
        "RECORD_RESULT",
        {
            "hypothesis_id": h.id,
            "control_id": ctrl.id,
            "state": h.state,
        },
    )
    return h


def finalize_hypothesis(
    hypothesis_id: str,
    control_description: str,
    result_summary: str,
    new_state: str,
    death_reason: Optional[str] = None,
    store: Optional[ProtocolStore] = None,
) -> Hypothesis:
    """Alias explícito de cierre con control (misma regla FT-CORE-03)."""
    return record_result(
        hypothesis_id,
        control_description,
        result_summary,
        new_state,
        death_reason=death_reason,
        store=store,
    )


def attempt_update_predicts_after_result(
    hypothesis_id: str,
    new_predicts: str,
    store: Optional[ProtocolStore] = None,
) -> None:
    """
    Intento ilegal: cambiar predicción después del resultado (FT-CORE-01).
    Siempre rechaza si ya hay resultado.
    """
    store = store or ProtocolStore()
    h = get_hypothesis(hypothesis_id, store)
    if h.has_result() or h.is_terminal():
        h.history.append(
            {
                "ts": _now(),
                "event": "predicts_attempt",
                "attempted": new_predicts,
            }
        )
        store.save_hypothesis(h)
        store.audit(
            "REJECT_PREDICT_REWRITE",
            {
                "hypothesis_id": hypothesis_id,
                "old": h.predicts,
                "attempted": new_predicts,
            },
        )
        raise ProtocolError(
            "FT-CORE-01",
            "No se puede cambiar la predicción después del resultado",
        )
    store.audit(
        "REJECT_PREDICT_REWRITE_PRE",
        {"hypothesis_id": hypothesis_id},
    )
    raise ProtocolError(
        "PREDICT_IMMUTABLE",
        "En CORE v0.1 la predicción es inmutable tras crear la ficha",
    )


def force_corrupt_predicts_for_audit(
    hypothesis_id: str,
    new_predicts: str,
    store: Optional[ProtocolStore] = None,
) -> Hypothesis:
    """
    SOLO para pruebas del auditor: simula corrupción del registro
    (reescribe predicción tras resultado saltándose el protocolo).
    No es API de uso normal.
    """
    store = store or ProtocolStore()
    h = get_hypothesis(hypothesis_id, store)
    h.predicts = new_predicts
    h.history.append(
        {
            "ts": _now(),
            "event": "predicts_changed",
            "note": "CORRUPTION_FOR_AUDIT_TEST",
        }
    )
    store.save_hypothesis(h)
    store.audit(
        "PREDICT_REWRITTEN",
        {"hypothesis_id": hypothesis_id, "new": new_predicts},
    )
    return h


def force_delete_hypothesis_for_audit(
    hypothesis_id: str,
    store: Optional[ProtocolStore] = None,
) -> None:
    """
    SOLO para pruebas del auditor: simula borrado ilegal del registro.
    """
    store = store or ProtocolStore()
    data = store._load(store._hypotheses)
    if hypothesis_id not in data:
        raise ProtocolError("NOT_FOUND", f"Hipótesis {hypothesis_id} no existe")
    del data[hypothesis_id]
    store._save(store._hypotheses, data)
    store.audit(
        "HYPOTHESIS_DELETED",
        {"hypothesis_id": hypothesis_id},
    )


def attempt_delete_hypothesis(
    hypothesis_id: str, store: Optional[ProtocolStore] = None
) -> None:
    store = store or ProtocolStore()
    store.delete_hypothesis_attempt(hypothesis_id)
