from __future__ import annotations

from .models import RationalComplexPoint, DirectedSegment


def completed_l3_symbolic_formula() -> str:
    return "(3/pi)^((s+1)/2) * Gamma((s+1)/2) * L(s,chi_3)"


def completed_l3_point_inert(point: RationalComplexPoint, precision_bits: int) -> None:
    raise NotImplementedError("Real L3 evaluations are locked under 006F")


def completed_l3_segment_inert(segment: DirectedSegment, precision_bits: int) -> None:
    raise NotImplementedError("Real L3 evaluations are locked under 006F")
