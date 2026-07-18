"""PASO 2.5 — el kernel debe caber investigaciones reales sin reglas nuevas."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from scripts.validate_athena_kernel import run


class KernelValidationTests(unittest.TestCase):
    def test_kernel_validation_pass(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = run(Path(tmp))
        self.assertEqual(out["kernel_validation"], "PASS")
        self.assertTrue(out["all_cases_fit"])
        self.assertEqual(out["auditor_verdict"], "PASS")
        self.assertFalse(out["new_protocol_rules_added"])
        self.assertEqual(len(out["cases"]), 6)


if __name__ == "__main__":
    unittest.main()
