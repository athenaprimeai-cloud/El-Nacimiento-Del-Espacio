# 006E29-POST-PATCH-NARROW-L-FUNCTION-SEMANTIC-PLAN

## 1. Estado y alcance

```text
phase_id = 006E29
status = post_patch_l_function_plan_completed
result = 006E29_POST_PATCH_L_FUNCTION_PLAN_COMPLETED
scope = planning_document_only
source_1 = 006E25P-PATCH-SUBBOX-FORMULA-TABLE-AUTHORITY
source_2 = 006E26-NARROW-NON-ADAPTIVE-L-FUNCTION-SEMANTIC-SMOKE
source_3 = 006E27-DOCUMENT-L-FUNCTION-SMOKE-RESULT-AND-PLAN-TENSION
source_4 = 006E28-POST-PATCH-L-FUNCTION-SMOKE-READINESS-REVIEW
new_tests_executed = false
flint_imported = false
arb_executed = false
acb_executed = false
ctx_workprec_executed = false
dirichlet_char_executed = false
l_function_executed = false
contour_execution = forbidden
Lambda_3_evaluation = forbidden
zero_isolation = forbidden
zero_counting = forbidden
zero_tables = not_generated
project_backend_invocation = forbidden
H2_pipeline_invocation = forbidden
MATHEMATICAL_PROOF = false
H2_CERTIFIED = false
006F = blocked
ZERO_CERTIFICATION = forbidden
ZERO_TABLES = not_generated
DOWNSTREAM_USE = forbidden
NOVELTY_CLAIM = false
```

006E29 is a documentary plan only. It prepares a possible future 006E30
semantic smoke phase, but it does not authorize execution.

## 2. Estado recibido

From 006E25P:

```text
006E25P_RESULT = 006E25P_PATCH_COMPLETED_TABLE_AUTHORITY_ACCEPTED
EXPANDED_RATIONAL_TABLE_IS_AUTHORITATIVE = true
NARRATIVE_FORMULA_IS_DESCRIPTIVE_ONLY = true
NARRATIVE_FORMULA_MUST_NOT_OVERRIDE_TABLE = true
006E26_ACCEPTED_AS_PASS_WITH_WARNINGS = true
006E26_RESULT_UPGRADED = false
006E26_RESULT_INVALIDATED = false
```

From 006E26 and 006E27:

```text
006E26_RESULT = 006E26_L_FUNCTION_SEMANTIC_SMOKE_PASS_WITH_WARNINGS
records = 30
records_pass = 30
diagnostics = 24
diagnostics_pass = 24
warning_historical = true
mathematical_proof_created = false
```

From 006E28:

```text
006E28_RESULT = 006E28_POST_PATCH_READINESS_DOCUMENTED
READY_TO_PLAN_NEXT_NARROW_L_SEMANTIC_PHASE = true
READY_TO_EXECUTE_NEXT_REAL_PHASE = false
EXPANDED_TABLE_AUTHORITY = true
```

006E29 therefore starts from a cleaned planning base: future input authority is
resolved, while the historical 006E26 warning remains preserved.

## 3. Matriz fija futura `acb` para 006E30

A future 006E30 may use a strictly fixed matrix with two named blocks:

```text
006E30_INPUT_BLOCK_A = CORE_006E25P_AUTHORITY
006E30_INPUT_BLOCK_B = CENTER_REFINEMENT_FIXED
adaptive_inputs = forbidden
formula_derived_unlisted_inputs = forbidden
```

The full future matrix would contain:

```text
core_parent_boxes = 3
core_subboxes = 12
center_refinement_boxes = 3
total_future_inputs = 18
```

Every entry must be an `acb(real_arb, imag_arb)` built from exact rational
midpoint and exact rational radius descriptors. No Python `float`, no Python
`complex`, no decimal literal, and no input chosen from runtime output may be
used.

### 3.1 CORE parent boxes from 006E25P

These entries are copied from the authoritative 006E25P table.

| Label | Real midpoint | Real radius | Imag midpoint | Imag radius |
| --- | --- | --- | --- | --- |
| `LBOX_P1` | `1/2` | `1/1000` | `7/5` | `1/2000` |
| `LBOX_P2` | `3/4` | `1/2000` | `2/1` | `1/1000` |
| `LBOX_P3` | `1/3` | `1/1500` | `5/3` | `1/1500` |

### 3.2 CORE subboxes from 006E25P

These entries are copied from the authoritative 006E25P table. The table, not
the older narrative formula, is the operative source of truth.

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

### 3.3 CENTER refinement boxes

006E30 may add only these three new fixed center-refinement boxes. They are
predeclared here as an exact table, not as runtime-derived inputs.

| Label | Parent | Real midpoint | Real radius | Imag midpoint | Imag radius |
| --- | --- | --- | --- | --- | --- |
| `LBOX_P1_C` | `LBOX_P1` | `1/2` | `1/4000` | `7/5` | `1/8000` |
| `LBOX_P2_C` | `LBOX_P2` | `3/4` | `1/8000` | `2/1` | `1/4000` |
| `LBOX_P3_C` | `LBOX_P3` | `1/3` | `1/6000` | `5/3` | `1/6000` |

Allowed interpretation of the center refinement:

```text
center_refinement = fixed_additional_smoke_inputs
center_refinement = not_adaptive
center_refinement = not_contour
center_refinement = not_zero_search
center_refinement = not_certification
```

The center boxes are meant to test one additional nonpoint `acb` box per
parent region, preserving exact rational discipline and limiting growth from
15 inputs to 18 inputs.

## 4. Reuso y extension de autoridad de tabla

006E30 must read the matrix in this order:

```text
1. Use the 006E25P expanded rational table exactly for CORE entries.
2. Use the 006E29 center-refinement table exactly for CENTER entries.
3. Treat all formulas and prose descriptions as non-authoritative.
4. Reject any unlisted input.
```

Authority rules:

```text
CORE_TABLE_AUTHORITY = 006E25P
CENTER_TABLE_AUTHORITY = 006E29
FORMULA_AUTHORITY = false
UNLISTED_INPUTS_ALLOWED = false
```

If a later phase detects a conflict between prose and table coordinates, the
table wins only if that table is explicitly named as authoritative. Otherwise
the phase must close as inconclusive or request a documentary patch.

## 5. Precisiones fijas para una futura 006E30

Recommended fixed precision list:

```text
ctx_workprec_values = [96, 128]
```

Reason:

```text
1. It preserves continuity with 006E26.
2. It avoids turning the next smoke into precision chasing.
3. It keeps the planned call count bounded: 18 inputs x 2 precisions = 36.
```

Forbidden precision behavior:

```text
precision_chasing = forbidden
adaptive_precision = forbidden
raising_precision_after_bad_output = forbidden
choosing_precision_from_previous_result = forbidden
using_precision_as_certification = forbidden
```

If 006E30 wants to add a third precision such as `160`, that value must be
explicitly authorized in 006E30 before execution. Without that separate
authorization, the only allowed precision values are `96` and `128`.

## 6. Disciplina de entradas exactas

Future 006E30 descriptors must be exact.

Allowed descriptors:

```text
integer_numerator
integer_denominator
exact_rational_string
fmpq_constructed_from_integers
```

Forbidden descriptors:

```text
Python_float
Python_complex
decimal_float_literal
computed_float_midpoint
computed_float_radius
adaptive_input_from_previous_output
input_selected_after_observing_result
```

Required pre-execution descriptor check for 006E30:

```text
float_inputs_present = false_required
complex_inputs_present = false_required
decimal_float_literals_present = false_required
adaptive_inputs_present = false_required
all_inputs_listed_in_authoritative_table = true_required
```

If any forbidden descriptor appears, 006E30 must close as scope failure.

## 7. Disciplina de ejecucion no adaptativa

006E30, if separately authorized, must execute the listed matrix in a fixed
order chosen before runtime. No output may influence:

```text
next_input
next_precision
whether_to_add_inputs
whether_to_drop_inputs
whether_to_repeat_inputs
whether_to_execute_diagnostics
```

Permitted fixed order:

```text
1. LBOX_P1, LBOX_P2, LBOX_P3
2. LBOX_P1_S1 through LBOX_P1_S4
3. LBOX_P2_S1 through LBOX_P2_S4
4. LBOX_P3_S1 through LBOX_P3_S4
5. LBOX_P1_C, LBOX_P2_C, LBOX_P3_C
```

For each input, 006E30 may run only the predeclared precision list. With the
recommended list, the future ledger size would be:

```text
inputs = 18
precisions = 2
planned_l_function_records = 36
```

## 8. Diagnosticos madre/subcaja solo como smoke

006E30 may run parent/subbox and parent/center diagnostics only as smoke-level
checks, if accessors remain available and unambiguous.

Allowed future diagnostics:

```text
parent_output_type_is_acb
child_output_type_is_acb
parent_output_is_finite
child_output_is_finite
parent_output_real_width_nonzero
parent_output_imag_width_nonzero
child_output_real_width_nonzero
child_output_imag_width_nonzero
parent_output_contains_child_output_if_API_supports_it
parent_output_overlaps_child_output_if_API_supports_it
```

Planned diagnostic count with recommended precision list:

```text
parents = 3
children_per_parent = 5
precisions = 2
planned_parent_child_diagnostics = 30
```

The five children per parent are:

```text
LBOX_Pn_S1
LBOX_Pn_S2
LBOX_Pn_S3
LBOX_Pn_S4
LBOX_Pn_C
```

Allowed interpretation:

```text
parent_child_diagnostic = smoke_only
```

Forbidden interpretation:

```text
parent_contains_child_outputs = proof_of_l_function_inclusion
parent_child_diagnostic = proof_of_input_region_coverage
parent_child_diagnostic = contour_argument
parent_child_diagnostic = zero_free_region_evidence
contains_true = mathematical_theorem
overlaps_true = mathematical_theorem
```

If containment or overlap accessors are unavailable, ambiguous, or produce
unreadable semantics, 006E30 must close that contract as inconclusive. It must
not reinterpret the diagnostic as a mathematical failure or proof.

## 9. Limitacion de identidad Arb

006E30 must preserve the 006E21R/006E23/006E26 limitation:

```text
python-flint_expected = 0.8.0
flint.__version___expected = 0.8.0
flint.__FLINT_VERSION___expected = 3.3.1
Arb_independent_version_seal = false
```

Required wording in 006E30:

```text
Arb functionality is exercised through python-flint 0.8.0 with observed FLINT
3.3.1 metadata. Arb is not independently versioned by the recorded metadata
chain.
```

Allowed interpretation:

```text
FLINT_VERSION_SEAL_LIMITED = environmental_metadata_limited
Arb_identity = not_independently_sealed
```

Forbidden interpretation:

```text
flint.__FLINT_VERSION__ = independent_Arb_version_certificate
python_flint_version = mathematical_evidence
version_metadata = proof_of_l_function_semantics
```

If the expected version metadata is missing or changed, 006E30 should close as
blocked unless Yonnah authorizes a separate metadata repair or review phase.

## 10. Resultados permitidos para una futura 006E30

Allowed result labels for a future 006E30:

```text
006E30_POST_PATCH_L_FUNCTION_SEMANTIC_SMOKE_PASS_LIMITED
006E30_POST_PATCH_L_FUNCTION_SEMANTIC_SMOKE_PASS_WITH_WARNINGS
006E30_INCONCLUSIVE_L_FUNCTION_SEMANTICS
006E30_BLOCKED_ENVIRONMENT
006E30_FAIL_SCOPE_OR_SEMANTICS
```

Maximum allowed future result:

```text
006E30_POST_PATCH_L_FUNCTION_SEMANTIC_SMOKE_PASS_LIMITED
```

Meaning of the maximum result:

```text
fixed_nonadaptive_l_function_inputs = passed_limited
parent_child_diagnostic = passed_limited_smoke_only
general_l_function_inclusion = not_proved
mathematical_proof = false
H2_CERTIFIED = false
006F = blocked
downstream_use = forbidden
```

Even the maximum future result would remain a smoke-level observation over a
finite fixed matrix.

## 11. Condiciones inconclusive, blocked y scope failure

006E30 should close as inconclusive when the authorized runtime exists and the
scope is preserved, but semantics cannot be read cleanly:

```text
l_function_rejects_fixed_nonpoint_acb
output_type_is_not_acb
output_finiteness_cannot_be_determined
output_width_cannot_be_determined
output_real_width_collapses_unexpectedly
output_imag_width_collapses_unexpectedly
parent_child_comparison_accessor_unavailable
parent_child_comparison_is_ambiguous
ctx_restoration_ambiguous
Arb_radius_semantics_ambiguous
result_ledger_incomplete_without_scope_breach
```

006E30 should close as blocked when the environment is unavailable or no
longer matches the authorized runtime identity:

```text
authorized_runtime_missing
runtime_not_authorized
import_flint_failed
python_flint_version_mismatch
flint_module_version_mismatch
FLINT_3_3_1_identity_missing_when_required
new_dependency_required
network_required
```

006E30 should close as scope failure if it executes or authorizes anything
outside the fixed plan:

```text
unlisted_input_used
Python_float_used
Python_complex_used
decimal_float_literal_used
adaptive_search_executed
precision_chasing_executed
contour_execution
Lambda_3_evaluation
zero_isolation
zero_counting
zero_table_generation
project_backend_invocation
H2_pipeline_invocation
H2_certification
006F_opening
downstream_use
novelty_claim
new_dependency_installation
network_use
```

## 12. Inferencias que siguen prohibidas

The following remain forbidden even if future 006E30 passes:

```text
general_l_function_inclusion_proved
general_Arb_semantics_proved
general_acb_semantics_proved
absence_of_midpoint_extraction_proved_for_all_inputs
parent_child_diagnostic_proves_coverage
finite_outputs_prove_zero_free_region
nonzero_width_outputs_certify_zeros_absent
zero_count_certified
zero_table_generated
Lambda_3_semantics_authorized
contour_execution_authorized
H2_certified
006F_opened
downstream_use_allowed
novelty_claim_true
```

006E30 must not be used as a mathematical proof or as a bridge into zero work.

## 13. Bloqueos preservados

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

006E29 preserves every major block inherited from 006E25P, 006E26, 006E27,
and 006E28.

## 14. Recomendacion no vinculante para Yonnah

Recommended next step, only if another real smoke is desired:

```text
NEXT_STEP = 006E30_POST_PATCH_NARROW_L_FUNCTION_SEMANTIC_SMOKE
```

Recommended authorization posture:

```text
AUTHORIZE_006E30 = only_after_explicit_Yonnah_authorization
AUTHORIZE_CONTOURS = false
AUTHORIZE_Lambda_3 = false
AUTHORIZE_ZERO_WORK = false
AUTHORIZE_H2 = false
AUTHORIZE_006F = false
AUTHORIZE_DOWNSTREAM = false
```

The cleanest future move would be a narrow 006E30 smoke over exactly the 18
listed inputs and the fixed precision list `[96, 128]`. Do not expand to
contours, `Lambda_3`, zero work, H2 certification, 006F, downstream use, or
novelty claims.

## 15. Veredicto

```text
006E29_RESULT = 006E29_POST_PATCH_L_FUNCTION_PLAN_COMPLETED
RESULT_MAXIMUM = 006E29_POST_PATCH_L_FUNCTION_PLAN_COMPLETED
PATCH_REQUIRED = no
SCOPE_LEAK = false
NEW_REAL_EXECUTION = false
FLINT_IMPORT = not_performed
ARB_EXECUTION = not_performed
ACB_EXECUTION = not_performed
CTX_WORKPREC_EXECUTION = not_performed
DIRICHLET_CHAR_EXECUTION = not_performed
L_FUNCTION_EXECUTION = not_performed
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

006E29 completes a documentary post-patch plan. It defines a future narrow,
fixed, non-adaptive `chi.l_function` smoke matrix while preserving all
mathematical, zero-work, H2, 006F, downstream, and novelty blocks.
