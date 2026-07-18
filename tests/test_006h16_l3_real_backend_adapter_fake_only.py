import builtins
import sys
import unittest
from dataclasses import replace
from unittest.mock import patch

from athena_azr.h2_zero_certifier.chi3_function import CHI3_METADATA


MATCHING_HASHES = {
    "python_executable_sha256": "a" * 64,
    "libflint_sha256": "b" * 64,
    "arb_extension_sha256": "c" * 64,
    "acb_extension_sha256": "d" * 64,
    "dirichlet_extension_sha256": "e" * 64,
}

MATCHING_SEAL = {
    "python_flint_distribution_version": "0.8.0",
    "flint_module_version": "0.8.0",
    "FLINT_native_version": "3.3.1",
    **MATCHING_HASHES,
}


class FakePrecisionScope:
    def __init__(self, ctx, bits):
        self.ctx = ctx
        self.bits = bits
        self.previous = None

    def __enter__(self):
        self.previous = self.ctx.precision_bits
        self.ctx.precision_bits = self.ctx.effective_bits or self.bits
        return self

    def __exit__(self, exc_type, exc, tb):
        if self.ctx.restore_on_exit:
            self.ctx.precision_bits = self.previous
        return False


class FakeCtx:
    def __init__(self):
        self.precision_bits = 53
        self.effective_bits = None
        self.restore_on_exit = True

    def workprec(self, bits):
        return FakePrecisionScope(self, bits)


class FakeBall:
    def __init__(
        self,
        kind,
        payload,
        *,
        finite=True,
        contains_zero=False,
        abs_lower="1",
        whole_box=False,
        precision_bits=192,
    ):
        self.kind = kind
        self.payload = dict(payload)
        self.finite = finite
        self.contains_zero = contains_zero
        self.abs_lower = abs_lower
        self.whole_box = whole_box
        self.precision_bits = precision_bits

    def evidence_payload(self):
        return {
            "abs_lower": self.abs_lower,
            "contains_zero": self.contains_zero,
            "finite": self.finite,
            "kind": self.kind,
            "payload": self.payload,
            "precision_bits": self.precision_bits,
            "whole_box": self.whole_box,
        }


class FakeFmpq:
    def __init__(self, numerator, denominator):
        self.numerator = numerator
        self.denominator = denominator

    def evidence_payload(self):
        return {"numerator": self.numerator, "denominator": self.denominator}


class FakeCharacter:
    def __init__(self, *, bad_metadata=False):
        self.metadata = dict(CHI3_METADATA)
        if bad_metadata:
            self.metadata["modulus"] = "5"
        self.l_function_called = False

    def l_function(self, _s):
        self.l_function_called = True
        raise AssertionError("chi.l_function must not be called")


class FakeAcbNamespace:
    def __init__(self, runtime):
        self.runtime = runtime

    def dirichlet_l(self, s, chi):
        self.runtime.calls.append(("acb.dirichlet_l", s, chi))
        return self.runtime.make_ball("native_dirichlet_l", {"input": s.evidence_payload()})

    def zeta(self, s, a=None):
        self.runtime.calls.append(("acb.zeta", s, a))
        payload = {"input": s.evidence_payload(), "a": a.evidence_payload()}
        return self.runtime.make_ball("hurwitz_zeta", payload)

    def log(self, value, analytic=False):
        self.runtime.calls.append(("acb.log", value, analytic))
        return self.runtime.make_ball(
            "complex_log_analytic",
            {"input": value.evidence_payload(), "analytic": analytic},
        )


class FakeFlintRuntime:
    __version__ = "0.8.0"

    def __init__(self):
        self.ctx = FakeCtx()
        self.acb = FakeAcbNamespace(self)
        self.calls = []
        self.bad_character = False
        self.nonfinite_operations = set()
        self.contains_zero_result = False
        self.abs_lower_result = "1"
        self.contains_zero_available = True

    def make_ball(self, kind, payload, *, whole_box=False):
        return FakeBall(
            kind,
            payload,
            finite=kind not in self.nonfinite_operations,
            contains_zero=self.contains_zero_result,
            abs_lower=self.abs_lower_result,
            whole_box=whole_box,
            precision_bits=self.ctx.precision_bits,
        )

    def fmpq(self, numerator, denominator):
        self.calls.append(("fmpq", numerator, denominator))
        return FakeFmpq(numerator, denominator)

    def arb(self, value):
        self.calls.append(("arb", value))
        if isinstance(value, FakeFmpq):
            payload = value.evidence_payload()
            kind = "arb_rational"
        else:
            payload = {"value": str(value)}
            kind = "arb_exact"
        return self.make_ball(kind, payload)

    def real_interval(self, lower, upper):
        self.calls.append(("real_interval", lower, upper))
        return self.make_ball(
            "real_interval",
            {"lower": lower.evidence_payload(), "upper": upper.evidence_payload()},
        )

    def complex_box(self, real_interval, imag_interval):
        self.calls.append(("complex_box", real_interval, imag_interval))
        return self.make_ball(
            "complex_box",
            {
                "real": real_interval.evidence_payload(),
                "imag": imag_interval.evidence_payload(),
            },
            whole_box=True,
        )

    def pi(self):
        self.calls.append(("arb.pi", self.ctx.precision_bits))
        return self.make_ball("pi", {"precision": self.ctx.precision_bits})

    def real_log(self, value):
        self.calls.append(("arb.log", value))
        return self.make_ball("real_log", {"input": value.evidence_payload()})

    def complex_exp(self, value):
        self.calls.append(("acb.exp", value))
        return self.make_ball("complex_exp", {"input": value.evidence_payload()})

    def complex_gamma(self, value):
        self.calls.append(("acb.gamma", value))
        return self.make_ball("complex_gamma", {"input": value.evidence_payload()})

    def complex_multiply(self, *values):
        self.calls.append(("acb.mul", values))
        return self.make_ball(
            "complex_multiply",
            {"inputs": [value.evidence_payload() for value in values]},
        )

    def complex_subtract(self, left, right):
        self.calls.append(("acb.sub", left, right))
        return self.make_ball(
            "complex_subtract",
            {"left": left.evidence_payload(), "right": right.evidence_payload()},
        )

    def complex_divide(self, numerator, denominator):
        self.calls.append(("acb.div", numerator, denominator))
        return self.make_ball(
            "complex_divide",
            {
                "numerator": numerator.evidence_payload(),
                "denominator": denominator.evidence_payload(),
            },
        )

    def real_ball_sum(self, values):
        self.calls.append(("arb.sum", values))
        return self.make_ball(
            "real_ball_sum",
            {"inputs": [value.evidence_payload() for value in values]},
        )

    def affine_half_plus_half(self, value):
        self.calls.append(("affine_half_plus_half", value))
        return self.make_ball("gamma_arg", {"input": value.evidence_payload()})

    def power_base_3_over_pi(self, pi_value):
        self.calls.append(("real_divide", 3, pi_value))
        return self.make_ball("3_over_pi", {"pi": pi_value.evidence_payload()})

    def dirichlet_char(self, modulus, number):
        self.calls.append(("dirichlet_char", modulus, number))
        return FakeCharacter(bad_metadata=self.bad_character)

    def contains_zero(self, value):
        self.calls.append(("contains_zero", value))
        if not self.contains_zero_available:
            return None
        return self.contains_zero_result

    def abs_lower(self, value):
        self.calls.append(("abs_lower", value))
        return self.make_ball("abs_lower", {"input": value.evidence_payload()})

    def is_finite(self, value):
        self.calls.append(("is_finite", value))
        return bool(getattr(value, "finite", False))


class H006H16L3RealBackendAdapterFakeOnlyTests(unittest.TestCase):
    def setUp(self):
        sys.modules.pop("flint", None)
        self.runtime = FakeFlintRuntime()

    def backend(self, **kwargs):
        from athena_azr.h2_zero_certifier.python_flint_backend import PythonFlintBackend

        return PythonFlintBackend.from_fake_runtime(
            self.runtime,
            runtime_seal=kwargs.pop("runtime_seal", MATCHING_SEAL),
            expected_binary_hashes=kwargs.pop("expected_hashes", MATCHING_HASHES),
            **kwargs,
        )

    def assertFailureState(self, state, callable_, *args, **kwargs):
        from athena_azr.h2_zero_certifier.python_flint_backend import RealBackendFailure

        with self.assertRaises(RealBackendFailure) as raised:
            callable_(*args, **kwargs)
        self.assertEqual(raised.exception.state, state)

    def test_lazy_import_guard_and_fake_runtime_do_not_import_flint(self):
        real_import = builtins.__import__

        def guarded_import(name, *args, **kwargs):
            if name == "flint" or name.startswith("flint."):
                raise AssertionError("FLINT import attempted")
            return real_import(name, *args, **kwargs)

        with patch("builtins.__import__", side_effect=guarded_import):
            from athena_azr.h2_zero_certifier import python_flint_backend

            backend = self.backend()

        self.assertTrue(backend.initialized)
        self.assertFalse(python_flint_backend.FLINT_REAL_IMPORT_ATTEMPTED)
        self.assertNotIn("flint", sys.modules)

    def test_canonical_inputs_are_accepted_and_float_is_rejected_before_runtime(self):
        backend = self.backend()

        integer = backend.construct_exact_real("1", precision_bits=192)
        rational = backend.construct_exact_real("1/3", precision_bits=192)
        decimal = backend.construct_exact_real("-0.5", precision_bits=192)

        self.assertEqual(integer.evidence.operation, "construct_exact_real")
        self.assertEqual(rational.value.kind, "arb_rational")
        self.assertEqual(decimal.value.kind, "arb_exact")
        self.assertFailureState("float_input_forbidden", backend.construct_exact_real, 1.0, precision_bits=192)
        self.assertFailureState("noncanonical_exact_input", backend.construct_exact_real, "1/1", precision_bits=192)

    def test_precision_context_restores_on_success_and_exception(self):
        backend = self.backend()

        with backend.precision_context(192) as evidence:
            self.assertEqual(self.runtime.ctx.precision_bits, 192)
            self.assertEqual(evidence["requested_precision_bits"], 192)
        self.assertEqual(self.runtime.ctx.precision_bits, 53)

        with self.assertRaises(RuntimeError):
            with backend.precision_context(192):
                raise RuntimeError("controlled")
        self.assertEqual(self.runtime.ctx.precision_bits, 53)

        self.runtime.ctx.effective_bits = 128
        self.assertFailureState("effective_precision_below_request", backend.pi_ball, precision_bits=192)

        self.runtime.ctx.effective_bits = None
        self.runtime.ctx.restore_on_exit = False
        self.assertFailureState("precision_context_not_restored", backend.pi_ball, precision_bits=192)

    def test_runtime_seal_validation_passes_and_deterministically_fails(self):
        backend = self.backend()
        seal = backend.validate_runtime_seal()
        self.assertEqual(seal["python_flint_distribution_version"], "0.8.0")
        self.assertEqual(len(backend.runtime_seal_id), 64)

        version_mismatch = dict(MATCHING_SEAL)
        version_mismatch["FLINT_native_version"] = "3.3.0"
        self.assertFailureState(
            "backend_version_mismatch",
            self.backend(runtime_seal=version_mismatch).validate_runtime_seal,
        )

        missing_hash = dict(MATCHING_SEAL)
        missing_hash.pop("acb_extension_sha256")
        self.assertFailureState(
            "runtime_hash_mismatch",
            self.backend(runtime_seal=missing_hash).validate_runtime_seal,
        )

        bad_hash = dict(MATCHING_SEAL)
        bad_hash["libflint_sha256"] = "f" * 64
        self.assertFailureState(
            "runtime_hash_mismatch",
            self.backend(runtime_seal=bad_hash).validate_runtime_seal,
        )

    def test_chi3_validation_uses_conrey_2_without_group_indexing_or_l_function(self):
        backend = self.backend()
        character = backend.character_chi3(precision_bits=192)

        self.assertEqual(character.metadata["modulus"], "3")
        self.assertEqual(character.metadata["number"], "2")
        self.assertIn(("dirichlet_char", 3, 2), self.runtime.calls)
        self.assertFalse(character.raw.l_function_called)

        self.runtime.bad_character = True
        self.assertFailureState("character_metadata_mismatch", backend.character_chi3, precision_bits=192)

    def test_native_l_uses_acb_dirichlet_l_whole_box_and_rejects_bad_inputs(self):
        backend = self.backend()
        box = backend.construct_complex_box("0", "1", "2", "3", precision_bits=192)
        native = backend.native_dirichlet_l(box, precision_bits=192)

        self.assertEqual(native.evidence.operation, "native_dirichlet_l")
        self.assertTrue(native.evidence.whole_box)
        self.assertEqual([call[0] for call in self.runtime.calls].count("acb.dirichlet_l"), 1)
        self.assertNotIn("flint", sys.modules)

        point_like = replace(box, evidence=replace(box.evidence, whole_box=False))
        self.assertFailureState("whole_box_semantics_missing", backend.native_dirichlet_l, point_like, precision_bits=192)

        tampered = replace(box, evidence=replace(box.evidence, digest="0" * 64))
        self.assertFailureState("parent_evidence_mismatch", backend.native_dirichlet_l, tampered, precision_bits=192)

        self.runtime.nonfinite_operations.add("native_dirichlet_l")
        self.assertFailureState("nonfinite_ball", backend.native_dirichlet_l, box, precision_bits=192)

    def test_hurwitz_control_uses_acb_zeta_as_control_only(self):
        backend = self.backend()
        box = backend.construct_complex_box("0", "1", "2", "3", precision_bits=192)
        control = backend.hurwitz_control(box, precision_bits=192)

        zeta_calls = [call for call in self.runtime.calls if call[0] == "acb.zeta"]
        self.assertEqual(len(zeta_calls), 2)
        self.assertEqual(control.evidence.operation, "hurwitz_control")
        self.assertTrue(backend.HURWITZ_CHANNEL_IS_CONTROL_ONLY)
        self.assertFalse(backend.NATIVE_AND_HURWITZ_INDEPENDENT)

    def test_lambda3_composition_records_dataflow_and_failure_states(self):
        backend = self.backend()
        box = backend.construct_complex_box("0", "1", "2", "3", precision_bits=192)
        result = backend.completed_lambda3(box, precision_bits=192)

        operations = [call[0] for call in self.runtime.calls]
        self.assertIn("arb.pi", operations)
        self.assertIn("arb.log", operations)
        self.assertIn("acb.exp", operations)
        self.assertIn("acb.gamma", operations)
        self.assertIn("acb.dirichlet_l", operations)
        self.assertEqual(result.evidence.operation, "completed_lambda3")
        self.assertEqual(len(result.evidence.parent_evidence_hashes), 3)

        self.runtime.nonfinite_operations.add("complex_exp")
        self.assertFailureState("nonfinite_ball", backend.completed_lambda3, box, precision_bits=192)

    def test_whole_box_propagation_preserves_exact_rectangular_hull(self):
        backend = self.backend()
        box = backend.construct_complex_box(
            "-1/2",
            "3/2",
            "0",
            "143",
            precision_bits=192,
        )

        self.assertTrue(box.evidence.whole_box)
        self.assertEqual(box.evidence.details["real_lower"], "-1/2")
        self.assertEqual(box.evidence.details["real_upper"], "3/2")
        self.assertEqual(
            box.value.payload["real"]["payload"]["lower"]["payload"]["numerator"],
            -1,
        )
        self.assertEqual(
            box.value.payload["real"]["payload"]["lower"]["payload"]["denominator"],
            2,
        )
        self.assertEqual(box.value.payload["imag"]["payload"]["upper"]["payload"]["value"], "143")

    def test_zero_exclusion_requires_containment_and_positive_abs_lower(self):
        backend = self.backend()
        box = backend.construct_complex_box("0", "1", "2", "3", precision_bits=192)

        self.runtime.contains_zero_result = False
        self.runtime.abs_lower_result = "0.25"
        witness = backend.certify_origin_excluded(box, precision_bits=192)
        self.assertEqual(witness["status"], "origin_excluded")

        self.runtime.contains_zero_result = True
        self.runtime.abs_lower_result = "0"
        self.assertFailureState("origin_not_excluded", backend.certify_origin_excluded, box, precision_bits=192)

        self.runtime.contains_zero_result = False
        self.runtime.abs_lower_result = "0"
        self.assertFailureState("origin_not_excluded", backend.certify_origin_excluded, box, precision_bits=192)

        self.runtime.contains_zero_available = False
        self.assertFailureState("origin_not_excluded", backend.certify_origin_excluded, box, precision_bits=192)

    def test_analytic_log_requires_zero_and_branch_certificates(self):
        backend = self.backend()
        box = backend.construct_complex_box("0", "1", "2", "3", precision_bits=192)

        self.assertFailureState(
            "principal_log_branch_not_certified",
            backend.complex_log_analytic,
            box,
            precision_bits=192,
        )

        branch = {
            "origin_excluded": True,
            "branch_domain_certified": True,
            "branch_relation": "right_half_plane",
        }
        logged = backend.complex_log_analytic(box, precision_bits=192, branch_certificate=branch)
        self.assertEqual(logged.evidence.operation, "complex_log_analytic")
        self.assertIn(("acb.log", box.value, True), self.runtime.calls)

    def test_evidence_is_canonical_and_failure_states_are_registered(self):
        from athena_azr.h2_zero_certifier.python_flint_backend import FAILURE_STATES

        backend = self.backend()
        box = backend.construct_complex_box("0", "1", "2", "3", precision_bits=192)
        encoded = box.evidence.canonical_json()

        self.assertTrue(encoded.endswith("\n"))
        self.assertNotIn("FakeBall object at", encoded)
        for state in (
            "authorization_missing",
            "runtime_missing",
            "runtime_mismatch",
            "backend_version_mismatch",
            "runtime_hash_mismatch",
            "character_metadata_mismatch",
            "effective_precision_below_request",
            "precision_context_not_restored",
            "precision_context_unavailable",
            "noncanonical_exact_input",
            "float_input_forbidden",
            "whole_box_semantics_missing",
            "nonfinite_ball",
            "origin_not_excluded",
            "principal_log_branch_not_certified",
            "native_L_semantics_unavailable",
            "hurwitz_control_unavailable",
            "parent_evidence_mismatch",
            "scope_or_semantic_leak",
        ):
            self.assertIn(state, FAILURE_STATES)


if __name__ == "__main__":
    unittest.main()
