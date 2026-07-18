import unittest

from athena_azr.h2_zero_certifier.real_completed_l3 import (
    InconclusiveRealEvaluation,
    evaluate_completed_l3,
)
from athena_azr.h2_zero_certifier.chi3_function import CHI3_METADATA
from athena_azr.h2_zero_certifier.real_evidence import (
    ComplexBallRecord,
    RealEvidenceFactory,
)


class FakeCompletedL3Runtime:
    def __init__(self):
        self.calls = []
        self.character_metadata = dict(CHI3_METADATA)
        self.effective_precision_bits = 192
        self.native_l_result = ComplexBallRecord("5", "6", "7", "8")

    def audit_ball_semantics(self):
        return {name: True for name in (
            "supports_nonzero_radius", "outward_rounded",
            "native_entire_dirichlet_l", "whole_box_evaluation",
            "rigorous_complex_log",
        )}

    def pi_ball(self, precision_bits): self.calls.append("pi_ball"); return "pi"
    def divide_exact_integer(self, numerator, denominator, precision_bits): return "3/pi"
    def real_log(self, value, precision_bits): self.calls.append("real_log"); return "log"
    def scale_and_shift_exponent(self, input_ball, log_base, precision_bits): return "exp-arg"
    def complex_exp(self, value, precision_bits): self.calls.append("complex_exp"); return "power"
    def affine_half_plus_half(self, input_ball, precision_bits): return "gamma-arg"
    def complex_gamma(self, value, precision_bits): self.calls.append("complex_gamma"); return "gamma"
    def native_dirichlet_l(self, value, *, modulus, conrey_number, precision_bits):
        self.calls.append("native_dirichlet_l")
        self.native_l_character = (modulus, conrey_number)
        return self.native_l_result
    def multiply(self, *values, precision_bits):
        self.calls.append("multiply")
        return ComplexBallRecord("1", "2", "3", "4")
    def is_finite_ball(self, value): return isinstance(value, ComplexBallRecord)


class H2RealCompletedL3Tests(unittest.TestCase):
    def setUp(self):
        self.runtime = FakeCompletedL3Runtime()
        self.factory = RealEvidenceFactory("fake", "a" * 64, "b" * 64)
        self.input_ball = ComplexBallRecord("0.4", "0.6", "7", "8")

    def test_completed_l3_uses_native_entire_l(self):
        result = evaluate_completed_l3(
            self.runtime, input_ball=self.input_ball,
            precision_bits=192, evidence_factory=self.factory,
            segment_id="segment-1",
        )
        self.assertEqual(self.runtime.native_l_character, (3, 2))
        self.assertEqual(self.runtime.calls, [
            "pi_ball", "real_log", "complex_exp", "complex_gamma",
            "native_dirichlet_l", "multiply",
        ])
        self.assertEqual(result.value, ComplexBallRecord("1", "2", "3", "4"))

    def test_completed_l3_rejects_wrong_character_metadata(self):
        self.runtime.character_metadata["modulus"] = "5"
        with self.assertRaises(InconclusiveRealEvaluation):
            evaluate_completed_l3(self.runtime, input_ball=self.input_ball,
                                  precision_bits=192, evidence_factory=self.factory)

    def test_completed_l3_rejects_low_effective_precision(self):
        self.runtime.effective_precision_bits = 128
        with self.assertRaises(InconclusiveRealEvaluation):
            evaluate_completed_l3(self.runtime, input_ball=self.input_ball,
                                  precision_bits=192, evidence_factory=self.factory)

    def test_completed_l3_rejects_nonfinite_native_l_ball(self):
        self.runtime.native_l_result = object()
        with self.assertRaises(InconclusiveRealEvaluation):
            evaluate_completed_l3(self.runtime, input_ball=self.input_ball,
                                  precision_bits=192, evidence_factory=self.factory)


if __name__ == "__main__":
    unittest.main()
