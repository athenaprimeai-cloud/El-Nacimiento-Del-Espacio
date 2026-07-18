from __future__ import annotations

from decimal import Decimal, ROUND_CEILING, ROUND_FLOOR

from .real_evidence import (
    InvalidRealEvidence,
    RealArgumentIncrementEvidence,
    RealBallRecord,
    RealCompletedL3PointEvidence,
    RealEvidenceFactory,
    RealHalfPlaneEvidence,
    RealSegmentImageEvidence,
)


class InconclusiveRealArgument(RuntimeError):
    """A rigorous argument branch or unique winding cannot be certified."""


def _nearest(lower: str, upper: str) -> Decimal:
    low = Decimal(lower)
    high = Decimal(upper)
    if low > 0:
        return low
    if high < 0:
        return high
    return Decimal(0)


def certify_real_half_plane(runtime, segment: RealSegmentImageEvidence,
                            precision_bits: int,
                            evidence_factory: RealEvidenceFactory) -> RealHalfPlaneEvidence:
    if segment.precision_bits != precision_bits:
        raise InvalidRealEvidence("half-plane precision does not match segment evidence")
    q_real = _nearest(segment.value.real_lower, segment.value.real_upper)
    q_imag = _nearest(segment.value.imag_lower, segment.value.imag_upper)
    if q_real == 0 and q_imag == 0:
        raise InconclusiveRealArgument("segment image can contain zero")
    rotation_real = str(q_real)
    rotation_imag = str(-q_imag)
    rotated = runtime.rotate_complex_ball(
        segment.value, rotation_real, rotation_imag, precision_bits
    )
    lower, _ = runtime.real_interval(rotated)
    if Decimal(lower) <= 0:
        raise InconclusiveRealArgument("rotated image is not strictly in the right half-plane")
    return evidence_factory.half_plane(
        segment=segment, rotation_real=rotation_real,
        rotation_imag=rotation_imag, rotated_real_lower=lower,
    )


def real_argument_increment(runtime, *, half_plane: RealHalfPlaneEvidence,
                            start_value: RealCompletedL3PointEvidence,
                            end_value: RealCompletedL3PointEvidence,
                            precision_bits: int,
                            evidence_factory: RealEvidenceFactory) -> RealArgumentIncrementEvidence:
    if any(item.precision_bits != precision_bits for item in (
        half_plane, start_value, end_value,
    )):
        raise InvalidRealEvidence("argument evidence uses mixed precision")
    segment_id = half_plane.segment.segment_id
    if start_value.segment_id != segment_id or end_value.segment_id != segment_id:
        raise InvalidRealEvidence("argument endpoint belongs to another segment")
    start = runtime.rotate_complex_ball(
        start_value.value, half_plane.rotation_real,
        half_plane.rotation_imag, precision_bits,
    )
    end = runtime.rotate_complex_ball(
        end_value.value, half_plane.rotation_real,
        half_plane.rotation_imag, precision_bits,
    )
    if runtime.certifies_principal_log(start) is not True:
        raise InconclusiveRealArgument("start endpoint lacks a certified log branch")
    if runtime.certifies_principal_log(end) is not True:
        raise InconclusiveRealArgument("end endpoint lacks a certified log branch")
    start_log = runtime.complex_log(start, precision_bits)
    end_log = runtime.complex_log(end, precision_bits)
    difference = runtime.subtract(end_log, start_log, precision_bits)
    lower, upper = runtime.imaginary_interval(difference)
    return evidence_factory.argument_increment(half_plane, lower, upper)


def accumulate_real_winding(runtime,
                            increments: tuple[RealArgumentIncrementEvidence, ...],
                            precision_bits: int,
                            evidence_factory: RealEvidenceFactory):
    if not increments or not all(isinstance(item, RealArgumentIncrementEvidence) for item in increments):
        raise InvalidRealEvidence("real winding requires real argument evidence")
    if any(item.precision_bits != precision_bits for item in increments):
        raise InvalidRealEvidence("winding evidence uses mixed precision")
    total = runtime.sum_real_balls(
        [item.delta_ball for item in increments], precision_bits
    )
    pi_ball = runtime.pi_ball(precision_bits)
    winding_ball = runtime.divide_by_two_pi(total, pi_ball, precision_bits)
    if not isinstance(winding_ball, RealBallRecord):
        raise InconclusiveRealArgument("runtime did not return a real winding ball")
    lower = Decimal(winding_ball.lower)
    upper = Decimal(winding_ball.upper)
    first = int(lower.to_integral_value(rounding=ROUND_CEILING))
    last = int(upper.to_integral_value(rounding=ROUND_FLOOR))
    if first != last or first < 0:
        raise InconclusiveRealArgument("winding ball has no unique nonnegative integer")
    return evidence_factory.winding(increments, winding_ball, first)
