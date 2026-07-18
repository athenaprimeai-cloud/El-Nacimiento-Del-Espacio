"""Meta-eval: process metrics M1 vs M2."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from athena_core.meta_eval import compare_modes
from athena_core.protocol import ProtocolStore


class MetaEvalTests(unittest.TestCase):
    def test_m2_reduces_budget(self):
        dirs = []

        def factory() -> ProtocolStore:
            d = Path(tempfile.mkdtemp())
            dirs.append(d)
            return ProtocolStore(d)

        out = compare_modes(n_candidates=50, store_factory=factory)
        self.assertTrue(out["comparison"]["posthoc_clean"])
        m1 = out["modes"]["M1"]
        m2 = out["modes"]["M2"]
        self.assertEqual(m1["auditor_verdict"], "PASS")
        self.assertEqual(m2["auditor_verdict"], "PASS")
        # Selector should propose fewer attacks than all OPEN
        self.assertLess(m2["budget_units"], m1["budget_units"])
        self.assertTrue(out["comparison"]["m2_improves_experiment_economy"])


if __name__ == "__main__":
    unittest.main()
