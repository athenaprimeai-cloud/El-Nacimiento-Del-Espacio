# 006E25-NARROW-NON-ADAPTIVE-L-FUNCTION-SEMANTICS-PLAN

## 1. Estado y alcance

```text
phase_id = 006E25
status = l_function_semantics_plan_completed
result = 006E25_L_FUNCTION_SEMANTICS_PLAN_COMPLETED
scope = planning_document_only
source_1 = 006E23-NARROW-REAL-SEMANTIC-TESTS
source_2 = 006E24-DOCUMENT-NARROW-SEMANTIC-RESULT-AND-BOUNDARIES
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

006E25 is a documentary plan for a possible future 006E26. It authorizes no
new runtime contact and does not extend the 006E23 evidence.

## 2. Estado recibido desde 006E23 y 006E24

Received 006E23 state:

```text
006E23_RESULT = 006E23_NARROW_SMOKE_PASS_LIMITED
REAL_FLINT_IMPORT = passed
FLINT_VERSION_SEAL_LIMITED = passed
ARB_SEMANTIC_NARROW_SMOKE = passed_limited
ACB_SEMANTIC_NARROW_SMOKE = passed_limited
NATIVE_L_NONPOINT_ACB_NARROW_SMOKE = passed_limited
MATHEMATICAL_PROOF = false
H2_CERTIFIED = false
006F = blocked
ZERO_CERTIFICATION = forbidden
ZERO_TABLES = not_generated
DOWNSTREAM_USE = forbidden
NOVELTY_CLAIM = false
```

Received 006E24 interpretation:

```text
006E24_RESULT = 006E24_NARROW_SEMANTIC_RESULT_DOCUMENTED
006E23_meaning = narrow_non_certifying_semantic_API_compatibility
general_Arb_semantics_proved = false
general_acb_semantics_proved = false
general_l_function_inclusion_proved = false
zero_free_regions_proved = false
H2_CERTIFIED = false
006F = blocked
```

## 3. Familia fija y no adaptativa de entradas `acb`

A future 006E26 may use only the fixed boxes listed below. The family is
predeclared, finite, non-adaptive, and not chosen from any observed output.

### Parent Boxes

Each parent box is a rectangular `acb(real_arb, imag_arb)` built from exact
rational midpoint and exact rational radius.

| Label | Real midpoint | Real radius | Imag midpoint | Imag radius | Purpose |
| --- | --- | --- | --- | --- | --- |
| `LBOX_P1` | `1/2` | `1/1000` | `7/5` | `1/2000` | Reuse 006E23 region. |
| `LBOX_P2` | `3/4` | `1/2000` | `2/1` | `1/1000` | Reuse 006E23 region. |
| `LBOX_P3` | `1/3` | `1/1500` | `5/3` | `1/1500` | Additional fixed off-axis region. |

### Subboxes

For each parent `LBOX_Pn`, 006E26 may build exactly four subboxes. Their
radii are half the parent radii and their centers are displaced by half a
subbox radius in each real/imaginary direction. This covers four interior
quadrants for a smoke comparison; it is not a proof of coverage of a contour
or any region.

For a parent with:

```text
real_mid = R
real_radius = r
imag_mid = I
imag_radius = s
sub_real_radius = r/2
sub_imag_radius = s/2
real_offsets = [-r/2, +r/2]
imag_offsets = [-s/2, +s/2]
```

the fixed subboxes are:

```text
LBOX_Pn_S1 = (R - r/2 +/- r/2) + i (I - s/2 +/- s/2)
LBOX_Pn_S2 = (R - r/2 +/- r/2) + i (I + s/2 +/- s/2)
LBOX_Pn_S3 = (R + r/2 +/- r/2) + i (I - s/2 +/- s/2)
LBOX_Pn_S4 = (R + r/2 +/- r/2) + i (I + s/2 +/- s/2)
```

Exact expanded subbox definitions:

| Label | Real midpoint | Real radius | Imag midpoint | Imag radius |
| --- | --- | --- | --- | --- |
| `LBOX_P1_S1` | `1999/4000` | `1/2000` | `5599/4000` | `1/4000` |
| `LBOX_P1_S2` | `1999/4000` | `1/2000` | `5601/4000` | `1/4000` |
| `LBOX_P1_S3` | `2001/4000` | `1/2000` | `5599/4000` | `1/4000` |
| `LBOX_P1_S4` | `2001/4000` | `1/2000` | `5601/4000` | `1/4000` |
| `LBOX_P2_S1` | `2999/4000` | `1/4000` | `3999/2000` | `1/2000` |
| `LBOX_P2_S2` | `2999/4000` | `1/4000` | `4001/2000` | `1/2000` |
| `LBOX_P2_S3` | `3001/4000` | `1/4000` | `3999/2000` | `1/2000` |
| `LBOX_P2_S4` | `3001/4000` | `1/4000` | `4001/2000` | `1/2000` |
| `LBOX_P3_S1` | `1999/6000` | `1/3000` | `4999/3000` | `1/3000` |
| `LBOX_P3_S2` | `1999/6000` | `1/3000` | `5001/3000` | `1/3000` |
| `LBOX_P3_S3` | `2001/6000` | `1/3000` | `4999/3000` | `1/3000` |
| `LBOX_P3_S4` | `2001/6000` | `1/3000` | `5001/3000` | `1/3000` |

Total future `l_function` calls, if fully authorized:

```text
parent_boxes = 3
subboxes = 12
total_l_function_inputs = 15
adaptive_inputs = forbidden
```

## 4. Precisiones fijas

006E26 may use only these fixed precision values:

```text
ctx_workprec_values = [96, 128]
```

Planned use:

| Precision | Use |
| --- | --- |
| `96` | Baseline continuity with 006E23 `l_function` calls. |
| `128` | Fixed higher-precision repeat for radius/finite-output stability smoke. |

Forbidden:

```text
precision_chasing = forbidden
choosing_precision_from_output = forbidden
raising_precision_until_result_looks_good = forbidden
using_precision_as_certification = forbidden
```

If a fixed precision gives inconclusive semantics, 006E26 must record that
state. It must not add more precision values during execution.

## 5. Parent/subbox comparison without mathematical proof

006E26 may compare each parent-box output to its four subbox outputs only as a
diagnostic smoke pattern.

Allowed comparisons:

```text
1. parent_output_type_is_acb
2. each_subbox_output_type_is_acb
3. parent_output_is_finite
4. each_subbox_output_is_finite
5. parent_output_real_width_nonzero
6. parent_output_imag_width_nonzero
7. each_subbox_output_real_width_nonzero
8. each_subbox_output_imag_width_nonzero
9. parent_output_contains_each_subbox_output_midpoint_if_API_supports_it
10. parent_output_intersects_each_subbox_output_if_API_supports_it
```

Allowed interpretation:

```text
parent_subbox_diagnostic = smoke_only
```

Forbidden interpretation:

```text
parent_contains_all_subbox_outputs = proof_of_inclusion
subbox_comparison = proof_of_general_l_function_semantics
subbox_comparison = contour_coverage
subbox_comparison = zero_free_evidence
```

If containment or intersection accessors are unavailable or ambiguous, the
comparison must close that contract as inconclusive, not as failure of the
mathematics.

## 6. Detecting midpoint collapse or radius loss

006E26 should classify possible collapse using only observable ball/box
properties:

```text
input_real_lower_ne_upper = required
input_imag_lower_ne_upper = required
output_real_lower_ne_upper = required
output_imag_lower_ne_upper = required
output_type = acb_required
output_finite = required
ctx_restored_after_call = required
```

Midpoint-collapse warning conditions:

```text
input_has_nonzero_width_but_output_real_width_zero
input_has_nonzero_width_but_output_imag_width_zero
parent_output_and_all_subbox_outputs_have_identical_display_bounds
output_width_cannot_be_read
output_component_accessors_are_ambiguous
```

If any warning condition occurs, the future result should be:

```text
006E26_INCONCLUSIVE_L_FUNCTION_SEMANTICS
```

unless a scope breach or environment failure requires a stricter result.

## 7. Finite outputs and nonzero widths

For every fixed input and fixed precision, 006E26 should record:

```text
input_label
precision_bits
input_real_lower
input_real_upper
input_imag_lower
input_imag_upper
output_type
output_finite
output_real_lower
output_real_upper
output_imag_lower
output_imag_upper
output_real_lower_ne_upper
output_imag_lower_ne_upper
ctx_before
ctx_inside
ctx_after
ctx_restored
```

Pass condition for this contract:

```text
all_outputs_type_acb = true
all_outputs_finite = true
all_output_real_widths_nonzero = true
all_output_imag_widths_nonzero = true
all_contexts_restored = true
```

This pass condition is still a smoke result only.

## 8. Exact input discipline and no `float`

All future inputs must be represented as exact rational strings or exact
integer/rational pairs before construction.

Allowed input descriptors:

```text
integer_numerator
integer_denominator
exact_rational_string
fmpq_constructed_from_integers
```

Forbidden input descriptors:

```text
Python_float
Python_complex
decimal_float_literal
computed_float_midpoint
computed_float_radius
adaptive_input_from_previous_output
```

006E26 should include a pre-execution descriptor scan:

```text
float_inputs_present = false_required
complex_inputs_present = false_required
adaptive_inputs_present = false_required
```

If any forbidden descriptor is present, 006E26 must close as:

```text
006E26_FAIL_SCOPE_OR_SEMANTICS
```

## 9. Arb identity limitation

006E26 must preserve the 006E21R/006E23 limitation:

```text
python-flint = 0.8.0
flint.__version__ = 0.8.0
flint.__FLINT_VERSION__ = 3.3.1
Arb_independent_version_seal = false
```

Required wording:

```text
Arb functionality is exercised through python-flint 0.8.0 with observed FLINT
3.3.1 metadata. Arb is not independently versioned by the recorded metadata
chain.
```

If the runtime no longer exposes the expected python-flint or FLINT identity,
006E26 must close as blocked unless Yonnah authorizes a metadata repair phase.

## 10. Inconclusive and blocked conditions

006E26 should close as inconclusive when the runtime exists and scope is
preserved, but semantics cannot be read cleanly:

```text
l_function_rejects_fixed_nonpoint_acb
output_type_is_not_acb
output_finiteness_cannot_be_determined
output_width_cannot_be_determined
output_real_width_collapses_unexpectedly
output_imag_width_collapses_unexpectedly
parent_subbox_comparison_accessor_unavailable
parent_subbox_comparison_is_ambiguous
ctx_restoration_ambiguous
Arb_radius_semantics_ambiguous
```

006E26 should close as blocked when the environment is unavailable or not the
authorized one:

```text
authorized_runtime_missing
import_flint_failed
python_flint_version_mismatch
flint_module_version_mismatch
FLINT_3_3_1_identity_missing_when_required
new_dependency_required
network_required
runtime_not_authorized
```

006E26 should close as scope failure if it executes or authorizes anything
outside the fixed plan:

```text
contour_execution
Lambda_3_evaluation
zero_isolation
zero_counting
zero_table_generation
adaptive_search
precision_chasing
project_backend_invocation
H2_pipeline_invocation
H2_certification
006F_opening
downstream_use
novelty_claim
```

## 11. Maximum allowed results for future 006E26

Allowed future 006E26 results:

```text
006E26_L_FUNCTION_SEMANTIC_SMOKE_PASS_LIMITED
006E26_L_FUNCTION_SEMANTIC_SMOKE_PASS_WITH_WARNINGS
006E26_INCONCLUSIVE_L_FUNCTION_SEMANTICS
006E26_BLOCKED_ENVIRONMENT
006E26_FAIL_SCOPE_OR_SEMANTICS
```

Maximum allowed result:

```text
006E26_L_FUNCTION_SEMANTIC_SMOKE_PASS_LIMITED
```

Meaning of maximum result:

```text
fixed_nonadaptive_l_function_inputs = passed_limited
parent_subbox_diagnostic = passed_limited
general_l_function_inclusion = not_proved
mathematical_proof = false
H2_CERTIFIED = false
006F = blocked
downstream_use = forbidden
```

## 12. Inferences that remain forbidden

The following remain forbidden even if 006E26 passes:

```text
general_l_function_inclusion_proved
general_Arb_semantics_proved
general_acb_semantics_proved
absence_of_midpoint_extraction_proved_for_all_inputs
zero_free_region_proved
zero_count_certified
zero_table_generated
Lambda_3_semantics_authorized
contour_execution_authorized
H2_certified
006F_opened
downstream_use_allowed
novelty_claim_true
```

006E26 must not be used as a mathematical proof or as a bridge into zero work.

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

006E25 preserves every major block inherited from 006E23 and 006E24.

## 14. Recomendacion no vinculante para Yonnah

Recommended next step:

```text
NEXT_STEP = 006E26_NARROW_NON_ADAPTIVE_L_FUNCTION_SEMANTIC_SMOKE
```

Authorize 006E26 only if the desired next move is another fixed, non-adaptive
semantic smoke over `chi.l_function`. Do not authorize contours, `Lambda_3`,
zero work, H2 certification, 006F, downstream use, or novelty claims.

If the Arb version limitation is not acceptable for the intended next step,
insert a metadata/build-attestation phase before 006E26.

## 15. Veredicto

```text
006E25_RESULT = 006E25_L_FUNCTION_SEMANTICS_PLAN_COMPLETED
RESULT_MAXIMUM = 006E25_L_FUNCTION_SEMANTICS_PLAN_COMPLETED
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

006E25 completes a documentary plan only. It does not execute the future
006E26 checks and does not change any mathematical or downstream status.
