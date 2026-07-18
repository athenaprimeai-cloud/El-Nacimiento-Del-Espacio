from __future__ import annotations

import csv
import hashlib
import io
import json
import os
import tempfile
from decimal import Decimal
from pathlib import Path

from .chi3_function import CHI3_METADATA
from .models import FunctionCertification


CSV_HEADER = (
    "index",
    "function_id",
    "conductor",
    "character_id",
    "parity",
    "real_lower",
    "real_upper",
    "imag_lower",
    "imag_upper",
    "multiplicity",
    "isolation_method",
    "working_precision_bits",
    "certificate_reference",
    "critical_line_certified",
)

L3_ZERO_CSV_HEADER = (
    "ordering_index",
    "function_id",
    "character_definition",
    "lower_gamma",
    "upper_gamma",
    "width",
    "midpoint_display_only",
    "multiplicity",
    "unique_zero_certified",
    "interval_disjoint_from_neighbors",
    "certification_method",
    "backend_evidence",
    "working_precision_bits",
    "certificate_reference",
    "critical_line_certified",
)


def canonical_json_bytes(payload) -> bytes:
    text = json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    )
    return (text + "\n").encode("utf-8")


def function_zero_csv_bytes(function: FunctionCertification) -> bytes:
    stream = io.StringIO(newline="")
    writer = csv.writer(stream, lineterminator="\n")
    writer.writerow(CSV_HEADER)
    for zero in function.zeros:
        writer.writerow(
            (
                zero.index,
                zero.function_id,
                zero.conductor,
                zero.character_id,
                zero.parity,
                zero.box.real.lower,
                zero.box.real.upper,
                zero.box.imag.lower,
                zero.box.imag.upper,
                zero.multiplicity,
                zero.isolation_method,
                zero.working_precision_bits,
                zero.certificate_reference,
                str(zero.critical_line_certified).lower(),
            )
        )
    return stream.getvalue().encode("utf-8")


def _decimal_string(value: Decimal) -> str:
    return format(value, "f")


def _synthetic_character_definition() -> dict[str, str]:
    return {
        "modulus": CHI3_METADATA["modulus"],
        "conductor": CHI3_METADATA["conductor"],
        "conrey_index": CHI3_METADATA["conrey_index"],
        "character_type": CHI3_METADATA["character_type"],
        "parity": CHI3_METADATA["parity"],
        "parity_name": CHI3_METADATA["parity_name"],
    }


def _synthetic_backend_identity() -> dict[str, object]:
    return {
        "kind": "synthetic_structural_only",
        "real_backend": False,
    }


def _synthetic_runtime_identity() -> dict[str, object]:
    return {
        "kind": "synthetic_structural_only",
        "real_runtime": False,
    }


def _synthetic_hash_marker() -> dict[str, object]:
    return {
        "status": "not_applicable_synthetic_structural",
        "execution_authorized": False,
        "source_phase": "006H08",
    }


def l3_zero_csv_bytes(function: FunctionCertification) -> bytes:
    if function.function_id != "L3":
        raise ValueError("l3 zero csv requires an L3 certification")
    stream = io.StringIO(newline="")
    writer = csv.writer(stream, lineterminator="\n")
    writer.writerow(L3_ZERO_CSV_HEADER)
    zeros = function.zeros
    for index, zero in enumerate(zeros):
        lower = Decimal(zero.box.imag.lower)
        upper = Decimal(zero.box.imag.upper)
        width = upper - lower
        midpoint = (lower + upper) / Decimal("2")
        previous_disjoint = index == 0 or zeros[index - 1].box.imag.is_disjoint_from(zero.box.imag)
        next_disjoint = index == len(zeros) - 1 or zero.box.imag.is_disjoint_from(zeros[index + 1].box.imag)
        writer.writerow(
            (
                zero.index,
                zero.function_id,
                f"modulus={zero.conductor};conrey={zero.character_id.split('.')[-1]};parity={zero.parity}",
                zero.box.imag.lower,
                zero.box.imag.upper,
                _decimal_string(width),
                _decimal_string(midpoint),
                zero.multiplicity,
                "true",
                str(previous_disjoint and next_disjoint).lower(),
                zero.isolation_method,
                zero.certificate_reference,
                zero.working_precision_bits,
                zero.certificate_reference,
                str(zero.critical_line_certified).lower(),
            )
        )
    return stream.getvalue().encode("utf-8")


def l3_isolation_report_json_bytes(function: FunctionCertification) -> bytes:
    if function.function_id != "L3":
        raise ValueError("l3 isolation report requires an L3 certification")
    zero_records = l3_zero_csv_bytes(function)
    payload = {
        "phase_id": "006H08",
        "function_id": "L3",
        "character_definition": _synthetic_character_definition(),
        "height_limit": 500,
        "target_isolation_width": "1e-20",
        "zero_records_file": "l3_zeros_T500.csv",
        "zero_records_sha256": hashlib.sha256(zero_records).hexdigest(),
        "total_isolated_with_multiplicity": sum(zero.multiplicity for zero in function.zeros),
        "unique_zero_failures": 0,
        "neighbor_disjointness_failures": 0,
        "unresolved_clusters": function.unresolved_clusters,
        "backend_identity": _synthetic_backend_identity(),
        "runtime_identity": _synthetic_runtime_identity(),
        "approved_code_hashes": _synthetic_hash_marker(),
        "protocol_hashes": _synthetic_hash_marker(),
        "authorization_id": "none_synthetic_structural_006H08",
        "certification_methods": sorted({zero.isolation_method for zero in function.zeros}),
        "status": "synthetic_structural_only",
        "real_certification": False,
    }
    return canonical_json_bytes(payload)


def l3_completeness_report_json_bytes(function: FunctionCertification) -> bytes:
    if function.function_id != "L3":
        raise ValueError("l3 completeness report requires an L3 certification")
    isolated_by_height = {
        str(count.requested_height): count.isolated_count_with_multiplicity
        for count in function.counts
    }
    independent_by_height = {
        str(count.requested_height): count.certified_total_count
        for count in function.counts
    }
    counts_match_by_height = {
        str(count.requested_height): count.counts_match
        for count in function.counts
    }
    winding_certificates = {
        str(count.requested_height): count.parameters.get(
            "winding_interval",
            "synthetic_structural_count_certificate",
        )
        for count in function.counts
    }
    unique_integer_counts = {
        str(count.requested_height): True
        for count in function.counts
    }
    payload = {
        "phase_id": "006H08",
        "function_id": "L3",
        "character_definition": _synthetic_character_definition(),
        "height_set": [count.requested_height for count in function.counts],
        "count_records": [
            {
                "target_height": count.requested_height,
                "boundary_zero_free": count.boundary_zero_free,
                "isolated_count_with_multiplicity": count.isolated_count_with_multiplicity,
                "independent_certified_count": count.certified_total_count,
                "counts_match": count.counts_match,
                "unresolved_clusters": function.unresolved_clusters,
                "winding_interval": count.parameters.get("winding_interval", "synthetic"),
                "unique_integer_count": True,
                "certificate_reference": count.parameters.get("source", "006H04_synthetic"),
            }
            for count in function.counts
        ],
        "boundary_convention": "exact_T_boundary",
        "boundary_zero_free_certificates": {
            str(count.requested_height): "synthetic_structural_only"
            for count in function.counts
        },
        "independent_count_method": "synthetic_structural_winding",
        "isolated_count_with_multiplicity_by_height": isolated_by_height,
        "independent_certified_count_by_height": independent_by_height,
        "counts_match_by_height": counts_match_by_height,
        "unresolved_clusters": function.unresolved_clusters,
        "winding_intervals_or_equivalent_count_certificates": winding_certificates,
        "unique_integer_counts": unique_integer_counts,
        "backend_identity": _synthetic_backend_identity(),
        "runtime_identity": _synthetic_runtime_identity(),
        "approved_code_hashes": _synthetic_hash_marker(),
        "protocol_hashes": _synthetic_hash_marker(),
        "authorization_id": "none_synthetic_structural_006H08",
        "status": "synthetic_structural_only",
        "real_certification": False,
    }
    return canonical_json_bytes(payload)


def write_bytes_atomic(path: Path, data: bytes, *, allowed_root: Path) -> None:
    root = allowed_root.resolve()
    target = path.resolve()
    if not target.is_relative_to(root):
        raise ValueError("target escapes allowed output root")

    target.parent.mkdir(parents=True, exist_ok=True)
    handle, temporary_name = tempfile.mkstemp(prefix=f".{target.name}.", dir=target.parent)
    try:
        with os.fdopen(handle, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        Path(temporary_name).replace(target)
    except BaseException:
        Path(temporary_name).unlink(missing_ok=True)
        raise
