from __future__ import annotations

from decimal import Decimal

from .config import CertificationConfig
from .models import CertificationBundle, FunctionCertification


def _is_sha256(value: str) -> bool:
    return len(value) == 64 and all(character in "0123456789abcdef" for character in value)


def _validate_function(
    function: FunctionCertification, config: CertificationConfig
) -> list[str]:
    errors: list[str] = []
    expected_indices = list(range(1, len(function.zeros) + 1))
    if [zero.index for zero in function.zeros] != expected_indices:
        errors.append(f"{function.function_id}: indices are not consecutive")

    previous = None
    for zero in function.zeros:
        if zero.function_id != function.function_id:
            errors.append(f"{function.function_id}: zero function id mismatch")
        if zero.box.real.width_decimal() > config.target_interval_width:
            errors.append(f"{function.function_id}: real interval too wide")
        if zero.box.imag.width_decimal() > config.target_interval_width:
            errors.append(f"{function.function_id}: imaginary interval too wide")
        if previous is not None and not previous.box.imag.is_disjoint_from(zero.box.imag):
            errors.append(f"{function.function_id}: overlap between zero intervals")
        previous = zero

    if function.unresolved_clusters:
        errors.append(f"{function.function_id}: unresolved clusters remain")

    if tuple(count.requested_height for count in function.counts) != config.requested_heights:
        errors.append(f"{function.function_id}: frozen counting heights missing")

    previous_total = -1
    for count in function.counts:
        if count.function_id != function.function_id:
            errors.append(f"{function.function_id}: count function id mismatch")
        if not count.boundary_zero_free:
            errors.append(f"{function.function_id}: counting boundary is not zero-free")
        if not count.counts_match:
            errors.append(f"{function.function_id}: count mismatch")
        if count.certified_total_count < previous_total:
            errors.append(f"{function.function_id}: counts are decreasing")
        previous_total = count.certified_total_count
        boundary = Decimal(count.requested_height)
        if any(zero.box.imag.contains_decimal(boundary) for zero in function.zeros):
            errors.append(f"{function.function_id}: zero interval crosses counting boundary")
    return errors


def validate_bundle(
    bundle: CertificationBundle, config: CertificationConfig
) -> tuple[str, ...]:
    errors: list[str] = []
    if not _is_sha256(bundle.protocol_sha256):
        errors.append("protocol sha256 is invalid")
    if not bundle.dependency_versions:
        errors.append("dependency versions are missing")
    if not bundle.protected_hashes or not all(
        _is_sha256(value) for value in bundle.protected_hashes.values()
    ):
        errors.append("protected sha256 inventory is invalid")

    identifiers = [function.function_id for function in bundle.functions]
    if sorted(identifiers) != ["L3", "zeta"]:
        errors.append("bundle must contain exactly zeta and L3")
    for function in bundle.functions:
        errors.extend(_validate_function(function, config))

    references = {reference.source.lower(): reference for reference in bundle.cross_references}
    for required_source in ("odlyzko", "lmfdb"):
        reference = references.get(required_source)
        if reference is None:
            errors.append(f"cross-reference {required_source} is missing")
            continue
        if reference.status != "match":
            errors.append(f"cross-reference {required_source} is not resolved as a match")
        if not _is_sha256(reference.source_sha256):
            errors.append(f"cross-reference {required_source} sha256 is invalid")
    if any(reference.status == "disagreement" for reference in bundle.cross_references):
        errors.append("cross-reference disagreement remains")
    return tuple(errors)
