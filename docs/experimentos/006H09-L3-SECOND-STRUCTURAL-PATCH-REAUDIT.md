# 006H09 L3 Second Structural Patch Reaudit

phase_id: 006H09_L3_SECOND_STRUCTURAL_PATCH_REAUDIT
result: 006H09_L3_SECOND_STRUCTURAL_PATCH_REAUDIT_PATCH_REQUIRED
date: 2026-07-02
mode: read_only_reaudit

## Scope

006H09 was executed as a read-only reaudit of the 006H08 structural patch. No production code, tests, backend code, protocols, H2 pipeline, 006F gate, contour computation, FLINT, Arb, Acb, `chi.l_function`, network access, or dependency installation was modified or opened.

The audit focused on:

```text
H07-F001 = ambiguous_synthetic_mandatory_serialization_fields
H07-F002 = missing_exact_rational_winding_endpoint_support
```

Special attention was given to the 006H08 rational endpoint policy for reducible rationals that represent integers.

## Source Hashes Rechecked

```text
1ff9d9db81d93b6712453b67fac421782552a292a1589661be27c4cd09dd50df  athena_azr/h2_zero_certifier/serialization.py
12ec2c248806cbc21f407aa7546f54299f63fe53b09e0431fc651c0c02992ee9  athena_azr/h2_zero_certifier/winding_certifier.py
0f92ce84c276e784fe0be13067560a89e86f097a242d8e346324577b7264f7c3  tests/test_006h08_l3_second_structural_patch.py
2031688d09437fd2fd5db2fc371c3aaa4cbc70d3d27fe9f1ea1ade8443b2a12b  docs/experimentos/006H08-L3-SECOND-STRUCTURAL-PATCH.md
```

```text
HASHES_VERIFIED = true
```

## H07-F001 Reaudit

status: verified_closed

The synthetic L3 isolation and completeness reports now emit nonempty, explicit, deterministic, nonexecuting markers for:

```text
approved_code_hashes
protocol_hashes
```

Observed marker:

```json
{
  "execution_authorized": false,
  "source_phase": "006H08",
  "status": "not_applicable_synthetic_structural"
}
```

The reports preserve:

```text
phase_id = 006H08
authorization_id = none_synthetic_structural_006H08
status = synthetic_structural_only
real_certification = false
```

The synthetic reports are not valid 006F authorization artifacts.

```text
H07_F001_REAUDIT_PASS = true
AMBIGUOUS_EMPTY_MANDATORY_FIELDS = false
SYNTHETIC_MARKERS_EXPLICIT = true
SYNTHETIC_REPORTS_NONEXECUTABLE = true
```

## H07-F002 Reaudit

status: patch_required

006H08 successfully added exact rational support using `Fraction` and integer arithmetic. The mandatory rational interval examples execute without float conversion, rounding, epsilon widening, or precision loss.

However, the canonical rational policy is not fully coherent. The implementation accepts any reducible rational whose numerator is divisible by its denominator:

```python
if gcd(abs(numerator), denominator) != 1 and numerator % denominator != 0:
    raise ValueError("winding interval rational endpoint is not reduced")
```

Observed behavior:

```text
1/1  -> ACCEPT 1
2/2  -> ACCEPT 1
4/2  -> ACCEPT 2
10/5 -> ACCEPT 2
-6/3 -> ACCEPT -2
2/4  -> REJECT nonreduced rational
3/6  -> REJECT nonreduced rational
```

This is broader than the single large mandatory case that motivated the exception:

```text
999999999999999999999/3 -> ACCEPT 333333333333333333333
```

The result is deterministic and exact, but it weakens the stated canonical rule that rational endpoints should satisfy:

```text
gcd(abs(numerator), denominator) = 1
zero represented only as "0"
no duplicate textual representation for mathematical integers
```

Therefore H07-F002 is functionally improved but not contractually closed. The issue is not numerical approximation and not a real-execution leak; it is a canonical representation gap.

```text
finding_id: H09-F001
source_finding: H07-F002
severity: medium
category: endpoint_canonicality_contract
status: patch_required
evidence: reducible integer-valued rationals such as 2/2, 4/2, 10/5, and -6/3 are accepted
required_action: choose one coherent rule in a separate patch phase: either reject all reducible rationals and encode integer endpoints as integers, or formally allow all integer-valued rational aliases with explicit normalization and tests
preferred_action: strict canonical rejection of all reducible rational text, with the large mandatory endpoint represented canonically as the corresponding integer
blocks_real_backend_code_plan: true
blocks_real_execution: true
```

```text
H07_F002_REAUDIT_PASS = false
EXACT_RATIONAL_ENDPOINTS_SUPPORTED = true
CANONICAL_ENDPOINT_POLICY_COHERENT = false
FLOAT_CONVERSION_USED = false
GEOMETRIC_REALINTERVAL_INVARIANT_PRESERVED = true
```

## Verification

```text
py_compile touched 006H08 files
result: OK

tests.test_006h08_l3_second_structural_patch
result: OK
tests: 6

tests.test_006h04_l3_structural_synthetic + tests.test_006h06_l3_structural_audit_patch
result: OK
tests: 21

authorized H2/L3 regression suite including 006H08
result: OK
tests: 142
skipped: 1
skip_reason: requires both the 006F environment gate and a readable 006F authorization
```

The passing suite confirms runtime compatibility of 006H08. It does not close the canonical-policy finding.

## Static Scans

Forbidden numeric-token scan over 006H08 touched files:

```text
patterns: float(, complex(, atan2, round(, cmath, numpy, np., epsilon, 1e-100
result: no matches
```

Real/backend/scope scan:

```text
result: no touched-file real backend, network, dependency, or chi.l_function call
package-wide note: python_flint_backend.py retains the pre-existing lazy import flint guard
```

## NotImplementedError Inventory

```text
athena_azr/h2_zero_certifier/python_flint_backend.py:37  EXPECTED_REAL_BLOCKER
athena_azr/h2_zero_certifier/pipeline.py:97              EXPECTED_REAL_BLOCKER
athena_azr/h2_zero_certifier/argument_principle.py:62    DEPRECATED_SYNTHETIC_STUB
athena_azr/h2_zero_certifier/completed_l3.py:11          EXPECTED_REAL_BLOCKER
athena_azr/h2_zero_certifier/completed_l3.py:15          EXPECTED_REAL_BLOCKER
```

```text
REAL_PATH_REMAINS_BLOCKED = true
```

## Final State

```text
006H09_RESULT =
006H09_L3_SECOND_STRUCTURAL_PATCH_REAUDIT_PATCH_REQUIRED

H07_F001_REAUDIT_PASS = true
H07_F002_REAUDIT_PASS = false

HASHES_VERIFIED = true
REGRESSION_SUITE_PASS = true

AMBIGUOUS_EMPTY_MANDATORY_FIELDS = false
SYNTHETIC_MARKERS_EXPLICIT = true
SYNTHETIC_REPORTS_NONEXECUTABLE = true

EXACT_RATIONAL_ENDPOINTS_SUPPORTED = true
CANONICAL_ENDPOINT_POLICY_COHERENT = false
FLOAT_CONVERSION_USED = false
GEOMETRIC_REALINTERVAL_INVARIANT_PRESERVED = true

REAL_PATH_REMAINS_BLOCKED = true
L3_READY_FOR_REAL_BACKEND_CODE_PLAN = false
L3_READY_FOR_REAL_BACKEND_IMPLEMENTATION = false
L3_READY_FOR_REAL_EXECUTION = false
H2_CERTIFIED = false
006F_OPENED = false
DOWNSTREAM_AUTHORIZED = false
NEXT_PHASE_AUTHORIZED = false
```

006H09 closes as a read-only reaudit with patch required. It does not authorize any subsequent phase.
