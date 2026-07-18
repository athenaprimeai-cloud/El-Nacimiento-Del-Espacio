import unittest
from athena_azr.h2_zero_certifier.completed_l3 import (
    completed_l3_symbolic_formula,
    completed_l3_point_inert,
    completed_l3_segment_inert,
)
from athena_azr.h2_zero_certifier.models import RationalComplexPoint, DirectedSegment


class H2CompletedL3Tests(unittest.TestCase):
    def test_symbolic_formula_matches_spec(self):
        self.assertEqual(
            completed_l3_symbolic_formula(),
            "(3/pi)^((s+1)/2) * Gamma((s+1)/2) * L(s,chi_3)"
        )

    def test_completed_l3_point_inert_raises_not_implemented(self):
        point = RationalComplexPoint("0.5", "12.5")
        with self.assertRaises(NotImplementedError):
            completed_l3_point_inert(point, 192)

    def test_completed_l3_segment_inert_raises_not_implemented(self):
        start = RationalComplexPoint("-0.5", "0.0")
        end = RationalComplexPoint("1.5", "0.0")
        segment = DirectedSegment(start, end)
        with self.assertRaises(NotImplementedError):
            completed_l3_segment_inert(segment, 192)


if __name__ == "__main__":
    unittest.main()
