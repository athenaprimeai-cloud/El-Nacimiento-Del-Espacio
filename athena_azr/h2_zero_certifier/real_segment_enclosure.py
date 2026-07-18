from __future__ import annotations

from decimal import Decimal

from .models import DirectedSegment
from .real_completed_l3 import InconclusiveRealEvaluation, evaluate_completed_l3
from .real_evidence import ComplexBallRecord, RealEvidenceFactory


class InconclusiveSegmentEnclosure(RuntimeError):
    """The full segment image cannot be enclosed by the injected runtime."""


def rectangular_hull(segment: DirectedSegment) -> ComplexBallRecord:
    return ComplexBallRecord(
        str(min(segment.start.real_decimal, segment.end.real_decimal)),
        str(max(segment.start.real_decimal, segment.end.real_decimal)),
        str(min(segment.start.imag_decimal, segment.end.imag_decimal)),
        str(max(segment.start.imag_decimal, segment.end.imag_decimal)),
    )


def _segment_id(segment: DirectedSegment) -> str:
    return (
        f"{segment.start.real},{segment.start.imag}->"
        f"{segment.end.real},{segment.end.imag}"
    )


def enclose_completed_l3_segment(runtime, segment: DirectedSegment,
                                 precision_bits: int,
                                 evidence_factory: RealEvidenceFactory):
    hull = rectangular_hull(segment)
    if Decimal(hull.real_lower) < Decimal("-0.5") or Decimal(hull.real_upper) > Decimal("1.5"):
        raise InconclusiveSegmentEnclosure("segment hull escapes the frozen real strip")
    try:
        point = evaluate_completed_l3(
            runtime, input_ball=hull, precision_bits=precision_bits,
            evidence_factory=evidence_factory, segment_id=_segment_id(segment),
        )
    except InconclusiveRealEvaluation as exc:
        raise InconclusiveSegmentEnclosure(str(exc)) from exc
    if runtime.certifies_whole_box(hull) is not True:
        raise InconclusiveSegmentEnclosure("runtime did not certify whole-box inclusion")
    return evidence_factory.segment_image(
        value=point.value, segment_id=_segment_id(segment),
        precision_bits=precision_bits,
    )
