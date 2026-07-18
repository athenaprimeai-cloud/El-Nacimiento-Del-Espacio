from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

from .ball_argument import verify_exclusion
from .contour import bisect_segment
from .models import DirectedSegment, SegmentImageCertificate


class InconclusiveBoundaryCertification(RuntimeError):
    """A structural boundary segment cannot be certified zero-free."""


@dataclass(frozen=True)
class SegmentCover:
    segment: DirectedSegment
    depth: int
    ordinal: int


@dataclass(frozen=True)
class SegmentExclusionCertificate:
    segment: DirectedSegment
    image: SegmentImageCertificate
    zero_excluded: bool
    positive_separation_witness: str
    precision_bits: int
    depth: int


@dataclass(frozen=True)
class BoundarySegmentCertificate:
    segment: DirectedSegment
    certificates: tuple[SegmentExclusionCertificate, ...]

    @property
    def zero_excluded(self) -> bool:
        return bool(self.certificates) and all(item.zero_excluded for item in self.certificates)

    @property
    def subdivision_count(self) -> int:
        return len(self.certificates)


def subdivide_segment_cover(segment: DirectedSegment, *, depth: int) -> tuple[SegmentCover, ...]:
    if depth < 0:
        raise ValueError("depth must be nonnegative")
    segments = (segment,)
    for _ in range(depth):
        next_segments = []
        for current in segments:
            first, second = bisect_segment(current)
            next_segments.extend((first, second))
        segments = tuple(next_segments)
    return tuple(
        SegmentCover(segment=current, depth=depth, ordinal=index)
        for index, current in enumerate(segments)
    )


def _axis_gap(lower: str, upper: str) -> Decimal:
    low = Decimal(lower)
    high = Decimal(upper)
    if high < 0:
        return -high
    if low > 0:
        return low
    return Decimal("0")


def _separation_witness(image: SegmentImageCertificate) -> str:
    real_gap = _axis_gap(image.enclosure_real.lower, image.enclosure_real.upper)
    imag_gap = _axis_gap(image.enclosure_imag.lower, image.enclosure_imag.upper)
    witness = max(real_gap, imag_gap)
    if witness <= 0:
        raise InconclusiveBoundaryCertification("segment image may contain zero")
    return str(witness)


def _certify_piece(backend, cover: SegmentCover, precision_bits: int) -> SegmentExclusionCertificate:
    image = backend.completed_l3_segment(cover.segment, precision_bits)
    if image.segment != cover.segment:
        raise InconclusiveBoundaryCertification("segment image identity mismatch")
    if not verify_exclusion(image):
        raise InconclusiveBoundaryCertification("segment image is not certified zero-free")
    return SegmentExclusionCertificate(
        segment=cover.segment,
        image=image,
        zero_excluded=True,
        positive_separation_witness=_separation_witness(image),
        precision_bits=precision_bits,
        depth=cover.depth,
    )


def certify_boundary_segment(
    backend,
    segment: DirectedSegment,
    *,
    precision_bits: int,
    max_depth: int,
) -> BoundarySegmentCertificate:
    if max_depth < 0:
        raise ValueError("max_depth must be nonnegative")
    last_error: Exception | None = None
    for depth in range(max_depth + 1):
        certificates: list[SegmentExclusionCertificate] = []
        try:
            for cover in subdivide_segment_cover(segment, depth=depth):
                certificates.append(_certify_piece(backend, cover, precision_bits))
            return BoundarySegmentCertificate(segment=segment, certificates=tuple(certificates))
        except InconclusiveBoundaryCertification as exc:
            last_error = exc
    raise InconclusiveBoundaryCertification("boundary segment could not exclude zero") from last_error
