from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNNER = ROOT / "scripts" / "run_006h14_tiny_semantic_smoke.py"
ARTIFACT_DIR = ROOT / "artifacts" / "006H14-tiny-semantic-smoke"
EXPECTED_RUNTIME = r"C:\Users\johnn\AppData\Local\Temp\athena-006e20r\Scripts\python.exe"
EXPECTED_PRECISIONS = [192, 256]
REQUIRED_ARTIFACTS = {
    "006H14_CALL_LEDGER.json",
    "006H14_RUNTIME_SEAL.json",
    "006H14_RESULTS.json",
    "006H14_SHA256SUMS.txt",
}
FORBIDDEN_HEIGHTS = ("143", "200", "300", "500")
FORBIDDEN_TOKENS = (
    "Lambda_3",
    "build_frozen_l3_contour",
    "certify_l3",
    "l3_box_winding_count",
    "zero_isolat",
    "zero_count",
    "requests",
    "urllib",
    "pip install",
    "numpy",
    "mpmath",
    "float(",
)


def _json(path: Path):
    if not path.is_file():
        raise AssertionError(f"required artifact is missing: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def _sha256(path: Path) -> str:
    if not path.is_file():
        raise AssertionError(f"required artifact is missing: {path}")
    return hashlib.sha256(path.read_bytes()).hexdigest()


class TinySemanticSmokeContractTests(unittest.TestCase):
    def test_runner_and_artifacts_exist(self):
        self.assertTrue(RUNNER.is_file())
        self.assertTrue(ARTIFACT_DIR.is_dir())
        self.assertEqual(
            REQUIRED_ARTIFACTS,
            {path.name for path in ARTIFACT_DIR.iterdir() if path.is_file()},
        )

    def test_runtime_precision_budgets_and_scope_flags(self):
        results = _json(ARTIFACT_DIR / "006H14_RESULTS.json")
        seal = _json(ARTIFACT_DIR / "006H14_RUNTIME_SEAL.json")
        ledger = _json(ARTIFACT_DIR / "006H14_CALL_LEDGER.json")

        self.assertEqual(seal["python_executable"], EXPECTED_RUNTIME)
        self.assertEqual(results["precision_bits"], EXPECTED_PRECISIONS)
        self.assertTrue(results["runtime_hashes_verified"])
        self.assertLessEqual(results["call_counts"]["native_dirichlet_l"], 4)
        self.assertLessEqual(results["call_counts"]["hurwitz_candidate_zeta"], 6)
        self.assertLessEqual(results["call_counts"]["gamma"], 4)
        self.assertLessEqual(results["call_counts"]["log"], 6)
        self.assertLessEqual(results["call_counts"]["exp"], 4)
        self.assertLessEqual(results["call_counts"]["pi"], 2)

        for value in results["scope_flags"].values():
            if isinstance(value, bool):
                self.assertIn(value, (True, False))
        self.assertTrue(results["scope_flags"]["FLINT_IMPORTED"])
        self.assertFalse(results["scope_flags"]["CHI_L_FUNCTION_CALLED"])
        self.assertFalse(results["scope_flags"]["LAMBDA_3_EVALUATED"])
        self.assertFalse(results["scope_flags"]["CONTOURS_EXECUTED"])
        self.assertFalse(results["scope_flags"]["ZEROS_ISOLATED"])
        self.assertFalse(results["scope_flags"]["ZEROS_COUNTED"])
        self.assertFalse(results["scope_flags"]["NETWORK_USED"])
        self.assertFalse(results["scope_flags"]["DEPENDENCIES_INSTALLED"])
        self.assertFalse(results["scope_flags"]["H2_OPENED"])
        self.assertFalse(results["scope_flags"]["006F_OPENED"])
        self.assertTrue(ledger)

    def test_artifact_hashes_match(self):
        self.assertTrue((ARTIFACT_DIR / "006H14_SHA256SUMS.txt").is_file())
        sums = (ARTIFACT_DIR / "006H14_SHA256SUMS.txt").read_text(encoding="utf-8").splitlines()
        observed = {}
        for line in sums:
            digest, name = line.split("  ", 1)
            observed[name] = digest
        self.assertEqual(REQUIRED_ARTIFACTS - {"006H14_SHA256SUMS.txt"}, set(observed))
        for name, digest in observed.items():
            self.assertEqual(_sha256(ARTIFACT_DIR / name), digest)

    def test_runner_static_scope(self):
        self.assertTrue(RUNNER.is_file())
        source = RUNNER.read_text(encoding="utf-8")
        for token in FORBIDDEN_TOKENS:
            self.assertNotIn(token, source)
        for height in FORBIDDEN_HEIGHTS:
            self.assertNotIn(f'"{height}"', source)
        self.assertIn(EXPECTED_RUNTIME, source)
        self.assertIn("PRECISION_BITS = (192, 256)", source)


if __name__ == "__main__":
    unittest.main()
