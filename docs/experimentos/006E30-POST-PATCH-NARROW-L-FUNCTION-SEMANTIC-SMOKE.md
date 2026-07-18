# 006E30-POST-PATCH-NARROW-L-FUNCTION-SEMANTIC-SMOKE

## 1. Estado inicial y bloqueos preservados

```text
phase_id = 006E30
status = post_patch_l_function_semantic_smoke_completed_with_warnings
result = 006E30_POST_PATCH_L_FUNCTION_SEMANTIC_SMOKE_PASS_WITH_WARNINGS
maximum_allowed_result = 006E30_POST_PATCH_L_FUNCTION_SEMANTIC_SMOKE_PASS_LIMITED
source_1 = 006E29-POST-PATCH-NARROW-L-FUNCTION-SEMANTIC-PLAN
source_2 = 006E25P-PATCH-SUBBOX-FORMULA-TABLE-AUTHORITY
scope = fixed_non_adaptive_l_function_semantic_smoke
fixed_inputs_authorized = 18
fixed_precisions_authorized = [96, 128]
planned_l_function_calls = 36
planned_parent_child_diagnostics = 30
adaptive_search = not_executed
precision_chasing = not_executed
project_backend_invocation = not_executed
H2_pipeline_invocation = not_executed
contour_execution = forbidden
Lambda_3_evaluation = forbidden
zero_isolation = forbidden
zero_counting = forbidden
zero_tables = not_generated
new_dependencies = not_installed
network = not_used
MATHEMATICAL_PROOF = false
H2_CERTIFIED = false
006F = blocked
ZERO_CERTIFICATION = forbidden
ZERO_TABLES = not_generated
DOWNSTREAM_USE = forbidden
NOVELTY_CLAIM = false
```

006E30 executed the post-patch matrix defined in 006E29. It did not execute
contours, `Lambda_3`, zero work, project backend, H2 pipeline, downstream use,
or novelty claims.

## 2. Runtime usado

```text
runtime_authorized = C:\Users\johnn\AppData\Local\Temp\athena-006e20r\Scripts\python.exe
runtime_sys_executable = C:\Users\johnn\AppData\Local\Temp\athena-006e20r\Scripts\python.exe
runtime_exists = true
runtime_matches_authorized = true
import_flint = PASS
```

## 3. Versiones observadas

```text
python = 3.12.13 (main, Mar  3 2026, 15:01:35) [MSC v.1944 64 bit (AMD64)]
platform = Windows-11-10.0.26200-SP0
python-flint_distribution = 0.8.0
flint.__version__ = 0.8.0
flint.__FLINT_VERSION__ = 3.3.1
```

The runtime version identity matched the authorized 006E20R/006E20B runtime
chain.

## 4. Lista fija exacta de entradas

Input discipline:

```text
input_count = 18
float_inputs_present = false
complex_inputs_present = false
decimal_float_literals_present = false
adaptive_inputs_present = false
all_inputs_constructed_from_exact_rational_descriptors = true
all_inputs_listed_in_authoritative_table = true
```

CORE parent boxes from 006E25P:

| Label | Real midpoint | Real radius | Imag midpoint | Imag radius |
| --- | --- | --- | --- | --- |
| `LBOX_P1` | `1/2` | `1/1000` | `7/5` | `1/2000` |
| `LBOX_P2` | `3/4` | `1/2000` | `2/1` | `1/1000` |
| `LBOX_P3` | `1/3` | `1/1500` | `5/3` | `1/1500` |

CORE subboxes from the 006E25P authoritative expanded table:

| Label | Parent | Real midpoint | Real radius | Imag midpoint | Imag radius |
| --- | --- | --- | --- | --- | --- |
| `LBOX_P1_S1` | `LBOX_P1` | `1999/4000` | `1/2000` | `5599/4000` | `1/4000` |
| `LBOX_P1_S2` | `LBOX_P1` | `1999/4000` | `1/2000` | `5601/4000` | `1/4000` |
| `LBOX_P1_S3` | `LBOX_P1` | `2001/4000` | `1/2000` | `5599/4000` | `1/4000` |
| `LBOX_P1_S4` | `LBOX_P1` | `2001/4000` | `1/2000` | `5601/4000` | `1/4000` |
| `LBOX_P2_S1` | `LBOX_P2` | `2999/4000` | `1/4000` | `3999/2000` | `1/2000` |
| `LBOX_P2_S2` | `LBOX_P2` | `2999/4000` | `1/4000` | `4001/2000` | `1/2000` |
| `LBOX_P2_S3` | `LBOX_P2` | `3001/4000` | `1/4000` | `3999/2000` | `1/2000` |
| `LBOX_P2_S4` | `LBOX_P2` | `3001/4000` | `1/4000` | `4001/2000` | `1/2000` |
| `LBOX_P3_S1` | `LBOX_P3` | `1999/6000` | `1/3000` | `4999/3000` | `1/3000` |
| `LBOX_P3_S2` | `LBOX_P3` | `1999/6000` | `1/3000` | `5001/3000` | `1/3000` |
| `LBOX_P3_S3` | `LBOX_P3` | `2001/6000` | `1/3000` | `4999/3000` | `1/3000` |
| `LBOX_P3_S4` | `LBOX_P3` | `2001/6000` | `1/3000` | `5001/3000` | `1/3000` |

CENTER refinement boxes from 006E29:

| Label | Parent | Real midpoint | Real radius | Imag midpoint | Imag radius |
| --- | --- | --- | --- | --- | --- |
| `LBOX_P1_C` | `LBOX_P1` | `1/2` | `1/4000` | `7/5` | `1/8000` |
| `LBOX_P2_C` | `LBOX_P2` | `3/4` | `1/8000` | `2/1` | `1/4000` |
| `LBOX_P3_C` | `LBOX_P3` | `1/3` | `1/6000` | `5/3` | `1/6000` |

## 5. Precisiones fijas

```text
ctx_workprec_values = [96, 128]
adaptive_precision = forbidden
precision_chasing = not_executed
```

No precision value was chosen from an observed output.

## 6. Resultados contrato por contrato

| Contract | Result | Notes |
| --- | --- | --- |
| Authorized runtime | PASS | Runtime exists and `sys.executable` matched exactly. |
| `import flint` | PASS | Import succeeded. |
| Version precheck | PASS | python-flint 0.8.0, `flint.__version__` 0.8.0, FLINT 3.3.1. |
| Exact input discipline | PASS | 18/18 entries were exact rational descriptors. |
| Fixed matrix size | PASS | 18 inputs x 2 precisions = 36 records. |
| `chi.l_function` output type | PASS | 36/36 outputs were `acb`. |
| Output finiteness | PASS | 36/36 outputs finite. |
| Nonzero real output width | PASS | 36/36 real output components had lower != upper. |
| Nonzero imaginary output width | PASS | 36/36 imaginary output components had lower != upper. |
| Context restoration | PASS | 36/36 calls restored `ctx.prec` to 53. |
| Parent/child diagnostic | PASS_DIAGNOSTIC | 30/30 diagnostics had `contains=true` and `overlaps=true`. |
| Report capture | WARNING | The console JSON containing all exact textual bounds was truncated by the host display. Summary counts and representative bound fields were captured; exact full bound strings are not fully persisted in this report. |
| Harness correction | WARNING | A pre-run `python -c` quoting issue occurred before import; an initial invalid `arb.add_error` constructor attempt then failed before `l_function`. The valid run used `arb(fmpq(mid), fmpq(radius))`, matching the documented 006E17 pattern. |

Summary of the valid run:

```text
records = 36
records_pass = 36
diagnostics = 30
diagnostics_pass = 30
all_contexts_restored = true
all_outputs_type_acb = true
all_outputs_finite = true
all_output_real_widths_nonzero = true
all_output_imag_widths_nonzero = true
semantic_runtime_result = 006E30_POST_PATCH_L_FUNCTION_SEMANTIC_SMOKE_PASS_LIMITED
reported_phase_result = 006E30_POST_PATCH_L_FUNCTION_SEMANTIC_SMOKE_PASS_WITH_WARNINGS
```

The warning is documentary/capture-level, not a failed `chi.l_function`
contract in the valid run.

## 7. Ledger compacto por entrada y precision

Column key:

```text
label = input_label
bits = precision_bits
input_bounds = lower/upper bounds were read for real and imaginary input components
output_bounds = lower/upper bounds were read for real and imaginary output components
rw/iw = output real/imag lower_ne_upper
ctx = ctx_before/ctx_inside/ctx_after
```

The host display truncated part of the raw JSON ledger. This compact ledger
preserves the per-call contract outcome without treating display strings as
canonical mathematical serialization.

```text
label|bits|input_bounds|output_type|finite|output_bounds|rw|iw|ctx|restored|result
LBOX_P1|96|read|acb|true|read|true|true|53/96/53|true|PASS
LBOX_P2|96|read|acb|true|read|true|true|53/96/53|true|PASS
LBOX_P3|96|read|acb|true|read|true|true|53/96/53|true|PASS
LBOX_P1_S1|96|read|acb|true|read|true|true|53/96/53|true|PASS
LBOX_P1_S2|96|read|acb|true|read|true|true|53/96/53|true|PASS
LBOX_P1_S3|96|read|acb|true|read|true|true|53/96/53|true|PASS
LBOX_P1_S4|96|read|acb|true|read|true|true|53/96/53|true|PASS
LBOX_P2_S1|96|read|acb|true|read|true|true|53/96/53|true|PASS
LBOX_P2_S2|96|read|acb|true|read|true|true|53/96/53|true|PASS
LBOX_P2_S3|96|read|acb|true|read|true|true|53/96/53|true|PASS
LBOX_P2_S4|96|read|acb|true|read|true|true|53/96/53|true|PASS
LBOX_P3_S1|96|read|acb|true|read|true|true|53/96/53|true|PASS
LBOX_P3_S2|96|read|acb|true|read|true|true|53/96/53|true|PASS
LBOX_P3_S3|96|read|acb|true|read|true|true|53/96/53|true|PASS
LBOX_P3_S4|96|read|acb|true|read|true|true|53/96/53|true|PASS
LBOX_P1_C|96|read|acb|true|read|true|true|53/96/53|true|PASS
LBOX_P2_C|96|read|acb|true|read|true|true|53/96/53|true|PASS
LBOX_P3_C|96|read|acb|true|read|true|true|53/96/53|true|PASS
LBOX_P1|128|read|acb|true|read|true|true|53/128/53|true|PASS
LBOX_P2|128|read|acb|true|read|true|true|53/128/53|true|PASS
LBOX_P3|128|read|acb|true|read|true|true|53/128/53|true|PASS
LBOX_P1_S1|128|read|acb|true|read|true|true|53/128/53|true|PASS
LBOX_P1_S2|128|read|acb|true|read|true|true|53/128/53|true|PASS
LBOX_P1_S3|128|read|acb|true|read|true|true|53/128/53|true|PASS
LBOX_P1_S4|128|read|acb|true|read|true|true|53/128/53|true|PASS
LBOX_P2_S1|128|read|acb|true|read|true|true|53/128/53|true|PASS
LBOX_P2_S2|128|read|acb|true|read|true|true|53/128/53|true|PASS
LBOX_P2_S3|128|read|acb|true|read|true|true|53/128/53|true|PASS
LBOX_P2_S4|128|read|acb|true|read|true|true|53/128/53|true|PASS
LBOX_P3_S1|128|read|acb|true|read|true|true|53/128/53|true|PASS
LBOX_P3_S2|128|read|acb|true|read|true|true|53/128/53|true|PASS
LBOX_P3_S3|128|read|acb|true|read|true|true|53/128/53|true|PASS
LBOX_P3_S4|128|read|acb|true|read|true|true|53/128/53|true|PASS
LBOX_P1_C|128|read|acb|true|read|true|true|53/128/53|true|PASS
LBOX_P2_C|128|read|acb|true|read|true|true|53/128/53|true|PASS
LBOX_P3_C|128|read|acb|true|read|true|true|53/128/53|true|PASS
```

Representative exact bound fields captured from the valid run:

```text
LBOX_P1|96 input real lower = [0.4989999999979772837832570076 +/- 1.13e-30]
LBOX_P1|96 input real upper = [0.5010000000020227162167429924 +/- 1.13e-30]
LBOX_P1|96 input imag lower = [1.399499999998079147189855576 +/- 4.44e-28]
LBOX_P1|96 input imag upper = [1.400500000001920852810144424 +/- 4.34e-28]
LBOX_P1|96 output real lower = [0.5594272225161875106395284800 +/- 3.13e-29]
LBOX_P1|96 output real upper = [0.6184906594453240253032247691 +/- 6.28e-30]
LBOX_P1|96 output imag lower = [0.3552149495239212444324786454 +/- 3.28e-29]
LBOX_P1|96 output imag upper = [0.4164717703837744226951892167 +/- 2.82e-29]
LBOX_P3_C|128 input real lower = [0.33316666666617796484691401322682698568 +/- 3.90e-39]
LBOX_P3_C|128 input real upper = [0.33350000000048870181975265343983968099 +/- 1.40e-39]
LBOX_P3_C|128 input imag lower = [1.6664999999995112981802473465601603190 +/- 8.46e-39]
LBOX_P3_C|128 input imag upper = [1.6668333333338220351530859867731730143 +/- 2.10e-38]
LBOX_P3_C|128 output real lower = [0.57528266960236931493617635369196722050 +/- 4.51e-39]
LBOX_P3_C|128 output real upper = [0.61210042515251541784144979119196722050 +/- 4.51e-39]
LBOX_P3_C|128 output imag lower = [0.47739183557762921734630105128249623949 +/- 7.52e-40]
LBOX_P3_C|128 output imag upper = [0.51421039771133259816943642725905873949 +/- 7.18e-40]
```

## 8. Diagnosticos madre/hijo

The parent/child comparison is smoke-only. It is not mathematical proof,
coverage proof, zero-free evidence, or contour evidence.

```text
parent|child|bits|contains|overlaps|result
LBOX_P1|LBOX_P1_S1|96|true|true|PASS_DIAGNOSTIC
LBOX_P1|LBOX_P1_S2|96|true|true|PASS_DIAGNOSTIC
LBOX_P1|LBOX_P1_S3|96|true|true|PASS_DIAGNOSTIC
LBOX_P1|LBOX_P1_S4|96|true|true|PASS_DIAGNOSTIC
LBOX_P1|LBOX_P1_C|96|true|true|PASS_DIAGNOSTIC
LBOX_P2|LBOX_P2_S1|96|true|true|PASS_DIAGNOSTIC
LBOX_P2|LBOX_P2_S2|96|true|true|PASS_DIAGNOSTIC
LBOX_P2|LBOX_P2_S3|96|true|true|PASS_DIAGNOSTIC
LBOX_P2|LBOX_P2_S4|96|true|true|PASS_DIAGNOSTIC
LBOX_P2|LBOX_P2_C|96|true|true|PASS_DIAGNOSTIC
LBOX_P3|LBOX_P3_S1|96|true|true|PASS_DIAGNOSTIC
LBOX_P3|LBOX_P3_S2|96|true|true|PASS_DIAGNOSTIC
LBOX_P3|LBOX_P3_S3|96|true|true|PASS_DIAGNOSTIC
LBOX_P3|LBOX_P3_S4|96|true|true|PASS_DIAGNOSTIC
LBOX_P3|LBOX_P3_C|96|true|true|PASS_DIAGNOSTIC
LBOX_P1|LBOX_P1_S1|128|true|true|PASS_DIAGNOSTIC
LBOX_P1|LBOX_P1_S2|128|true|true|PASS_DIAGNOSTIC
LBOX_P1|LBOX_P1_S3|128|true|true|PASS_DIAGNOSTIC
LBOX_P1|LBOX_P1_S4|128|true|true|PASS_DIAGNOSTIC
LBOX_P1|LBOX_P1_C|128|true|true|PASS_DIAGNOSTIC
LBOX_P2|LBOX_P2_S1|128|true|true|PASS_DIAGNOSTIC
LBOX_P2|LBOX_P2_S2|128|true|true|PASS_DIAGNOSTIC
LBOX_P2|LBOX_P2_S3|128|true|true|PASS_DIAGNOSTIC
LBOX_P2|LBOX_P2_S4|128|true|true|PASS_DIAGNOSTIC
LBOX_P2|LBOX_P2_C|128|true|true|PASS_DIAGNOSTIC
LBOX_P3|LBOX_P3_S1|128|true|true|PASS_DIAGNOSTIC
LBOX_P3|LBOX_P3_S2|128|true|true|PASS_DIAGNOSTIC
LBOX_P3|LBOX_P3_S3|128|true|true|PASS_DIAGNOSTIC
LBOX_P3|LBOX_P3_S4|128|true|true|PASS_DIAGNOSTIC
LBOX_P3|LBOX_P3_C|128|true|true|PASS_DIAGNOSTIC
```

Allowed interpretation:

```text
parent_child_diagnostic = smoke_only
contains_true = API_diagnostic_only
overlaps_true = API_diagnostic_only
```

Forbidden interpretation:

```text
contains_true = mathematical_theorem
overlaps_true = mathematical_theorem
parent_child_diagnostic = proof_of_l_function_inclusion
parent_child_diagnostic = proof_of_region_coverage
parent_child_diagnostic = contour_argument
parent_child_diagnostic = zero_free_region_evidence
```

## 9. Advertencias y errores

Warnings preserved in this report:

```text
warning_1 = valid semantic run passed limited, but report label kept WITH_WARNINGS because full textual bounds ledger was truncated by host display
warning_2 = initial command transport using python -c stripped quotes before import; corrected by using python stdin
warning_3 = initial arb.add_error constructor attempt failed before l_function; corrected to arb(fmpq(mid), fmpq(radius))
warning_4 = Arb_independent_version_seal remains false
```

The valid run was not downgraded by a `chi.l_function` failure. The warnings
are about arnes/capture limitations and the standing Arb identity limitation.

No inconclusive semantic contract remained in the valid run:

```text
valid_run_records_inconclusive = 0
valid_run_diagnostics_inconclusive = 0
```

## 10. Pruebas explicitamente no realizadas

```text
contours = not_executed
Lambda_3 = not_evaluated
zero_isolation = not_executed
zero_counting = not_executed
zero_tables = not_generated
adaptive_search = not_executed
precision_chasing = not_executed
project_backend = not_invoked
H2_pipeline = not_invoked
H2_certification = not_performed
006F_opening = not_performed
downstream_use = forbidden
novelty_claim = false
new_dependencies = not_installed
network = not_used
```

## 11. Limite de identidad Arb

```text
python-flint = 0.8.0
flint.__version__ = 0.8.0
flint.__FLINT_VERSION__ = 3.3.1
Arb_independent_version_seal = false
```

Arb functionality is exercised through python-flint 0.8.0 with observed FLINT
3.3.1 metadata. Arb is not independently versioned by the recorded metadata
chain.

## 12. Veredicto limitado

```text
006E30_RESULT = 006E30_POST_PATCH_L_FUNCTION_SEMANTIC_SMOKE_PASS_WITH_WARNINGS
MAXIMUM_ALLOWED_RESULT = 006E30_POST_PATCH_L_FUNCTION_SEMANTIC_SMOKE_PASS_LIMITED
VALID_RUNTIME_SEMANTIC_RESULT = 006E30_POST_PATCH_L_FUNCTION_SEMANTIC_SMOKE_PASS_LIMITED
REPORT_LABEL_WARNING_REASON = arnes_and_capture_warnings_preserved
REAL_FLINT_IMPORT = passed
FLINT_VERSION_SEAL_LIMITED = passed
FIXED_NONADAPTIVE_L_FUNCTION_INPUTS = passed_limited_with_warnings
PARENT_CHILD_DIAGNOSTIC = passed_limited_smoke_only
MATHEMATICAL_PROOF = false
H2_CERTIFIED = false
H2_CERTIFIED_TRUE = false
006F = blocked
006F_OPENED = false
ZERO_CERTIFICATION = forbidden
ZERO_CERTIFICATION_COMPLETED = false
ZERO_TABLES = not_generated
DOWNSTREAM_USE = forbidden
DOWNSTREAM_USE_ALLOWED = false
NOVELTY_CLAIM = false
```

006E30 is a post-patch narrow semantic smoke result only. It does not prove
general `chi.l_function` inclusion semantics, Arb semantics, acb semantics,
zero-free regions, H2, or any downstream theorem.

## 13. Recomendacion no vinculante para Yonnah

Recommended next step:

```text
NEXT_STEP = 006E31_DOCUMENT_POST_PATCH_L_FUNCTION_SMOKE_RESULT
```

Do not proceed to contours, `Lambda_3`, zero work, H2 certification, 006F, or
downstream use. The next phase should document what 006E30 means, including
the difference between the clean semantic pass of the valid run and the
warnings retained for arnes/capture limitations.
