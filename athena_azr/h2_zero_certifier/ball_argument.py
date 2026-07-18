from __future__ import annotations

from decimal import Decimal

from .models import (
    ArgumentIncrementCertificate,
    HalfPlaneCertificate,
    RealInterval,
    SegmentImageCertificate,
)


class InconclusiveArgument(RuntimeError):
    """A structural certificate cannot establish a continuous argument branch."""


def verify_exclusion(certificate: SegmentImageCertificate) -> bool:
    return (
        certificate.entire_segment_covered
        and certificate.arithmetic == "rigorous_ball"
        and not certificate.contains_zero
    )


def _scale_interval(interval: RealInterval, scalar: Decimal) -> tuple[Decimal, Decimal]:
    products = (Decimal(interval.lower) * scalar, Decimal(interval.upper) * scalar)
    return min(products), max(products)


def certify_half_plane(
    certificate: SegmentImageCertificate,
    *,
    rotation_real: str,
    rotation_imag: str,
) -> HalfPlaneCertificate:
    if not verify_exclusion(certificate):
        raise InconclusiveArgument("segment image is not a full zero-free ball enclosure")

    real_part = _scale_interval(certificate.enclosure_real, Decimal(rotation_real))
    imag_part = _scale_interval(certificate.enclosure_imag, Decimal(rotation_imag))
    rotated_lower = real_part[0] - imag_part[1]
    if rotated_lower <= 0:
        raise InconclusiveArgument("rotation does not place the full image in the right half-plane")

    return HalfPlaneCertificate(
        segment_certificate=certificate,
        rotation_real=rotation_real,
        rotation_imag=rotation_imag,
        rotated_real_lower=str(rotated_lower),
    )


def certify_argument_increment(
    half_plane_certificate: HalfPlaneCertificate,
    rigorous_delta: RealInterval,
) -> ArgumentIncrementCertificate:
    """Wrap an interval supplied by a future rigorous logarithm backend.

    This function deliberately performs no transcendental approximation.
    """
    return ArgumentIncrementCertificate(
        half_plane_certificate=half_plane_certificate,
        delta_lower=rigorous_delta.lower,
        delta_upper=rigorous_delta.upper,
    )
