import importlib
import sys
import unittest
from pathlib import Path


SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))


class Run006E71NarrowSmokeContractTests(unittest.TestCase):
    def test_authorized_phase_constants_match_006e70(self):
        module = importlib.import_module("run_006e71_narrow_smoke")

        self.assertEqual(module.PHASE_ID, "006E71")
        self.assertEqual(module.MATRIX_ID, "006E71_REPLAY_PLUS_CENTER_YOCTO_TIGHT")
        self.assertEqual(module.ARTIFACT_DIR.as_posix(), "artifacts/006E71-next-narrow-fixed-semantic-ledger")
        self.assertEqual(module.PRECISIONS, [96, 128])
        self.assertEqual(module.EXPECTED_RECORDS, 90)
        self.assertEqual(module.EXPECTED_DIAGNOSTICS, 84)
        self.assertEqual(module.RESULT_FAIL_SCOPE, "006E71_FAIL_SCOPE_OR_SEMANTICS")

    def test_matrix_extends_006e67_with_three_yocto_boxes_only(self):
        module = importlib.import_module("run_006e71_narrow_smoke")

        self.assertEqual(len(module.MATRIX), 45)
        replay_rows = [row for row in module.MATRIX if row["source"] == "replay_006E67"]
        yocto_rows = [row for row in module.MATRIX if row["source"] == "new_006E71"]

        self.assertEqual(len(replay_rows), 42)
        self.assertEqual(len(yocto_rows), 3)
        self.assertEqual(
            {
                (
                    row["label"],
                    row["block"],
                    row["parent"],
                    row["real_mid"],
                    row["real_radius"],
                    row["imag_mid"],
                    row["imag_radius"],
                )
                for row in yocto_rows
            },
            {
                ("LBOX_P1_C_YOCTO", "CENTER_YOCTO_TIGHT", "LBOX_P1_C_ZEPTO", "1/2", "1/2048000", "7/5", "1/4096000"),
                ("LBOX_P2_C_YOCTO", "CENTER_YOCTO_TIGHT", "LBOX_P2_C_ZEPTO", "3/4", "1/4096000", "2/1", "1/2048000"),
                ("LBOX_P3_C_YOCTO", "CENTER_YOCTO_TIGHT", "LBOX_P3_C_ZEPTO", "1/3", "1/3072000", "5/3", "1/3072000"),
            },
        )

    def test_diagnostic_pairs_include_zepto_to_yocto_without_expanding_scope(self):
        module = importlib.import_module("run_006e71_narrow_smoke")

        pairs = module.build_diagnostic_pairs()

        self.assertEqual(len(pairs), 42)
        self.assertEqual(
            [pair for pair in pairs if pair[0] == "zepto_tight_to_yocto_tight_children"],
            [
                ("zepto_tight_to_yocto_tight_children", "LBOX_P1_C_ZEPTO", "LBOX_P1_C_YOCTO"),
                ("zepto_tight_to_yocto_tight_children", "LBOX_P2_C_ZEPTO", "LBOX_P2_C_YOCTO"),
                ("zepto_tight_to_yocto_tight_children", "LBOX_P3_C_ZEPTO", "LBOX_P3_C_YOCTO"),
            ],
        )


if __name__ == "__main__":
    unittest.main()
