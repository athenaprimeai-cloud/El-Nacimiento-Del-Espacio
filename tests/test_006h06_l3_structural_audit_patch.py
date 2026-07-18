import hashlib
import json
import unittest
from decimal import Decimal

from athena_azr.h2_zero_certifier.models import (
    CountCertificate,
    RealInterval,
    SegmentImageCertificate,
)


class H006H06StructuralAuditPatchTests(unittest.TestCase):
    def increment(self, source_id, lower="0.1", upper="0.2", precision=192, provenance=None):
        from athena_azr.h2_zero_certifier.argument_increment import (
            ArgumentIncrementInterval,
        )

        return ArgumentIncrementInterval(
            source_id,
            lower,
            upper,
            precision,
            provenance=provenance,
        )

    def test_same_provenance_passes(self):
        from athena_azr.h2_zero_certifier.argument_increment import sum_argument_intervals

        provenance = {"backend_id": "synthetic", "authorization_digest": "a" * 64}
        total = sum_argument_intervals(
            (
                self.increment("seg-1", provenance=provenance),
                self.increment("seg-2", provenance=provenance),
            ),
            contour_id="C_143",
        )

        self.assertEqual(total.lower, "0.2")
        self.assertEqual(total.upper, "0.4")

    def test_same_content_different_mapping_order_passes(self):
        from athena_azr.h2_zero_certifier.argument_increment import sum_argument_intervals

        first_provenance = {"backend_id": "synthetic", "authorization_digest": "a" * 64}
        second_provenance = {"authorization_digest": "a" * 64, "backend_id": "synthetic"}
        total = sum_argument_intervals(
            (
                self.increment("seg-1", provenance=first_provenance),
                self.increment("seg-2", provenance=second_provenance),
            ),
            contour_id="C_143",
        )

        self.assertEqual(total.lower, "0.2")
        self.assertEqual(total.upper, "0.4")

    def test_mixed_provenance_fails(self):
        from athena_azr.h2_zero_certifier.argument_increment import (
            InconclusiveArgumentIncrement,
            sum_argument_intervals,
        )

        with self.assertRaises(InconclusiveArgumentIncrement):
            sum_argument_intervals(
                (
                    self.increment(
                        "seg-1",
                        provenance={
                            "backend_id": "synthetic-a",
                            "authorization_digest": "a" * 64,
                        },
                    ),
                    self.increment(
                        "seg-2",
                        provenance={
                            "backend_id": "synthetic-b",
                            "authorization_digest": "a" * 64,
                        },
                    ),
                ),
                contour_id="C_143",
            )

    def test_missing_provenance_fails_if_required(self):
        from athena_azr.h2_zero_certifier.argument_increment import (
            InconclusiveArgumentIncrement,
            sum_argument_intervals,
        )

        with self.assertRaises(InconclusiveArgumentIncrement):
            sum_argument_intervals(
                (
                    self.increment("seg-1"),
                    self.increment("seg-2"),
                ),
                contour_id="C_143",
            )

    def test_mixed_precision_still_fails(self):
        from athena_azr.h2_zero_certifier.argument_increment import (
            InconclusiveArgumentIncrement,
            sum_argument_intervals,
        )

        provenance = {"backend_id": "synthetic", "authorization_digest": "a" * 64}
        with self.assertRaises(InconclusiveArgumentIncrement):
            sum_argument_intervals(
                (
                    self.increment("seg-1", precision=192, provenance=provenance),
                    self.increment("seg-2", precision=256, provenance=provenance),
                ),
                contour_id="C_143",
            )

    def test_duplicate_source_still_fails(self):
        from athena_azr.h2_zero_certifier.argument_increment import (
            InconclusiveArgumentIncrement,
            sum_argument_intervals,
        )

        provenance = {"backend_id": "synthetic", "authorization_digest": "a" * 64}
        with self.assertRaises(InconclusiveArgumentIncrement):
            sum_argument_intervals(
                (
                    self.increment("seg-1", provenance=provenance),
                    self.increment("seg-1", provenance=provenance),
                ),
                contour_id="C_143",
            )

    def l3_function(self):
        from athena_azr.h2_zero_certifier.l3_certifier import certify_l3_synthetic
        from athena_azr.h2_zero_certifier.l3_isolator import (
            SyntheticL3ZeroCandidate,
            isolate_synthetic_l3_zeros,
        )

        zeros = isolate_synthetic_l3_zeros(
            (
                SyntheticL3ZeroCandidate(
                    real_lower="0.49999999999999999999999",
                    real_upper="0.50000000000000000000001",
                    imag_lower="100.000000000000000000001",
                    imag_upper="100.000000000000000000002",
                    multiplicity=1,
                    critical_line_certified=True,
                    certificate_reference="synthetic-zero-1",
                ),
                SyntheticL3ZeroCandidate(
                    real_lower="0.49999999999999999999999",
                    real_upper="0.50000000000000000000001",
                    imag_lower="250.000000000000000000001",
                    imag_upper="250.000000000000000000002",
                    multiplicity=2,
                    critical_line_certified=False,
                    certificate_reference="synthetic-zero-2",
                ),
            )
        )
        return certify_l3_synthetic(
            zeros,
            winding_counts={143: 1, 200: 1, 300: 3, 500: 3},
        )

    def test_l3_isolation_report_matches_006h01_schema(self):
        from athena_azr.h2_zero_certifier.serialization import (
            l3_isolation_report_json_bytes,
            l3_zero_csv_bytes,
        )

        function = self.l3_function()
        payload = json.loads(l3_isolation_report_json_bytes(function).decode("utf-8"))
        expected_fields = {
            "phase_id",
            "function_id",
            "character_definition",
            "height_limit",
            "target_isolation_width",
            "zero_records_file",
            "zero_records_sha256",
            "total_isolated_with_multiplicity",
            "unique_zero_failures",
            "neighbor_disjointness_failures",
            "unresolved_clusters",
            "backend_identity",
            "runtime_identity",
            "approved_code_hashes",
            "protocol_hashes",
            "authorization_id",
            "certification_methods",
            "status",
            "real_certification",
        }

        self.assertEqual(set(payload), expected_fields)
        self.assertEqual(payload["status"], "synthetic_structural_only")
        self.assertFalse(payload["real_certification"])
        self.assertEqual(
            payload["zero_records_sha256"],
            hashlib.sha256(l3_zero_csv_bytes(function)).hexdigest(),
        )

    def test_l3_completeness_report_matches_006h01_schema(self):
        from athena_azr.h2_zero_certifier.serialization import (
            l3_completeness_report_json_bytes,
        )

        payload = json.loads(
            l3_completeness_report_json_bytes(self.l3_function()).decode("utf-8")
        )
        expected_fields = {
            "phase_id",
            "function_id",
            "character_definition",
            "height_set",
            "count_records",
            "boundary_convention",
            "boundary_zero_free_certificates",
            "independent_count_method",
            "isolated_count_with_multiplicity_by_height",
            "independent_certified_count_by_height",
            "counts_match_by_height",
            "unresolved_clusters",
            "winding_intervals_or_equivalent_count_certificates",
            "unique_integer_counts",
            "backend_identity",
            "runtime_identity",
            "approved_code_hashes",
            "protocol_hashes",
            "authorization_id",
            "status",
            "real_certification",
        }

        self.assertEqual(set(payload), expected_fields)
        self.assertEqual(payload["status"], "synthetic_structural_only")
        self.assertFalse(payload["real_certification"])
        self.assertEqual(payload["height_set"], [143, 200, 300, 500])
        self.assertEqual(payload["isolated_count_with_multiplicity_by_height"]["300"], 3)
        self.assertTrue(payload["counts_match_by_height"]["500"])

    def test_degenerate_integer_interval_cases(self):
        from athena_azr.h2_zero_certifier import winding_certifier as winding

        self.assertEqual(winding.integers_in_closed_interval("1", "1"), (1,))
        self.assertEqual(winding.integers_in_closed_interval("0", "0"), (0,))
        self.assertEqual(winding.integers_in_closed_interval("-2", "-2"), (-2,))
        self.assertEqual(
            winding.integers_in_closed_interval("0.999999999999999999999999", "1.000000000000000000000001"),
            (1,),
        )
        self.assertEqual(winding.integers_in_closed_interval("0.1", "0.9"), ())
        self.assertEqual(winding.integers_in_closed_interval("0", "1"), (0, 1))
        self.assertEqual(winding.integers_in_closed_interval("-1.2", "-0.8"), (-1,))

    def test_degenerate_unique_winding_uses_closed_interval_without_relaxing_realinterval(self):
        from athena_azr.h2_zero_certifier import winding_certifier as winding

        self.assertEqual(
            winding.certify_unique_integer_winding_bounds(
                "0", "0", precision_bits=192
            ).winding_number,
            0,
        )
        with self.assertRaises(ValueError):
            RealInterval("0", "0")

    def test_boundary_certifier_subdivides_after_parent_failure(self):
        from athena_azr.h2_zero_certifier.boundary_certifier import (
            InconclusiveBoundaryCertification,
            certify_boundary_segment,
        )
        from athena_azr.h2_zero_certifier.contour import build_frozen_l3_contour

        segment = build_frozen_l3_contour(143).segments[0]
        backend = ProgressiveSegmentBackend(maximum_length="1")

        with self.assertRaises(InconclusiveBoundaryCertification):
            certify_boundary_segment(backend, segment, precision_bits=192, max_depth=0)

        backend = ProgressiveSegmentBackend(maximum_length="1")
        certificate = certify_boundary_segment(
            backend,
            segment,
            precision_bits=192,
            max_depth=1,
        )

        self.assertTrue(certificate.zero_excluded)
        self.assertEqual(certificate.subdivision_count, 2)
        self.assertEqual(certificate.certificates[0].segment.start, segment.start)
        self.assertEqual(certificate.certificates[-1].segment.end, segment.end)
        self.assertEqual(
            certificate.certificates[0].segment.end,
            certificate.certificates[1].segment.start,
        )
        self.assertEqual(backend.rejected_segments, 1)
        self.assertEqual(backend.accepted_segments, 2)


class ProgressiveSegmentBackend:
    def __init__(self, *, maximum_length):
        self.maximum_length = Decimal(maximum_length)
        self.rejected_segments = 0
        self.accepted_segments = 0

    def completed_l3_segment(self, segment, precision_bits):
        length_real = abs(segment.end.real_decimal - segment.start.real_decimal)
        length_imag = abs(segment.end.imag_decimal - segment.start.imag_decimal)
        length = max(length_real, length_imag)
        if length > self.maximum_length:
            self.rejected_segments += 1
            real = RealInterval("-1", "1")
            imag = RealInterval("-1", "1")
        else:
            self.accepted_segments += 1
            real = RealInterval("2", "3")
            imag = RealInterval("4", "5")
        return SegmentImageCertificate(
            segment=segment,
            enclosure_real=real,
            enclosure_imag=imag,
            entire_segment_covered=True,
            arithmetic="rigorous_ball",
        )


if __name__ == "__main__":
    unittest.main()
