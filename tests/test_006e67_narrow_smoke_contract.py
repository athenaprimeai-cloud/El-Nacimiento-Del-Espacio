import importlib
import sys
import unittest
from pathlib import Path


SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))


class Run006E67NarrowSmokeContractTests(unittest.TestCase):
    def test_authorized_phase_constants_match_006e66(self):
        module = importlib.import_module("run_006e67_narrow_smoke")

        self.assertEqual(module.PHASE_ID, "006E67")
        self.assertEqual(module.MATRIX_ID, "006E67_REPLAY_PLUS_CENTER_ZEPTO_TIGHT")
        self.assertEqual(module.ARTIFACT_DIR.as_posix(), "artifacts/006E67-next-narrow-fixed-semantic-ledger")
        self.assertEqual(module.PRECISIONS, [96, 128])
        self.assertEqual(module.EXPECTED_RECORDS, 84)
        self.assertEqual(module.EXPECTED_DIAGNOSTICS, 78)
        self.assertEqual(module.RESULT_FAIL_SCOPE, "006E67_FAIL_SCOPE_OR_SEMANTICS")

    def test_matrix_extends_006e63_with_three_zepto_boxes_only(self):
        module = importlib.import_module("run_006e67_narrow_smoke")

        self.assertEqual(len(module.MATRIX), 42)
        replay_rows = [row for row in module.MATRIX if row["source"] == "replay_006E63"]
        zepto_rows = [row for row in module.MATRIX if row["source"] == "new_006E67"]

        self.assertEqual(len(replay_rows), 39)
        self.assertEqual(len(zepto_rows), 3)
        self.assertEqual(
            {(row["label"], row["parent"], row["real_radius"], row["imag_radius"]) for row in zepto_rows},
            {
                ("LBOX_P1_C_ZEPTO", "LBOX_P1_C_ATTO", "1/1024000", "1/2048000"),
                ("LBOX_P2_C_ZEPTO", "LBOX_P2_C_ATTO", "1/2048000", "1/1024000"),
                ("LBOX_P3_C_ZEPTO", "LBOX_P3_C_ATTO", "1/1536000", "1/1536000"),
            },
        )

    def test_diagnostic_pairs_include_atto_to_zepto_without_expanding_scope(self):
        module = importlib.import_module("run_006e67_narrow_smoke")

        pairs = module.build_diagnostic_pairs()

        self.assertEqual(len(pairs), 39)
        self.assertEqual(
            [pair for pair in pairs if pair[0] == "atto_tight_to_zepto_tight_children"],
            [
                ("atto_tight_to_zepto_tight_children", "LBOX_P1_C_ATTO", "LBOX_P1_C_ZEPTO"),
                ("atto_tight_to_zepto_tight_children", "LBOX_P2_C_ATTO", "LBOX_P2_C_ZEPTO"),
                ("atto_tight_to_zepto_tight_children", "LBOX_P3_C_ATTO", "LBOX_P3_C_ZEPTO"),
            ],
        )


if __name__ == "__main__":
    unittest.main()
