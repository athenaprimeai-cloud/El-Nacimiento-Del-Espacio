# 006E45-NEXT-NARROW-FIXED-SEMANTIC-REPLAY-AND-MICRO-TIGHT-CENTER-SMOKE

## 1. Estado inicial y alcance ejecutado

```text
phase_id = 006E45
source_plan = 006E44-NEXT-NARROW-FIXED-SEMANTIC-PLAN
matrix_id = 006E45_REPLAY_PLUS_CENTER_MICRO_TIGHT
scope = controlled_real_semantic_smoke
runtime_authorized = C:\Users\johnn\AppData\Local\Temp\athena-006e20r\Scripts\python.exe
artifact_directory = artifacts/006E45-next-narrow-fixed-semantic-ledger/
replay_inputs_from_006E41 = 24
new_center_micro_tight_inputs = 3
total_input_count = 27
precision_values = [96, 128]
expected_l_function_records = 54
expected_diagnostics = 48
new_dependencies = not_installed
network = not_used
adaptive_search = not_executed
precision_chasing = not_executed
project_backend_invocation = not_executed
H2_pipeline_invocation = not_executed
contour_execution = forbidden
Lambda_3_evaluation = forbidden
zero_isolation = forbidden
zero_counting = forbidden
zero_tables = not_generated
MATHEMATICAL_PROOF = false
H2_CERTIFIED = false
006F = blocked
ZERO_CERTIFICATION = forbidden
ZERO_TABLES = not_generated
DOWNSTREAM_USE = forbidden
NOVELTY_CLAIM = false
```

006E45 executed the fixed matrix authorized by 006E44. No unlisted input,
unlisted precision, adaptive search, precision chasing, contour, `Lambda_3`,
zero procedure, project backend, or H2 pipeline was executed.

## 2. Runtime y versiones observadas

```text
runtime_exists = true
runtime_sys_executable = C:\Users\johnn\AppData\Local\Temp\athena-006e20r\Scripts\python.exe
runtime_matches_authorized = true
import_flint = PASS
python = 3.12.13 (main, Mar  3 2026, 15:01:35) [MSC v.1944 64 bit (AMD64)]
platform = Windows-11-10.0.26200-SP0
python-flint_distribution = 0.8.0
flint.__version__ = 0.8.0
flint.__FLINT_VERSION__ = 3.3.1
Arb_independent_version_seal = false
```

Arb remains not separately versioned by the recorded metadata chain.

## 3. Matriz fija exacta usada

006E45 used exactly 27 labels: 24 replay entries from 006E41 and 3 new
`CENTER_MICRO_TIGHT` entries from 006E44.

| label | block | parent | real_mid | real_rad | imag_mid | imag_rad | source |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `LBOX_P1` | `CORE_PARENT` | none | `1/2` | `1/1000` | `7/5` | `1/2000` | replay_006E41 |
| `LBOX_P1_S1` | `CORE_SUBBOX` | `LBOX_P1` | `1999/4000` | `1/2000` | `5599/4000` | `1/4000` | replay_006E41 |
| `LBOX_P1_S2` | `CORE_SUBBOX` | `LBOX_P1` | `1999/4000` | `1/2000` | `5601/4000` | `1/4000` | replay_006E41 |
| `LBOX_P1_S3` | `CORE_SUBBOX` | `LBOX_P1` | `2001/4000` | `1/2000` | `5599/4000` | `1/4000` | replay_006E41 |
| `LBOX_P1_S4` | `CORE_SUBBOX` | `LBOX_P1` | `2001/4000` | `1/2000` | `5601/4000` | `1/4000` | replay_006E41 |
| `LBOX_P1_C` | `CENTER_REFINEMENT` | `LBOX_P1` | `1/2` | `1/4000` | `7/5` | `1/8000` | replay_006E41 |
| `LBOX_P1_CT` | `CENTER_TIGHT` | `LBOX_P1_C` | `1/2` | `1/8000` | `7/5` | `1/16000` | replay_006E41 |
| `LBOX_P1_CUT` | `CENTER_ULTRA_TIGHT` | `LBOX_P1_CT` | `1/2` | `1/16000` | `7/5` | `1/32000` | replay_006E41 |
| `LBOX_P1_CMT` | `CENTER_MICRO_TIGHT` | `LBOX_P1_CUT` | `1/2` | `1/32000` | `7/5` | `1/64000` | new_006E45 |
| `LBOX_P2` | `CORE_PARENT` | none | `3/4` | `1/2000` | `2/1` | `1/1000` | replay_006E41 |
| `LBOX_P2_S1` | `CORE_SUBBOX` | `LBOX_P2` | `2999/4000` | `1/4000` | `3999/2000` | `1/2000` | replay_006E41 |
| `LBOX_P2_S2` | `CORE_SUBBOX` | `LBOX_P2` | `2999/4000` | `1/4000` | `4001/2000` | `1/2000` | replay_006E41 |
| `LBOX_P2_S3` | `CORE_SUBBOX` | `LBOX_P2` | `3001/4000` | `1/4000` | `3999/2000` | `1/2000` | replay_006E41 |
| `LBOX_P2_S4` | `CORE_SUBBOX` | `LBOX_P2` | `3001/4000` | `1/4000` | `4001/2000` | `1/2000` | replay_006E41 |
| `LBOX_P2_C` | `CENTER_REFINEMENT` | `LBOX_P2` | `3/4` | `1/8000` | `2/1` | `1/4000` | replay_006E41 |
| `LBOX_P2_CT` | `CENTER_TIGHT` | `LBOX_P2_C` | `3/4` | `1/16000` | `2/1` | `1/8000` | replay_006E41 |
| `LBOX_P2_CUT` | `CENTER_ULTRA_TIGHT` | `LBOX_P2_CT` | `3/4` | `1/32000` | `2/1` | `1/16000` | replay_006E41 |
| `LBOX_P2_CMT` | `CENTER_MICRO_TIGHT` | `LBOX_P2_CUT` | `3/4` | `1/64000` | `2/1` | `1/32000` | new_006E45 |
| `LBOX_P3` | `CORE_PARENT` | none | `1/3` | `1/1500` | `5/3` | `1/1500` | replay_006E41 |
| `LBOX_P3_S1` | `CORE_SUBBOX` | `LBOX_P3` | `1999/6000` | `1/3000` | `4999/3000` | `1/3000` | replay_006E41 |
| `LBOX_P3_S2` | `CORE_SUBBOX` | `LBOX_P3` | `1999/6000` | `1/3000` | `5001/3000` | `1/3000` | replay_006E41 |
| `LBOX_P3_S3` | `CORE_SUBBOX` | `LBOX_P3` | `2001/6000` | `1/3000` | `4999/3000` | `1/3000` | replay_006E41 |
| `LBOX_P3_S4` | `CORE_SUBBOX` | `LBOX_P3` | `2001/6000` | `1/3000` | `5001/3000` | `1/3000` | replay_006E41 |
| `LBOX_P3_C` | `CENTER_REFINEMENT` | `LBOX_P3` | `1/3` | `1/6000` | `5/3` | `1/6000` | replay_006E41 |
| `LBOX_P3_CT` | `CENTER_TIGHT` | `LBOX_P3_C` | `1/3` | `1/12000` | `5/3` | `1/12000` | replay_006E41 |
| `LBOX_P3_CUT` | `CENTER_ULTRA_TIGHT` | `LBOX_P3_CT` | `1/3` | `1/24000` | `5/3` | `1/24000` | replay_006E41 |
| `LBOX_P3_CMT` | `CENTER_MICRO_TIGHT` | `LBOX_P3_CUT` | `1/3` | `1/48000` | `5/3` | `1/48000` | new_006E45 |

Input discipline:

```text
all_inputs_constructed_from_exact_rational_descriptors = true
float_inputs_present = false
complex_inputs_present = false
decimal_float_literals_present = false
adaptive_inputs_present = false
```

## 4. Precisiones fijas usadas

```text
precision_values = [96, 128]
precision_count = 2
unlisted_precision_used = false
precision_chasing = not_executed
adaptive_precision_selection = not_executed
```

No precision outside `[96, 128]` was used.

## 5. Resultados contrato por contrato

```text
records_expected = 54
records_observed = 54
records_pass = 54
diagnostics_expected = 48
diagnostics_observed = 48
diagnostics_pass = 48
files_present = true
hash_verified = true
ctx_restored_for_all_calls = true
output_type_acb_for_all_calls = true
output_finite_for_all_calls = true
output_width_nonzero_for_all_calls = true
input_width_nonzero_for_all_calls = true
```

Per-call contracts:

| Contract | Result | Count |
| --- | --- | ---: |
| `chi.l_function` calls over fixed input matrix | PASS | 54/54 |
| Output type is `acb` | PASS | 54/54 |
| Output finite | PASS | 54/54 |
| Output real lower/upper non-equal | PASS | 54/54 |
| Output imaginary lower/upper non-equal | PASS | 54/54 |
| Context restored after call | PASS | 54/54 |
| Parent/child diagnostics | PASS | 48/48 |
| Diagnostic `contains=true` | PASS | 48/48 |
| Diagnostic `overlaps=true` | PASS | 48/48 |

These are smoke contracts only. `54/54`, `48/48`, `contains=true`, and
`overlaps=true` are not mathematical theorems.

## 6. Diagnosticos ejecutados

Allowed diagnostics were executed exactly:

```text
parent_to_existing_children = 3 parents x 5 children x 2 precisions = 30
center_to_tight_children = 3 centers x 1 child x 2 precisions = 6
tight_to_ultra_tight_children = 3 tight centers x 1 child x 2 precisions = 6
ultra_tight_to_micro_tight_children = 3 ultra tight centers x 1 child x 2 precisions = 6
total_diagnostics = 48
diagnostics_are_smoke_only = true
```

No diagnostic was used as a zero test, contour test, H2 test, or downstream
certificate.

## 7. Artefactos persistidos

All required artifacts were persisted under:

```text
artifacts/006E45-next-narrow-fixed-semantic-ledger/
```

| Artifact | Bytes | Authority |
| --- | ---: | --- |
| `ledger.jsonl` | 86647 | Primary |
| `ledger.csv` | 44832 | Secondary |
| `ledger-compact.md` | 8943 | Summary only |
| `diagnostics.jsonl` | 10974 | Primary diagnostics |
| `diagnostics.csv` | 5397 | Secondary diagnostics |
| `manifest.json` | 3781 | Identity and counts |
| `SHA256SUMS.txt` | 495 | File integrity only |

Line counts:

```text
ledger_jsonl_lines = 54
ledger_csv_lines = 55
diagnostics_jsonl_lines = 48
diagnostics_csv_lines = 49
```

CSV line counts include one header row.

Authority:

```text
JSONL_AUTHORITY = primary
CSV_AUTHORITY = secondary
MARKDOWN_COMPACT_AUTHORITY = summary_only
MANIFEST_AUTHORITY = identity_and_counts
SHA256SUMS_AUTHORITY = file_integrity_only
CONSOLE_SCROLLBACK_AUTHORITY = none
```

## 8. Hashes SHA-256

`SHA256SUMS.txt` contains:

```text
d45912baaa5f6d1c91441360f2e058d2e1647554b7878546bc10c098649aecfd  ledger.jsonl
02d78768b704b1fa8ce33e5e68dcbadb8d7a1761fc1005b936a4c461b3a25262  ledger.csv
c7bf5d6306be1213895dfedde9025f31effe7332a8d4db604439877eeb211547  ledger-compact.md
884954b73c7026e5de32a903eac84ce7387673e3550ce0babec936b60722f711  diagnostics.jsonl
b78343884082a59223ecd27af770c280b86cd7ccf1877fdb8f1adeef2ce61c1c  diagnostics.csv
bf8bd025283d2c8d8420c4c10e384a3cef819f078d5fb727b98227bce67d805c  manifest.json
```

Hash verification result:

```text
hash_verified = true
```

SHA-256 verifies file integrity only. It is not mathematical evidence.

## 9. Advertencia de captura/arnes

The first harness summary classified the run as `FAIL_SCOPE_OR_SEMANTICS`
because `files_present` was computed before `manifest.json` existed. The
semantic records and diagnostic records had already passed:

```text
initial_harness_result = 006E45_FAIL_SCOPE_OR_SEMANTICS
records_observed = 54
records_pass = 54
diagnostics_observed = 48
diagnostics_pass = 48
```

Final classification:

```text
006E45_RESULT = 006E45_NEXT_NARROW_FIXED_SEMANTIC_SMOKE_PASS_WITH_WARNINGS
VALID_RUNTIME_SEMANTIC_RESULT = 006E45_NEXT_NARROW_FIXED_SEMANTIC_SMOKE_PASS_LIMITED
CAPTURE_WARNING = initial_harness_files_present_flag_computed_before_manifest_write
SEMANTIC_RERUN_PERFORMED_FOR_CAPTURE_CORRECTION = false
HASHES_RECOMPUTED_AFTER_MANIFEST_CORRECTION = true
UNRESOLVED_CAPTURE_WARNING = false
```

The metadata correction did not rerun FLINT, did not alter the input matrix,
did not alter the precision set, and did not alter semantic or diagnostic
records.

## 10. Pruebas explicitamente no realizadas

```text
contours = not_executed
Lambda_3 = not_evaluated
zero_isolation = not_executed
zero_counting = not_executed
zero_tables = not_generated
adaptive_search = not_executed
precision_chasing = not_executed
unlisted_inputs = not_used
unlisted_precisions = not_used
project_backend = not_invoked
H2_pipeline = not_invoked
H2_certification = not_performed
006F_opening = not_performed
downstream_use = forbidden
novelty_claim = false
new_dependencies = not_installed
network = not_used
```

## 11. Inferencias prohibidas

The following remain forbidden:

```text
54_of_54 = mathematical_proof
48_of_48_diagnostics = mathematical_proof
complete_ledger = mathematical_proof
hash_verified = mathematical_proof
complete_ledger = zero_free_region_evidence
contains_true = mathematical_theorem
overlaps_true = mathematical_theorem
center_micro_tight_pass = zero_absence
006E45 = H2_certification
006E45 = 006F_readiness
006E45 = downstream_permission
006E45 = novelty_claim
```

Forbidden operational promotions:

```text
authorize_contours_from_006E45 = false
authorize_Lambda_3_from_006E45 = false
authorize_zero_work_from_006E45 = false
authorize_H2_from_006E45 = false
open_006F_from_006E45 = false
allow_downstream_use_from_006E45 = false
claim_novelty_from_006E45 = false
```

## 12. Bloqueos preservados

```text
MATHEMATICAL_PROOF = false
H2_CERTIFIED = false
006F = blocked
ZERO_CERTIFICATION = forbidden
ZERO_TABLES = not_generated
DOWNSTREAM_USE = forbidden
NOVELTY_CLAIM = false
REAL_CONTOUR_EXECUTION = forbidden
LAMBDA_3_EVALUATION = forbidden
PROJECT_BACKEND_INVOCATION = forbidden
H2_PIPELINE_INVOCATION = forbidden
```

006E45 does not change H2, 006F, zero status, downstream status, or novelty
status.

## 13. Recomendacion no vinculante para Yonnah

Recommended next step:

```text
NEXT_STEP = 006E46_DOCUMENT_006E45_RESULT_AND_CAPTURE_WARNING
```

006E46 should be documentary only. It should interpret the `54/54` and `48/48`
result, preserve the distinction between the historical `PASS_WITH_WARNINGS`
label and the valid runtime semantic `PASS_LIMITED`, and keep all mathematical
and downstream blocks closed.

Do not proceed to contours, `Lambda_3`, zero work, H2 certification, 006F,
downstream use, or novelty claims.

## 14. Veredicto

```text
006E45_RESULT = 006E45_NEXT_NARROW_FIXED_SEMANTIC_SMOKE_PASS_WITH_WARNINGS
RESULT_MAXIMUM = 006E45_NEXT_NARROW_FIXED_SEMANTIC_SMOKE_PASS_LIMITED
VALID_RUNTIME_SEMANTIC_RESULT = 006E45_NEXT_NARROW_FIXED_SEMANTIC_SMOKE_PASS_LIMITED
INITIAL_HARNESS_RESULT = 006E45_FAIL_SCOPE_OR_SEMANTICS
RUN_ID = 006E45-20260627T045916Z
ARTIFACT_DIRECTORY = artifacts/006E45-next-narrow-fixed-semantic-ledger/
RUNTIME_MATCHES_AUTHORIZED = true
REAL_FLINT_IMPORT = passed
python-flint = 0.8.0
flint.__version__ = 0.8.0
flint.__FLINT_VERSION__ = 3.3.1
ARB_INDEPENDENT_VERSION_SEAL = false
MATRIX_ID = 006E45_REPLAY_PLUS_CENTER_MICRO_TIGHT
INPUTS_TOTAL = 27
INPUTS_REPLAY_FROM_006E41 = 24
INPUTS_CENTER_MICRO_TIGHT = 3
PRECISIONS = [96, 128]
records_expected = 54
records_observed = 54
records_pass = 54
diagnostics_expected = 48
diagnostics_observed = 48
diagnostics_pass = 48
files_present = true
hash_verified = true
ctx_restored_for_all_calls = true
output_type_acb_for_all_calls = true
output_finite_for_all_calls = true
output_width_nonzero_for_all_calls = true
JSONL_AUTHORITY = primary
CSV_AUTHORITY = secondary
MARKDOWN_COMPACT_AUTHORITY = summary_only
MANIFEST_AUTHORITY = identity_and_counts
SHA256SUMS_AUTHORITY = file_integrity_only
CONSOLE_SCROLLBACK_AUTHORITY = none
CAPTURE_WARNING = initial_harness_files_present_flag_computed_before_manifest_write
SEMANTIC_RERUN_PERFORMED_FOR_CAPTURE_CORRECTION = false
HASHES_RECOMPUTED_AFTER_MANIFEST_CORRECTION = true
UNRESOLVED_CAPTURE_WARNING = false
SCOPE_LEAK = false
NEW_DEPENDENCIES_INSTALLED = false
NETWORK_USED = false
CONTOUR_EXECUTION = forbidden
LAMBDA_3_EVALUATION = forbidden
ZERO_CERTIFICATION = forbidden
ZERO_TABLES = not_generated
MATHEMATICAL_PROOF = false
H2_CERTIFIED = false
006F = blocked
006F_OPENED = false
DOWNSTREAM_USE = forbidden
NOVELTY_CLAIM = false
```

006E45 completes the next narrow fixed semantic replay and micro-tight center
smoke with warnings. The valid runtime semantic smoke passed limited; the phase
label keeps warnings because of the resolved capture/manifest timing issue. It
is not a mathematical proof.
