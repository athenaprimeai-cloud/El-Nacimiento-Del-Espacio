"""PASO 3 — éxito = presión absorbida, no idea brillante."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from athena_core.auditor import audit_store
from athena_core.explorer import explore_pressure
from athena_core.protocol import ProtocolStore


class ExplorerPressureTests(unittest.TestCase):
    def test_kernel_survives_noise(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = ProtocolStore(Path(tmp))
            report = explore_pressure(
                "¿Pregunta de presión?",
                n_candidates=50,
                store=store,
            )
            audit = audit_store(store)
        self.assertEqual(report.n_requested, 50)
        self.assertGreater(report.n_rejected, report.n_accepted)
        self.assertEqual(audit.verdict, "PASS")
        self.assertGreater(report.n_accepted, 0)  # some well-formed get in


if __name__ == "__main__":
    unittest.main()
