from __future__ import annotations

from typing import Mapping, Protocol
from .models import (
    ComplexBox,
    CountCertificate,
    RealInterval,
    RationalComplexPoint,
    DirectedSegment,
    SegmentImageCertificate,
    ArgumentIncrementCertificate,
    HalfPlaneCertificate,
)
from .real_evidence import (
    RealCompletedL3PointEvidence,
    RealSegmentImageEvidence,
)


class BallBackend(Protocol):
    def metadata(self) -> Mapping[str, str]: ...

    def chi3_metadata(self) -> Mapping[str, str]: ...

    def zeta_zero(self, index: int, precision_bits: int) -> ComplexBox: ...

    def zeta_count_certificate(
        self, requested_height: int, precision_bits: int
    ) -> CountCertificate: ...

    # Completed L3 Argument Principle backend contracts
    def completed_l3_point(self, point: RationalComplexPoint, precision_bits: int) -> ComplexBox: ...

    def completed_l3_segment(
        self, segment: DirectedSegment, precision_bits: int
    ) -> SegmentImageCertificate: ...

    def validate_half_plane(
        self,
        segment_certificate: SegmentImageCertificate,
        precision_bits: int,
    ) -> HalfPlaneCertificate: ...

    def argument_increment(
        self, half_plane_certificate: HalfPlaneCertificate, precision_bits: int
    ) -> ArgumentIncrementCertificate: ...

    def unique_integer(self, interval_lower: str, interval_upper: str) -> int: ...

    # L3 box winding count (which uses the above routines internally)
    def l3_box_winding_count(self, box: ComplexBox, precision_bits: int) -> int: ...

    def l3_critical_line_certified(
        self, box: ComplexBox, precision_bits: int
    ) -> bool: ...

    def l3_count_certificate(
        self, requested_height: int, precision_bits: int
    ) -> CountCertificate: ...

    def real_completed_l3_point(
        self, point, precision_bits: int
    ) -> RealCompletedL3PointEvidence: ...

    def real_completed_l3_segment(
        self, segment: DirectedSegment, precision_bits: int
    ) -> RealSegmentImageEvidence: ...
