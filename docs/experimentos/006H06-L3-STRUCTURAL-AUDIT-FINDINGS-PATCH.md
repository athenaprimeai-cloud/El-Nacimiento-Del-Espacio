# 006H06: L3 structural audit findings patch

```text
phase_id = 006H06
phase_name = L3_STRUCTURAL_AUDIT_FINDINGS_PATCH
phase_type = structural_patch_after_static_audit
real_execution = false
FLINT_imported = false
Arb_or_Acb_imported = false
chi_l_function_called = false
Lambda_3_numerically_evaluated = false
real_contours_executed = false
real_zeros_isolated = false
real_zeros_counted = false
H2_opened = false
006F_opened = false
network_used = false
dependencies_installed = false
downstream_authorized = false
novelty_claim = false
```

## 1. Scope

006H06 applies minimal structural patches for the authorized 006H05 findings:

```text
H05-F001 = mixed/missing argument-increment provenance
H05-F002 = incomplete synthetic L3 JSON serializers
H05-F003 = degenerate closed integer intervals for winding
H05-F004 = missing progressive subdivision coverage test
```

No real backend implementation was added. No `NotImplementedError` in the real
path was removed. No H2 or 006F execution path was opened.

## 2. Files changed

Modified:

```text
athena_azr/h2_zero_certifier/argument_increment.py
athena_azr/h2_zero_certifier/winding_certifier.py
athena_azr/h2_zero_certifier/serialization.py
tests/test_006h04_l3_structural_synthetic.py
```

Created:

```text
tests/test_006h06_l3_structural_audit_patch.py
docs/experimentos/006H06-L3-STRUCTURAL-AUDIT-FINDINGS-PATCH.md
```

`models.py` was not modified; the `RealInterval` positive-width invariant
remains preserved.

## 3. Patch summary

### H05-F001

`argument_increment.py` now canonicalizes provenance as a deterministic sorted
tuple of nonempty string pairs. `sum_argument_intervals` rejects:

```text
missing provenance when required
mixed provenance
mixed precision
duplicate source_id
```

Identical provenance content passes even when mappings were constructed in
different key order.

### H05-F002

`serialization.py` now emits all required 006H01 fields for:

```text
l3_isolation_report_json_bytes
l3_completeness_report_json_bytes
```

Synthetic output is explicitly marked:

```text
status = synthetic_structural_only
real_certification = false
backend_identity.kind = synthetic_structural_only
runtime_identity.kind = synthetic_structural_only
authorization_id = none_synthetic_structural_006H06
```

No real backend/runtime identity was invented.

### H05-F003

`winding_certifier.py` now provides a separate closed-interval winding API:

```text
ClosedWindingInterval
integers_in_closed_interval(lower, upper)
certify_unique_integer_winding_bounds(lower, upper, precision_bits=...)
```

This supports exact degenerate cases such as `[1,1]`, `[0,0]` and `[-2,-2]`
without relaxing geometric `RealInterval`.

### H05-F004

`tests/test_006h06_l3_structural_audit_patch.py` adds a progressive synthetic
backend test where:

```text
parent segment fails
max_depth = 0 closes inconclusive
max_depth = 1 certifies both children
coverage has no gap
endpoints are preserved exactly
```

The behavior already existed; the patch adds the missing coverage.

## 4. RED to GREEN record

### RED

Command:

```text
python -m unittest tests.test_006h06_l3_structural_audit_patch -v
```

Observed result before production-code patches:

```text
Ran 11 tests in 0.042s
FAILED (failures=4, errors=2)
```

Expected RED details:

```text
RED_F001:
  mixed_provenance_fails = failed because no exception was raised
  missing_provenance_fails_if_required = failed because no exception was raised

RED_F002:
  l3_isolation_report_matches_006h01_schema = failed due missing fields
  l3_completeness_report_matches_006h01_schema = failed due missing fields

RED_F003:
  integers_in_closed_interval = missing API
  certify_unique_integer_winding_bounds = missing API

RED_F004:
  progressive subdivision test passed during RED, confirming H05-F004 was a
  coverage gap rather than an implementation defect.
```

### GREEN focal

Command:

```text
python -m unittest tests.test_006h06_l3_structural_audit_patch -v
```

Observed result after patches:

```text
Ran 11 tests in 0.103s
OK
```

### 006H04 regression

Command:

```text
python -m unittest tests.test_006h04_l3_structural_synthetic -v
```

Observed result:

```text
Ran 10 tests in 0.116s
OK
```

## 5. Final verification

### py_compile

Command:

```text
python -m py_compile \
  athena_azr/h2_zero_certifier/argument_increment.py \
  athena_azr/h2_zero_certifier/winding_certifier.py \
  athena_azr/h2_zero_certifier/serialization.py \
  tests/test_006h04_l3_structural_synthetic.py \
  tests/test_006h06_l3_structural_audit_patch.py
```

Observed result:

```text
exit_code = 0
```

### Authorized H2 suite with 006H06

Command:

```text
python -m unittest \
  tests.test_006h06_l3_structural_audit_patch \
  tests.test_006h04_l3_structural_synthetic \
  tests.test_h2_models \
  tests.test_h2_contour \
  tests.test_h2_argument_principle \
  tests.test_h2_ball_argument \
  tests.test_h2_l3_argument_count \
  tests.test_h2_l3_isolation \
  tests.test_h2_l3_certifier \
  tests.test_h2_real_completed_l3 \
  tests.test_h2_real_segment_enclosure \
  tests.test_h2_real_argument \
  tests.test_h2_real_evidence \
  tests.test_h2_rigorous_ball_runtime \
  tests.test_h2_authorization \
  tests.test_h2_pipeline_guard \
  tests.test_h2_root_issuance \
  tests.test_h2_serialization \
  tests.test_h2_validation \
  tests.test_h2_zeta_certifier \
  tests.test_h2_real_flint_guarded \
  -v
```

Observed result:

```text
Ran 136 tests in 0.332s
OK (skipped=1)
```

Skipped test:

```text
tests.test_h2_real_flint_guarded.H2RealFlintGuardedTests.
test_real_flint_certification_requires_a_reviewed_implementation

skip reason =
requires both the 006F environment gate and a readable 006F authorization
```

The real FLINT test remains omitted as required.

## 6. Static scans

Forbidden-operation scan over touched files:

```text
rg "float\(|complex\(|atan2|round\(|cmath|numpy|np\.|epsilon|1e-100" ...
```

Observed matches:

```text
tests/test_006h04_l3_structural_synthetic.py:60 root_number_epsilon metadata text
tests/test_006h04_l3_structural_synthetic.py:69 root_number_epsilon metadata text
tests/test_006h04_l3_structural_synthetic.py:323 forbidden-token test string
```

Interpretation:

```text
forbidden_numeric_operation_in_touched_production_code = false
epsilon_hack_detected = false
artificial_interval_widening_detected = false
```

Backend/scope scan over H2 package and 006H04/006H06 tests:

```text
rg "import flint|from flint|import arb|from arb|import acb|from acb|chi\.l_function|l_function\(|requests|urllib|socket|pip install|Start-Process|Invoke-WebRequest|subprocess|http" ...
```

Observed match:

```text
athena_azr/h2_zero_certifier/python_flint_backend.py:22:
        import flint  # type: ignore[import-not-found]  # lazy by design
```

Interpretation:

```text
FLINT_IMPORT_STATEMENT_PRESENT = lazy_guarded_only
FLINT_IMPORTED_DURING_006H06 = false
CHI_L_FUNCTION_CALLED = false
NETWORK_USED = false
DEPENDENCIES_INSTALLED = false
```

## 7. NotImplementedError inventory

```text
athena_azr/h2_zero_certifier/argument_principle.py:62
classification = DEPRECATED_SYNTHETIC_STUB
reason = legacy rigorous winding entrypoint remains inert and excluded from probative runtime inventory

athena_azr/h2_zero_certifier/completed_l3.py:11
classification = EXPECTED_REAL_BLOCKER
reason = real completed L3 point evaluation locked under 006F

athena_azr/h2_zero_certifier/completed_l3.py:15
classification = EXPECTED_REAL_BLOCKER
reason = real completed L3 segment evaluation locked under 006F

athena_azr/h2_zero_certifier/python_flint_backend.py:37
classification = EXPECTED_REAL_BLOCKER
reason = real FLINT mathematics reserved for 006F

athena_azr/h2_zero_certifier/pipeline.py:97
classification = EXPECTED_REAL_BLOCKER
reason = real certification pipeline body reserved for 006F
```

```text
UNEXPECTED_MISSING_IMPLEMENTATION = false
REAL_PATH_REMAINS_BLOCKED = true
```

## 8. SHA-256 hashes

```text
cc4de6621b7006fe61f43fe7209015cfc1869570387ade0633fe60cfc09e973c  athena_azr/h2_zero_certifier/argument_increment.py
240b801682241b74049610d46b3af86ec36297a33101341e6d20ba9093e1e625  athena_azr/h2_zero_certifier/winding_certifier.py
4a55677e13cdc0428844bebc3cca64052f6026f339b520038c1974a9199d0b28  athena_azr/h2_zero_certifier/serialization.py
b4fdf09d7f052caa96d40c3f536ca220ecc89223624b9fbd2498da3a8b60410b  tests/test_006h04_l3_structural_synthetic.py
1ea25796c9b330d47743a1c57bbecead318f94220f656ed53a118103112241c1  tests/test_006h06_l3_structural_audit_patch.py
```

The hash of this 006H06 report is computed after final bytes are written.

## 9. Acceptance criteria

```text
H05_F001_PATCHED = true
H05_F002_PATCHED = true
H05_F003_PATCHED = true
H05_F004_TEST_ADDED = true

MIXED_PROVENANCE_REJECTED = true
L3_JSON_SCHEMAS_MATCH_006H01 = true
DEGENERATE_INTEGER_INTERVAL_SUPPORTED = true
GEOMETRIC_REALINTERVAL_INVARIANT_PRESERVED = true
REAL_PATH_REMAINS_BLOCKED = true
```

## 10. Final status

```text
006H06_RESULT =
006H06_L3_STRUCTURAL_AUDIT_FINDINGS_PATCH_PASS

STRUCTURAL_AUDIT_FINDINGS_PATCHED = true
REAL_BACKEND_COMPLETE = false
L3_READY_FOR_REAL_EXECUTION = false
H2_CERTIFIED = false
006F_OPENED = false
DOWNSTREAM_AUTHORIZED = false
NOVELTY_CLAIMED = false
NEXT_PHASE_AUTHORIZED = false
```

006H06 only repairs the 006H05 structural findings. It returns the structural
layer to candidate status for a future audit; it does not authorize any later
phase.
