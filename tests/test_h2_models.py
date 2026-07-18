import unittest
from decimal import Decimal

from athena_azr.h2_zero_certifier.config import CertificationConfig
from athena_azr.h2_zero_certifier.models import (
    ComplexBox,
    CountCertificate,
    RealInterval,
    ZeroCertificate,
)


class H2ModelsTests(unittest.TestCase):
    def test_real_interval_validates_order_and_width(self):
        interval = RealInterval("1.0", "1.000000000000000000001")

        self.assertEqual(interval.width_decimal(), Decimal("0.000000000000000000001"))
        self.assertTrue(interval.contains_decimal(Decimal("1.0")))

        with self.assertRaises(ValueError):
            RealInterval("2", "1")

        with self.assertRaises(ValueError):
            RealInterval("1", "1")

    def test_intervals_detect_overlap_and_disjointness(self):
        left = RealInterval("1", "2")
        touching = RealInterval("2", "3")
        right = RealInterval("2.0001", "3")

        self.assertFalse(left.is_disjoint_from(touching))
        self.assertTrue(left.is_disjoint_from(right))

    def test_zero_certificate_rejects_invalid_identity(self):
        box = ComplexBox(
            RealInterval("0.4999999999999999999999", "0.5000000000000000000001"),
            RealInterval("8", "8.1"),
        )

        with self.assertRaises(ValueError):
            ZeroCertificate(
                index=0,
                function_id="L3",
                conductor=3,
                character_id="3.2",
                parity=1,
                box=box,
                multiplicity=1,
                isolation_method="synthetic",
                working_precision_bits=192,
                certificate_reference="fixture",
                critical_line_certified=True,
            )

    def test_count_certificate_reports_exact_match(self):
        certificate = CountCertificate(
            function_id="zeta",
            requested_height=143,
            counting_boundary="143.5",
            boundary_zero_free=True,
            certified_total_count=10,
            isolated_count_with_multiplicity=10,
            counting_method="synthetic_turing",
            working_precision_bits=192,
            parameters={"fixture": "true"},
        )

        self.assertTrue(certificate.counts_match)

    def test_frozen_config_matches_006c_and_rejects_overrides(self):
        config = CertificationConfig.frozen_default()

        self.assertEqual(config.requested_heights, (143, 200, 300, 500))
        self.assertEqual(config.target_interval_width, Decimal("1e-20"))
        self.assertEqual(config.precision_steps_bits, (192, 256, 384, 512, 768, 1024))
        self.assertEqual(config.l3_conductor, 3)
        self.assertEqual(config.l3_conrey_number, 2)

        with self.assertRaises(TypeError):
            CertificationConfig.frozen_default(max_height=100)


if __name__ == "__main__":
    unittest.main()
