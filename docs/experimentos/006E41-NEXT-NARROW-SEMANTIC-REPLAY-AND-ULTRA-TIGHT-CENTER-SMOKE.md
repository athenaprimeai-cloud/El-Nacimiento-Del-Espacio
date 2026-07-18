# 006E41-NEXT-NARROW-SEMANTIC-REPLAY-AND-ULTRA-TIGHT-CENTER-SMOKE

## 1. Estado inicial y alcance ejecutado

```text
phase_id = 006E41
status = next_narrow_semantic_smoke_pass_with_warnings
result = 006E41_NEXT_NARROW_SEMANTIC_SMOKE_PASS_WITH_WARNINGS
valid_runtime_semantic_result = 006E41_NEXT_NARROW_SEMANTIC_SMOKE_PASS_LIMITED
maximum_allowed_result = 006E41_NEXT_NARROW_SEMANTIC_SMOKE_PASS_LIMITED
source_plan = 006E40-NEXT-NARROW-SEMANTIC-PLAN-AFTER-006E39
scope = controlled_real_semantic_smoke
runtime_authorized = C:\Users\johnn\AppData\Local\Temp\athena-006e20r\Scripts\python.exe
artifact_directory = artifacts/006E41-next-narrow-semantic-ledger/
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

006E41 executed only the fixed matrix authorized by 006E40:

```text
future_matrix_id = 006E41_REPLAY_PLUS_CENTER_ULTRA_TIGHT
replay_inputs_from_006E37 = 21
new_center_ultra_tight_inputs = 3
total_input_count = 24
precision_values = [96, 128]
expected_l_function_records = 48
expected_diagnostics = 42
```

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

006E41 used the 24 labels authorized by 006E40 and no other inputs.

| label | block | parent | real_mid | real_rad | imag_mid | imag_rad |
| --- | --- | --- | --- | --- | --- | --- |
| `LBOX_P1` | `CORE_PARENT` | none | `1/2` | `1/1000` | `7/5` | `1/2000` |
| `LBOX_P1_S1` | `CORE_SUBBOX` | `LBOX_P1` | `1999/4000` | `1/2000` | `5599/4000` | `1/4000` |
| `LBOX_P1_S2` | `CORE_SUBBOX` | `LBOX_P1` | `1999/4000` | `1/2000` | `5601/4000` | `1/4000` |
| `LBOX_P1_S3` | `CORE_SUBBOX` | `LBOX_P1` | `2001/4000` | `1/2000` | `5599/4000` | `1/4000` |
| `LBOX_P1_S4` | `CORE_SUBBOX` | `LBOX_P1` | `2001/4000` | `1/2000` | `5601/4000` | `1/4000` |
| `LBOX_P1_C` | `CENTER_REFINEMENT` | `LBOX_P1` | `1/2` | `1/4000` | `7/5` | `1/8000` |
| `LBOX_P1_CT` | `CENTER_TIGHT` | `LBOX_P1_C` | `1/2` | `1/8000` | `7/5` | `1/16000` |
| `LBOX_P1_CUT` | `CENTER_ULTRA_TIGHT` | `LBOX_P1_CT` | `1/2` | `1/16000` | `7/5` | `1/32000` |
| `LBOX_P2` | `CORE_PARENT` | none | `3/4` | `1/2000` | `2/1` | `1/1000` |
| `LBOX_P2_S1` | `CORE_SUBBOX` | `LBOX_P2` | `2999/4000` | `1/4000` | `3999/2000` | `1/2000` |
| `LBOX_P2_S2` | `CORE_SUBBOX` | `LBOX_P2` | `2999/4000` | `1/4000` | `4001/2000` | `1/2000` |
| `LBOX_P2_S3` | `CORE_SUBBOX` | `LBOX_P2` | `3001/4000` | `1/4000` | `3999/2000` | `1/2000` |
| `LBOX_P2_S4` | `CORE_SUBBOX` | `LBOX_P2` | `3001/4000` | `1/4000` | `4001/2000` | `1/2000` |
| `LBOX_P2_C` | `CENTER_REFINEMENT` | `LBOX_P2` | `3/4` | `1/8000` | `2/1` | `1/4000` |
| `LBOX_P2_CT` | `CENTER_TIGHT` | `LBOX_P2_C` | `3/4` | `1/16000` | `2/1` | `1/8000` |
| `LBOX_P2_CUT` | `CENTER_ULTRA_TIGHT` | `LBOX_P2_CT` | `3/4` | `1/32000` | `2/1` | `1/16000` |
| `LBOX_P3` | `CORE_PARENT` | none | `1/3` | `1/1500` | `5/3` | `1/1500` |
| `LBOX_P3_S1` | `CORE_SUBBOX` | `LBOX_P3` | `1999/6000` | `1/3000` | `4999/3000` | `1/3000` |
| `LBOX_P3_S2` | `CORE_SUBBOX` | `LBOX_P3` | `1999/6000` | `1/3000` | `5001/3000` | `1/3000` |
| `LBOX_P3_S3` | `CORE_SUBBOX` | `LBOX_P3` | `2001/6000` | `1/3000` | `4999/3000` | `1/3000` |
| `LBOX_P3_S4` | `CORE_SUBBOX` | `LBOX_P3` | `2001/6000` | `1/3000` | `5001/3000` | `1/3000` |
| `LBOX_P3_C` | `CENTER_REFINEMENT` | `LBOX_P3` | `1/3` | `1/6000` | `5/3` | `1/6000` |
| `LBOX_P3_CT` | `CENTER_TIGHT` | `LBOX_P3_C` | `1/3` | `1/12000` | `5/3` | `1/12000` |
| `LBOX_P3_CUT` | `CENTER_ULTRA_TIGHT` | `LBOX_P3_CT` | `1/3` | `1/24000` | `5/3` | `1/24000` |

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
records_expected = 48
records_observed = 48
records_pass = 48
diagnostics_expected = 42
diagnostics_observed = 42
diagnostics_pass = 42
files_present = true
hash_verified = true
ctx_restored_for_all_calls = true
output_type_acb_for_all_calls = true
output_finite_for_all_calls = true
output_width_nonzero_for_all_calls = true
```

Per-call contracts:

| Contract | Result | Count |
| --- | --- | ---: |
| `chi.l_function` calls over fixed input matrix | PASS | 48/48 |
| Output type is `acb` | PASS | 48/48 |
| Output finite | PASS | 48/48 |
| Output real lower/upper non-equal | PASS | 48/48 |
| Output imaginary lower/upper non-equal | PASS | 48/48 |
| Context restored after call | PASS | 48/48 |
| Parent/child diagnostics | PASS | 42/42 |
| Diagnostic `contains=true` | PASS | 42/42 |
| Diagnostic `overlaps=true` | PASS | 42/42 |

These are smoke contracts only. `contains=true`, `overlaps=true`, `48/48`, and
`42/42` are not mathematical theorems.

## 6. Diagnosticos ejecutados

Allowed diagnostics were executed exactly:

```text
parent_to_existing_children = 3 parents x 5 children x 2 precisions = 30
center_to_tight_children = 3 centers x 1 child x 2 precisions = 6
tight_to_ultra_tight_children = 3 tight centers x 1 child x 2 precisions = 6
total_diagnostics = 42
diagnostics_are_smoke_only = true
```

No diagnostic was used as a zero test, contour test, H2 test, or downstream
certificate.

## 7. Artefactos persistidos

All required artifacts were persisted under:

```text
artifacts/006E41-next-narrow-semantic-ledger/
```

| Artifact | Bytes | Authority |
| --- | ---: | --- |
| `ledger.jsonl` | 75542 | Primary |
| `ledger.csv` | 39367 | Secondary |
| `ledger-compact.md` | 7971 | Summary only |
| `diagnostics.jsonl` | 9537 | Primary diagnostics |
| `diagnostics.csv` | 4777 | Secondary diagnostics |
| `manifest.json` | 3239 | Identity and counts |
| `SHA256SUMS.txt` | 495 | File integrity only |

Line counts:

```text
ledger_jsonl_lines = 48
ledger_csv_lines = 49
diagnostics_jsonl_lines = 42
diagnostics_csv_lines = 43
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
945c1cf3f4d20422bc585cb56cc4392104eae447337d832ebb5e3c80832ee498  ledger.jsonl
fb3a207823112aadd0c65c32421bd435c0f3ea92802c8b44286bca07839ef248  ledger.csv
0bbc1b459075cef01c327408b5cf109fe243065701db275747373a50e3c32e62  ledger-compact.md
e37ee4f47c258c0a35aef70dd2f9a7b8079eae2396f90ff5e08219f8cc359849  diagnostics.jsonl
1fe2562acb42096afc24ca2e55d879a0f3732c416dfd4feacea5d9ff1291737c  diagnostics.csv
be56659bf3f2929c6721bdb7eb4534136d5377a1dd7ba347b2bd8f18df76a233  manifest.json
```

Hash verification result:

```text
hash_verified = true
```

SHA-256 verifies file integrity only. It is not mathematical evidence.

## 9. Advertencia de captura/arnes

The first harness summary classified the run as `FAIL_SCOPE_OR_SEMANTICS`
because the `files_present` flag was computed before `manifest.json` existed.
The semantic records and diagnostic records had already passed.

Final classification:

```text
006E41_RESULT = 006E41_NEXT_NARROW_SEMANTIC_SMOKE_PASS_WITH_WARNINGS
VALID_RUNTIME_SEMANTIC_RESULT = 006E41_NEXT_NARROW_SEMANTIC_SMOKE_PASS_LIMITED
capture_warning = initial_harness_files_present_flag_computed_before_manifest_write
semantic_rerun_performed_for_capture_correction = false
hashes_recomputed_after_manifest_correction = true
unresolved_capture_warning = false
```

The warning does not invalidate the valid semantic run:

```text
semantic_records_changed_by_capture_correction = false
diagnostic_records_changed_by_capture_correction = false
input_matrix_changed_by_capture_correction = false
precision_set_changed_by_capture_correction = false
```

The historical phase label remains `PASS_WITH_WARNINGS` because the harness
emitted a transient capture classification before metadata finalization.

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
48_of_48 = mathematical_proof
42_of_42 = mathematical_proof
complete_ledger = mathematical_proof
hash_verified = mathematical_proof
complete_ledger = zero_free_region_evidence
contains_true = mathematical_theorem
overlaps_true = mathematical_theorem
center_ultra_tight_pass = zero_absence
006E41 = H2_certification
006E41 = 006F_readiness
006E41 = downstream_permission
006E41 = novelty_claim
```

Forbidden operational promotions:

```text
authorize_contours_from_006E41 = false
authorize_Lambda_3_from_006E41 = false
authorize_zero_work_from_006E41 = false
authorize_H2_from_006E41 = false
open_006F_from_006E41 = false
allow_downstream_use_from_006E41 = false
claim_novelty_from_006E41 = false
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

006E41 does not change H2, 006F, zero status, downstream status, or novelty
status.

## 13. Recomendacion no vinculante para Yonnah

Recommended next step:

```text
NEXT_STEP = 006E42_DOCUMENT_006E41_RESULT_AND_CAPTURE_WARNING
```

006E42 should be documentary only. It should interpret the 48/48 and 42/42
result, preserve the distinction between `PASS_WITH_WARNINGS` and the valid
runtime semantic `PASS_LIMITED`, and keep all mathematical/downstream blocks
closed.

Do not proceed to contours, `Lambda_3`, zero work, H2 certification, 006F,
downstream use, or novelty claims.

## 14. Veredicto

```text
006E41_RESULT = 006E41_NEXT_NARROW_SEMANTIC_SMOKE_PASS_WITH_WARNINGS
RESULT_MAXIMUM = 006E41_NEXT_NARROW_SEMANTIC_SMOKE_PASS_LIMITED
VALID_RUNTIME_SEMANTIC_RESULT = 006E41_NEXT_NARROW_SEMANTIC_SMOKE_PASS_LIMITED
RUN_ID = 006E41-20260627T043058Z
ARTIFACT_DIRECTORY = artifacts/006E41-next-narrow-semantic-ledger/
RUNTIME_MATCHES_AUTHORIZED = true
REAL_FLINT_IMPORT = passed
python-flint = 0.8.0
flint.__version__ = 0.8.0
flint.__FLINT_VERSION__ = 3.3.1
ARB_INDEPENDENT_VERSION_SEAL = false
MATRIX_ID = 006E41_REPLAY_PLUS_CENTER_ULTRA_TIGHT
INPUTS_TOTAL = 24
INPUTS_REPLAY_FROM_006E37 = 21
INPUTS_CENTER_ULTRA_TIGHT = 3
PRECISIONS = [96, 128]
records_expected = 48
records_observed = 48
records_pass = 48
diagnostics_expected = 42
diagnostics_observed = 42
diagnostics_pass = 42
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

006E41 completes the next narrow semantic replay and ultra-tight center smoke
with warnings. The valid runtime semantic smoke passed limited; the phase label
keeps warnings because of the resolved capture/manifest timing issue. It is
not a mathematical proof.
