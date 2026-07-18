import unittest

from athena_azr.h2_zero_certifier.models import DirectedSegment, RationalComplexPoint
from athena_azr.h2_zero_certifier.chi3_function import CHI3_METADATA
from athena_azr.h2_zero_certifier.real_evidence import ComplexBallRecord, RealEvidenceFactory
from athena_azr.h2_zero_certifier.real_segment_enclosure import (
    InconclusiveSegmentEnclosure,
    enclose_completed_l3_segment,
    rectangular_hull,
)


class SegmentRuntime:
    def __init__(self, *, coverage=True, whole_box=True):
        self.coverage = coverage
        self.whole_box = whole_box
        self.inputs = []
        self.character_metadata = dict(CHI3_METADATA)
        self.effective_precision_bits = 192

    def audit_ball_semantics(self):
        result = {name: True for name in (
            "supports_nonzero_radius", "outward_rounded",
            "native_entire_dirichlet_l", "rigorous_complex_log",
        )}
        result["whole_box_evaluation"] = self.whole_box
        return result
    def pi_ball(self, precision_bits): return "pi"
    def divide_exact_integer(self, numerator, denominator, precision_bits): return "3/pi"
    def real_log(self, value, precision_bits): return "log"
    def scale_and_shift_exponent(self, input_ball, log_base, precision_bits): return "exp-arg"
    def complex_exp(self, value, precision_bits): return "power"
    def affine_half_plus_half(self, input_ball, precision_bits): return "gamma-arg"
    def complex_gamma(self, value, precision_bits): return "gamma"
    def native_dirichlet_l(self, value, **kwargs): self.inputs.append(value); return value
    def multiply(self, *values, precision_bits): return self.inputs[-1]
    def is_finite_ball(self, value): return True
    def certifies_whole_box(self, value): return self.coverage


class H2RealSegmentEnclosureTests(unittest.TestCase):
    def setUp(self):
        self.segment = DirectedSegment(
            RationalComplexPoint("-0.5", "3"),
            RationalComplexPoint("1.5", "7"),
        )
        self.factory = RealEvidenceFactory("fake", "a" * 64, "b" * 64)

    def test_rectangular_hull_contains_the_entire_segment(self):
        self.assertEqual(
            rectangular_hull(self.segment),
            ComplexBallRecord("-0.5", "1.5", "3", "7"),
        )

    def test_segment_enclosure_evaluates_the_full_hull(self):
        runtime = SegmentRuntime()
        result = enclose_completed_l3_segment(runtime, self.segment, 192, self.factory)
        self.assertEqual(runtime.inputs, [ComplexBallRecord("-0.5", "1.5", "3", "7")])
        self.assertTrue(result.entire_segment_covered)
        self.assertEqual(result.mechanism, "whole_rectangular_complex_ball")

    def test_segment_enclosure_rejects_unproved_coverage(self):
        with self.assertRaises(InconclusiveSegmentEnclosure):
            enclose_completed_l3_segment(
                SegmentRuntime(coverage=False), self.segment, 192, self.factory
            )

    def test_segment_enclosure_rejects_endpoint_sampling_runtime(self):
        with self.assertRaises(InconclusiveSegmentEnclosure):
            enclose_completed_l3_segment(
                SegmentRuntime(whole_box=False), self.segment, 192, self.factory
            )


if __name__ == "__main__":
    unittest.main()
