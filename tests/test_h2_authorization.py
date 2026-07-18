import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from athena_azr.h2_zero_certifier.authorization import (
    ExecutionNotAuthorized,
    RUNTIME_CODE_FILES,
    require_execution_authorization,
)


class H2ProbativeInventoryTests(unittest.TestCase):
    def test_probative_inventory_excludes_float_synthetic_module(self):
        from athena_azr.h2_zero_certifier.authorization import (
            PROBATIVE_RUNTIME_CODE_FILES,
            SYNTHETIC_TEST_ONLY_FILES,
        )
        self.assertNotIn(
            "athena_azr/h2_zero_certifier/argument_principle.py",
            PROBATIVE_RUNTIME_CODE_FILES,
        )
        self.assertIn(
            "athena_azr/h2_zero_certifier/argument_principle.py",
            SYNTHETIC_TEST_ONLY_FILES,
        )
        self.assertIn(
            "athena_azr/h2_zero_certifier/real_evidence.py",
            PROBATIVE_RUNTIME_CODE_FILES,
        )


PLAN_HASH = "c" * 64
PROTOCOL_HASH = "4f110d0926067e9e1eb44cbbfe78ee1acc93f85f526176c81d98446eafd492cb"
SPEC_006E2_HASH = "4b14ba44d08d80941a4ab69776c41479453f0f08661ffec9fcb304204f1212c5"
PLAN_006E3_HASH = "4b7a277e939fab39ac6a9ce95cfe771944964a90a37dab12d005908ab849e931"
REVIEW_HASHES = {
    "plan_006e7_sha256": "7" * 64,
    "report_006e8_sha256": "8" * 64,
    "review_006e9_sha256": "9" * 64,
    "corrections_006e10_sha256": "a" * 64,
}


def authorization_payload(output_dir: Path) -> dict:
    return {
        "experiment_id": "G5B-006F",
        "execution_authorized": True,
        "max_height": 500,
        "requested_heights": [143, 200, 300, 500],
        "protocol_006b_sha256": PROTOCOL_HASH,
        "plan_006c_sha256": PLAN_HASH,
        "spec_006e2_sha256": SPEC_006E2_HASH,
        "plan_006e3_sha256": PLAN_006E3_HASH,
        "approved_code_hashes": {"module.py": hashlib.sha256(b"code").hexdigest()},
        "output_directory": str(output_dir),
        **REVIEW_HASHES,
    }


def post_006e7_authorization_payload(output_dir: Path) -> dict:
    return authorization_payload(output_dir)


class H2AuthorizationTests(unittest.TestCase):
    def test_post_006e7_review_chain_is_required_and_validated(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            output = root / "output"
            (root / "module.py").write_bytes(b"code")
            path = root / "authorization.json"
            path.write_text(
                json.dumps(post_006e7_authorization_payload(output)),
                encoding="utf-8",
            )

            authorization = require_execution_authorization(
                path,
                expected_protocol_hash=PROTOCOL_HASH,
                expected_plan_hash=PLAN_HASH,
                expected_spec_hash=SPEC_006E2_HASH,
                expected_inert_plan_hash=PLAN_006E3_HASH,
                expected_review_hashes=REVIEW_HASHES,
                expected_output_dir=output,
                code_root=root,
            )

            self.assertEqual(authorization.review_chain_hashes, REVIEW_HASHES)

    def test_runtime_inventory_contains_all_inert_argument_modules(self):
        self.assertTrue(
            {
                "athena_azr/h2_zero_certifier/completed_l3.py",
                "athena_azr/h2_zero_certifier/contour.py",
                "athena_azr/h2_zero_certifier/ball_argument.py",
                "athena_azr/h2_zero_certifier/l3_argument_count.py",
            }.issubset(RUNTIME_CODE_FILES)
        )

    def test_missing_authorization_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(ExecutionNotAuthorized):
                require_execution_authorization(
                    Path(directory) / "missing.json",
                    expected_protocol_hash=PROTOCOL_HASH,
                    expected_plan_hash=PLAN_HASH,
                    expected_spec_hash=SPEC_006E2_HASH,
                    expected_inert_plan_hash=PLAN_006E3_HASH,
                    expected_review_hashes=REVIEW_HASHES,
                    expected_output_dir=Path(directory) / "output",
                    code_root=Path(directory),
                )

    def test_false_or_extra_fields_are_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            output = root / "output"
            payload = authorization_payload(output)
            payload["execution_authorized"] = False
            payload["unexpected"] = True
            path = root / "authorization.json"
            path.write_text(json.dumps(payload), encoding="utf-8")

            with self.assertRaises(ExecutionNotAuthorized):
                require_execution_authorization(
                    path,
                    expected_protocol_hash=PROTOCOL_HASH,
                    expected_plan_hash=PLAN_HASH,
                    expected_spec_hash=SPEC_006E2_HASH,
                    expected_inert_plan_hash=PLAN_006E3_HASH,
                    expected_review_hashes=REVIEW_HASHES,
                    expected_output_dir=output,
                    code_root=root,
                )

    def test_valid_authorization_is_immutable_and_normalized(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            output = root / "output"
            (root / "module.py").write_bytes(b"code")
            path = root / "authorization.json"
            path.write_text(json.dumps(authorization_payload(output)), encoding="utf-8")

            authorization = require_execution_authorization(
                path,
                expected_protocol_hash=PROTOCOL_HASH,
                expected_plan_hash=PLAN_HASH,
                expected_spec_hash=SPEC_006E2_HASH,
                expected_inert_plan_hash=PLAN_006E3_HASH,
                expected_review_hashes=REVIEW_HASHES,
                expected_output_dir=output,
                code_root=root,
            )

            self.assertTrue(authorization.execution_authorized)
            self.assertEqual(authorization.requested_heights, (143, 200, 300, 500))
            with self.assertRaises(TypeError):
                authorization.approved_code_hashes["other.py"] = "bad"

    def test_tampered_approved_code_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            output = root / "output"
            (root / "module.py").write_bytes(b"tampered")
            path = root / "authorization.json"
            path.write_text(json.dumps(authorization_payload(output)), encoding="utf-8")

            with self.assertRaises(ExecutionNotAuthorized):
                require_execution_authorization(
                    path,
                    expected_protocol_hash=PROTOCOL_HASH,
                    expected_plan_hash=PLAN_HASH,
                    expected_spec_hash=SPEC_006E2_HASH,
                    expected_inert_plan_hash=PLAN_006E3_HASH,
                    expected_review_hashes=REVIEW_HASHES,
                    expected_output_dir=output,
                    code_root=root,
                )

    def test_missing_required_runtime_hash_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            output = root / "output"
            (root / "module.py").write_bytes(b"code")
            path = root / "authorization.json"
            path.write_text(json.dumps(authorization_payload(output)), encoding="utf-8")

            with self.assertRaises(ExecutionNotAuthorized):
                require_execution_authorization(
                    path,
                    expected_protocol_hash=PROTOCOL_HASH,
                    expected_plan_hash=PLAN_HASH,
                    expected_spec_hash=SPEC_006E2_HASH,
                    expected_inert_plan_hash=PLAN_006E3_HASH,
                    expected_review_hashes=REVIEW_HASHES,
                    expected_output_dir=output,
                    code_root=root,
                    required_code_files=("module.py", "other.py"),
                )


if __name__ == "__main__":
    unittest.main()
