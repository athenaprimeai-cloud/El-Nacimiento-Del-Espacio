# 006E25P-PATCH-SUBBOX-FORMULA-TABLE-AUTHORITY

## 1. Estado recibido desde 006E27

```text
phase_id = 006E25P
status = patch_completed_table_authority_accepted
result = 006E25P_PATCH_COMPLETED_TABLE_AUTHORITY_ACCEPTED
source_1 = 006E25-NARROW-NON-ADAPTIVE-L-FUNCTION-SEMANTICS-PLAN
source_2 = 006E26-NARROW-NON-ADAPTIVE-L-FUNCTION-SEMANTIC-SMOKE
source_3 = 006E27-DOCUMENT-L-FUNCTION-SMOKE-RESULT-AND-PLAN-TENSION
scope = documentary_patch_only
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

006E27 received and interpreted 006E26 as:

```text
006E26_RESULT = 006E26_L_FUNCTION_SEMANTIC_SMOKE_PASS_WITH_WARNINGS
records = 30
records_pass = 30
diagnostics = 24
diagnostics_pass = 24
warning = 006E25 subbox formula/table tension noted; exact expanded table used
PATCH_REQUIRED_FOR_006E26_ACCEPTANCE = no
PATCH_RECOMMENDED_FOR_006E25 = yes
```

006E25P applies the recommended documentary patch. It does not re-run,
upgrade, or mathematically reinterpret 006E26.

## 2. Descripcion exacta de la tension formula/tabla

006E25 described subboxes in two ways:

```text
1. Narrative formula:
   subbox centers are displaced by half a subbox radius in each
   real/imaginary direction.

2. Exact expanded table:
   explicit rational coordinates for LBOX_P1_S1 through LBOX_P3_S4.
```

The formula and the expanded table are not perfectly aligned in every
coordinate. The tension is documentary rather than computational:

```text
tension_type = formula_table_documentary_mismatch
runtime_failure = false
semantic_failure = false
scope_leak = false
adaptive_input_introduced = false
```

006E26 resolved the ambiguity operationally by using the exact expanded table
as the source of truth.

## 3. Decision documental adoptada

Decision:

```text
EXPANDED_RATIONAL_TABLE_IS_AUTHORITATIVE = true
NARRATIVE_FORMULA_IS_DESCRIPTIVE_ONLY = true
NARRATIVE_FORMULA_MUST_NOT_OVERRIDE_TABLE = true
006E26_INPUT_LIST_REMAINS_VALID = true
```

The patch adopts the expanded rational table from 006E25 as the future
operational authority for the 006E25/006E26 subbox family.

This patch does not rewrite the historical 006E26 result. It clarifies how to
read 006E25 after 006E27:

```text
read_006E25_subbox_formula = non_authoritative_description
read_006E25_expanded_table = authoritative_input_list
```

## 4. Tabla expandida exacta preservada como autoridad futura

Parent boxes:

| Label | Real midpoint | Real radius | Imag midpoint | Imag radius |
| --- | --- | --- | --- | --- |
| `LBOX_P1` | `1/2` | `1/1000` | `7/5` | `1/2000` |
| `LBOX_P2` | `3/4` | `1/2000` | `2/1` | `1/1000` |
| `LBOX_P3` | `1/3` | `1/1500` | `5/3` | `1/1500` |

Authoritative subbox table:

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

Future references to the 006E25 subbox family must use this table unless a
later explicitly authorized documentary patch supersedes it.

## 5. Status of 006E26

006E26 remains accepted as:

```text
006E26_ACCEPTED_AS = 006E26_L_FUNCTION_SEMANTIC_SMOKE_PASS_WITH_WARNINGS
006E26_RESULT_UPGRADED = false
006E26_RESULT_INVALIDATED = false
006E26_RUNTIME_SMOKE_VALIDITY = preserved_limited_with_warning
```

The warning was appropriate because 006E26 ran while the formula/table tension
was still active. This patch clarifies future authority but does not
retroactively change the reported result.

## 6. No mathematical proof created

This patch does not convert 006E26 into proof:

```text
mathematical_proof_created = false
general_l_function_inclusion_proved = false
general_Arb_semantics_proved = false
general_acb_semantics_proved = false
zero_free_region_proved = false
zero_certificate_created = false
H2_CERTIFIED = false
006F = blocked
```

The 30/30 and 24/24 observations from 006E26 remain smoke-level API evidence
only.

## 7. No new tests authorized

006E25P authorizes no new execution:

```text
new_real_execution_authorized = false
flint_import_authorized = false
arb_execution_authorized = false
acb_execution_authorized = false
ctx_workprec_execution_authorized = false
dirichlet_char_execution_authorized = false
l_function_execution_authorized = false
contour_execution_authorized = false
Lambda_3_evaluation_authorized = false
zero_work_authorized = false
backend_invocation_authorized = false
H2_pipeline_invocation_authorized = false
```

Any later execution requires separate explicit Yonnah authorization.

## 8. Bloqueos preservados

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

No H2, 006F, zero, downstream, or novelty state changes in 006E25P.

## 9. Recomendacion no vinculante para Yonnah

Recommended status after this patch:

```text
006E25P = accepted_table_authority_patch
006E26 = remains_pass_with_warnings
WARNING_FOR_FORMULA_TABLE_TENSION = resolved_for_future_authority
WARNING_FOR_006E26_HISTORICAL_LABEL = remains
```

The next phase, if any, should be documentary first: document whether the
resolved table authority is sufficient to plan another narrow semantic phase.
Do not proceed to contours, `Lambda_3`, zero work, H2 certification, 006F,
downstream use, or novelty claims.

## 10. Veredicto

```text
006E25P_RESULT = 006E25P_PATCH_COMPLETED_TABLE_AUTHORITY_ACCEPTED
RESULT_MAXIMUM = 006E25P_PATCH_COMPLETED_TABLE_AUTHORITY_ACCEPTED
PATCH_TYPE = table_authority_accepted
FORMULA_CORRECTED_INLINE = no
EXPANDED_TABLE_AUTHORITY = true
006E26_ACCEPTED_AS_PASS_WITH_WARNINGS = true
006E26_RESULT_UPGRADED = false
006E26_RESULT_INVALIDATED = false
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

006E25P resolves the future authority of the subbox table while preserving
006E26 as a limited smoke result with historical warning.
