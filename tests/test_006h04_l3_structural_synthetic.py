import importlib
import importlib.util
import tempfile
import unittest
from decimal import Decimal
from pathlib import Path

from athena_azr.h2_zero_certifier.chi3_function import (
    CHI3_METADATA,
    completed_l3_formula,
    validate_chi3_metadata,
)
from athena_azr.h2_zero_certifier.models import (
    CountCertificate,
    RealInterval,
    SegmentImageCertificate,
)


def require_module(testcase: unittest.TestCase, name: str):
    testcase.assertIsNotNone(importlib.util.find_spec(name), f"{name} must exist")
    return importlib.import_module(name)


class SegmentBackend:
    def __init__(self, *, contains_zero=False):
        self.contains_zero = contains_zero
        self.segments = []

    def completed_l3_segment(self, segment, precision_bits):
        self.segments.append((segment, precision_bits))
        if self.contains_zero:
            real = RealInterval("-1", "1")
            imag = RealInterval("-1", "1")
        else:
            real = RealInterval("2", "3")
            imag = RealInterval("4", "5")
        return SegmentImageCertificate(
            segment=segment,
            enclosure_real=real,
            enclosure_imag=imag,
            entire_segment_covered=True,
            arithmetic="rigorous_ball",
        )


class H006H04L3StructuralSyntheticTests(unittest.TestCase):
    def test_chi3_metadata_is_the_006h02_identity(self):
        expected = {
            "modulus": "3",
            "conductor": "3",
            "number": "2",
            "conrey_index": "2",
            "character_type": "primitive_real_nonprincipal",
            "primitive": "true",
            "real": "true",
            "principal": "false",
            "parity": "1",
            "parity_name": "odd",
            "root_number_epsilon": "1",
            "chi_3(1)": "1",
            "chi_3(2)": "-1",
            "chi_3(n_mod_0)": "0",
        }
        self.assertTrue(expected.items() <= CHI3_METADATA.items())
        self.assertIn("Gamma((s+1)/2)", completed_l3_formula())
        validate_chi3_metadata(CHI3_METADATA)
        incomplete = dict(CHI3_METADATA)
        incomplete.pop("root_number_epsilon")
        with self.assertRaises(ValueError):
            validate_chi3_metadata(incomplete)

    def test_frozen_contours_reject_t_star_and_unknown_heights(self):
        contour_module = require_module(self, "athena_azr.h2_zero_certifier.contour")

        contours = contour_module.build_frozen_l3_contours()

        self.assertEqual(tuple(contours), (143, 200, 300, 500))
        contour_143 = contours[143]
        self.assertEqual(contour_143.orientation, "positive")
        self.assertEqual(contour_143.segments[0].start.real, "-0.5")
        self.assertEqual(contour_143.segments[0].start.imag, "0")
        self.assertEqual(contour_143.segments[2].start.imag, "143")
        with self.assertRaises(ValueError):
            contour_module.build_frozen_l3_contour(144)
        with self.assertRaises(ValueError):
            contour_module.build_frozen_l3_contour(143, boundary_mode="T_star")
        with self.assertRaises(ValueError):
            contour_module.build_frozen_l3_contour(143, allow_t_star=True)

    def test_boundary_certifier_covers_segments_and_rejects_zero_images(self):
        contour_module = require_module(self, "athena_azr.h2_zero_certifier.contour")
        boundary = require_module(self, "athena_azr.h2_zero_certifier.boundary_certifier")
        segment = contour_module.build_frozen_l3_contour(143).segments[0]

        cover = boundary.subdivide_segment_cover(segment, depth=2)

        self.assertEqual(len(cover), 4)
        self.assertEqual(cover[0].segment.start, segment.start)
        self.assertEqual(cover[-1].segment.end, segment.end)
        for left, right in zip(cover, cover[1:]):
            self.assertEqual(left.segment.end, right.segment.start)

        cert = boundary.certify_boundary_segment(
            SegmentBackend(), segment, precision_bits=192, max_depth=0
        )
        self.assertTrue(cert.zero_excluded)
        self.assertEqual(cert.subdivision_count, 1)
        with self.assertRaises(boundary.InconclusiveBoundaryCertification):
            boundary.certify_boundary_segment(
                SegmentBackend(contains_zero=True),
                segment,
                precision_bits=192,
                max_depth=0,
            )

    def test_argument_increment_sums_only_matching_provenance(self):
        argument = require_module(self, "athena_azr.h2_zero_certifier.argument_increment")

        provenance = {"backend_id": "synthetic", "authorization_digest": "a" * 64}
        first = argument.ArgumentIncrementInterval("seg-1", "0.49", "0.51", 192, provenance)
        second = argument.ArgumentIncrementInterval("seg-2", "0.49", "0.51", 192, provenance)
        total = argument.sum_argument_intervals((first, second), contour_id="C_143")

        self.assertEqual(total.lower, "0.98")
        self.assertEqual(total.upper, "1.02")
        with self.assertRaises(argument.InconclusiveArgumentIncrement):
            argument.sum_argument_intervals(
                (
                    first,
                    argument.ArgumentIncrementInterval(
                        "seg-3",
                        "0",
                        "1",
                        256,
                        provenance,
                    ),
                ),
                contour_id="C_143",
            )
        with self.assertRaises(argument.InconclusiveArgumentIncrement):
            argument.ArgumentIncrementInterval("", "0", "1", 192)

    def test_winding_unique_integer_cases(self):
        winding = require_module(self, "athena_azr.h2_zero_certifier.winding_certifier")

        self.assertEqual(
            winding.certify_unique_integer_winding(
                RealInterval("-0.01", "0.01"), precision_bits=192
            ).winding_number,
            0,
        )
        self.assertEqual(
            winding.certify_unique_integer_winding(
                RealInterval("0.99", "1.01"), precision_bits=192
            ).winding_number,
            1,
        )
        self.assertEqual(
            winding.certify_unique_integer_winding(
                RealInterval("1.99", "2.01"), precision_bits=192
            ).winding_number,
            2,
        )
        for interval in (
            RealInterval("0.1", "0.9"),
            RealInterval("0.9", "2.1"),
            RealInterval("0", "1"),
        ):
            with self.assertRaises(winding.InconclusiveWindingCertification):
                winding.certify_unique_integer_winding(interval, precision_bits=192)

    def test_l3_isolator_handles_multiplicity_clusters_and_overlap(self):
        isolator = require_module(self, "athena_azr.h2_zero_certifier.l3_isolator")

        zeros = isolator.isolate_synthetic_l3_zeros(
            (
                isolator.SyntheticL3ZeroCandidate(
                    real_lower="0.49999999999999999999999",
                    real_upper="0.50000000000000000000001",
                    imag_lower="100.000000000000000000001",
                    imag_upper="100.000000000000000000002",
                    multiplicity=2,
                    critical_line_certified=True,
                    certificate_reference="resolved-multiplicity",
                ),
            )
        )
        self.assertEqual(zeros[0].multiplicity, 2)
        self.assertTrue(zeros[0].critical_line_certified)

        unresolved = isolator.SyntheticL3ZeroCandidate(
            real_lower="0.4",
            real_upper="0.400000000000000000001",
            imag_lower="10",
            imag_upper="10.000000000000000000001",
            multiplicity=None,
            certificate_reference="unresolved-multiplicity",
        )
        with self.assertRaises(isolator.InconclusiveL3Isolation):
            isolator.isolate_synthetic_l3_zeros((unresolved,))

        unresolved_cluster = isolator.SyntheticL3ZeroCandidate(
            real_lower="0.4",
            real_upper="0.400000000000000000001",
            imag_lower="11",
            imag_upper="11.000000000000000000001",
            multiplicity=1,
            cluster_resolved=False,
            certificate_reference="unresolved-cluster",
        )
        with self.assertRaises(isolator.InconclusiveL3Isolation):
            isolator.isolate_synthetic_l3_zeros((unresolved_cluster,))

    def test_l3_certifier_blocks_complete_result_when_one_height_fails(self):
        isolator = require_module(self, "athena_azr.h2_zero_certifier.l3_isolator")
        certifier = require_module(self, "athena_azr.h2_zero_certifier.l3_certifier")

        zeros = isolator.isolate_synthetic_l3_zeros(
            tuple(
                isolator.SyntheticL3ZeroCandidate(
                    real_lower="0.49999999999999999999999",
                    real_upper="0.50000000000000000000001",
                    imag_lower=str(Decimal(height) + Decimal("1e-21")),
                    imag_upper=str(Decimal(height) + Decimal("2e-21")),
                    multiplicity=1,
                    critical_line_certified=(height != 250),
                    certificate_reference=f"synthetic-{height}",
                )
                for height in (100, 150, 250, 400)
            )
        )

        result = certifier.certify_l3_synthetic(
            zeros,
            winding_counts={143: 1, 200: 2, 300: 3, 500: 4},
        )

        self.assertEqual([count.certified_total_count for count in result.counts], [1, 2, 3, 4])
        self.assertFalse(result.zeros[2].critical_line_certified)
        with self.assertRaises(certifier.InconclusiveL3Certification):
            certifier.certify_l3_synthetic(
                zeros,
                winding_counts={143: 1, 200: 99, 300: 3, 500: 4},
            )

    def test_l3_serialization_outputs_canonical_synthetic_artifacts(self):
        isolator = require_module(self, "athena_azr.h2_zero_certifier.l3_isolator")
        certifier = require_module(self, "athena_azr.h2_zero_certifier.l3_certifier")
        serialization = require_module(self, "athena_azr.h2_zero_certifier.serialization")

        zeros = isolator.isolate_synthetic_l3_zeros(
            (
                isolator.SyntheticL3ZeroCandidate(
                    real_lower="0.49999999999999999999999",
                    real_upper="0.50000000000000000000001",
                    imag_lower="100.000000000000000000001",
                    imag_upper="100.000000000000000000002",
                    multiplicity=1,
                    critical_line_certified=True,
                    certificate_reference="serial",
                ),
            )
        )
        result = certifier.certify_l3_synthetic(
            zeros,
            winding_counts={143: 1, 200: 1, 300: 1, 500: 1},
        )

        csv_data = serialization.l3_zero_csv_bytes(result)
        self.assertTrue(csv_data.startswith(b"ordering_index,function_id,character_definition"))
        self.assertNotIn(b"\r\n", csv_data)
        report = serialization.l3_completeness_report_json_bytes(result)
        self.assertTrue(report.endswith(b"\n"))
        self.assertIn(b'"function_id":"L3"', report)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / "l3_completeness_report.json"
            serialization.write_bytes_atomic(target, report, allowed_root=root)
            self.assertEqual(target.read_bytes(), report)

    def test_documentary_006f_schema_is_recognized_without_authorizing_execution(self):
        authorization = require_module(self, "athena_azr.h2_zero_certifier.authorization")
        pipeline = require_module(self, "athena_azr.h2_zero_certifier.pipeline")

        payload = {
            "authorization_id": "G5B-006F-EXPLICIT-AUTHORIZATION-TEST",
            "phase_id": "006F",
            "authorized_runtime": {"python": "sealed"},
            "authorized_backend_versions": {"arb": "sealed", "acb": "sealed"},
            "authorized_code_hashes": {"module.py": "a" * 64},
            "authorized_protocol_hashes": {"006H01": "b" * 64, "006H02": "c" * 64},
            "authorized_functions": ["zeta", "L3"],
            "authorized_heights": [143, 200, 300, 500],
            "authorized_artifact_directory": "artifacts/future-006f/",
            "network_policy": "forbidden",
            "dependency_policy": "no_installation_during_execution",
            "execution_scope": {"purpose": "H2 zero certification only"},
            "forbidden_scope": ["network", "dependency_installation"],
            "issued_by": "human",
            "issued_at": "2026-07-02T00:00:00Z",
        }
        normalized = authorization.validate_g5b_006f_authorization_schema(payload)
        self.assertEqual(normalized["phase_id"], "006F")
        self.assertFalse(normalized["execution_authorized"])
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / authorization.G5B_006F_AUTHORIZATION_FILENAME
            path.write_text(authorization.canonical_authorization_schema_json(payload), encoding="utf-8")
            self.assertEqual(
                pipeline.recognize_documentary_006f_authorization(path)["authorization_id"],
                payload["authorization_id"],
            )

    def test_probative_modules_do_not_use_float_or_heuristic_argument_tracking(self):
        modules = (
            "athena_azr/h2_zero_certifier/boundary_certifier.py",
            "athena_azr/h2_zero_certifier/argument_increment.py",
            "athena_azr/h2_zero_certifier/winding_certifier.py",
            "athena_azr/h2_zero_certifier/l3_isolator.py",
        )
        for relative in modules:
            text = Path(relative).read_text(encoding="utf-8").lower()
            for forbidden in ("float", "complex(", "atan2", "round("):
                self.assertNotIn(forbidden, text, f"{forbidden} leaked into {relative}")


if __name__ == "__main__":
    unittest.main()
