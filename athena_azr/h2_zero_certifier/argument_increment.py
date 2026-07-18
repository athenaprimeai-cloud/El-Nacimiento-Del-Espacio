from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from types import MappingProxyType
from typing import Mapping, Sequence

from .models import RealInterval


class InconclusiveArgumentIncrement(RuntimeError):
    """A structural argument increment lacks a certified local branch."""


def _canonical_provenance(provenance: Mapping[str, str] | None) -> tuple[tuple[str, str], ...]:
    if not provenance:
        return ()
    items: list[tuple[str, str]] = []
    for key, value in provenance.items():
        if not isinstance(key, str) or not key or not isinstance(value, str) or not value:
            raise InconclusiveArgumentIncrement("argument provenance must contain nonempty strings")
        items.append((key, value))
    return tuple(sorted(items))


@dataclass(frozen=True)
class ArgumentIncrementInterval:
    source_id: str
    lower: str
    upper: str
    precision_bits: int
    provenance: Mapping[str, str] | None = None

    def __post_init__(self) -> None:
        if not self.source_id:
            raise InconclusiveArgumentIncrement("argument increment source is required")
        if self.precision_bits < 1:
            raise InconclusiveArgumentIncrement("precision must be positive")
        interval = RealInterval(self.lower, self.upper)
        object.__setattr__(self, "lower", interval.lower)
        object.__setattr__(self, "upper", interval.upper)
        object.__setattr__(
            self,
            "provenance",
            MappingProxyType(dict(_canonical_provenance(self.provenance))),
        )


@dataclass(frozen=True)
class ArgumentTotal:
    contour_id: str
    lower: str
    upper: str
    precision_bits: int
    sources: tuple[str, ...]


def sum_argument_intervals(
    increments: Sequence[ArgumentIncrementInterval],
    *,
    contour_id: str,
    require_provenance: bool = True,
) -> RealInterval:
    if not contour_id:
        raise InconclusiveArgumentIncrement("contour id is required")
    if not increments:
        raise InconclusiveArgumentIncrement("at least one increment is required")
    precision = increments[0].precision_bits
    provenance = _canonical_provenance(increments[0].provenance)
    if require_provenance and not provenance:
        raise InconclusiveArgumentIncrement("argument increment provenance is required")
    source_ids: set[str] = set()
    total_lower = Decimal("0")
    total_upper = Decimal("0")
    for increment in increments:
        if increment.precision_bits != precision:
            raise InconclusiveArgumentIncrement("mixed precision increments are not allowed")
        if _canonical_provenance(increment.provenance) != provenance:
            raise InconclusiveArgumentIncrement("mixed argument increment provenance is not allowed")
        if increment.source_id in source_ids:
            raise InconclusiveArgumentIncrement("duplicate increment source")
        source_ids.add(increment.source_id)
        total_lower += Decimal(increment.lower)
        total_upper += Decimal(increment.upper)
    return RealInterval(str(total_lower), str(total_upper))
