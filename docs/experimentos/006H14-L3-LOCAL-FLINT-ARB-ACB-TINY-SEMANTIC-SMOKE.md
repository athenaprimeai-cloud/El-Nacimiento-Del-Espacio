# 006H14 L3 Local FLINT Arb Acb Tiny Semantic Smoke

```text
phase_id = 006H14_L3_LOCAL_FLINT_ARB_ACB_TINY_SEMANTIC_SMOKE
phase_type = tiny_fixed_local_semantic_smoke
result = 006H14_TINY_SEMANTIC_SMOKE_PASS
runtime = C:\Users\johnn\AppData\Local\Temp\athena-006e20r\Scripts\python.exe
```

## 1. Scope

006H14 executed the fixed local smoke authorized after 006H13 to resolve local
API and semantic ambiguities for the sealed python-flint runtime.

It did not implement the project backend, did not modify
`athena_azr/h2_zero_certifier/`, did not evaluate the completed L3 product, did
not run contours, did not search for zeros, did not isolate or count zeros, did
not open H2 and did not open 006F.

## 2. Runtime and Binary Seal

The runner verified the required runtime and critical binary hashes before
executing mathematical smoke calls.

```text
python executable hash verified = true
python-flint version = 0.8.0
FLINT native version = 3.3.1
libflint hash verified = true
arb extension hash verified = true
acb extension hash verified = true
dirichlet extension hash verified = true
```

Result:

```text
RUNTIME_HASHES_VERIFIED = true
```

## 3. Fixed Budget

Authorized precisions:

```text
precision_bits = [192, 256]
```

Observed call counts:

| call class | observed | budget |
| --- | ---: | ---: |
| `native_dirichlet_l` | 4 | 4 |
| `hurwitz_candidate_zeta` | 4 | 6 |
| `gamma` | 4 | 4 |
| `log` | 6 | 6 |
| `exp` | 4 | 4 |
| `pi` | 2 | 2 |

```text
budget_ok = true
```

No frozen H2 heights were used.

## 4. Arb Construction

The smoke constructed exact integer, exact rational and closed real interval
objects using local FLINT APIs without Python floats.

Minimum cases:

| case | status | zero relation | abs_lower relation |
| --- | --- | --- | --- |
| `1` | finite Arb | excludes zero | strictly positive |
| `1/3` | finite Arb from `fmpq(1,3)` | excludes zero | strictly positive |
| `[1,2]` | finite Arb interval via `union` | excludes zero | strictly positive |
| `[-1,1]` | finite Arb interval via `union` | contains zero | abs lower contains zero |

Result:

```text
ARB_CONSTRUCTION_SEMANTICS = VERIFIED
```

## 5. Acb Rectangular Construction

The smoke constructed nondegenerate rectangular Acb boxes from Arb real and
imaginary parts:

```text
B0: real in [1,2], imag in [-1/3,1/3]
B1: real in [-1,1], imag in [-1,1]
```

Observed:

```text
B0 contains zero = false
B0 abs_lower strictly positive = true
B1 contains zero = true
B1 abs_lower contains zero = true
```

Result:

```text
ACB_RECTANGULAR_CONSTRUCTION = VERIFIED
```

## 6. Precision Context

For each authorized precision, the runner recorded:

```text
prec_before = 53
prec_inside = requested bits
prec_after = 53
exception_prec_inside = requested bits
exception_prec_after = 53
```

Observed for both `192` and `256`:

```text
PRECISION_CONTEXT_RESTORATION = VERIFIED
```

This verifies local context restoration for `flint.ctx.workprec(bits)` in this
smoke. It does not by itself certify every future adapter path.

## 7. Elementary Identities

The smoke executed only the authorized identities:

```text
pi = arb.pi()
log(1) = 0
exp(0) = 1
Gamma(1) = 1
complex_log(1) = 0
complex_exp(0) = 1
complex_Gamma(1) = 1
```

For non-pi exact identities, validation used inclusion:

```text
result.contains(expected_exact_value)
```

Result:

```text
ELEMENTARY_ARB_ACB_IDENTITIES = VERIFIED
```

## 8. Complex Analytic Log Surface

The smoke constructed the authorized right-half-plane box:

```text
real in [1, 3/2]
imag in [-1/4, 1/4]
```

It excluded zero by the local policy:

```text
not contains_zero and abs_lower strictly positive
```

The call:

```text
flint.acb.log(box, analytic=True)
```

executed at both `192` and `256` and returned finite outputs.

Result:

```text
ACB_ANALYTIC_LOG_SURFACE = VERIFIED
```

No argument increments or winding values were computed from this log result.

## 9. chi_3 Surface

The smoke constructed only:

```text
chi = flint.dirichlet_char(3, 2)
```

Observed:

```text
modulus = 3
number = 2
index = 1
primitive = true
principal = false
real = true
parity = 1
l_function_attribute_present = true
l_function_called = false
```

The runner did not use group indexing as a substitute.

## 10. Native Dirichlet L Smoke

The only native L API called was:

```text
flint.acb.dirichlet_l(s, chi)
```

It was called at `s = 2` and on the fixed nondegenerate Acb box:

```text
real in [199/100, 201/100]
imag in [-1/100, 1/100]
```

Observed for both precisions:

```text
exact point output finite = true
box output finite = true
input_has_nonzero_width = true
box output contains exact-point result at s=2 = true
```

Result:

```text
NATIVE_L_EXACT_POINT_SMOKE = PASS
NATIVE_L_WHOLE_BOX_SMOKE = PASS
```

Interpretation remains limited:

```text
point_results_contained_by_box_result = smoke evidence only
```

This is not a proof of general whole-continuum inclusion semantics.

## 11. Hurwitz Candidate Smoke

The smoke used the local candidate:

```text
flint.acb.zeta(s, a)
```

only at:

```text
s = 2
a = 1/3
a = 2/3
```

It formed:

```text
L_control(2) = (zeta(2,1/3) - zeta(2,2/3)) / 9
```

and compared it with:

```text
flint.acb.dirichlet_l(2, chi_3)
```

using overlap/containment only, not midpoint or decimal-string equality.

Observed for both precisions:

```text
HURWITZ_CANDIDATE_API_EXECUTED = true
HURWITZ_CONTROL_FINITE = true
NATIVE_AND_CONTROL_OVERLAP = true
```

Result:

```text
HURWITZ_CANDIDATE_SMOKE = PASS
```

No independence between native L and Hurwitz channels is claimed.

## 12. Zero Exclusion Policy

006H14 freezes the local future policy:

```text
origin_excluded =
not contains_zero
and abs_lower strictly positive
```

It explicitly rejects:

```text
is_zero = false
```

as a standalone zero-exclusion certificate.

Result:

```text
ZERO_EXCLUSION_POLICY = DEFINED
```

## 13. Artifacts

Created artifact directory:

```text
artifacts/006H14-tiny-semantic-smoke/
```

Files:

```text
006H14_CALL_LEDGER.json
006H14_RUNTIME_SEAL.json
006H14_RESULTS.json
006H14_SHA256SUMS.txt
```

Artifact hashes:

```text
135b05fb7562c4a156b268a79731cd186e34bfa352367bdd3ea66d30f7492801  006H14_CALL_LEDGER.json
c7f30c981b974586cce2cfdd739bec2c899f15f8321899dc5eee404e3fca3452  006H14_RUNTIME_SEAL.json
bacb14a12cf0eddd68a512a5e53862f53bef6f169dbbd638a49abd97f4be4131  006H14_RESULTS.json
0c8e0cbb09d65def0bc0833daf7b56fd7081332420ef72f9916d3519dbdb47a9  006H14_SHA256SUMS.txt
```

## 14. Test Record

RED:

```text
python -m unittest tests.test_006h14_tiny_semantic_smoke_contract -v
result = FAILED
tests = 4
reason = runner/artifacts missing
```

GREEN:

```text
python -m unittest tests.test_006h14_tiny_semantic_smoke_contract -v
result = OK
tests = 4
```

The test verifies:

```text
fixed runtime path
fixed precision set
call budgets not exceeded
no forbidden heights in runner
no contour construction in runner
no completed L3 function in runner
no zero isolation/counting in runner
no network/dependency install markers in runner
all artifacts present
artifact hashes match
```

## 15. File Hashes

Created files:

```text
8245967d7318cd13bc514b97e02e5599a84a1bed2a655ca382d8a9ce2b72642a  scripts/run_006h14_tiny_semantic_smoke.py
be6f600dd9f4d06a0c4832983442c6beddc0fb857ecb159c67ff97da6bc9ed6c  tests/test_006h14_tiny_semantic_smoke_contract.py
```

The final hash of this report is computed after final bytes are written.

## 16. Final State

```text
RUNTIME_HASHES_VERIFIED = true
ARB_CONSTRUCTION_SEMANTICS = VERIFIED
ACB_RECTANGULAR_CONSTRUCTION = VERIFIED
PRECISION_CONTEXT_RESTORATION = VERIFIED
ELEMENTARY_ARB_ACB_IDENTITIES = VERIFIED
ACB_ANALYTIC_LOG_SURFACE = VERIFIED
ZERO_EXCLUSION_POLICY = DEFINED
NATIVE_L_EXACT_POINT_SMOKE = PASS
NATIVE_L_WHOLE_BOX_SMOKE = PASS
HURWITZ_CANDIDATE_SMOKE = PASS

L3_READY_FOR_REAL_BACKEND_CODE_IMPLEMENTATION_AUTHORIZATION = true
L3_READY_FOR_REAL_BACKEND_IMPLEMENTATION = false
L3_READY_FOR_REAL_EXECUTION = false
H2_CERTIFIED = false
006F_OPENED = false
NEXT_PHASE_AUTHORIZED = false
```

## 17. Scope Verification

```text
FLINT_IMPORTED = true
FLINT_ANALYTIC_OPERATIONS_EXECUTED = false
ARB_ANALYTIC_OPERATIONS_EXECUTED = false
ACB_ANALYTIC_OPERATIONS_EXECUTED = false
CHI_L_FUNCTION_CALLED = false
LAMBDA_3_EVALUATED = false
CONTOURS_EXECUTED = false
ZEROS_ISOLATED = false
ZEROS_COUNTED = false
NETWORK_USED = false
DEPENDENCIES_INSTALLED = false
H2_OPENED = false
006F_OPENED = false
```

The smoke confirms local fixed behavior under the sealed runtime and fixed
inputs. It does not certify general Arb/Acb semantics, does not certify
`Lambda_3`, does not certify zeros and does not authorize any subsequent phase.
