import unittest
from decimal import Decimal
from athena_azr.h2_zero_certifier.models import (
    RationalComplexPoint,
    DirectedSegment,
    RectangularContour,
    RealInterval,
    SegmentImageCertificate,
    ArgumentIncrementCertificate,
    HalfPlaneCertificate,
)
from athena_azr.h2_zero_certifier.l3_argument_count import (
    accumulate_winding,
    count_contour_winding,
    InconclusiveWindingCount,
)
from athena_azr.h2_zero_certifier.ball_argument import InconclusiveArgument
from athena_azr.h2_zero_certifier.contour import build_rectangular_contour


class H2L3ArgumentCountTests(unittest.TestCase):
    def increment(self, lower, upper):
        seg = DirectedSegment(
            RationalComplexPoint("0", "0"),
            RationalComplexPoint("1", "0"),
        )
        img_cert = SegmentImageCertificate(
            segment=seg,
            enclosure_real=RealInterval("1", "2"),
            enclosure_imag=RealInterval("-1", "1"),
            entire_segment_covered=True,
        )
        half_plane = HalfPlaneCertificate(img_cert, "1", "0", "1")
        return ArgumentIncrementCertificate(half_plane, lower, upper)

    def test_accumulate_winding_success_one(self):
        # A sequence of increments summing to ~2*pi (6.28...)
        # We represent them as certificates.
        seg = DirectedSegment(
            RationalComplexPoint("0", "0"),
            RationalComplexPoint("1", "0"),
        )
        img_cert = SegmentImageCertificate(
            segment=seg,
            enclosure_real=RealInterval("1", "2"),
            enclosure_imag=RealInterval("-1", "1"),
            entire_segment_covered=True,
        )
        
        # Increments: 4 segments, each delta around pi/2 = 1.5707...
        # Delta intervals: [1.56, 1.58]
        certs = [self.increment("1.56", "1.58") for _ in range(4)]
        
        # Accumulate. W = A / (2*pi).
        # Sum is [6.24, 6.32]. Divided by 2*pi (using pi in [3.1415, 3.1416])
        # W_lower = 6.24 / 6.2832 = 0.9931
        # W_upper = 6.32 / 6.283 = 1.0058
        # Strictly contained in (0.5, 1.5), unique integer = 1.
        winding_cert = accumulate_winding(certs, precision_bits=192)
        self.assertEqual(winding_cert.winding_number, 1)
        self.assertEqual(winding_cert.working_precision_bits, 192)

    def test_accumulate_winding_success_zero(self):
        # Winding number = 0
        seg = DirectedSegment(
            RationalComplexPoint("0", "0"),
            RationalComplexPoint("1", "0"),
        )
        img_cert = SegmentImageCertificate(
            segment=seg,
            enclosure_real=RealInterval("1", "2"),
            enclosure_imag=RealInterval("-1", "1"),
            entire_segment_covered=True,
        )
        
        certs = [self.increment("0.1", "0.2"), self.increment("-0.2", "-0.1")]
        
        # Sum is [-0.1, 0.1]. W is in [-0.016, 0.016].
        # Strictly in (-0.5, 0.5), unique integer = 0.
        winding_cert = accumulate_winding(certs, precision_bits=256)
        self.assertEqual(winding_cert.winding_number, 0)
        self.assertEqual(winding_cert.working_precision_bits, 256)

    def test_accumulate_winding_inconclusive_overlaps_semientero(self):
        seg = DirectedSegment(
            RationalComplexPoint("0", "0"),
            RationalComplexPoint("1", "0"),
        )
        img_cert = SegmentImageCertificate(
            segment=seg,
            enclosure_real=RealInterval("1", "2"),
            enclosure_imag=RealInterval("-1", "1"),
            entire_segment_covered=True,
        )
        
        # Increments sum to [3.0, 3.3]. W = [0.477, 0.525] which contains/overlaps 0.5
        certs = [self.increment("3.0", "3.3")]
        
        with self.assertRaises(InconclusiveWindingCount):
            accumulate_winding(certs, precision_bits=192)

    def test_accumulate_winding_inconclusive_multiple_integers(self):
        seg = DirectedSegment(
            RationalComplexPoint("0", "0"),
            RationalComplexPoint("1", "0"),
        )
        img_cert = SegmentImageCertificate(
            segment=seg,
            enclosure_real=RealInterval("1", "2"),
            enclosure_imag=RealInterval("-1", "1"),
            entire_segment_covered=True,
        )
        
        # Increments sum to [-1.0, 10.0]. W contains both 0 and 1.
        certs = [self.increment("-1.0", "10.0")]
        
        with self.assertRaises(InconclusiveWindingCount):
            accumulate_winding(certs, precision_bits=192)

    def test_rejects_interval_that_contains_no_integer(self):
        with self.assertRaises(InconclusiveWindingCount):
            accumulate_winding([self.increment("2.6", "2.7")], precision_bits=192)

    def test_counts_a_synthetic_contour_from_segment_certificates(self):
        backend = SyntheticSegmentBackend(
            maximum_segment_length=None,
            delta_lower="1.5707963267948966192313216916397",
            delta_upper="1.5707963267948966192313216916398",
        )
        contour = build_rectangular_contour("-0.5", "1.5", "0", "2")

        result = count_contour_winding(
            backend,
            contour,
            precision_bits=192,
            max_depth=4,
        )

        self.assertEqual(result.winding_number, 1)
        self.assertEqual(backend.accepted_segments, 4)

    def test_subdivides_segments_before_accumulating(self):
        backend = SyntheticSegmentBackend(
            maximum_segment_length=Decimal("1.1"),
            delta_lower="0.7853981633974483096156608458198",
            delta_upper="0.7853981633974483096156608458199",
        )
        contour = build_rectangular_contour("-0.5", "1.5", "0", "2")

        result = count_contour_winding(
            backend,
            contour,
            precision_bits=192,
            max_depth=2,
        )

        self.assertEqual(result.winding_number, 1)
        self.assertEqual(backend.accepted_segments, 8)

    def test_fails_closed_when_subdivision_depth_is_exhausted(self):
        backend = SyntheticSegmentBackend(
            maximum_segment_length=Decimal("0.1"),
            delta_lower="0.1",
            delta_upper="0.2",
        )
        contour = build_rectangular_contour("-0.5", "1.5", "0", "2")

        with self.assertRaises(InconclusiveWindingCount):
            count_contour_winding(
                backend,
                contour,
                precision_bits=192,
                max_depth=1,
            )

    def test_rejects_directly_constructed_negative_contour(self):
        valid = build_rectangular_contour("-0.5", "1.5", "0", "2")
        bypassed = RectangularContour(valid.segments, orientation="negative")
        backend = SyntheticSegmentBackend(
            maximum_segment_length=None,
            delta_lower="1.5707963267948966192313216916397",
            delta_upper="1.5707963267948966192313216916398",
        )

        with self.assertRaises(ValueError):
            count_contour_winding(
                backend,
                bypassed,
                precision_bits=192,
                max_depth=1,
            )

        self.assertEqual(backend.accepted_segments, 0)

    def test_rejects_mismatched_half_plane_certificate_identity(self):
        backend = MismatchedCertificateBackend()
        contour = build_rectangular_contour("-0.5", "1.5", "0", "2")

        with self.assertRaises(InconclusiveWindingCount):
            count_contour_winding(
                backend,
                contour,
                precision_bits=192,
                max_depth=0,
            )

    def test_rejects_mismatched_argument_increment_identity(self):
        backend = MismatchedIncrementBackend()
        contour = build_rectangular_contour("-0.5", "1.5", "0", "2")

        with self.assertRaises(InconclusiveWindingCount):
            count_contour_winding(
                backend,
                contour,
                precision_bits=192,
                max_depth=0,
            )


class SyntheticSegmentBackend:
    def __init__(self, maximum_segment_length, delta_lower, delta_upper):
        self.maximum_segment_length = maximum_segment_length
        self.delta_lower = delta_lower
        self.delta_upper = delta_upper
        self.accepted_segments = 0

    def completed_l3_segment(self, segment, precision_bits):
        length = abs(segment.end.real_decimal - segment.start.real_decimal) + abs(
            segment.end.imag_decimal - segment.start.imag_decimal
        )
        if self.maximum_segment_length is not None and length > self.maximum_segment_length:
            raise InconclusiveArgument("synthetic enclosure requires subdivision")
        self.accepted_segments += 1
        return SegmentImageCertificate(
            segment=segment,
            enclosure_real=RealInterval("1", "2"),
            enclosure_imag=RealInterval("-0.25", "0.25"),
            entire_segment_covered=True,
        )

    def validate_half_plane(self, segment_certificate, precision_bits):
        return HalfPlaneCertificate(segment_certificate, "1", "0", "1")

    def argument_increment(self, half_plane_certificate, precision_bits):
        return ArgumentIncrementCertificate(
            half_plane_certificate,
            self.delta_lower,
            self.delta_upper,
        )


class MismatchedCertificateBackend(SyntheticSegmentBackend):
    def __init__(self):
        super().__init__(
            None,
            "1.5707963267948966192313216916397",
            "1.5707963267948966192313216916398",
        )

    def validate_half_plane(self, segment_certificate, precision_bits):
        other_segment = DirectedSegment(
            RationalComplexPoint("10", "10"),
            RationalComplexPoint("11", "10"),
        )
        other_image = SegmentImageCertificate(
            segment=other_segment,
            enclosure_real=RealInterval("1", "2"),
            enclosure_imag=RealInterval("-0.25", "0.25"),
            entire_segment_covered=True,
        )
        return HalfPlaneCertificate(other_image, "1", "0", "1")


class MismatchedIncrementBackend(SyntheticSegmentBackend):
    def __init__(self):
        super().__init__(
            None,
            "1.5707963267948966192313216916397",
            "1.5707963267948966192313216916398",
        )

    def argument_increment(self, half_plane_certificate, precision_bits):
        other_segment = DirectedSegment(
            RationalComplexPoint("10", "10"),
            RationalComplexPoint("11", "10"),
        )
        other_image = SegmentImageCertificate(
            segment=other_segment,
            enclosure_real=RealInterval("1", "2"),
            enclosure_imag=RealInterval("-0.25", "0.25"),
            entire_segment_covered=True,
        )
        other_half_plane = HalfPlaneCertificate(other_image, "1", "0", "1")
        return ArgumentIncrementCertificate(
            other_half_plane,
            self.delta_lower,
            self.delta_upper,
        )


if __name__ == "__main__":
    unittest.main()
