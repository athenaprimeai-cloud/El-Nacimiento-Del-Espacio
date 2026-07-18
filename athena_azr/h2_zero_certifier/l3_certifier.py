from __future__ import annotations

from decimal import Decimal
from typing import Mapping
from .chi3_function import validate_chi3_metadata
from .config import CertificationConfig
from .models import (
    CountCertificate,
    FunctionCertification,
    ZeroCertificate,
    ComplexBox,
    RealInterval,
)
from .l3_argument_count import InconclusiveWindingCount


class InconclusiveL3Certification(RuntimeError):
    """L3 isolation and independent strip count do not close."""


SHIFTS = [
    Decimal("0"),
    Decimal("0.125"), Decimal("-0.125"),
    Decimal("0.0625"), Decimal("-0.0625"),
    Decimal("0.03125"), Decimal("-0.03125"),
    Decimal("0.015625"), Decimal("-0.015625"),
    Decimal("0.0078125"), Decimal("-0.0078125"),
    Decimal("0.00390625"), Decimal("-0.00390625"),
    Decimal("0.001953125"), Decimal("-0.001953125"),
    Decimal("0.0009765625"), Decimal("-0.0009765625"),
]


def _isolate_box(
    box: ComplexBox,
    parent_count: int,
    backend,
    config: CertificationConfig,
    precision_bits: int,
    depth: int,
) -> list[ZeroCertificate]:
    if parent_count < 0:
        raise InconclusiveL3Certification("parent winding count must be nonnegative")
    if parent_count == 0:
        return []

    width_real = Decimal(box.real.upper) - Decimal(box.real.lower)
    width_imag = Decimal(box.imag.upper) - Decimal(box.imag.lower)

    if parent_count == 1:
        if width_real <= config.target_interval_width and width_imag <= config.target_interval_width:
            critical_line_certified = backend.l3_critical_line_certified(
                box, precision_bits
            )

            # Keep the box as is
            return [
                ZeroCertificate(
                    index=1,  # will be indexed later
                    function_id="L3",
                    conductor=config.l3_conductor,
                    character_id=f"{config.l3_conductor}.{config.l3_conrey_number}",
                    parity=config.l3_parity,
                    box=box,
                    multiplicity=1,
                    isolation_method="pure_argument_principle_bisections",
                    working_precision_bits=precision_bits,
                    certificate_reference=f"L3-isolated-zero-{box.imag.lower}-{box.imag.upper}",
                    critical_line_certified=critical_line_certified,
                )
            ]

    if depth >= config.max_root_isolation_depth:
        raise InconclusiveL3Certification(
            "Maximum root isolation depth "
            f"({config.max_root_isolation_depth}) reached for box {box} "
            f"containing {parent_count} zeros"
        )

    # Subdivide along the longest dimension
    if width_real > width_imag:
        split_dir = "real"
        mid = (Decimal(box.real.lower) + Decimal(box.real.upper)) / 2
        size = width_real
    else:
        split_dir = "imag"
        mid = (Decimal(box.imag.lower) + Decimal(box.imag.upper)) / 2
        size = width_imag

    # Try boundary shifts to avoid zeros on the border
    success = False
    box_left = None
    box_right = None
    count_left = 0
    count_right = 0

    for s in SHIFTS:
        shifted_mid = mid + s * size
        if split_dir == "real":
            if shifted_mid <= Decimal(box.real.lower) or shifted_mid >= Decimal(box.real.upper):
                continue
            b_left = ComplexBox(RealInterval(box.real.lower, str(shifted_mid)), box.imag)
            b_right = ComplexBox(RealInterval(str(shifted_mid), box.real.upper), box.imag)
        else:
            if shifted_mid <= Decimal(box.imag.lower) or shifted_mid >= Decimal(box.imag.upper):
                continue
            b_left = ComplexBox(box.real, RealInterval(box.imag.lower, str(shifted_mid)))
            b_right = ComplexBox(box.real, RealInterval(str(shifted_mid), box.imag.upper))

        try:
            c_left = backend.l3_box_winding_count(b_left, precision_bits)
            c_right = backend.l3_box_winding_count(b_right, precision_bits)
            if c_left + c_right == parent_count:
                box_left = b_left
                box_right = b_right
                count_left = c_left
                count_right = c_right
                success = True
                break
        except InconclusiveWindingCount:
            continue

    if not success or box_left is None or box_right is None:
        raise InconclusiveL3Certification(
            f"Could not find a zero-free division boundary for box {box} with {parent_count} zeros"
        )

    zeros_left = _isolate_box(box_left, count_left, backend, config, precision_bits, depth + 1)
    zeros_right = _isolate_box(box_right, count_right, backend, config, precision_bits, depth + 1)
    return zeros_left + zeros_right


def certify_l3(backend, config: CertificationConfig) -> FunctionCertification:
    try:
        validate_chi3_metadata(backend.chi3_metadata())
    except ValueError as exc:
        raise InconclusiveL3Certification(str(exc)) from exc

    # Attempt isolation using precision sequence from config
    zeros_found: list[ZeroCertificate] = []
    precision_used = config.precision_steps_bits[0]

    for precision in config.precision_steps_bits:
        precision_used = precision
        # Define complete bounding box: Re in [-0.5, 1.5], Imag in [0, max_height]
        initial_box = ComplexBox(
            RealInterval(str(config.contour_sigma_left), str(config.contour_sigma_right)),
            RealInterval("0.0", str(config.max_height)),
        )
        try:
            total_count = backend.l3_box_winding_count(initial_box, precision)
            zeros_found = _isolate_box(initial_box, total_count, backend, config, precision, 0)
            break
        except (InconclusiveL3Certification, InconclusiveWindingCount):
            continue
    else:
        raise InconclusiveL3Certification(
            f"L3 boxes not isolated within frozen precision budget: {config.precision_steps_bits}"
        )

    if not zeros_found:
        raise InconclusiveL3Certification("L3 sequence is empty below the maximum height")

    # Sort zeros by imaginary part coordinate (strictly disjoint and ordered)
    zeros_found.sort(key=lambda z: Decimal(z.box.imag.lower))

    # Index zeros and validate disjointness
    zeros: list[ZeroCertificate] = []
    previous_upper: Decimal | None = None
    for index, z in enumerate(zeros_found, start=1):
        imag_lower = Decimal(z.box.imag.lower)
        imag_upper = Decimal(z.box.imag.upper)

        if previous_upper is not None and imag_lower <= previous_upper:
            raise InconclusiveL3Certification("L3 boxes are not strictly ordered and disjoint")

        # Check requested height boundaries (no zero box must intersect them)
        for height in config.requested_heights:
            if imag_lower <= Decimal(height) <= imag_upper:
                raise InconclusiveL3Certification(
                    f"L3 box {index} intersects frozen boundary {height}"
                )

        zeros.append(
            ZeroCertificate(
                index=index,
                function_id=z.function_id,
                conductor=z.conductor,
                character_id=z.character_id,
                parity=z.parity,
                box=z.box,
                multiplicity=z.multiplicity,
                isolation_method=z.isolation_method,
                working_precision_bits=z.working_precision_bits,
                certificate_reference=z.certificate_reference,
                critical_line_certified=z.critical_line_certified,
            )
        )
        previous_upper = imag_upper

    # Winding count matches for requested heights
    counts: list[CountCertificate] = []
    for height in config.requested_heights:
        isolated = sum(
            zero.multiplicity
            for zero in zeros
            if Decimal(zero.box.imag.upper) < Decimal(height)
        )
        count = backend.l3_count_certificate(height, precision_used)
        if count.function_id != "L3" or count.requested_height != height:
            raise InconclusiveL3Certification("L3 count certificate identity mismatch")
        if not count.boundary_zero_free:
            raise InconclusiveL3Certification("L3 counting boundary is not certified zero-free")
        total = count.certified_total_count
        if total != isolated or not count.counts_match:
            raise InconclusiveL3Certification(
                f"L3 count mismatch at {height}: strip={total}, isolated={isolated}"
            )
        counts.append(
            CountCertificate(
                function_id="L3",
                requested_height=height,
                counting_boundary=count.counting_boundary,
                boundary_zero_free=count.boundary_zero_free,
                certified_total_count=total,
                isolated_count_with_multiplicity=isolated,
                counting_method=count.counting_method,
                working_precision_bits=count.working_precision_bits,
                parameters=count.parameters,
            )
        )

    return FunctionCertification(function_id="L3", zeros=tuple(zeros), counts=tuple(counts))


def certify_l3_synthetic(
    zeros: tuple[ZeroCertificate, ...],
    *,
    winding_counts: Mapping[int, int],
    config: CertificationConfig | None = None,
) -> FunctionCertification:
    active_config = config or CertificationConfig.frozen_default()
    if tuple(sorted(winding_counts)) != active_config.requested_heights:
        raise InconclusiveL3Certification("synthetic winding counts must cover frozen heights")
    ordered = tuple(sorted(zeros, key=lambda zero: Decimal(zero.box.imag.lower)))
    if [zero.index for zero in ordered] != list(range(1, len(ordered) + 1)):
        raise InconclusiveL3Certification("synthetic zeros must be consecutively indexed")

    previous_upper: Decimal | None = None
    for zero in ordered:
        if zero.function_id != "L3":
            raise InconclusiveL3Certification("synthetic L3 certifier only accepts L3 zeros")
        imag_lower = Decimal(zero.box.imag.lower)
        imag_upper = Decimal(zero.box.imag.upper)
        if previous_upper is not None and imag_lower <= previous_upper:
            raise InconclusiveL3Certification("synthetic L3 zeros overlap")
        for height in active_config.requested_heights:
            boundary = Decimal(height)
            if imag_lower <= boundary <= imag_upper:
                raise InconclusiveL3Certification("synthetic zero intersects frozen height")
        previous_upper = imag_upper

    counts: list[CountCertificate] = []
    for height in active_config.requested_heights:
        isolated = sum(
            zero.multiplicity
            for zero in ordered
            if Decimal(zero.box.imag.upper) < Decimal(height)
        )
        total = winding_counts[height]
        if total != isolated:
            raise InconclusiveL3Certification(
                f"synthetic L3 count mismatch at {height}: winding={total}, isolated={isolated}"
            )
        counts.append(
            CountCertificate(
                function_id="L3",
                requested_height=height,
                counting_boundary=str(height),
                boundary_zero_free=True,
                certified_total_count=total,
                isolated_count_with_multiplicity=isolated,
                counting_method="synthetic_structural_winding_no_symmetry_division",
                working_precision_bits=ordered[-1].working_precision_bits if ordered else 1,
                parameters={
                    "source": "006H04_synthetic",
                    "symmetry_division": "forbidden",
                    "critical_line_required": "false",
                },
            )
        )
    return FunctionCertification(function_id="L3", zeros=ordered, counts=tuple(counts))
