"""
Auditor CORE: vigila reglas, no matemáticas.
Casos A/B/C del diseño PASO 2.
"""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from athena_core.auditor import AuditVerdict, audit_store
from athena_core.protocol import (
    HypothesisState,
    ProtocolStore,
    attempt_update_predicts_after_result,
    create_hypothesis,
    create_question,
    force_corrupt_predicts_for_audit,
    force_delete_hypothesis_for_audit,
    record_result,
)


class AuditorCoreTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.store = ProtocolStore(Path(self._tmp.name))

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def _make_open(self):
        q = create_question("¿A difiere de B?", domain="toy", store=self.store)
        return create_hypothesis(
            q.id,
            "H toy",
            predicts="X ocurre",
            weakens_if="casi X",
            dies_if="Y ocurre",
            store=self.store,
        )

    def test_case_a_post_result_change_detected_fail(self):
        """Caso A: hipótesis/predicción cambia después del resultado → FAIL."""
        h = self._make_open()
        record_result(
            h.id,
            control_description="Control C",
            result_summary="Y",
            new_state=HypothesisState.DEBILITADA.value,
            store=self.store,
        )
        # Protocol rejects live rewrite
        with self.assertRaises(Exception):
            attempt_update_predicts_after_result(
                h.id, "predicción reescrita", store=self.store
            )
        # Corruption path: auditor must still FAIL
        force_corrupt_predicts_for_audit(
            h.id, "predicción corrupta", store=self.store
        )
        report = audit_store(self.store)
        self.assertEqual(report.verdict, AuditVerdict.FAIL.value)
        codes = {f.code for f in report.findings}
        self.assertTrue(
            "POST_RESULT_PREDICT_CHANGE" in codes
            or "PREDICT_REWRITTEN" in codes
            or "POST_RESULT_PREDICT_ATTEMPT" in codes
        )

    def test_case_b_no_sabemos_allowed_pass(self):
        """Caso B: resultado ambiguo → NO_SABEMOS permitido (PASS)."""
        h = self._make_open()
        record_result(
            h.id,
            control_description="Control C",
            result_summary="señal mixta",
            new_state=HypothesisState.NO_SABEMOS.value,
            store=self.store,
        )
        report = audit_store(self.store)
        self.assertEqual(report.verdict, AuditVerdict.PASS.value)
        self.assertEqual(report.hypotheses_checked, 1)

    def test_case_c_deleted_dead_detected_fail(self):
        """Caso C: hipótesis muerta eliminada → FAIL."""
        h = self._make_open()
        record_result(
            h.id,
            control_description="Control C",
            result_summary="murió",
            new_state=HypothesisState.MUERTA.value,
            death_reason="Y ocurrió",
            store=self.store,
        )
        force_delete_hypothesis_for_audit(h.id, store=self.store)
        report = audit_store(self.store)
        self.assertEqual(report.verdict, AuditVerdict.FAIL.value)
        codes = {f.code for f in report.findings}
        self.assertIn("HYPOTHESIS_DELETED", codes)

    def test_clean_dead_archived_pass(self):
        h = self._make_open()
        record_result(
            h.id,
            control_description="Control C",
            result_summary="murió",
            new_state=HypothesisState.MUERTA.value,
            death_reason="Y",
            store=self.store,
        )
        report = audit_store(self.store)
        self.assertEqual(report.verdict, AuditVerdict.PASS.value)


if __name__ == "__main__":
    unittest.main()
