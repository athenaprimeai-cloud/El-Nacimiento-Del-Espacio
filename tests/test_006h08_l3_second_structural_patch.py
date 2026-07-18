import json
import tempfile
import unittest
from pathlib import Path

from athena_azr.h2_zero_certifier.models import RealInterval


class H006H08L3SecondStructuralPatchTests(unittest.TestCase):
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
            )
        )
        return certify_l3_synthetic(
            zeros,
            winding_counts={143: 1, 200: 1, 300: 1, 500: 1},
        )

    def assert_synthetic_marker(self, marker):
        self.assertEqual(
            marker,
            {
                "status": "not_applicable_synthetic_structural",
                "execution_authorized": False,
                "source_phase": "006H08",
            },
        )

    def test_synthetic_reports_use_explicit_nonexecuting_hash_markers(self):
        from athena_azr.h2_zero_certifier.serialization import (
            l3_completeness_report_json_bytes,
            l3_isolation_report_json_bytes,
        )

        function = self.l3_function()
        reports = (
            json.loads(l3_isolation_report_json_bytes(function).decode("utf-8")),
            json.loads(l3_completeness_report_json_bytes(function).decode("utf-8")),
        )

        for payload in reports:
            self.assertEqual(payload["phase_id"], "006H08")
            self.assertEqual(payload["status"], "synthetic_structural_only")
            self.assertFalse(payload["real_certification"])
            self.assertEqual(payload["authorization_id"], "none_synthetic_structural_006H08")
            self.assert_synthetic_marker(payload["approved_code_hashes"])
            self.assert_synthetic_marker(payload["protocol_hashes"])

    def test_synthetic_reports_cannot_pass_real_authorization_validation(self):
        from athena_azr.h2_zero_certifier.authorization import (
            ExecutionNotAuthorized,
            require_execution_authorization,
        )
        from athena_azr.h2_zero_certifier.pipeline import (
            recognize_documentary_006f_authorization,
        )
        from athena_azr.h2_zero_certifier.serialization import (
            l3_completeness_report_json_bytes,
        )

        report = l3_completeness_report_json_bytes(self.l3_function())
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "G5B-006F-AUTHORIZATION.json"
            path.write_bytes(report)
            with self.assertRaises(ExecutionNotAuthorized):
                recognize_documentary_006f_authorization(path)
            with self.assertRaises(ExecutionNotAuthorized):
                require_execution_authorization(
                    path,
                    expected_plan_hash="a" * 64,
                    expected_review_hashes={},
                    expected_output_dir=Path(directory) / "out",
                    code_root=Path.cwd(),
                    required_code_files=(),
                )

    def test_exact_rational_closed_interval_integer_enumeration(self):
        from athena_azr.h2_zero_certifier import winding_certifier as winding

        cases = (
            ("1", "1", (1,)),
            ("0", "0", (0,)),
            ("-2", "-2", (-2,)),
            ("1/3", "2/3", ()),
            ("-1", "1", (-1, 0, 1)),
            ("-3/2", "-1/2", (-1,)),
            ("1", "2", (1, 2)),
            ("-2/3", "1/3", (0,)),
            (
                "333333333333333333333",
                "1000000000000000000001/3",
                (333333333333333333333,),
            ),
        )

        for lower, upper, expected in cases:
            with self.subTest(lower=lower, upper=upper):
                self.assertEqual(
                    winding.integers_in_exact_closed_interval(lower, upper),
                    expected,
                )
                self.assertEqual(
                    winding.integers_in_closed_interval(lower, upper),
                    expected,
                )

    def test_endpoint_canonicality_and_invalid_values_are_rejected(self):
        from athena_azr.h2_zero_certifier import winding_certifier as winding

        invalid_values = (
            "01",
            "+1",
            "1.0",
            "1/01",
            "2/4",
            "1/-2",
            "0/5",
            "NaN",
            "Infinity",
            "",
            " 1",
            "1 ",
        )

        for value in invalid_values:
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    winding.parse_canonical_exact_endpoint(value)

        with self.assertRaises(ValueError):
            winding.integers_in_exact_closed_interval("2", "1")
        with self.assertRaises(ValueError):
            winding.integers_in_exact_closed_interval("1/0", "1")

    def test_decimal_and_rational_endpoints_remain_exact(self):
        from fractions import Fraction

        from athena_azr.h2_zero_certifier import winding_certifier as winding

        self.assertEqual(winding.parse_canonical_exact_endpoint("0.125"), Fraction(1, 8))
        self.assertEqual(winding.parse_canonical_exact_endpoint("-0.5"), Fraction(-1, 2))
        self.assertEqual(winding.parse_canonical_exact_endpoint("-1/2"), Fraction(-1, 2))

    def test_closed_winding_interval_may_be_degenerate_but_realinterval_may_not(self):
        from athena_azr.h2_zero_certifier import winding_certifier as winding

        interval = winding.ClosedWindingInterval("1/3", "1/3")
        self.assertEqual(interval.lower, "1/3")
        self.assertEqual(interval.upper, "1/3")
        with self.assertRaises(ValueError):
            RealInterval("0", "0")


if __name__ == "__main__":
    unittest.main()
