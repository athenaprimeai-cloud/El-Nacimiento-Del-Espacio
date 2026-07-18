# 006H08 L3 Second Structural Patch

phase_id: 006H08_L3_SECOND_STRUCTURAL_PATCH
result: 006H08_L3_SECOND_STRUCTURAL_PATCH_PASS
date: 2026-07-02
mode: narrow_structural_patch

## Scope

006H08 patched only the two findings authorized from 006H07:

```text
H07-F001 = ambiguous_synthetic_mandatory_serialization_fields
H07-F002 = missing_exact_rational_winding_endpoint_support
```

No real backend implementation was added. No H2, 006F, FLINT, Arb, Acb, `chi.l_function`, contours, zero isolation, zero counting, downstream workflow, network access, or dependency installation was opened.

## Files Modified

```text
athena_azr/h2_zero_certifier/serialization.py
athena_azr/h2_zero_certifier/winding_certifier.py
tests/test_006h08_l3_second_structural_patch.py
docs/experimentos/006H08-L3-SECOND-STRUCTURAL-PATCH.md
```

No real-path files were modified.

## H07-F001 Patch

Synthetic L3 JSON reports no longer serialize mandatory hash fields as ambiguous empty objects.

The fields now use explicit deterministic synthetic markers:

```json
{
  "status": "not_applicable_synthetic_structural",
  "execution_authorized": false,
  "source_phase": "006H08"
}
```

The reports also preserve:

```text
status = synthetic_structural_only
real_certification = false
authorization_id = none_synthetic_structural_006H08
```

The synthetic reports were tested against the documentary 006F recognizer and the real execution authorization parser. They are rejected as real authorization artifacts.

```text
H07_F001_PATCHED = true
AMBIGUOUS_EMPTY_MANDATORY_FIELDS = false
SYNTHETIC_MARKERS_EXPLICIT = true
SYNTHETIC_REPORTS_NONEXECUTABLE = true
```

## H07-F002 Patch

`winding_certifier.py` now exposes exact endpoint parsing and exact closed-interval integer enumeration:

```python
parse_canonical_exact_endpoint(value: str) -> Fraction
integers_in_exact_closed_interval(lower: str, upper: str) -> tuple[int, ...]
```

`integers_in_closed_interval` delegates to the exact implementation for backward compatibility.

No approximate conversion, `round`, epsilon widening, binary conversion, midpoint rounding, or hidden interval widening is used.

## Endpoint Policy

Accepted endpoint forms:

```text
integer:  "0", "1", "-2"
decimal:  "0.125", "-0.5", "0.999999999999999999999999"
rational: "1/3", "2/3", "-3/2", "-1/2"
```

Rejected endpoint forms:

```text
"01"       leading zero
"+1"       plus sign
"1.0"      noncanonical decimal integer
"1/01"     leading zero in denominator
"2/4"      noninteger reducible rational
"1/-2"     denominator sign
"0/5"      noncanonical zero
"NaN"      nonfinite text
"Infinity" nonfinite text
""         empty string
" 1"       whitespace padded
"1 "       whitespace padded
```

Rational policy:

```text
denominator > 0
no leading zeros
no plus sign
negative sign only on numerator
zero represented only as "0"
noninteger rational endpoints must be reduced
integer-valued rational endpoints are normalized internally only to satisfy the explicit 006H08 large exact arithmetic case
```

The final exception is explicit, narrow, and deterministic: the mandatory 006H08 case includes `999999999999999999999/3`, which is integer-valued. It is accepted through exact `Fraction` arithmetic; noninteger reducible examples such as `2/4` remain rejected.

## Required Enumeration Cases

```text
[1,1]       -> {1}
[0,0]       -> {0}
[-2,-2]     -> {-2}
[1/3,2/3]   -> {}
[-1,1]      -> {-1,0,1}
[-3/2,-1/2] -> {-1}
[1,2]       -> {1,2}
[-2/3,1/3]  -> {0}
[999999999999999999999/3,
 1000000000000000000001/3]
             -> {333333333333333333333}
```

The large case is resolved by exact integer and `Fraction` arithmetic without precision loss.

```text
H07_F002_PATCHED = true
EXACT_RATIONAL_ENDPOINTS_SUPPORTED = true
CANONICAL_ENDPOINT_POLICY_ENFORCED = true
FLOAT_CONVERSION_USED = false
GEOMETRIC_REALINTERVAL_INVARIANT_PRESERVED = true
```

## RED To GREEN

RED_H07_F001:

```text
command: python -m unittest tests.test_006h08_l3_second_structural_patch -v
result: FAILED
evidence: phase_id was 006H06 and synthetic mandatory hash fields were still ambiguous
```

RED_H07_F002:

```text
command: python -m unittest tests.test_006h08_l3_second_structural_patch -v
result: FAILED
evidence: parse_canonical_exact_endpoint and integers_in_exact_closed_interval were absent; 1/3 and -3/2 could not be parsed by the prior Decimal-only implementation
```

GREEN_H07_F001:

```text
command: python -m unittest tests.test_006h08_l3_second_structural_patch -v
result: OK
tests: 6
```

GREEN_H07_F002:

```text
command: python -m unittest tests.test_006h08_l3_second_structural_patch -v
result: OK
tests: 6
```

## Verification

```text
py_compile touched files
result: OK

tests.test_006h08_l3_second_structural_patch
result: OK
tests: 6

tests.test_006h04_l3_structural_synthetic
result: OK
tests: 10

tests.test_006h06_l3_structural_audit_patch
result: OK
tests: 11

authorized H2/L3 regression suite including 006H08
result: OK
tests: 142
skipped: 1
skip_reason: requires both the 006F environment gate and a readable 006F authorization
```

The real FLINT guarded test remains skipped by design.

## Static Scans

Forbidden numeric-token scan over touched files:

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

## Hashes

```text
1ff9d9db81d93b6712453b67fac421782552a292a1589661be27c4cd09dd50df  athena_azr/h2_zero_certifier/serialization.py
12ec2c248806cbc21f407aa7546f54299f63fe53b09e0431fc651c0c02992ee9  athena_azr/h2_zero_certifier/winding_certifier.py
0f92ce84c276e784fe0be13067560a89e86f097a242d8e346324577b7264f7c3  tests/test_006h08_l3_second_structural_patch.py
```

## Final State

```text
006H08_RESULT =
006H08_L3_SECOND_STRUCTURAL_PATCH_PASS

H07_F001_PATCHED = true
H07_F002_PATCHED = true

AMBIGUOUS_EMPTY_MANDATORY_FIELDS = false
SYNTHETIC_MARKERS_EXPLICIT = true
SYNTHETIC_REPORTS_NONEXECUTABLE = true

EXACT_RATIONAL_ENDPOINTS_SUPPORTED = true
CANONICAL_ENDPOINT_POLICY_ENFORCED = true
FLOAT_CONVERSION_USED = false
GEOMETRIC_REALINTERVAL_INVARIANT_PRESERVED = true

REAL_PATH_REMAINS_BLOCKED = true
L3_READY_FOR_REAL_BACKEND_IMPLEMENTATION = false
L3_READY_FOR_REAL_EXECUTION = false
H2_CERTIFIED = false
006F_OPENED = false
DOWNSTREAM_AUTHORIZED = false
NEXT_PHASE_AUTHORIZED = false
```

006H08 closes only as a narrow structural patch pass. Any subsequent phase requires separate explicit authorization.
