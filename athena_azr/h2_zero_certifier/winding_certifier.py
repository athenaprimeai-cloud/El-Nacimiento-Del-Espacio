from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from math import gcd

from .models import RealInterval


class InconclusiveWindingCertification(RuntimeError):
    """A winding interval does not contain exactly one allowed integer."""


@dataclass(frozen=True)
class ClosedWindingInterval:
    lower: str
    upper: str

    def __post_init__(self) -> None:
        _closed_exact_bounds(self.lower, self.upper)


@dataclass(frozen=True)
class StructuralWindingCertificate:
    winding_number: int
    winding_interval: ClosedWindingInterval
    precision_bits: int
    unique_integer_count: bool = True


def _parse_canonical_integer_text(value: str, *, allow_zero: bool) -> int:
    if not value:
        raise ValueError("winding interval endpoint is empty")
    if value.startswith("+"):
        raise ValueError("winding interval endpoint must not use a plus sign")
    negative = value.startswith("-")
    digits = value[1:] if negative else value
    if not digits or not digits.isdigit():
        raise ValueError("winding interval endpoint must be numeric")
    if len(digits) > 1 and digits.startswith("0"):
        raise ValueError("winding interval endpoint has leading zeros")
    if digits == "0":
        if negative or not allow_zero:
            raise ValueError("winding interval endpoint has noncanonical zero")
        return 0
    result = int(digits)
    return -result if negative else result


def _parse_canonical_decimal_text(value: str) -> Fraction:
    negative = value.startswith("-")
    body = value[1:] if negative else value
    if body.count(".") != 1:
        raise ValueError("winding interval decimal endpoint is malformed")
    integer_part, fractional_part = body.split(".", 1)
    if (
        not integer_part
        or not fractional_part
        or not integer_part.isdigit()
        or not fractional_part.isdigit()
    ):
        raise ValueError("winding interval decimal endpoint is malformed")
    if len(integer_part) > 1 and integer_part.startswith("0"):
        raise ValueError("winding interval decimal endpoint has leading zeros")
    if fractional_part.endswith("0"):
        raise ValueError("winding interval decimal endpoint is not canonical")
    denominator = 10 ** len(fractional_part)
    numerator = int(integer_part) * denominator + int(fractional_part)
    if numerator == 0:
        raise ValueError("winding interval endpoint has noncanonical zero")
    if negative:
        numerator = -numerator
    return Fraction(numerator, denominator)


def parse_canonical_exact_endpoint(value: str) -> Fraction:
    if not isinstance(value, str) or not value or value != value.strip():
        raise ValueError("winding interval endpoint must be a canonical string")

    if "/" in value:
        if value.count("/") != 1:
            raise ValueError("winding interval rational endpoint is malformed")
        numerator_text, denominator_text = value.split("/", 1)
        numerator = _parse_canonical_integer_text(numerator_text, allow_zero=False)
        if (
            not denominator_text
            or denominator_text.startswith(("+", "-"))
            or not denominator_text.isdigit()
        ):
            raise ValueError("winding interval rational denominator is malformed")
        if len(denominator_text) > 1 and denominator_text.startswith("0"):
            raise ValueError("winding interval rational denominator has leading zeros")
        denominator = int(denominator_text)
        if denominator <= 0:
            raise ValueError("winding interval rational denominator must be positive")
        if numerator % denominator == 0:
            raise ValueError("integer-valued rational endpoint must use integer syntax")
        if gcd(abs(numerator), denominator) != 1:
            raise ValueError("winding interval rational endpoint is not reduced")
        return Fraction(numerator, denominator)

    if "." in value:
        return _parse_canonical_decimal_text(value)

    return Fraction(_parse_canonical_integer_text(value, allow_zero=True), 1)


def _ceil_fraction(value: Fraction) -> int:
    return -((-value.numerator) // value.denominator)


def _floor_fraction(value: Fraction) -> int:
    return value.numerator // value.denominator


def _closed_exact_bounds(lower: str, upper: str) -> tuple[Fraction, Fraction]:
    low = parse_canonical_exact_endpoint(lower)
    high = parse_canonical_exact_endpoint(upper)
    if low > high:
        raise ValueError("winding interval lower endpoint must not exceed upper endpoint")
    return low, high


def _closed_decimal_bounds(lower: str, upper: str) -> tuple[Fraction, Fraction]:
    return _closed_exact_bounds(lower, upper)


def integers_in_exact_closed_interval(lower: str, upper: str) -> tuple[int, ...]:
    low, high = _closed_exact_bounds(lower, upper)
    first = _ceil_fraction(low)
    last = _floor_fraction(high)
    if first > last:
        return ()
    return tuple(range(first, last + 1))


def integers_in_closed_interval(lower: str, upper: str) -> tuple[int, ...]:
    return integers_in_exact_closed_interval(lower, upper)


def integers_in_interval(interval: RealInterval) -> tuple[int, ...]:
    return integers_in_closed_interval(interval.lower, interval.upper)


def certify_unique_integer_winding_bounds(
    lower: str,
    upper: str,
    *,
    precision_bits: int,
) -> StructuralWindingCertificate:
    if precision_bits < 1:
        raise InconclusiveWindingCertification("precision must be positive")
    integers = integers_in_closed_interval(lower, upper)
    if len(integers) != 1 or integers[0] < 0:
        raise InconclusiveWindingCertification(
            "winding interval does not contain exactly one nonnegative integer"
        )
    return StructuralWindingCertificate(
        winding_number=integers[0],
        winding_interval=ClosedWindingInterval(lower, upper),
        precision_bits=precision_bits,
    )


def certify_unique_integer_winding(
    interval: RealInterval,
    *,
    precision_bits: int,
) -> StructuralWindingCertificate:
    return certify_unique_integer_winding_bounds(
        interval.lower,
        interval.upper,
        precision_bits=precision_bits,
    )
