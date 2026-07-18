import unittest

from athena_azr.h2_zero_certifier.real_argument import (
    InconclusiveRealArgument,
    accumulate_real_winding,
    certify_real_half_plane,
    real_argument_increment,
)
from athena_azr.h2_zero_certifier.real_evidence import (
    ComplexBallRecord,
    InvalidRealEvidence,
    RealBallRecord,
    RealEvidenceFactory,
)


class ArgumentRuntime:
    def __init__(self):
        self.rotated_real_interval = ("10", "20")
        self.pi_requests = []
        self.log_branch_certified = True

    def rotate_complex_ball(self, value, real, imag, precision_bits): return value
    def real_interval(self, value): return self.rotated_real_interval
    def complex_log(self, value, precision_bits): return value
    def certifies_principal_log(self, value): return self.log_branch_certified
    def subtract(self, left, right, precision_bits): return left
    def imaginary_interval(self, value): return ("1.56", "1.58")
    def sum_real_balls(self, values, precision_bits): return RealBallRecord("6.24", "6.32")
    def pi_ball(self, precision_bits): self.pi_requests.append(precision_bits); return RealBallRecord("3.1415", "3.1416")
    def divide_by_two_pi(self, value, pi_ball, precision_bits): return RealBallRecord("0.99", "1.01")


class H2RealArgumentTests(unittest.TestCase):
    def setUp(self):
        self.factory = RealEvidenceFactory("fake", "a" * 64, "b" * 64)
        self.segment = self.factory.segment_image(
            value=ComplexBallRecord("2", "3", "4", "5"),
            segment_id="segment-1", precision_bits=192,
        )
        self.start = self.factory.completed_l3_point(
            ComplexBallRecord("2", "3", "4", "5"),
            precision_bits=192, segment_id="segment-1",
        )
        self.end = self.factory.completed_l3_point(
            ComplexBallRecord("3", "4", "5", "6"),
            precision_bits=192, segment_id="segment-1",
        )

    def test_nearest_rectangle_rotation_is_certified(self):
        result = certify_real_half_plane(ArgumentRuntime(), self.segment, 192, self.factory)
        self.assertEqual((result.rotation_real, result.rotation_imag), ("2", "-4"))

    def test_half_plane_is_inconclusive_if_delta_touches_zero(self):
        runtime = ArgumentRuntime()
        runtime.rotated_real_interval = ("0", "20")
        with self.assertRaises(InconclusiveRealArgument):
            certify_real_half_plane(runtime, self.segment, 192, self.factory)

    def test_argument_increment_preserves_parent_identity(self):
        runtime = ArgumentRuntime()
        half_plane = certify_real_half_plane(runtime, self.segment, 192, self.factory)
        result = real_argument_increment(
            runtime, half_plane=half_plane, start_value=self.start,
            end_value=self.end, precision_bits=192, evidence_factory=self.factory,
        )
        self.assertEqual(result.half_plane.digest, half_plane.digest)

    def test_argument_increment_rejects_foreign_endpoint(self):
        runtime = ArgumentRuntime()
        half_plane = certify_real_half_plane(runtime, self.segment, 192, self.factory)
        foreign = self.factory.completed_l3_point(
            ComplexBallRecord("1", "2", "1", "2"),
            precision_bits=192, segment_id="foreign",
        )
        with self.assertRaises(InvalidRealEvidence):
            real_argument_increment(
                runtime, half_plane=half_plane, start_value=foreign,
                end_value=self.end, precision_bits=192, evidence_factory=self.factory,
            )

    def test_argument_increment_rejects_uncertified_log_branch(self):
        runtime = ArgumentRuntime()
        runtime.log_branch_certified = False
        half_plane = certify_real_half_plane(runtime, self.segment, 192, self.factory)
        with self.assertRaises(InconclusiveRealArgument):
            real_argument_increment(
                runtime, half_plane=half_plane, start_value=self.start,
                end_value=self.end, precision_bits=192,
                evidence_factory=self.factory,
            )

    def test_argument_increment_rejects_mixed_precision_evidence(self):
        runtime = ArgumentRuntime()
        half_plane = certify_real_half_plane(runtime, self.segment, 192, self.factory)
        low_precision = self.factory.completed_l3_point(
            ComplexBallRecord("1", "2", "1", "2"),
            precision_bits=128, segment_id="segment-1",
        )
        with self.assertRaises(InvalidRealEvidence):
            real_argument_increment(
                runtime, half_plane=half_plane, start_value=low_precision,
                end_value=self.end, precision_bits=192,
                evidence_factory=self.factory,
            )

    def test_real_winding_uses_runtime_pi_ball(self):
        runtime = ArgumentRuntime()
        half_plane = certify_real_half_plane(runtime, self.segment, 192, self.factory)
        increment = real_argument_increment(
            runtime, half_plane=half_plane, start_value=self.start,
            end_value=self.end, precision_bits=192, evidence_factory=self.factory,
        )
        result = accumulate_real_winding(runtime, (increment,) * 4, 192, self.factory)
        self.assertEqual(result.winding_number, 1)
        self.assertEqual(runtime.pi_requests, [192])

    def test_real_winding_rejects_ambiguous_integer_ball(self):
        runtime = ArgumentRuntime()
        runtime.divide_by_two_pi = lambda value, pi, precision: RealBallRecord("0.9", "2.1")
        half_plane = certify_real_half_plane(runtime, self.segment, 192, self.factory)
        increment = real_argument_increment(
            runtime, half_plane=half_plane, start_value=self.start,
            end_value=self.end, precision_bits=192, evidence_factory=self.factory,
        )
        with self.assertRaises(InconclusiveRealArgument):
            accumulate_real_winding(runtime, (increment,), 192, self.factory)

    def test_real_winding_rejects_mixed_precision_increments(self):
        runtime = ArgumentRuntime()
        half_plane = certify_real_half_plane(runtime, self.segment, 192, self.factory)
        increment = real_argument_increment(
            runtime, half_plane=half_plane, start_value=self.start,
            end_value=self.end, precision_bits=192, evidence_factory=self.factory,
        )
        other_segment = self.factory.segment_image(
            value=ComplexBallRecord("2", "3", "4", "5"),
            segment_id="segment-2", precision_bits=128,
        )
        other_half_plane = certify_real_half_plane(
            runtime, other_segment, 128, self.factory,
        )
        other_increment = self.factory.argument_increment(
            other_half_plane, "1.56", "1.58",
        )
        with self.assertRaises(InvalidRealEvidence):
            accumulate_real_winding(
                runtime, (increment, other_increment), 192, self.factory,
            )


if __name__ == "__main__":
    unittest.main()
