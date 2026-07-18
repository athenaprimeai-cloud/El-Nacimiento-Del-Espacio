import builtins
import sys
import tempfile
import unittest
from dataclasses import replace
from pathlib import Path
from unittest.mock import patch

from athena_azr.h2_zero_certifier.authorization import (
    ExecutionAuthorization,
    ExecutionNotAuthorized,
)
from athena_azr.h2_zero_certifier.pipeline import expected_output_path, run_certification_pipeline
from athena_azr.h2_zero_certifier.pipeline import require_probative_evidence
from athena_azr.h2_zero_certifier.python_flint_backend import PythonFlintBackend
from athena_azr.h2_zero_certifier.real_evidence import (
    ComplexBallRecord,
    InvalidRealEvidence,
    RealEvidenceFactory,
)
from scripts.run_h2_zero_certification import main
from tests.h2_test_support import validated_test_authorization


class H2PipelineGuardTests(unittest.TestCase):
    def test_pipeline_accepts_only_validated_authorization_evidence(self):
        factory = RealEvidenceFactory.from_authorization(
            validated_test_authorization(),
            backend_id="authorized-fake-runtime",
        )
        evidence = factory.completed_l3_point(
            ComplexBallRecord("1", "2", "3", "4"),
            precision_bits=192,
        )
        self.assertIs(require_probative_evidence(evidence), evidence)

    def test_pipeline_rejects_real_evidence_from_unvalidated_factory(self):
        factory = RealEvidenceFactory("forged", "a" * 64, "b" * 64)
        evidence = factory.completed_l3_point(
            ComplexBallRecord("1", "2", "3", "4"),
            precision_bits=192,
        )
        with self.assertRaises(InvalidRealEvidence):
            require_probative_evidence(evidence)

    def test_unvalidated_factory_cannot_promote_itself_to_probative(self):
        factory = RealEvidenceFactory("forged", "a" * 64, "b" * 64)
        factory.probative = True
        factory.review_chain_digest = "c" * 64
        evidence = factory.completed_l3_point(
            ComplexBallRecord("1", "2", "3", "4"),
            precision_bits=192,
        )
        with self.assertRaises(InvalidRealEvidence):
            require_probative_evidence(evidence)

    def test_pipeline_rejects_synthetic_evidence(self):
        from athena_azr.h2_zero_certifier.models import RealInterval
        with self.assertRaises(InvalidRealEvidence):
            require_probative_evidence(RealInterval("0", "1"))

    def test_dataclasses_replace_cannot_inject_non_probative_ancestor(self):
        trusted = RealEvidenceFactory.from_authorization(
            validated_test_authorization(),
            backend_id="sealed-backend",
        )
        trusted_segment = trusted.segment_image(
            value=ComplexBallRecord("1", "2", "3", "4"),
            segment_id="trusted-segment",
            precision_bits=192,
        )
        trusted_half_plane = trusted.half_plane(
            segment=trusted_segment,
            rotation_real="1",
            rotation_imag="0",
            rotated_real_lower="1",
        )

        forged = RealEvidenceFactory(
            trusted_segment.backend_id,
            trusted_segment.authorization_digest,
            trusted_segment.runtime_code_digest,
        )
        bad_segment = forged.segment_image(
            value=ComplexBallRecord("1", "2", "3", "4"),
            segment_id="bad-segment",
            precision_bits=192,
        )
        with self.assertRaises(InvalidRealEvidence):
            replace(
                trusted_half_plane,
                segment=bad_segment,
                parent_evidence_hashes=(bad_segment.digest,),
            )

    def test_execution_authorization_cannot_be_constructed_without_parser_validation(self):
        with self.assertRaises(ExecutionNotAuthorized):
            ExecutionAuthorization(
                experiment_id="G5B-006F",
                execution_authorized=True,
                max_height=500,
                requested_heights=(143, 200, 300, 500),
                protocol_006b_sha256="a" * 64,
                plan_006c_sha256="b" * 64,
                spec_006e2_sha256="c" * 64,
                plan_006e3_sha256="d" * 64,
                approved_code_hashes={"module.py": "e" * 64},
                review_chain_hashes={
                    "plan_006e7_sha256": "7" * 64,
                    "report_006e8_sha256": "8" * 64,
                    "review_006e9_sha256": "9" * 64,
                    "corrections_006e10_sha256": "a" * 64,
                },
                output_directory=Path("artifacts"),
                source_digest="f" * 64,
            )

    def test_backend_construction_does_not_import_flint(self):
        sys.modules.pop("flint", None)
        real_import = builtins.__import__

        def guarded_import(name, *args, **kwargs):
            if name == "flint" or name.startswith("flint."):
                raise AssertionError("FLINT import attempted")
            return real_import(name, *args, **kwargs)

        with patch("builtins.__import__", side_effect=guarded_import):
            backend = PythonFlintBackend()

        self.assertFalse(backend.initialized)
        self.assertNotIn("flint", sys.modules)

    def test_backend_initialize_requires_validated_authorization(self):
        backend = PythonFlintBackend()

        with self.assertRaises(ExecutionNotAuthorized):
            backend.initialize(authorization=object())

        self.assertNotIn("flint", sys.modules)

    def test_pipeline_rejects_before_backend_factory_or_output_creation(self):
        calls = []

        def backend_factory():
            calls.append("called")
            return object()

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            output = root / "artifacts" / "goldbach_cesaro" / "c03b_h2_zero_certification"

            with self.assertRaises(ExecutionNotAuthorized):
                run_certification_pipeline(
                    authorization_path=root / "missing.json",
                    output_dir=output,
                    backend_factory=backend_factory,
                    expected_plan_hash="c" * 64,
                )

            self.assertEqual(calls, [])
            self.assertFalse(output.exists())

    def test_pipeline_rejects_a_noncanonical_output_directory(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.assertEqual(
                expected_output_path(root),
                root / "artifacts" / "goldbach_cesaro" / "c03b_h2_zero_certification",
            )
            with self.assertRaises(ExecutionNotAuthorized):
                run_certification_pipeline(
                    authorization_path=root / "missing.json",
                    output_dir=root / "other-output",
                    backend_factory=lambda: object(),
                    expected_plan_hash="c" * 64,
                    code_root=root,
                )

    def test_cli_dry_validation_does_not_import_flint_or_create_output(self):
        sys.modules.pop("flint", None)
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "output"
            exit_code = main(["--dry-validate-config", "--output-dir", str(output)])

            self.assertEqual(exit_code, 0)
            self.assertFalse(output.exists())
            self.assertNotIn("flint", sys.modules)

    def test_cli_without_authorization_fails_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            output = root / "output"
            exit_code = main(
                [
                    "--authorization",
                    str(root / "missing.json"),
                    "--output-dir",
                    str(output),
                ]
            )

            self.assertEqual(exit_code, 2)
            self.assertFalse(output.exists())


if __name__ == "__main__":
    unittest.main()
