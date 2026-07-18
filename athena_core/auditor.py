"""
ATHENA AUDITOR CORE — PASO 2

Vigila reglas del laboratorio. No juzga matemáticas.
Salida: PASS | WARN | FAIL + hallazgos.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional

from .protocol import (
    Hypothesis,
    HypothesisState,
    ProtocolStore,
    _TERMINAL,
)


class AuditVerdict(str, Enum):
    PASS = "PASS"
    WARN = "WARN"
    FAIL = "FAIL"


@dataclass
class Finding:
    code: str
    severity: str  # FAIL | WARN
    message: str
    hypothesis_id: Optional[str] = None


@dataclass
class AuditReport:
    verdict: str
    findings: List[Finding] = field(default_factory=list)
    hypotheses_checked: int = 0
    audit_events_checked: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "verdict": self.verdict,
            "hypotheses_checked": self.hypotheses_checked,
            "audit_events_checked": self.audit_events_checked,
            "findings": [asdict(f) for f in self.findings],
        }


def _load_audit_log(store: ProtocolStore) -> List[Dict[str, Any]]:
    path: Path = store._audit
    if not path.exists():
        return []
    events: List[Dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            events.append(json.loads(line))
        except json.JSONDecodeError:
            events.append({"event": "CORRUPT_LOG_LINE", "raw": line})
    return events


def audit_hypothesis(h: Hypothesis) -> List[Finding]:
    """Revisa una ficha aislada (sin opinión científica)."""
    findings: List[Finding] = []
    hid = h.id

    # Estado desconocido
    try:
        state = HypothesisState(h.state)
    except ValueError:
        findings.append(
            Finding(
                "INVALID_STATE",
                "FAIL",
                f"Estado no reconocido: {h.state!r}",
                hid,
            )
        )
        return findings

    # Terminal sin control → FAIL (conclusión sin marco)
    if state in _TERMINAL:
        if not h.control_id or not (h.result_summary and h.result_summary.strip()):
            findings.append(
                Finding(
                    "TERMINAL_WITHOUT_CONTROL",
                    "FAIL",
                    "Estado terminal sin control/result_summary",
                    hid,
                )
            )
        if state == HypothesisState.MUERTA and not (
            h.death_reason and h.death_reason.strip()
        ):
            findings.append(
                Finding(
                    "DEAD_WITHOUT_REASON",
                    "FAIL",
                    "MUERTA sin death_reason (memoria negativa incompleta)",
                    hid,
                )
            )

    # OPEN no debe pretender estar "soportada"
    if state == HypothesisState.OPEN and h.control_id:
        findings.append(
            Finding(
                "OPEN_WITH_CONTROL",
                "WARN",
                "OPEN con control_id; estado inconsistente",
                hid,
            )
        )

    # Ficha incompleta
    for field_name, value in (
        ("predicts", h.predicts),
        ("weakens_if", h.weakens_if),
        ("dies_if", h.dies_if),
        ("statement", h.statement),
    ):
        if not value or not str(value).strip():
            findings.append(
                Finding(
                    "INCOMPLETE_FICHA",
                    "FAIL",
                    f"Campo vacío: {field_name}",
                    hid,
                )
            )

    # Historial: reescritura de predicción post-resultado
    saw_result = False
    baseline_predicts = h.predicts
    for ev in h.history:
        if ev.get("event") == "result_recorded":
            saw_result = True
        if saw_result and ev.get("event") == "predicts_changed":
            findings.append(
                Finding(
                    "POST_RESULT_PREDICT_CHANGE",
                    "FAIL",
                    "La predicción cambió después del resultado",
                    hid,
                )
            )
        if saw_result and ev.get("event") == "predicts_attempt":
            findings.append(
                Finding(
                    "POST_RESULT_PREDICT_ATTEMPT",
                    "FAIL",
                    "Intento de reescribir predicción post-resultado registrado",
                    hid,
                )
            )

    # SOPORTADA exige control (doble check semántico)
    if state == HypothesisState.SOPORTADA_BAJO_CONTROL and not h.control_id:
        findings.append(
            Finding(
                "SUPPORT_WITHOUT_CONTROL",
                "FAIL",
                "SOPORTADA_BAJO_CONTROL sin control",
                hid,
            )
        )

    return findings


def audit_store(store: ProtocolStore) -> AuditReport:
    """Auditoría completa del registro del núcleo."""
    findings: List[Finding] = []
    hyps = store.all_hypotheses()
    events = _load_audit_log(store)

    for h in hyps:
        findings.extend(audit_hypothesis(h))

    # Eventos de rechazo esperados (informativos); violaciones si hubo DELETE success
    for ev in events:
        name = ev.get("event", "")
        if name == "CORRUPT_LOG_LINE":
            findings.append(
                Finding("CORRUPT_AUDIT_LOG", "FAIL", "Línea de audit log corrupta")
            )
        if name == "HYPOTHESIS_DELETED":
            findings.append(
                Finding(
                    "HYPOTHESIS_DELETED",
                    "FAIL",
                    f"Se registró borrado de hipótesis {ev.get('hypothesis_id')}",
                    ev.get("hypothesis_id"),
                )
            )
        if name == "PREDICT_REWRITTEN":
            findings.append(
                Finding(
                    "PREDICT_REWRITTEN",
                    "FAIL",
                    f"Se reescribió predicción post-hoc en {ev.get('hypothesis_id')}",
                    ev.get("hypothesis_id"),
                )
            )

    # Controles huérfanos / hipótesis con control_id inexistente
    controls = store._load(store._controls)
    for h in hyps:
        if h.control_id and h.control_id not in controls:
            findings.append(
                Finding(
                    "MISSING_CONTROL_RECORD",
                    "FAIL",
                    f"control_id {h.control_id} no está en el registro",
                    h.id,
                )
            )

    # NO_SABEMOS y MUERTA deben poder existir — no son FAIL
    # (solo se verifica que si existen, cumplan forma)

    fails = [f for f in findings if f.severity == "FAIL"]
    warns = [f for f in findings if f.severity == "WARN"]
    if fails:
        verdict = AuditVerdict.FAIL.value
    elif warns:
        verdict = AuditVerdict.WARN.value
    else:
        verdict = AuditVerdict.PASS.value

    return AuditReport(
        verdict=verdict,
        findings=findings,
        hypotheses_checked=len(hyps),
        audit_events_checked=len(events),
    )


def audit_path(data_root: Path) -> AuditReport:
    return audit_store(ProtocolStore(data_root))
