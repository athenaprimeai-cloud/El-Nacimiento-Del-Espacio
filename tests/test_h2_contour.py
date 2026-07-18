import unittest
from decimal import Decimal
from athena_azr.h2_zero_certifier.models import (
    RationalComplexPoint,
    DirectedSegment,
    RectangularContour,
)
from athena_azr.h2_zero_certifier.contour import (
    build_rectangular_contour,
    validate_contour_orientation,
)


class H2ContourTests(unittest.TestCase):
    def test_rational_complex_point_creation(self):
        p = RationalComplexPoint("-0.5", "143.0")
        self.assertEqual(p.real, "-0.5")
        self.assertEqual(p.imag, "143.0")
        self.assertEqual(p.real_decimal, Decimal("-0.5"))
        self.assertEqual(p.imag_decimal, Decimal("143.0"))

        with self.assertRaises(ValueError):
            RationalComplexPoint("not-a-number", "0")

    def test_directed_segment_creation(self):
        start = RationalComplexPoint("0", "0")
        end = RationalComplexPoint("1", "1")
        segment = DirectedSegment(start, end)
        self.assertEqual(segment.start, start)
        self.assertEqual(segment.end, end)

        with self.assertRaises(ValueError):
            DirectedSegment(start, start)

    def test_rectangular_contour_construction(self):
        # Build standard rectangle boundary with positive orientation
        # (-0.5, 0) -> (1.5, 0) -> (1.5, 143) -> (-0.5, 143) -> (-0.5, 0)
        contour = build_rectangular_contour("-0.5", "1.5", "0.0", "143.0")
        self.assertEqual(contour.orientation, "positive")
        self.assertEqual(len(contour.segments), 4)

        # Check closing property
        self.assertEqual(contour.segments[0].start, RationalComplexPoint("-0.5", "0.0"))
        self.assertEqual(contour.segments[0].end, RationalComplexPoint("1.5", "0.0"))
        self.assertEqual(contour.segments[1].start, RationalComplexPoint("1.5", "0.0"))
        self.assertEqual(contour.segments[1].end, RationalComplexPoint("1.5", "143.0"))
        self.assertEqual(contour.segments[2].start, RationalComplexPoint("1.5", "143.0"))
        self.assertEqual(contour.segments[2].end, RationalComplexPoint("-0.5", "143.0"))
        self.assertEqual(contour.segments[3].start, RationalComplexPoint("-0.5", "143.0"))
        self.assertEqual(contour.segments[3].end, RationalComplexPoint("-0.5", "0.0"))

    def test_rejects_incorrect_orientation(self):
        # Create a contour oriented negatively (clockwise)
        # (-0.5, 0) -> (-0.5, 143) -> (1.5, 143) -> (1.5, 0) -> (-0.5, 0)
        p0 = RationalComplexPoint("-0.5", "0.0")
        p1 = RationalComplexPoint("-0.5", "143.0")
        p2 = RationalComplexPoint("1.5", "143.0")
        p3 = RationalComplexPoint("1.5", "0.0")

        seg0 = DirectedSegment(p0, p1)
        seg1 = DirectedSegment(p1, p2)
        seg2 = DirectedSegment(p2, p3)
        seg3 = DirectedSegment(p3, p0)

        with self.assertRaises(ValueError):
            validate_contour_orientation(RectangularContour((seg0, seg1, seg2, seg3)))

    def test_rejects_disconnected_segments(self):
        p0 = RationalComplexPoint("-0.5", "0.0")
        p1 = RationalComplexPoint("1.5", "0.0")
        p2 = RationalComplexPoint("1.5", "143.0")
        p3 = RationalComplexPoint("0.0", "5.0")  # Disconnected

        seg0 = DirectedSegment(p0, p1)
        seg1 = DirectedSegment(p1, p2)
        seg2 = DirectedSegment(p2, p3)
        seg3 = DirectedSegment(p3, p0)

        with self.assertRaises(ValueError):
            build_rectangular_contour("-0.5", "1.5", "0.0", "143.0", custom_segments=(seg0, seg1, seg2, seg3))

    def test_rejects_reversed_or_degenerate_rectangle_bounds(self):
        with self.assertRaises(ValueError):
            build_rectangular_contour("1.5", "-0.5", "143", "0")
        with self.assertRaises(ValueError):
            build_rectangular_contour("-0.5", "-0.5", "0", "143")


if __name__ == "__main__":
    unittest.main()
