"""
FT-CORE: intentar romper el protocolo, no demostrar matemáticas.
"""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from athena_core.protocol import (
    HypothesisState,
    ProtocolError,
    ProtocolStore,
    attempt_delete_hypothesis,
    attempt_update_predicts_after_result,
    create_hypothesis,
    create_question,
    get_hypothesis,
    record_result,
)


class CoreProtocolTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.store = ProtocolStore(Path(self._tmp.name))

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def _open_h(self):
        q = create_question(
            "¿Existe diferencia medible entre A y B?",
            domain="toy",
            store=self.store,
        )
        h = create_hypothesis(
            q.id,
            "H: A y B difieren en métrica M",
            predicts="Si H, |M(A)-M(B)| > 0.1 bajo control C",
            weakens_if="Diferencia < 0.1 pero > 0",
            dies_if="Diferencia ≈ 0 bajo el mismo control C",
            store=self.store,
        )
        return h

    def test_happy_path_muerta_archived(self):
        h = self._open_h()
        h2 = record_result(
            h.id,
            control_description="Control C: misma malla, A vs B",
            result_summary="Diferencia ≈ 0",
            new_state=HypothesisState.MUERTA.value,
            death_reason="Ocurrió dies_if: diferencia nula",
            store=self.store,
        )
        self.assertEqual(h2.state, HypothesisState.MUERTA.value)
        self.assertIsNotNone(h2.control_id)
        self.assertIsNotNone(h2.death_reason)
        # still in store
        again = get_hypothesis(h.id, self.store)
        self.assertEqual(again.state, HypothesisState.MUERTA.value)

    def test_no_sabemos_is_first_class(self):
        h = self._open_h()
        h2 = record_result(
            h.id,
            control_description="Control C",
            result_summary="Señal mixta",
            new_state=HypothesisState.NO_SABEMOS.value,
            store=self.store,
        )
        self.assertEqual(h2.state, HypothesisState.NO_SABEMOS.value)

    def test_ft_core_01_reject_predict_change_after_result(self):
        h = self._open_h()
        record_result(
            h.id,
            control_description="Control C",
            result_summary="ok",
            new_state=HypothesisState.DEBILITADA.value,
            store=self.store,
        )
        with self.assertRaises(ProtocolError) as ctx:
            attempt_update_predicts_after_result(
                h.id, "nueva predicción post-hoc", store=self.store
            )
        self.assertEqual(ctx.exception.code, "FT-CORE-01")

    def test_ft_core_02_reject_delete_dead(self):
        h = self._open_h()
        record_result(
            h.id,
            control_description="Control C",
            result_summary="murió",
            new_state=HypothesisState.MUERTA.value,
            death_reason="dies_if",
            store=self.store,
        )
        with self.assertRaises(ProtocolError) as ctx:
            attempt_delete_hypothesis(h.id, store=self.store)
        self.assertEqual(ctx.exception.code, "FT-CORE-02")
        # still exists
        self.assertEqual(
            get_hypothesis(h.id, self.store).state, HypothesisState.MUERTA.value
        )

    def test_ft_core_03_block_close_without_control(self):
        h = self._open_h()
        with self.assertRaises(ProtocolError) as ctx:
            record_result(
                h.id,
                control_description="   ",
                result_summary="algo",
                new_state=HypothesisState.SOPORTADA_BAJO_CONTROL.value,
                store=self.store,
            )
        self.assertEqual(ctx.exception.code, "FT-CORE-03")
        # still OPEN
        self.assertEqual(
            get_hypothesis(h.id, self.store).state, HypothesisState.OPEN.value
        )

    def test_muerta_requires_death_reason(self):
        h = self._open_h()
        with self.assertRaises(ProtocolError) as ctx:
            record_result(
                h.id,
                control_description="Control C",
                result_summary="murió",
                new_state=HypothesisState.MUERTA.value,
                death_reason=None,
                store=self.store,
            )
        self.assertEqual(ctx.exception.code, "DEATH_REASON_REQUIRED")


if __name__ == "__main__":
    unittest.main()
