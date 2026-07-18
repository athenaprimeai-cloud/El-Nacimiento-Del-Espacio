import unittest
from decimal import Decimal

from athena_azr.h2_zero_certifier.ball_argument import (
    InconclusiveArgument,
    certify_argument_increment,
    certify_half_plane,
    verify_exclusion,
)
from athena_azr.h2_zero_certifier.models import (
    DirectedSegment,
    HalfPlaneCertificate,
    RationalComplexPoint,
    RealInterval,
    SegmentImageCertificate,
)


def segment_certificate(real_lower, real_upper, imag_lower, imag_upper, *, covered=True):
    segment = DirectedSegment(
        RationalComplexPoint("0", "0"),
        RationalComplexPoint("1", "0"),
    )
    return SegmentImageCertificate(
        segment=segment,
        enclosure_real=RealInterval(real_lower, real_upper),
        enclosure_imag=RealInterval(imag_lower, imag_upper),
        entire_segment_covered=covered,
    )


class H2BallArgumentTests(unittest.TestCase):
    def test_half_plane_certificate_rejects_an_image_containing_zero(self):
        segment = DirectedSegment(
            RationalComplexPoint("0", "0"),
            RationalComplexPoint("1", "0"),
        )
        image = SegmentImageCertificate(
            segment=segment,
            enclosure_real=RealInterval("-1", "1"),
            enclosure_imag=RealInterval("-1", "1"),
            entire_segment_covered=True,
        )

        with self.assertRaises(ValueError):
            HalfPlaneCertificate(image, "1", "0", "1")

    def test_exclusion_requires_a_full_rigorous_segment_enclosure(self):
        with_zero = segment_certificate("-1", "1", "-1", "1")
        partial = segment_certificate("1", "2", "-1", "1", covered=False)
        valid = segment_certificate("1", "2", "-1", "1")

        self.assertFalse(verify_exclusion(with_zero))
        self.assertFalse(verify_exclusion(partial))
        self.assertTrue(verify_exclusion(valid))

    def test_certifies_exact_axis_rotations_without_float_arithmetic(self):
        right = certify_half_plane(
            segment_certificate("1", "2", "-0.5", "0.5"),
            rotation_real="1",
            rotation_imag="0",
        )
        upper = certify_half_plane(
            segment_certificate("-0.5", "0.5", "1", "2"),
            rotation_real="0",
            rotation_imag="-1",
        )

        self.assertEqual(Decimal(right.rotated_real_lower), Decimal("1"))
        self.assertEqual(Decimal(upper.rotated_real_lower), Decimal("1"))

    def test_rejects_rotation_without_strict_half_plane_separation(self):
        cert = segment_certificate("-0.5", "0.5", "1", "2")

        with self.assertRaises(InconclusiveArgument):
            certify_half_plane(cert, rotation_real="1", rotation_imag="0")

    def test_argument_increment_only_wraps_a_prevalidated_rigorous_interval(self):
        half_plane = certify_half_plane(
            segment_certificate("1", "2", "-0.5", "0.5"),
            rotation_real="1",
            rotation_imag="0",
        )

        increment = certify_argument_increment(
            half_plane,
            RealInterval("-0.0000000001", "0.0000000001"),
        )

        self.assertIs(increment.half_plane_certificate, half_plane)
        self.assertEqual(increment.delta_lower, "-0.0000000001")
        self.assertEqual(increment.delta_upper, "0.0000000001")


if __name__ == "__main__":
    unittest.main()
