from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import Sequence

from .models import ComplexBox, RealInterval, ZeroCertificate


class InconclusiveL3Isolation(RuntimeError):
    """Synthetic L3 isolation data does not satisfy the structural contract."""


@dataclass(frozen=True)
class SyntheticL3ZeroCandidate:
    real_lower: str
    real_upper: str
    imag_lower: str
    imag_upper: str
    multiplicity: int | None
    certificate_reference: str
    unique_zero: bool = True
    cluster_resolved: bool = True
    critical_line_certified: bool = False
    isolation_method: str = "synthetic_structural_l3_isolator"
    working_precision_bits: int = 192

    def box(self) -> ComplexBox:
        return ComplexBox(
            RealInterval(self.real_lower, self.real_upper),
            RealInterval(self.imag_lower, self.imag_upper),
        )


def _validate_candidate(candidate: SyntheticL3ZeroCandidate, target_width: Decimal) -> ComplexBox:
    if candidate.multiplicity is None or candidate.multiplicity < 1:
        raise InconclusiveL3Isolation("multiplicity is unresolved")
    if not candidate.unique_zero:
        raise InconclusiveL3Isolation("zero uniqueness is unresolved")
    if not candidate.cluster_resolved:
        raise InconclusiveL3Isolation("cluster is unresolved")
    if not candidate.certificate_reference:
        raise InconclusiveL3Isolation("certificate reference is required")
    if candidate.working_precision_bits < 1:
        raise InconclusiveL3Isolation("precision must be positive")
    box = candidate.box()
    if box.real.width_decimal() > target_width or box.imag.width_decimal() > target_width:
        raise InconclusiveL3Isolation("candidate interval is wider than target")
    return box


def isolate_synthetic_l3_zeros(
    candidates: Sequence[SyntheticL3ZeroCandidate],
    *,
    target_width: Decimal = Decimal("1e-20"),
) -> tuple[ZeroCertificate, ...]:
    boxes: list[tuple[SyntheticL3ZeroCandidate, ComplexBox]] = []
    for candidate in candidates:
        boxes.append((candidate, _validate_candidate(candidate, target_width)))
    boxes.sort(key=lambda item: Decimal(item[1].imag.lower))

    zeros: list[ZeroCertificate] = []
    previous: ComplexBox | None = None
    for index, (candidate, box) in enumerate(boxes, start=1):
        if previous is not None and not previous.imag.is_disjoint_from(box.imag):
            raise InconclusiveL3Isolation("isolating intervals overlap")
        zeros.append(
            ZeroCertificate(
                index=index,
                function_id="L3",
                conductor=3,
                character_id="3.2",
                parity=1,
                box=box,
                multiplicity=candidate.multiplicity,
                isolation_method=candidate.isolation_method,
                working_precision_bits=candidate.working_precision_bits,
                certificate_reference=candidate.certificate_reference,
                critical_line_certified=candidate.critical_line_certified,
            )
        )
        previous = box
    return tuple(zeros)
