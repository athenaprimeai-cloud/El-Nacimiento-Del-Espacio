# 006H10 L3 Rational Endpoint Canonicality Patch

phase_id: 006H10_L3_RATIONAL_ENDPOINT_CANONICALITY_PATCH
result: 006H10_L3_RATIONAL_ENDPOINT_CANONICALITY_PATCH_PASS
date: 2026-07-02
mode: narrow_structural_patch

## Scope

006H10 closes only H09-F001 by enforcing strict unique textual representation for exact winding endpoints.

No backend real was implemented. No H2, 006F, FLINT, Arb, Acb, `chi.l_function`, contour execution, zero isolation, zero counting, network access, dependency installation, or downstream use was opened.

## Files Modified

```text
athena_azr/h2_zero_certifier/winding_certifier.py
tests/test_006h08_l3_second_structural_patch.py
tests/test_006h10_l3_rational_endpoint_canonicality_patch.py
docs/experimentos/006H10-L3-RATIONAL-ENDPOINT-CANONICALITY-PATCH.md
```

No real-path files were modified.

## Canonical Endpoint Policy

```text
ENDPOINT_CANONICALITY_POLICY = STRICT_UNIQUE_TEXTUAL_REPRESENTATION
```

Integer-valued endpoints must use integer syntax:

```text
"0"
"1"
"-1"
"333333333333333333333"
```

Noninteger rational endpoints must use reduced `p/q` syntax:

```text
"1/3"
"2/3"
"-3/2"
"-1/2"
"1000000000000000000001/3"
```

Decimal endpoints keep the existing canonical decimal syntax.

The central 006H10 rule is now enforced:

```text
Any rational string p/q whose exact Fraction value is an integer is rejected.
```

Rejected integer-valued rational aliases:

```text
"1/1"
"2/2"
"4/2"
"10/5"
"-6/3"
"999999999999999999999/3"
```

The canonical replacements are:

```text
"1"
"1"
"2"
"2"
"-2"
"333333333333333333333"
```

## Patch Summary

`parse_canonical_exact_endpoint` now rejects `p/q` before constructing the endpoint if:

```text
numerator % denominator == 0
```

It then preserves the prior reduced-rational requirement:

```text
gcd(abs(numerator), denominator) = 1
```

This means:

```text
"2/4" rejected as nonreduced rational
"1/1" rejected as integer-valued rational requiring integer syntax
"1000000000000000000001/3" accepted as noninteger reduced rational
```

No float, rounding, epsilon, approximation, or hidden widening was added.

## Corrected Large Exact Case

006H08 previously used:

```text
["999999999999999999999/3", "1000000000000000000001/3"]
```

006H10 corrected this to:

```text
["333333333333333333333", "1000000000000000000001/3"]
```

The exact enumeration remains:

```text
{333333333333333333333}
```

This preserves large exact arithmetic while enforcing unique textual representation.

## RED To GREEN

RED:

```text
command: python -m unittest tests.test_006h10_l3_rational_endpoint_canonicality_patch -v
result: FAILED
tests: 5
failures: 6
evidence: 1/1, 2/2, 4/2, 10/5, -6/3, and 999999999999999999999/3 were accepted instead of rejected
```

GREEN:

```text
command: python -m unittest tests.test_006h10_l3_rational_endpoint_canonicality_patch -v
result: OK
tests: 5
```

Regression of the corrected 006H08 large case:

```text
command: python -m unittest tests.test_006h08_l3_second_structural_patch -v
result: OK
tests: 6
```

## Verification

```text
tests.test_006h10_l3_rational_endpoint_canonicality_patch
result: OK
tests: 5

tests.test_006h08_l3_second_structural_patch
result: OK
tests: 6

tests.test_006h06_l3_structural_audit_patch
result: OK
tests: 11

tests.test_006h04_l3_structural_synthetic
result: OK
tests: 10

py_compile touched files
result: OK

authorized H2/L3 regression suite including 006H10
result: OK
tests: 147
skipped: 1
skip_reason: requires both the 006F environment gate and a readable 006F authorization
```

The real FLINT guarded test remains skipped by design.

## Static Scans

Forbidden numeric-operation scan over touched code and tests:

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
athena_azr/h2_zero_certifier/argument_principle.py:62    DEPRECATED_SYNTHETIC_STUB
athena_azr/h2_zero_certifier/completed_l3.py:11          EXPECTED_REAL_BLOCKER
athena_azr/h2_zero_certifier/completed_l3.py:15          EXPECTED_REAL_BLOCKER
athena_azr/h2_zero_certifier/python_flint_backend.py:37  EXPECTED_REAL_BLOCKER
athena_azr/h2_zero_certifier/pipeline.py:97              EXPECTED_REAL_BLOCKER
```

```text
REAL_PATH_REMAINS_BLOCKED = true
```

## Hashes

```text
db66e4466a7f7a9129ab8c40662b6add898cf6cf13993f108875ce2791777c1c  athena_azr/h2_zero_certifier/winding_certifier.py
84b684131237cb06b9254b4930c041b059cee7f321d744aa46700227cc0daf99  tests/test_006h08_l3_second_structural_patch.py
2e3a8d549028437d27ba019e11f8ca925bd917553ffe69ab25a271f0ef2b0170  tests/test_006h10_l3_rational_endpoint_canonicality_patch.py
```

## Final State

```text
006H10_RESULT =
006H10_L3_RATIONAL_ENDPOINT_CANONICALITY_PATCH_PASS

H09_F001_PATCHED = true
INTEGER_VALUED_RATIONALS_REJECTED = true
NONINTEGER_REDUCED_RATIONALS_ACCEPTED = true
UNIQUE_TEXTUAL_REPRESENTATION = true
EXACT_ARITHMETIC_PRESERVED = true
FLOAT_CONVERSION_USED = false
ROUNDING_USED = false
EPSILON_USED = false
HIDDEN_WIDENING = false

REAL_PATH_REMAINS_BLOCKED = true
L3_READY_FOR_REAL_BACKEND_IMPLEMENTATION = false
L3_READY_FOR_REAL_EXECUTION = false
REAL_BACKEND_COMPLETE = false
H2_CERTIFIED = false
006F_OPENED = false
DOWNSTREAM_AUTHORIZED = false
NEXT_PHASE_AUTHORIZED = false
```

006H10 closes only as a narrow canonicality patch pass. Any subsequent phase requires separate explicit authorization.
