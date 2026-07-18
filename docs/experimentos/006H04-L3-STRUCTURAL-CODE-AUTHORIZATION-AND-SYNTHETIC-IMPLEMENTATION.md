# 006H04: L3 structural code authorization and synthetic implementation

```text
phase_id = 006H04
phase_name = L3_STRUCTURAL_CODE_AUTHORIZATION_AND_SYNTHETIC_IMPLEMENTATION
phase_type = structural_synthetic_code
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
```

## 1. Scope

006H04 implements only the structural, contractual and synthetic layer described
by 006H03. It does not complete the real FLINT/Arb/Acb backend, does not certify
any real L3 boundary, does not certify any real winding, does not isolate or
count real zeros, and does not authorize a later phase.

## 2. Files created

```text
athena_azr/h2_zero_certifier/boundary_certifier.py
athena_azr/h2_zero_certifier/argument_increment.py
athena_azr/h2_zero_certifier/winding_certifier.py
athena_azr/h2_zero_certifier/l3_isolator.py
tests/test_006h04_l3_structural_synthetic.py
docs/experimentos/006H04-L3-STRUCTURAL-CODE-AUTHORIZATION-AND-SYNTHETIC-IMPLEMENTATION.md
```

## 3. Files modified

```text
athena_azr/h2_zero_certifier/chi3_function.py
athena_azr/h2_zero_certifier/contour.py
athena_azr/h2_zero_certifier/l3_certifier.py
athena_azr/h2_zero_certifier/serialization.py
athena_azr/h2_zero_certifier/authorization.py
athena_azr/h2_zero_certifier/pipeline.py
tests/test_h2_l3_certifier.py
tests/test_h2_l3_isolation.py
tests/test_h2_real_completed_l3.py
tests/test_h2_real_segment_enclosure.py
docs/experimentos/006H03-L3-BACKEND-COMPLETION-CODE-PLAN.md
```

006H03 corrections:

```text
duplicate tests/test_h2_real_evidence.py entry = removed
006E7-006E17 range = confirmed in source table
```

## 4. Implementation summary

### chi3 contract

`chi3_function.py` now carries the 006H02 identity fields:

```text
conductor = 3
character_type = primitive_real_nonprincipal
parity_name = odd
conrey_index = 2
root_number_epsilon = 1
Lambda_3 definition = frozen symbolic string
```

The validator now rejects missing or mismatched 006H02 fields. This is still
metadata validation only; it does not evaluate `Lambda_3`.

### frozen contours

`contour.py` now exposes frozen L3 contour builders:

```text
build_frozen_l3_contour(T)
build_frozen_l3_contours()
T in [143, 200, 300, 500]
boundary_mode = exact_T_boundary
T_star = rejected
adaptive boundary change = rejected
```

### structural modules

```text
boundary_certifier.py = deterministic subdivision and synthetic zero exclusion
argument_increment.py = abstract increment intervals and provenance checks
winding_certifier.py = unique integer winding rule without midpoint rounding
l3_isolator.py = synthetic L3 zero isolation, multiplicity and cluster checks
```

### l3 certification and serialization

`l3_certifier.py` now has `certify_l3_synthetic`, which compares synthetic
winding counts against synthetic isolated multiplicities at all frozen heights.
A mismatch at any height blocks the complete L3 synthetic result.

`serialization.py` now emits structural L3 bytes for:

```text
l3_zeros_T500.csv
l3_isolation_report.json
l3_completeness_report.json
```

### authorization and pipeline

`authorization.py` and `pipeline.py` recognize the documentary
`G5B-006F-AUTHORIZATION.json` schema. Recognition does not create an executable
`ExecutionAuthorization`, does not initialize a backend, and does not open 006F.

`PROBATIVE_RUNTIME_CODE_FILES` now includes the new structural modules while
`argument_principle.py` remains excluded as synthetic test-only code.

## 5. TDD record

RED command:

```text
python -m unittest tests.test_006h04_l3_structural_synthetic -v
```

Observed RED result under the Codex Python runtime:

```text
Ran 10 tests
FAILED (failures=7, errors=3)
```

Main RED causes:

```text
boundary_certifier.py missing
argument_increment.py missing
winding_certifier.py missing
l3_isolator.py missing
chi3 metadata incomplete
frozen contour builders missing
documentary 006F schema recognition missing
```

GREEN command:

```text
python -m unittest tests.test_006h04_l3_structural_synthetic -v
```

Observed GREEN result:

```text
Ran 10 tests
OK
```

## 6. Authorized suite executed

Command executed with the local Codex Python runtime:

```text
python -m unittest \
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
Ran 125 tests in 0.287s
OK (skipped=1)
```

The single skipped test is:

```text
tests.test_h2_real_flint_guarded.H2RealFlintGuardedTests.
test_real_flint_certification_requires_a_reviewed_implementation

skip reason =
requires both the 006F environment gate and a readable 006F authorization
```

This confirms that the real FLINT path remains blocked by default.

## 7. Guard evidence

Static guard check:

```text
rg "import flint|from flint|chi\.l_function|l_function\(|requests|urllib|pip install|Start-Process|Invoke-WebRequest"
```

Observed result:

```text
athena_azr/h2_zero_certifier/python_flint_backend.py:22:
        import flint  # lazy by design
```

Interpretation:

```text
FLINT_IMPORTED = false during tests
FLINT_IMPORT_STATEMENT_PRESENT = lazy_guarded_only
network_code_in_006H04_path = not_detected
dependency_installation_code_in_006H04_path = not_detected
chi_l_function_call = not_detected
```

The authorized suite includes guards proving backend construction does not import
FLINT and that real execution remains gated.

## 8. NotImplementedError inventory

Fresh inventory after 006H04:

```text
athena_azr/h2_zero_certifier/argument_principle.py: rigorous winding certification is not implemented
athena_azr/h2_zero_certifier/completed_l3.py: Real L3 evaluations are locked under 006F
athena_azr/h2_zero_certifier/completed_l3.py: Real L3 evaluations are locked under 006F
athena_azr/h2_zero_certifier/pipeline.py: real certification pipeline is reserved for 006F
athena_azr/h2_zero_certifier/python_flint_backend.py: real FLINT operations are reserved for 006F
```

Interpretation:

```text
real Lambda_3 evaluation = blocked
real segment enclosure = blocked
real winding certification = blocked
real pipeline completion = blocked
real FLINT operations = blocked
```

## 9. Hashes of touched files

```text
4d300c4b4d26085be37fe030c21db5c54537a4b27b7e129a03aba518e31adf68  athena_azr/h2_zero_certifier/chi3_function.py
bae15a7bb1d874cceb8e2869011e6f4063eb81650cad2937be2c8b5d551ee681  athena_azr/h2_zero_certifier/contour.py
58fe227d07c290ef63376ae0bdbfdceed3b69fcb1b3a7d35f130218f35a5cbb3  athena_azr/h2_zero_certifier/boundary_certifier.py
decf71d56015c2f9e6b5c030db5d741275f3d00baa4f2a97a8b3bef1b05e860a  athena_azr/h2_zero_certifier/argument_increment.py
6c3399f99aee790439a4432afed7da9a884ef520967b2ebd47df8d3f911bb370  athena_azr/h2_zero_certifier/winding_certifier.py
6ce3f330d60721592725eba981e2d57fe9bda035ffd87daee209c453984bbca6  athena_azr/h2_zero_certifier/l3_isolator.py
9fe62ab42b1ec80f96ad18869f46fecf8cdfc5ff3c86e11cdc9c072591c0c9b8  athena_azr/h2_zero_certifier/l3_certifier.py
170af0a98435149ea95f9a353149cbf3238b1242dd43263eaf19700da8081f99  athena_azr/h2_zero_certifier/serialization.py
80758c8ab8759926a1b302e511c8ffadce13b72d2c9a91cb9a25dcb997867802  athena_azr/h2_zero_certifier/authorization.py
3b35bc44312609cedbdd5628d6c8846b7e9280d6eb1baf5432c1c91b267e2eb2  athena_azr/h2_zero_certifier/pipeline.py
3537028f981354634b30f01f24515c5d3cf53c82cbdcd1574801aa3712dd1c10  tests/test_006h04_l3_structural_synthetic.py
e3e4539bdcf1cb13bf7606362c45d4215aaea8d28ad75edff2add4536e372ae4  tests/test_h2_l3_certifier.py
3d5f7943bd3f42adc13632e448883f2d4e4b13a44f771f353c7f6320bec52292  tests/test_h2_l3_isolation.py
6846db430d8bdf46ae19d67da0edcdd96f537d1e16971e64c81dfe833018e1c7  tests/test_h2_real_completed_l3.py
290c44b585775df9c5ebfc21fe3d387585db9873d6350d066344b3df86ce3a01  tests/test_h2_real_segment_enclosure.py
b94ac502cf08ba896770591b72fba9627080de4fcb33d4bb3ff4e69682f9cf5b  docs/experimentos/006H03-L3-BACKEND-COMPLETION-CODE-PLAN.md
```

The hash of this 006H04 report is computed after final bytes are written.

## 10. Final status

```text
006H04_RESULT =
006H04_L3_STRUCTURAL_SYNTHETIC_IMPLEMENTATION_PASS

STRUCTURAL_CODE_IMPLEMENTED = true
PURE_AND_SYNTHETIC_TESTS_PASS = true
CONTRACTS_006H01_006H02_REFLECTED = true
REAL_INTEGRATION_REMAINS_BLOCKED = true
NEXT_PHASE_AUTHORIZED = false
```

Explicit non-claims:

```text
REAL_BACKEND_COMPLETE = false
ARB_ACB_SEMANTICS_VALIDATED = false
REAL_BOUNDARY_ZERO_FREE_CERTIFIED = false
REAL_WINDING_CERTIFIED = false
L3_ZEROS_ISOLATED_OR_COUNTED = false
H2_CERTIFIED = false
006F_OPENED = false
NOVELTY_CLAIMED = false
```
