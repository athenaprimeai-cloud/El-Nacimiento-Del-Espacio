import importlib
import sys
import unittest
from pathlib import Path


SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))


class Run006E74ReplayOnlyCaptureReproContractTests(unittest.TestCase):
    def test_authorized_phase_constants_match_006e73_and_user_authorization(self):
        module = importlib.import_module("run_006e74_replay_only_capture_repro")

        self.assertEqual(module.PHASE_ID, "006E74")
        self.assertEqual(module.MATRIX_ID, "006E74_REPLAY_ONLY_006E71_CAPTURE_REPRO")
        self.assertEqual(module.ARTIFACT_DIR.as_posix(), "artifacts/006E74-replay-only-006E71-capture-repro")
        self.assertEqual(module.PRECISIONS, [96, 128])
        self.assertEqual(module.EXPECTED_RECORDS, 90)
        self.assertEqual(module.EXPECTED_DIAGNOSTICS, 84)
        self.assertEqual(module.RESULT_FAIL_SCOPE, "006E74_FAIL_SCOPE_OR_SEMANTICS")

    def test_matrix_is_exact_replay_of_006e71_with_no_new_inputs(self):
        module = importlib.import_module("run_006e74_replay_only_capture_repro")
        source = importlib.import_module("run_006e71_narrow_smoke")

        self.assertEqual(len(module.MATRIX), 45)
        self.assertEqual(len(source.MATRIX), 45)

        replay_rows = [row for row in module.MATRIX if row["source"] == "replay_006E71"]
        new_rows = [row for row in module.MATRIX if row["source"] != "replay_006E71"]
        self.assertEqual(len(replay_rows), 45)
        self.assertEqual(new_rows, [])

        for replay_row, source_row in zip(module.MATRIX, source.MATRIX):
            expected = dict(source_row)
            expected["source"] = "replay_006E71"
            self.assertEqual(replay_row, expected)

    def test_diagnostic_pairs_replay_006e71_without_expanding_scope(self):
        module = importlib.import_module("run_006e74_replay_only_capture_repro")
        source = importlib.import_module("run_006e71_narrow_smoke")

        self.assertEqual(module.build_diagnostic_pairs(), source.build_diagnostic_pairs())
        self.assertEqual(len(module.build_diagnostic_pairs()), 42)
        self.assertEqual(
            [pair for pair in module.build_diagnostic_pairs() if pair[0] == "zepto_tight_to_yocto_tight_children"],
            [
                ("zepto_tight_to_yocto_tight_children", "LBOX_P1_C_ZEPTO", "LBOX_P1_C_YOCTO"),
                ("zepto_tight_to_yocto_tight_children", "LBOX_P2_C_ZEPTO", "LBOX_P2_C_YOCTO"),
                ("zepto_tight_to_yocto_tight_children", "LBOX_P3_C_ZEPTO", "LBOX_P3_C_YOCTO"),
            ],
        )


if __name__ == "__main__":
    unittest.main()
