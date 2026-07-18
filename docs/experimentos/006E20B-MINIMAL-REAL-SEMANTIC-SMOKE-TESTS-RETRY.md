# 006E20B-MINIMAL-REAL-SEMANTIC-SMOKE-TESTS-RETRY

## 1. Estado y alcance

```text
phase_id = 006E20B
status = minimal_real_semantic_smoke_retry_completed_with_warnings
result = 006E20B_SMOKE_PASS_WITH_WARNINGS
runtime_authorized = C:\Users\johnn\AppData\Local\Temp\athena-006e20r\Scripts\python.exe
scope = minimal_non_certifying_semantic_smoke
contour_execution = forbidden
Lambda_3_evaluation = forbidden
zero_isolation = forbidden
zero_counting = forbidden
zero_tables = not_generated
H2_CERTIFIED = false
006F = blocked
DOWNSTREAM_USE = forbidden
NOVELTY_CLAIM = false
```

006E20B repeated the minimal real semantic smoke test using the environment
prepared by 006E20R. The phase did not call project backend code or the H2
pipeline.

The result is limited because simple Python-level metadata did not expose
separate FLINT/Arb version accessors, even though `python-flint` imported and
the authorized smoke checks passed.

## 2. Precheck obligatorio

```text
runtime_exists = PASS
import_flint = PASS
python-flint = 0.8.0
flint.__version__ = 0.8.0
python_version = 3.12.13 (main, Mar  3 2026, 15:01:35) [MSC v.1944 64 bit (AMD64)]
platform = Windows-11-10.0.26200-SP0
```

Runtime used:

```text
C:\Users\johnn\AppData\Local\Temp\athena-006e20r\Scripts\python.exe
```

The broken project `.venv` and the workspace `.venv-006e20r` were not used.

## 3. Versiones observadas

```text
python-flint_distribution_version = 0.8.0
flint.__version__ = 0.8.0
flint.version = unavailable
flint.flint_version = unavailable
flint.arb_version = unavailable
```

Warning:

```text
FLINT/Arb version accessors unavailable via simple python-flint metadata
```

This warning does not invalidate the smoke checks, but it prevents claiming a
complete separate FLINT/Arb version report from this phase alone.

## 4. Pruebas realizadas

### 4.1 Contexto global

```text
ctx_workprec_restores_after_success = PASS
before = 53
inside = 96
after = 53
```

```text
ctx_workprec_restores_after_exception = PASS
before = 53
inside = 104
after = 53
```

The global precision context was restored after both normal exit and an
intentional exception.

### 4.2 `arb` desde entradas exactas

```text
arb_exact_input_lower_upper_nonzero_radius = PASS
input_midpoint_exact = 1/3
input_radius_exact = 1/1000
finite = true
contains_exact_midpoint = true
lower_ne_upper = true
lower = [0.332333333329492 +/- 3.73e-16]
upper = [0.334333333337175 +/- 3.90e-17]
```

No Python `float` was used to construct this ball.

### 4.3 `acb` rectangular con radios no nulos

```text
acb_rectangular_nonzero_radii = PASS
finite = true
real_lower_ne_upper = true
imag_lower_ne_upper = true
real_lower = [0.332333333329492 +/- 3.73e-16]
real_upper = [0.334333333337175 +/- 3.90e-17]
imag_lower = [1.39949999999808 +/- 8.54e-16]
imag_upper = [1.40050000000192 +/- 8.53e-16]
```

The input was a non-point rectangular complex ball.

### 4.4 Identidad basica de `chi_3`

```text
dirichlet_char_3_2_basic_identity = PASS
modulus = 3
number = 2
conductor = 3
is_primitive = true
is_principal = false
is_real = true
order = 2
parity = 1
chi(0) = 0
chi(1) = 1.00000000000000
chi(2) = -1.00000000000000
```

The metadata and values match the intended primitive real non-principal
character modulo 3 at this smoke level.

### 4.5 `chi.l_function` con entrada `acb` no puntual

```text
native_l_function_nonpoint_acb_smoke = PASS
input_nonpoint_acb = true
output_type = acb
output_finite = true
output_has_nonzero_width = true
ctx_before = 128
ctx_after = 128
output_real_lower = [0.469979046280747 +/- 6.30e-17]
output_real_upper = [0.611096462137317 +/- 5.36e-17]
output_imag_lower = [0.339871321344753 +/- 3.42e-16]
output_imag_upper = [0.489491189602768 +/- 2.83e-16]
```

This is only a non-certifying smoke test that the native L-function accepts a
non-point `acb` input and returns a finite `acb` with nonzero-width output.

## 5. Pruebas explicitamente no realizadas

```text
contours = not_executed
Lambda_3 = not_evaluated
zero_isolation = not_executed
zero_counting = not_executed
zero_tables = not_generated
H2_certification = not_performed
006F_opening = not_performed
downstream_use = forbidden
novelty_claim = false
project_backend = not_invoked
H2_pipeline = not_invoked
```

No green smoke result from this phase is a proof of H2, a zero certificate, a
completeness certificate, or permission to use outputs downstream.

## 6. Resultados por contrato

| Contract | Result | Notes |
| --- | --- | --- |
| Authorized runtime exists | PASS | Tempdir runtime from 006E20R. |
| `import flint` | PASS | `python-flint==0.8.0`. |
| `flint.__version__ == 0.8.0` | PASS | Basic module version matched. |
| `ctx.workprec` restores after success | PASS | Returned to precision 53. |
| `ctx.workprec` restores after exception | PASS | Returned to precision 53. |
| Exact-input `arb` construction | PASS | Used `fmpq`, not float. |
| `arb.lower()` / `arb.upper()` nonzero width | PASS | Bounds distinct. |
| Rectangular `acb` construction | PASS | Real and imaginary balls distinct. |
| Nonzero `acb` radii | PASS | Both components had distinct bounds. |
| `dirichlet_char(3,2)` identity | PASS | Basic metadata and values matched. |
| `chi.l_function(nonpoint_acb)` | PASS | Returned finite `acb` with nonzero-width output. |
| Separate FLINT/Arb version report | WARNING | Simple accessors unavailable. |

## 7. Errores o inconclusiones

No smoke-contract error was observed in the final normalized run.

The only warning is:

```text
FLINT/Arb version accessors unavailable via simple python-flint metadata
```

An earlier strict comparison treated `modulus = "3"` and `chi(1) =
"1.00000000000000"` as a failure because it compared against Python integer
string forms too narrowly. The final run normalized numeric display strings and
the identity smoke passed.

## 8. Bloqueos preservados

```text
H2_CERTIFIED = false
006F = blocked
ZERO_CERTIFICATION = forbidden
ZERO_TABLES = not_generated
DOWNSTREAM_USE = forbidden
NOVELTY_CLAIM = false
REAL_CONTOUR_EXECUTION = forbidden
LAMBDA_3_EVALUATION = forbidden
```

## 9. Recomendacion no vinculante para Yonnah

The next reasonable phase, if authorized, should be documentary and
contract-focused rather than mathematical certification:

```text
recommendation = 006E21_document_real_smoke_semantics_and_version_gap
```

That phase should decide whether the unavailable FLINT/Arb version accessors
are acceptable, or whether a more precise version-inspection method is required
before any larger real semantic tests. It should still not open 006F, evaluate
contours, isolate/count zeros, or certify H2.

## 10. Veredicto

```text
006E20B_RESULT = 006E20B_SMOKE_PASS_WITH_WARNINGS
MAXIMUM_ALLOWED_RESULT = 006E20B_SMOKE_PASS_LIMITED
REAL_FLINT_IMPORT = passed
ARB_SEMANTIC_SMOKE = passed_limited
ACB_SEMANTIC_SMOKE = passed_limited
NATIVE_L_NONPOINT_ACB_SMOKE = passed_limited
MATHEMATICAL_PROOF = false
H2_CERTIFIED_TRUE = false
006F_OPENED = false
ZERO_CERTIFICATION_COMPLETED = false
DOWNSTREAM_USE_ALLOWED = false
NOVELTY_CLAIM = false
```

006E20B establishes only that the authorized tempdir environment can run the
minimal non-certifying real semantic smoke checks listed above.
