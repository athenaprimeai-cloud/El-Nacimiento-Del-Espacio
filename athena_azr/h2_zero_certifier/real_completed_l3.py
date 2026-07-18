from __future__ import annotations

from .chi3_function import validate_chi3_metadata
from .real_evidence import ComplexBallRecord, RealEvidenceFactory
from .rigorous_ball_runtime import UnsupportedBallSemantics, audit_runtime_semantics


class InconclusiveRealEvaluation(RuntimeError):
    """The injected ball runtime cannot certify a completed L3 evaluation."""


def evaluate_completed_l3(runtime, *, input_ball: ComplexBallRecord,
                          precision_bits: int,
                          evidence_factory: RealEvidenceFactory,
                          segment_id: str = ""):
    try:
        audit_runtime_semantics(runtime)
        validate_chi3_metadata(runtime.character_metadata)
    except (UnsupportedBallSemantics, ValueError) as exc:
        raise InconclusiveRealEvaluation(str(exc)) from exc
    if runtime.effective_precision_bits < precision_bits:
        raise InconclusiveRealEvaluation("effective precision is below the request")

    pi_value = runtime.pi_ball(precision_bits)
    base = runtime.divide_exact_integer(3, pi_value, precision_bits)
    log_base = runtime.real_log(base, precision_bits)
    exponent = runtime.scale_and_shift_exponent(input_ball, log_base, precision_bits)
    power = runtime.complex_exp(exponent, precision_bits)
    gamma_arg = runtime.affine_half_plus_half(input_ball, precision_bits)
    gamma_value = runtime.complex_gamma(gamma_arg, precision_bits)
    l_value = runtime.native_dirichlet_l(
        input_ball, modulus=3, conrey_number=2, precision_bits=precision_bits
    )
    if not runtime.is_finite_ball(l_value):
        raise InconclusiveRealEvaluation("native L evaluation is not finite")
    product = runtime.multiply(power, gamma_value, l_value, precision_bits=precision_bits)
    if not isinstance(product, ComplexBallRecord) or not runtime.is_finite_ball(product):
        raise InconclusiveRealEvaluation("completed L3 product is not a finite complex ball")
    return evidence_factory.completed_l3_point(
        product, precision_bits=precision_bits, segment_id=segment_id
    )
