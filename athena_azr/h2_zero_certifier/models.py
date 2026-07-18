from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal, InvalidOperation
from types import MappingProxyType
from typing import Literal, Mapping


FunctionId = Literal["zeta", "L3"]


def _decimal(value: str) -> Decimal:
    try:
        result = Decimal(value)
    except InvalidOperation as exc:
        raise ValueError(f"invalid decimal: {value!r}") from exc
    if not result.is_finite():
        raise ValueError("interval endpoints must be finite")
    return result


@dataclass(frozen=True)
class RealInterval:
    lower: str
    upper: str

    def __post_init__(self) -> None:
        if _decimal(self.lower) >= _decimal(self.upper):
            raise ValueError("interval lower endpoint must be strictly below upper endpoint")

    def width_decimal(self) -> Decimal:
        return _decimal(self.upper) - _decimal(self.lower)

    def contains_decimal(self, value: Decimal) -> bool:
        return _decimal(self.lower) <= value <= _decimal(self.upper)

    def is_disjoint_from(self, other: "RealInterval") -> bool:
        return _decimal(self.upper) < _decimal(other.lower) or _decimal(other.upper) < _decimal(
            self.lower
        )


@dataclass(frozen=True)
class ComplexBox:
    real: RealInterval
    imag: RealInterval


@dataclass(frozen=True)
class IsolatedZeroBox:
    box: ComplexBox
    multiplicity: int
    unique_zero: bool
    certificate_reference: str

    def __post_init__(self) -> None:
        if self.multiplicity < 1:
            raise ValueError("multiplicity must be positive")
        if not self.certificate_reference:
            raise ValueError("certificate reference must be nonempty")


@dataclass(frozen=True)
class ZeroCertificate:
    index: int
    function_id: FunctionId
    conductor: int
    character_id: str
    parity: int
    box: ComplexBox
    multiplicity: int
    isolation_method: str
    working_precision_bits: int
    certificate_reference: str
    critical_line_certified: bool

    def __post_init__(self) -> None:
        if self.index < 1:
            raise ValueError("zero index must be positive")
        if self.function_id not in ("zeta", "L3"):
            raise ValueError("unsupported function id")
        if self.conductor < 1:
            raise ValueError("conductor must be positive")
        if self.parity not in (0, 1):
            raise ValueError("parity must be 0 or 1")
        if self.multiplicity < 1:
            raise ValueError("multiplicity must be positive")
        if self.working_precision_bits < 1:
            raise ValueError("working precision must be positive")
        if not self.isolation_method or not self.certificate_reference:
            raise ValueError("certificate metadata must be nonempty")


@dataclass(frozen=True)
class CountCertificate:
    function_id: FunctionId
    requested_height: int
    counting_boundary: str
    boundary_zero_free: bool
    certified_total_count: int
    isolated_count_with_multiplicity: int
    counting_method: str
    working_precision_bits: int
    parameters: Mapping[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.function_id not in ("zeta", "L3"):
            raise ValueError("unsupported function id")
        if self.requested_height <= 0:
            raise ValueError("requested height must be positive")
        _decimal(self.counting_boundary)
        if self.certified_total_count < 0 or self.isolated_count_with_multiplicity < 0:
            raise ValueError("counts must be nonnegative")
        if self.working_precision_bits < 1:
            raise ValueError("working precision must be positive")
        object.__setattr__(self, "parameters", MappingProxyType(dict(self.parameters)))

    @property
    def counts_match(self) -> bool:
        return self.certified_total_count == self.isolated_count_with_multiplicity


@dataclass(frozen=True)
class FunctionCertification:
    function_id: FunctionId
    zeros: tuple[ZeroCertificate, ...]
    counts: tuple[CountCertificate, ...]
    unresolved_clusters: int = 0


@dataclass(frozen=True)
class CrossReferenceResult:
    source: str
    status: Literal["match", "disagreement", "not_checked"]
    source_sha256: str = ""


@dataclass(frozen=True)
class CertificationBundle:
    protocol_sha256: str
    dependency_versions: Mapping[str, str]
    functions: tuple[FunctionCertification, ...]
    protected_hashes: Mapping[str, str]
    cross_references: tuple[CrossReferenceResult, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "dependency_versions", MappingProxyType(dict(self.dependency_versions))
        )
        object.__setattr__(self, "protected_hashes", MappingProxyType(dict(self.protected_hashes)))


@dataclass(frozen=True)
class RationalComplexPoint:
    real: str
    imag: str

    def __post_init__(self) -> None:
        _decimal(self.real)
        _decimal(self.imag)

    @property
    def real_decimal(self) -> Decimal:
        return _decimal(self.real)

    @property
    def imag_decimal(self) -> Decimal:
        return _decimal(self.imag)


@dataclass(frozen=True)
class DirectedSegment:
    start: RationalComplexPoint
    end: RationalComplexPoint

    def __post_init__(self) -> None:
        if self.start == self.end:
            raise ValueError("directed segment endpoints must be distinct")


@dataclass(frozen=True)
class RectangularContour:
    segments: tuple[DirectedSegment, DirectedSegment, DirectedSegment, DirectedSegment]
    orientation: Literal["positive", "negative"] = "positive"


@dataclass(frozen=True)
class SegmentImageCertificate:
    segment: DirectedSegment
    enclosure_real: RealInterval
    enclosure_imag: RealInterval
    entire_segment_covered: bool
    arithmetic: str = "rigorous_ball"

    @property
    def contains_zero(self) -> bool:
        real_zero = _decimal(self.enclosure_real.lower) <= Decimal(0) <= _decimal(self.enclosure_real.upper)
        imag_zero = _decimal(self.enclosure_imag.lower) <= Decimal(0) <= _decimal(self.enclosure_imag.upper)
        return real_zero and imag_zero


@dataclass(frozen=True)
class HalfPlaneCertificate:
    segment_certificate: SegmentImageCertificate
    rotation_real: str
    rotation_imag: str
    rotated_real_lower: str

    def __post_init__(self) -> None:
        _decimal(self.rotation_real)
        _decimal(self.rotation_imag)
        if _decimal(self.rotated_real_lower) <= 0:
            raise ValueError("rotated segment image must lie strictly in the right half-plane")
        if not self.segment_certificate.entire_segment_covered:
            raise ValueError("half-plane certificate requires the entire segment image")
        if self.segment_certificate.arithmetic != "rigorous_ball":
            raise ValueError("half-plane certificate requires rigorous ball arithmetic")
        if self.segment_certificate.contains_zero:
            raise ValueError("half-plane certificate requires a zero-free segment image")


@dataclass(frozen=True)
class ArgumentIncrementCertificate:
    half_plane_certificate: HalfPlaneCertificate
    delta_lower: str
    delta_upper: str

    def __post_init__(self) -> None:
        if _decimal(self.delta_lower) >= _decimal(self.delta_upper):
            raise ValueError("argument increment interval must have positive width")


@dataclass(frozen=True)
class WindingCertificate:
    winding_number: int
    winding_interval_lower: str
    winding_interval_upper: str
    working_precision_bits: int

    def __post_init__(self) -> None:
        _decimal(self.winding_interval_lower)
        _decimal(self.winding_interval_upper)
        if self.working_precision_bits < 1:
            raise ValueError("precision must be positive")


@dataclass(frozen=True)
class RectangleZeroCountCertificate:
    function_id: str
    conductor: int
    character_id: str
    parity: int
    rectangle_real_lower: str
    rectangle_real_upper: str
    rectangle_imag_lower: str
    rectangle_imag_upper: str
    orientation: str
    boundary_zero_free: bool
    certified_total_count: int
    working_precision_bits: int
    maximum_subdivision_depth_used: int
    segment_certificate_hashes: tuple[str, ...]
    method: str = "pure_argument_principle"

    def __post_init__(self) -> None:
        _decimal(self.rectangle_real_lower)
        _decimal(self.rectangle_real_upper)
        _decimal(self.rectangle_imag_lower)
        _decimal(self.rectangle_imag_upper)
        if self.certified_total_count < 0:
            raise ValueError("count must be non-negative")
