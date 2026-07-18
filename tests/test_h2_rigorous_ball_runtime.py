import unittest

from athena_azr.h2_zero_certifier.rigorous_ball_runtime import (
    RigorousBallRuntime,
    UnsupportedBallSemantics,
    audit_runtime_semantics,
)


class SemanticsRuntime:
    def __init__(self, *, full_ball=True):
        self.full_ball = full_ball

    def audit_ball_semantics(self):
        return {
            "supports_nonzero_radius": self.full_ball,
            "outward_rounded": True,
            "native_entire_dirichlet_l": True,
            "whole_box_evaluation": True,
            "rigorous_complex_log": True,
        }


class H2RigorousBallRuntimeTests(unittest.TestCase):
    def test_protocol_declares_every_probative_ball_operation(self):
        required = {
            "complex_ball",
            "pi_ball",
            "divide_exact_integer",
            "real_log",
            "scale_and_shift_exponent",
            "affine_half_plus_half",
            "complex_exp",
            "complex_gamma",
            "native_dirichlet_l",
            "multiply",
            "rotate_complex_ball",
            "complex_log",
            "subtract",
            "imaginary_interval",
            "real_interval",
            "sum_real_balls",
            "divide_by_two_pi",
            "certifies_whole_box",
            "certifies_principal_log",
            "is_finite_ball",
            "audit_ball_semantics",
        }
        self.assertTrue(required.issubset(RigorousBallRuntime.__dict__))

    def test_runtime_audit_accepts_all_required_semantics(self):
        audit_runtime_semantics(SemanticsRuntime())

    def test_runtime_audit_rejects_midpoint_only_semantics(self):
        with self.assertRaises(UnsupportedBallSemantics):
            audit_runtime_semantics(SemanticsRuntime(full_ball=False))


if __name__ == "__main__":
    unittest.main()
