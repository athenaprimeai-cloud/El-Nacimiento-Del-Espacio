from __future__ import annotations

from decimal import Decimal, ROUND_CEILING, ROUND_FLOOR
from typing import Sequence
from .ball_argument import InconclusiveArgument
from .contour import bisect_segment, validate_contour_orientation
from .models import (
    ArgumentIncrementCertificate,
    DirectedSegment,
    RectangularContour,
    WindingCertificate,
)


class InconclusiveWindingCount(RuntimeError):
    """The interval winding number cannot be resolved to a unique integer."""


# Safe rigorous bounds for Pi
PI_LOWER = Decimal("3.14159265358979323846264338327950")
PI_UPPER = Decimal("3.14159265358979323846264338327951")


def _certify_segment(
    backend,
    segment: DirectedSegment,
    *,
    precision_bits: int,
    depth: int,
    max_depth: int,
) -> list[ArgumentIncrementCertificate]:
    try:
        image = backend.completed_l3_segment(segment, precision_bits)
        if image.segment != segment:
            raise InconclusiveWindingCount("segment image certificate identity mismatch")
        half_plane = backend.validate_half_plane(image, precision_bits)
        if half_plane.segment_certificate != image:
            raise InconclusiveWindingCount("half-plane certificate identity mismatch")
        increment = backend.argument_increment(half_plane, precision_bits)
        if increment.half_plane_certificate != half_plane:
            raise InconclusiveWindingCount("argument increment certificate identity mismatch")
        return [increment]
    except InconclusiveArgument as exc:
        if depth >= max_depth:
            raise InconclusiveWindingCount(
                f"contour subdivision depth {max_depth} exhausted"
            ) from exc
        first, second = bisect_segment(segment)
        return _certify_segment(
            backend,
            first,
            precision_bits=precision_bits,
            depth=depth + 1,
            max_depth=max_depth,
        ) + _certify_segment(
            backend,
            second,
            precision_bits=precision_bits,
            depth=depth + 1,
            max_depth=max_depth,
        )


def count_contour_winding(
    backend,
    contour: RectangularContour,
    *,
    precision_bits: int,
    max_depth: int,
) -> WindingCertificate:
    if max_depth < 0:
        raise ValueError("max_depth must be nonnegative")
    validate_contour_orientation(contour)
    increments: list[ArgumentIncrementCertificate] = []
    for segment in contour.segments:
        increments.extend(
            _certify_segment(
                backend,
                segment,
                precision_bits=precision_bits,
                depth=0,
                max_depth=max_depth,
            )
        )
    return accumulate_winding(increments, precision_bits)


def accumulate_winding(
    certificates: Sequence[ArgumentIncrementCertificate],
    precision_bits: int,
) -> WindingCertificate:
    if not certificates:
        raise InconclusiveWindingCount("No argument increment certificates provided")

    # 1. Sum intervals Delta_ab in order
    sum_lower = Decimal("0")
    sum_upper = Decimal("0")

    for cert in certificates:
        sum_lower += Decimal(cert.delta_lower)
        sum_upper += Decimal(cert.delta_upper)

    # 2. Divide by 2 * pi
    # W = A / [2 * PI_LOWER, 2 * PI_UPPER]
    two_pi_l = 2 * PI_LOWER
    two_pi_u = 2 * PI_UPPER

    quotients = (
        sum_lower / two_pi_l,
        sum_lower / two_pi_u,
        sum_upper / two_pi_l,
        sum_upper / two_pi_u,
    )
    w_lower = min(quotients)
    w_upper = max(quotients)

    smallest_integer = int(w_lower.to_integral_value(rounding=ROUND_CEILING))
    largest_integer = int(w_upper.to_integral_value(rounding=ROUND_FLOOR))

    if smallest_integer != largest_integer or smallest_integer < 0:
        raise InconclusiveWindingCount(
            f"winding interval [{w_lower}, {w_upper}] does not contain exactly one nonnegative integer"
        )

    return WindingCertificate(
        winding_number=smallest_integer,
        winding_interval_lower=str(w_lower),
        winding_interval_upper=str(w_upper),
        working_precision_bits=precision_bits,
    )
