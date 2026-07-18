from __future__ import annotations

from decimal import Decimal
from types import MappingProxyType
from .models import RationalComplexPoint, DirectedSegment, RectangularContour


FROZEN_L3_HEIGHTS = (143, 200, 300, 500)
FROZEN_L3_SIGMA_LEFT = "-0.5"
FROZEN_L3_SIGMA_RIGHT = "1.5"
FROZEN_L3_BOTTOM_HEIGHT = "0"
BOUNDARY_MODE_EXACT_T = "exact_T_boundary"


def bisect_segment(segment: DirectedSegment) -> tuple[DirectedSegment, DirectedSegment]:
    midpoint = RationalComplexPoint(
        str((segment.start.real_decimal + segment.end.real_decimal) / 2),
        str((segment.start.imag_decimal + segment.end.imag_decimal) / 2),
    )
    return DirectedSegment(segment.start, midpoint), DirectedSegment(midpoint, segment.end)


def validate_contour_orientation(contour: RectangularContour) -> None:
    if contour.orientation != "positive":
        raise ValueError("Contour orientation must be declared positive")

    # 1. Verify segments are closed in a loop
    segs = contour.segments
    if len(segs) != 4:
        raise ValueError("RectangularContour must have exactly 4 segments")

    for i in range(4):
        curr_seg = segs[i]
        next_seg = segs[(i + 1) % 4]
        if curr_seg.end != next_seg.start:
            raise ValueError(
                f"Contour segments do not form a closed loop: segment {i} ends at {curr_seg.end} but segment {(i+1)%4} starts at {next_seg.start}"
            )

    # 1b. Verify segments are axis-aligned and perpendicular
    # seg0: horizontal (constant imag)
    # seg1: vertical (constant real)
    # seg2: horizontal (constant imag)
    # seg3: vertical (constant real)
    if segs[0].start.imag_decimal != segs[0].end.imag_decimal:
        raise ValueError("Segment 0 is not horizontal")
    if segs[1].start.real_decimal != segs[1].end.real_decimal:
        raise ValueError("Segment 1 is not vertical")
    if segs[2].start.imag_decimal != segs[2].end.imag_decimal:
        raise ValueError("Segment 2 is not horizontal")
    if segs[3].start.real_decimal != segs[3].end.real_decimal:
        raise ValueError("Segment 3 is not vertical")

    # 2. Check signed area (shoelace formula) for positive orientation
    # A > 0 means CCW
    x0, y0 = segs[0].start.real_decimal, segs[0].start.imag_decimal
    x1, y1 = segs[1].start.real_decimal, segs[1].start.imag_decimal
    x2, y2 = segs[2].start.real_decimal, segs[2].start.imag_decimal
    x3, y3 = segs[3].start.real_decimal, segs[3].start.imag_decimal


    # Signed area sum
    area = (
        (x0 * y1 - x1 * y0)
        + (x1 * y2 - x2 * y1)
        + (x2 * y3 - x3 * y2)
        + (x3 * y0 - x0 * y3)
    )

    if area <= 0:
        raise ValueError("Contour orientation must be positive (counter-clockwise)")


def build_rectangular_contour(
    sigma_left: str,
    sigma_right: str,
    t_bottom: str,
    t_top: str,
    *,
    custom_segments: tuple[DirectedSegment, DirectedSegment, DirectedSegment, DirectedSegment] | None = None,
) -> RectangularContour:
    if custom_segments is not None:
        contour = RectangularContour(custom_segments)
        validate_contour_orientation(contour)
        return contour

    if Decimal(sigma_left) >= Decimal(sigma_right):
        raise ValueError("sigma_left must be strictly below sigma_right")
    if Decimal(t_bottom) >= Decimal(t_top):
        raise ValueError("t_bottom must be strictly below t_top")

    # Standard positive CCW rectangular path:
    # 1. bottom edge: (sigma_left, t_bottom) -> (sigma_right, t_bottom)
    # 2. right edge:  (sigma_right, t_bottom) -> (sigma_right, t_top)
    # 3. top edge:    (sigma_right, t_top) -> (sigma_left, t_top)
    # 4. left edge:   (sigma_left, t_top) -> (sigma_left, t_bottom)

    p0 = RationalComplexPoint(sigma_left, t_bottom)
    p1 = RationalComplexPoint(sigma_right, t_bottom)
    p2 = RationalComplexPoint(sigma_right, t_top)
    p3 = RationalComplexPoint(sigma_left, t_top)

    seg0 = DirectedSegment(p0, p1)
    seg1 = DirectedSegment(p1, p2)
    seg2 = DirectedSegment(p2, p3)
    seg3 = DirectedSegment(p3, p0)

    contour = RectangularContour((seg0, seg1, seg2, seg3))
    validate_contour_orientation(contour)
    return contour


def build_frozen_l3_contour(
    height: int,
    *,
    boundary_mode: str = BOUNDARY_MODE_EXACT_T,
    allow_t_star: bool = False,
) -> RectangularContour:
    if height not in FROZEN_L3_HEIGHTS:
        raise ValueError("height is not authorized for frozen L3 contours")
    if boundary_mode != BOUNDARY_MODE_EXACT_T or allow_t_star:
        raise ValueError("T_star or adaptive boundary changes are not authorized")
    return build_rectangular_contour(
        FROZEN_L3_SIGMA_LEFT,
        FROZEN_L3_SIGMA_RIGHT,
        FROZEN_L3_BOTTOM_HEIGHT,
        str(height),
    )


def build_frozen_l3_contours() -> MappingProxyType:
    return MappingProxyType({height: build_frozen_l3_contour(height) for height in FROZEN_L3_HEIGHTS})
