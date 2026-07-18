"""
ATHENA CORE PROTOCOL — PASO 1
Árbitro de disciplina. Sin IA. Sin agentes. Sin descubrimiento.
"""

from .auditor import AuditReport, AuditVerdict, audit_store
from .protocol import (
    HypothesisState,
    ProtocolError,
    ProtocolStore,
    attempt_delete_hypothesis,
    attempt_update_predicts_after_result,
    create_hypothesis,
    create_question,
    finalize_hypothesis,
    get_hypothesis,
    list_hypotheses,
    record_result,
)

__all__ = [
    "AuditReport",
    "AuditVerdict",
    "HypothesisState",
    "ProtocolError",
    "ProtocolStore",
    "attempt_delete_hypothesis",
    "attempt_update_predicts_after_result",
    "audit_store",
    "create_hypothesis",
    "create_question",
    "finalize_hypothesis",
    "get_hypothesis",
    "list_hypotheses",
    "record_result",
]

__version__ = "0.1.0"
