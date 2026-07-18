from __future__ import annotations

import json
import platform
import sys
from datetime import datetime, timezone
from importlib.metadata import version as distribution_version
from pathlib import Path

from run_006e59_narrow_smoke import (
    bounds,
    component,
    is_finite_acb,
    sha256_file,
    verify_sha256sums,
    write_csv,
    write_jsonl_record,
)
from run_006e71_narrow_smoke import (
    MATRIX as MATRIX_006E71,
    build_diagnostic_pairs as build_006e71_diagnostic_pairs,
)


PHASE_ID = "006E74"
RESULT_PASS = "006E74_REPLAY_ONLY_CAPTURE_REPRO_SMOKE_PASS_LIMITED"
RESULT_WARNINGS = "006E74_REPLAY_ONLY_CAPTURE_REPRO_SMOKE_PASS_WITH_WARNINGS"
RESULT_BLOCKED = "006E74_BLOCKED_ENVIRONMENT_OR_CAPTURE"
RESULT_INCONCLUSIVE = "006E74_INCONCLUSIVE_SEMANTICS_OR_CAPTURE"
RESULT_FAIL_SCOPE = "006E74_FAIL_SCOPE_OR_SEMANTICS"
MATRIX_ID = "006E74_REPLAY_ONLY_006E71_CAPTURE_REPRO"
AUTHORIZED_RUNTIME = r"C:\Users\johnn\AppData\Local\Temp\athena-006e20r\Scripts\python.exe"
ARTIFACT_DIR = Path("artifacts/006E74-replay-only-006E71-capture-repro")
PRECISIONS = [96, 128]
EXPECTED_RECORDS = 90
EXPECTED_DIAGNOSTICS = 84

REQUIRED_FILES = [
    "ledger.jsonl",
    "ledger.csv",
    "ledger-compact.md",
    "diagnostics.jsonl",
    "diagnostics.csv",
    "manifest.json",
    "SHA256SUMS.txt",
]

HASHED_FILES = [
    "ledger.jsonl",
    "ledger.csv",
    "ledger-compact.md",
    "diagnostics.jsonl",
    "diagnostics.csv",
    "manifest.json",
]


def replay_row_from_006e71(row: dict) -> dict:
    replay = dict(row)
    replay["source"] = "replay_006E71"
    return replay


MATRIX = [replay_row_from_006e71(row) for row in MATRIX_006E71]


def fail_summary(result: str, message: str) -> int:
    print(json.dumps({"message": message, "phase_id": PHASE_ID, "result": result}, sort_keys=True))
    return 1


def build_diagnostic_pairs() -> list[tuple[str, str, str]]:
    return build_006e71_diagnostic_pairs()


def validate_static_contract() -> list[str]:
    errors: list[str] = []
    if PHASE_ID != "006E74":
        errors.append("phase id drifted")
    if MATRIX_ID != "006E74_REPLAY_ONLY_006E71_CAPTURE_REPRO":
        errors.append("matrix id drifted")
    if ARTIFACT_DIR != Path("artifacts/006E74-replay-only-006E71-capture-repro"):
        errors.append("artifact directory drifted")
    if PRECISIONS != [96, 128]:
        errors.append("precision values drifted")
    if EXPECTED_RECORDS != 90:
        errors.append("expected record count drifted")
    if EXPECTED_DIAGNOSTICS != 84:
        errors.append("expected diagnostic count drifted")
    if len(MATRIX) != 45:
        errors.append("matrix size is not 45")

    replay_rows = [row for row in MATRIX if row.get("source") == "replay_006E71"]
    non_replay_rows = [row for row in MATRIX if row.get("source") != "replay_006E71"]
    if len(replay_rows) != 45:
        errors.append("replay row count is not 45")
    if non_replay_rows:
        errors.append("new inputs are present in replay-only matrix")

    labels = [row["label"] for row in MATRIX]
    if len(labels) != len(set(labels)):
        errors.append("matrix labels are not unique")

    for replay_row, source_row in zip(MATRIX, MATRIX_006E71):
        expected = dict(source_row)
        expected["source"] = "replay_006E71"
        if replay_row != expected:
            errors.append(f"{replay_row.get('label', '<missing>')} does not replay 006E71 exactly")

    for row in MATRIX:
        for key in ("real_mid", "real_radius", "imag_mid", "imag_radius"):
            value = row[key]
            if not isinstance(value, str) or "." in value:
                errors.append(f"{row['label']} has non-rational descriptor {key}={value!r}")
    if len(build_diagnostic_pairs()) != 42:
        errors.append("diagnostic pair count is not 42")
    if len(build_diagnostic_pairs()) * len(PRECISIONS) != EXPECTED_DIAGNOSTICS:
        errors.append("diagnostic pair count does not match expected diagnostics")
    return errors


def write_compact_markdown(path: Path, records: list[dict], diagnostics: list[dict]) -> None:
    lines = [
        "# 006E74 Compact Ledger",
        "",
        "This file is a human summary only. JSONL remains the primary authority.",
        "",
        "## Semantic Records",
        "",
        "| input_label | precision_bits | result | output_type | output_finite | output_real_width_nonzero | output_imag_width_nonzero | ctx_restored |",
        "|---|---:|---|---|---|---|---|---|",
    ]
    for record in records:
        lines.append(
            "| {input_label} | {precision_bits} | {result} | {output_type} | {output_finite} | {output_real_lower_ne_upper} | {output_imag_lower_ne_upper} | {ctx_restored} |".format(**record)
        )
    lines.extend([
        "",
        "## Diagnostics",
        "",
        "| diagnostic_block | parent | child | precision_bits | contains | overlaps | result |",
        "|---|---|---|---:|---|---|---|",
    ])
    for diagnostic in diagnostics:
        lines.append(
            "| {diagnostic_block} | {parent} | {child} | {precision_bits} | {contains} | {overlaps} | {result} |".format(**diagnostic)
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    static_errors = validate_static_contract()
    if static_errors:
        return fail_summary(RESULT_FAIL_SCOPE, "; ".join(static_errors))

    if not Path(AUTHORIZED_RUNTIME).exists():
        return fail_summary(RESULT_BLOCKED, "authorized runtime does not exist")
    if str(Path(sys.executable)) != AUTHORIZED_RUNTIME:
        return fail_summary(RESULT_BLOCKED, "sys.executable does not match authorized runtime")

    if ARTIFACT_DIR.exists() and any(ARTIFACT_DIR.iterdir()):
        return fail_summary(RESULT_BLOCKED, "artifact directory already exists and is not empty")
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)

    ledger_jsonl = ARTIFACT_DIR / "ledger.jsonl"
    diagnostics_jsonl = ARTIFACT_DIR / "diagnostics.jsonl"
    ledger_jsonl.write_text("", encoding="utf-8")
    diagnostics_jsonl.write_text("", encoding="utf-8")

    try:
        import flint
        from flint import acb, arb, ctx, dirichlet_char, fmpq
    except Exception as exc:  # pragma: no cover - environment gate
        return fail_summary(RESULT_BLOCKED, f"import flint failed: {exc!r}")

    python_flint_version = distribution_version("python-flint")
    flint_version = str(getattr(flint, "__version__", "unavailable"))
    flint_native_version = str(getattr(flint, "__FLINT_VERSION__", getattr(flint, "FLINT_VERSION", "unavailable")))
    if python_flint_version != "0.8.0" or flint_version != "0.8.0" or flint_native_version != "3.3.1":
        return fail_summary(RESULT_BLOCKED, "version precheck failed")

    def make_ball(mid: str, radius: str):
        return arb(fmpq(mid), fmpq(radius))

    def make_box(row: dict):
        return acb(make_ball(row["real_mid"], row["real_radius"]), make_ball(row["imag_mid"], row["imag_radius"]))

    run_id = PHASE_ID + "-" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    chi = dirichlet_char(3, 2)
    outputs: dict[tuple[str, int], object] = {}
    records: list[dict] = []
    diagnostics: list[dict] = []

    for row in MATRIX:
        input_box = make_box(row)
        input_real = component(input_box, "real")
        input_imag = component(input_box, "imag")
        input_real_lower, input_real_upper, input_real_width = bounds(input_real)
        input_imag_lower, input_imag_upper, input_imag_width = bounds(input_imag)

        for bits in PRECISIONS:
            ctx_before = int(ctx.prec)
            try:
                with ctx.workprec(bits):
                    ctx_inside = int(ctx.prec)
                    output = chi.l_function(input_box)
                ctx_after = int(ctx.prec)
                output_real = component(output, "real")
                output_imag = component(output, "imag")
                output_real_lower, output_real_upper, output_real_width = bounds(output_real)
                output_imag_lower, output_imag_upper, output_imag_width = bounds(output_imag)
                output_type = type(output).__name__
                output_finite = is_finite_acb(output)
                ctx_restored = ctx_after == ctx_before
                passed = (
                    output_type == "acb"
                    and output_finite
                    and output_real_width
                    and output_imag_width
                    and input_real_width
                    and input_imag_width
                    and ctx_restored
                )
                record = {
                    "phase_id": PHASE_ID,
                    "run_id": run_id,
                    "matrix_id": MATRIX_ID,
                    "runtime_authorized": AUTHORIZED_RUNTIME,
                    "runtime_sys_executable": sys.executable,
                    "python": sys.version,
                    "platform": platform.platform(),
                    "python_flint_distribution": python_flint_version,
                    "flint_version": flint_version,
                    "flint_FLINT_VERSION": flint_native_version,
                    "arb_independent_version_seal": False,
                    "input_label": row["label"],
                    "input_source": row["source"],
                    "input_block": row["block"],
                    "input_parent": row["parent"],
                    "real_midpoint_rational": row["real_mid"],
                    "real_radius_rational": row["real_radius"],
                    "imag_midpoint_rational": row["imag_mid"],
                    "imag_radius_rational": row["imag_radius"],
                    "precision_bits": bits,
                    "input_real_lower": input_real_lower,
                    "input_real_upper": input_real_upper,
                    "input_imag_lower": input_imag_lower,
                    "input_imag_upper": input_imag_upper,
                    "input_real_lower_ne_upper": input_real_width,
                    "input_imag_lower_ne_upper": input_imag_width,
                    "output_type": output_type,
                    "output_finite": output_finite,
                    "output_real_lower": output_real_lower,
                    "output_real_upper": output_real_upper,
                    "output_imag_lower": output_imag_lower,
                    "output_imag_upper": output_imag_upper,
                    "output_real_lower_ne_upper": output_real_width,
                    "output_imag_lower_ne_upper": output_imag_width,
                    "ctx_before": ctx_before,
                    "ctx_inside": ctx_inside,
                    "ctx_after": ctx_after,
                    "ctx_restored": ctx_restored,
                    "result": "PASS" if passed else "FAIL",
                }
                outputs[(row["label"], bits)] = output
            except Exception as exc:
                ctx_after = int(ctx.prec)
                record = {
                    "phase_id": PHASE_ID,
                    "run_id": run_id,
                    "matrix_id": MATRIX_ID,
                    "runtime_authorized": AUTHORIZED_RUNTIME,
                    "runtime_sys_executable": sys.executable,
                    "python": sys.version,
                    "platform": platform.platform(),
                    "python_flint_distribution": python_flint_version,
                    "flint_version": flint_version,
                    "flint_FLINT_VERSION": flint_native_version,
                    "arb_independent_version_seal": False,
                    "input_label": row["label"],
                    "input_source": row["source"],
                    "input_block": row["block"],
                    "input_parent": row["parent"],
                    "real_midpoint_rational": row["real_mid"],
                    "real_radius_rational": row["real_radius"],
                    "imag_midpoint_rational": row["imag_mid"],
                    "imag_radius_rational": row["imag_radius"],
                    "precision_bits": bits,
                    "input_real_lower": input_real_lower,
                    "input_real_upper": input_real_upper,
                    "input_imag_lower": input_imag_lower,
                    "input_imag_upper": input_imag_upper,
                    "input_real_lower_ne_upper": input_real_width,
                    "input_imag_lower_ne_upper": input_imag_width,
                    "output_type": "error",
                    "output_finite": False,
                    "output_real_lower": None,
                    "output_real_upper": None,
                    "output_imag_lower": None,
                    "output_imag_upper": None,
                    "output_real_lower_ne_upper": False,
                    "output_imag_lower_ne_upper": False,
                    "ctx_before": ctx_before,
                    "ctx_inside": None,
                    "ctx_after": ctx_after,
                    "ctx_restored": ctx_after == ctx_before,
                    "error": repr(exc),
                    "result": "FAIL",
                }
            records.append(record)
            write_jsonl_record(ledger_jsonl, record)

    for bits in PRECISIONS:
        for block, parent, child in build_diagnostic_pairs():
            parent_output = outputs.get((parent, bits))
            child_output = outputs.get((child, bits))
            try:
                contains = bool(parent_output.contains(child_output)) if parent_output is not None and child_output is not None else False
                overlaps = bool(parent_output.overlaps(child_output)) if parent_output is not None and child_output is not None else False
                result = "PASS_DIAGNOSTIC" if contains and overlaps else "FAIL_DIAGNOSTIC"
                diagnostic = {
                    "phase_id": PHASE_ID,
                    "run_id": run_id,
                    "diagnostic_block": block,
                    "parent": parent,
                    "child": child,
                    "precision_bits": bits,
                    "contains": contains,
                    "overlaps": overlaps,
                    "result": result,
                }
            except Exception as exc:
                diagnostic = {
                    "phase_id": PHASE_ID,
                    "run_id": run_id,
                    "diagnostic_block": block,
                    "parent": parent,
                    "child": child,
                    "precision_bits": bits,
                    "contains": False,
                    "overlaps": False,
                    "error": repr(exc),
                    "result": "FAIL_DIAGNOSTIC",
                }
            diagnostics.append(diagnostic)
            write_jsonl_record(diagnostics_jsonl, diagnostic)

    ledger_csv = ARTIFACT_DIR / "ledger.csv"
    diagnostics_csv = ARTIFACT_DIR / "diagnostics.csv"
    compact_md = ARTIFACT_DIR / "ledger-compact.md"
    manifest_path = ARTIFACT_DIR / "manifest.json"
    sha_path = ARTIFACT_DIR / "SHA256SUMS.txt"

    write_csv(ledger_csv, records)
    write_csv(diagnostics_csv, diagnostics)
    write_compact_markdown(compact_md, records, diagnostics)

    records_pass = sum(1 for record in records if record["result"] == "PASS")
    diagnostics_pass = sum(1 for diagnostic in diagnostics if diagnostic["result"] == "PASS_DIAGNOSTIC")
    input_labels = {row["label"] for row in MATRIX}

    clean_semantics = (
        len(records) == EXPECTED_RECORDS
        and records_pass == EXPECTED_RECORDS
        and len(diagnostics) == EXPECTED_DIAGNOSTICS
        and diagnostics_pass == EXPECTED_DIAGNOSTICS
    )
    result = RESULT_PASS if clean_semantics else RESULT_INCONCLUSIVE

    manifest = {
        "phase_id": PHASE_ID,
        "source_phase": "006E73",
        "source_runtime_phase": "006E71",
        "result": result,
        "result_maximum": RESULT_PASS,
        "valid_runtime_semantic_result": RESULT_PASS if clean_semantics else RESULT_INCONCLUSIVE,
        "run_id": run_id,
        "runtime_authorized": AUTHORIZED_RUNTIME,
        "runtime_exists": Path(AUTHORIZED_RUNTIME).exists(),
        "runtime_sys_executable": sys.executable,
        "runtime_matches_authorized": str(Path(sys.executable)) == AUTHORIZED_RUNTIME,
        "python": sys.version,
        "platform": platform.platform(),
        "python_flint_distribution": python_flint_version,
        "flint_version": flint_version,
        "flint_FLINT_VERSION": flint_native_version,
        "arb_independent_version_seal": False,
        "matrix_id": MATRIX_ID,
        "source_matrix_id": "006E71_REPLAY_PLUS_CENTER_YOCTO_TIGHT",
        "input_count": len(MATRIX),
        "replay_inputs_from_006E71": 45,
        "new_inputs": 0,
        "precision_values": PRECISIONS,
        "expected_l_function_records": EXPECTED_RECORDS,
        "observed_l_function_records": len(records),
        "records_pass": records_pass,
        "expected_diagnostics": EXPECTED_DIAGNOSTICS,
        "observed_diagnostics": len(diagnostics),
        "diagnostics_pass": diagnostics_pass,
        "ledger_jsonl_lines": sum(1 for _ in ledger_jsonl.open("r", encoding="utf-8")),
        "diagnostics_jsonl_lines": sum(1 for _ in diagnostics_jsonl.open("r", encoding="utf-8")),
        "unique_input_labels": len(input_labels),
        "all_inputs_constructed_from_exact_rational_descriptors": True,
        "float_inputs_present": False,
        "complex_inputs_present": False,
        "decimal_float_literals_present": False,
        "adaptive_inputs_present": False,
        "adaptive_search": "not_executed",
        "precision_chasing": "not_executed",
        "ctx_restored_for_all_calls": all(record["ctx_restored"] for record in records),
        "output_type_acb_for_all_calls": all(record["output_type"] == "acb" for record in records),
        "output_finite_for_all_calls": all(record["output_finite"] for record in records),
        "output_width_nonzero_for_all_calls": all(record["output_real_lower_ne_upper"] and record["output_imag_lower_ne_upper"] for record in records),
        "input_width_nonzero_for_all_calls": all(record["input_real_lower_ne_upper"] and record["input_imag_lower_ne_upper"] for record in records),
        "diagnostics_are_smoke_only": True,
        "jsonl_path": str(ledger_jsonl),
        "csv_path": str(ledger_csv),
        "markdown_compact_path": str(compact_md),
        "diagnostics_jsonl_path": str(diagnostics_jsonl),
        "diagnostics_csv_path": str(diagnostics_csv),
        "manifest_authority": "identity_and_counts",
        "jsonl_authority": "primary",
        "csv_authority": "secondary",
        "markdown_authority": "summary_only",
        "sha256sums_authority": "file_integrity_only",
        "console_scrollback_authority": "none",
        "manifest_initial_write_before_files_present_check": True,
        "files_present_computed_after_manifest_initial_write": True,
        "manifest_final_written_before_final_SHA256SUMS": True,
        "SHA256SUMS_written_after_final_manifest": True,
        "hashes_computed_after_manifest_finalization": True,
        "hashes_verified_after_SHA256SUMS_write": True,
        "semantic_rerun_performed_for_capture_correction": False,
        "capture_warning": "none",
        "unresolved_capture_warning": False,
        "contours": "not_executed",
        "Lambda_3": "not_evaluated",
        "zero_isolation": "not_executed",
        "zero_counting": "not_executed",
        "zero_tables": "not_generated",
        "project_backend": "not_invoked",
        "H2_pipeline": "not_invoked",
        "mathematical_proof": False,
        "H2_certified": False,
        "006F": "blocked",
        "zero_certification": "forbidden",
        "downstream_use": "forbidden",
        "novelty_claim": False,
    }
    manifest_path.write_text(json.dumps(manifest, indent=4, sort_keys=True) + "\n", encoding="utf-8")

    files_present = all((ARTIFACT_DIR / name).exists() for name in HASHED_FILES)
    manifest["pre_sha_required_files_present_after_manifest_write"] = files_present
    manifest["files_present"] = files_present
    manifest["sha256sums_path"] = str(sha_path)
    manifest["hash_records"] = len(HASHED_FILES)
    manifest["hash_verified"] = True
    manifest_path.write_text(json.dumps(manifest, indent=4, sort_keys=True) + "\n", encoding="utf-8")

    sha_lines = [f"{sha256_file(ARTIFACT_DIR / name)}  {name}" for name in HASHED_FILES]
    sha_path.write_text("\n".join(sha_lines) + "\n", encoding="utf-8")
    hash_verified = verify_sha256sums(sha_path, ARTIFACT_DIR)
    if not hash_verified:
        manifest["hash_verified"] = False
        manifest["result"] = RESULT_INCONCLUSIVE
        manifest["valid_runtime_semantic_result"] = RESULT_INCONCLUSIVE
        manifest_path.write_text(json.dumps(manifest, indent=4, sort_keys=True) + "\n", encoding="utf-8")
        return fail_summary(RESULT_INCONCLUSIVE, "hash verification failed")

    final_all_required_present = all((ARTIFACT_DIR / name).exists() for name in REQUIRED_FILES)
    summary = {
        "phase_id": PHASE_ID,
        "result": result,
        "valid_runtime_semantic_result": manifest["valid_runtime_semantic_result"],
        "records_expected": EXPECTED_RECORDS,
        "records_observed": len(records),
        "records_pass": records_pass,
        "diagnostics_expected": EXPECTED_DIAGNOSTICS,
        "diagnostics_observed": len(diagnostics),
        "diagnostics_pass": diagnostics_pass,
        "files_present": files_present and final_all_required_present,
        "hash_verified": hash_verified,
        "capture_warning": "none",
        "scope_leak": False,
        "artifact_directory": str(ARTIFACT_DIR),
    }
    print(json.dumps(summary, sort_keys=True))
    return 0 if result == RESULT_PASS else 1


if __name__ == "__main__":
    raise SystemExit(main())
