# 006E23-NARROW-REAL-SEMANTIC-TESTS

## 1. Estado inicial y bloqueos preservados

```text
phase_id = 006E23
status = narrow_real_semantic_tests_completed
result = 006E23_NARROW_SMOKE_PASS_LIMITED
maximum_allowed_result = 006E23_NARROW_SMOKE_PASS_LIMITED
scope = narrow_real_semantic_tests_only
adaptive_search = not_executed
precision_chasing_for_certification = not_executed
project_backend_invocation = not_executed
H2_pipeline_invocation = not_executed
contour_execution = forbidden
Lambda_3_evaluation = forbidden
zero_isolation = forbidden
zero_counting = forbidden
zero_tables = not_generated
MATHEMATICAL_PROOF = false
H2_CERTIFIED = false
006F = blocked
ZERO_CERTIFICATION = forbidden
DOWNSTREAM_USE = forbidden
NOVELTY_CLAIM = false
```

006E23 executed only the narrow real semantic contracts authorized from the
006E22 plan. It did not invoke the project backend, the H2 pipeline, contours,
`Lambda_3`, zero logic, zero tables, certification, downstream use, or novelty
claims.

## 2. Runtime usado

```text
runtime_authorized = C:\Users\johnn\AppData\Local\Temp\athena-006e20r\Scripts\python.exe
runtime_sys_executable = C:\Users\johnn\AppData\Local\Temp\athena-006e20r\Scripts\python.exe
runtime_exists = true
runtime_matches_authorized = true
import_flint = PASS
```

The project `.venv` and workspace `.venv-006e20r` were not used for execution.

## 3. Versiones observadas

```text
python = 3.12.13 (main, Mar  3 2026, 15:01:35) [MSC v.1944 64 bit (AMD64)]
platform = Windows-11-10.0.26200-SP0
python-flint_distribution = 0.8.0
flint.__version__ = 0.8.0
flint.__FLINT_VERSION__ = 3.3.1
```

Version precheck:

```text
python_flint_distribution_is_0_8_0 = true
flint.__version___is_0_8_0 = true
flint.__FLINT_VERSION___is_3_3_1 = true
```

## 4. Lista fija exacta de entradas

Fixed `arb` inputs, all constructed from exact `fmpq` midpoint and exact
`fmpq` radius:

| Label | Midpoint | Radius |
| --- | --- | --- |
| `arb_A_one_third_radius_1_over_1000` | `1/3` | `1/1000` |
| `arb_B_minus_two_fifths_radius_1_over_10000` | `-2/5` | `1/10000` |
| `arb_C_two_radius_1_over_1000000` | `2/1` | `1/1000000` |

Fixed `acb` inputs, all rectangular boxes from exact non-point `arb`
components:

| Label | Real midpoint | Real radius | Imag midpoint | Imag radius |
| --- | --- | --- | --- | --- |
| `acb_S1` | `1/2` | `1/1000` | `7/5` | `1/2000` |
| `acb_S2` | `3/4` | `1/2000` | `2/1` | `1/1000` |

Float guard:

```text
float_inputs_present = false
float_input_guard = PASS
```

No Python `float` input was used in any constructor path.

## 5. Lista fija exacta de precisiones

```text
ctx_workprec_values = [64, 96]
l_function_workprec_bits = 96
```

The precision list was fixed before execution and was not expanded
adaptively.

## 6. Resultados contrato por contrato

| Contract | Result | Limited meaning |
| --- | --- | --- |
| Authorized runtime exists | PASS | The exact tempdir Python executable exists. |
| `import flint` | PASS | `flint` imported in the authorized runtime. |
| python-flint version | PASS | Distribution version is `0.8.0`. |
| `flint.__version__` | PASS | Module version is `0.8.0`. |
| `flint.__FLINT_VERSION__` | PASS | Native FLINT string identity is `3.3.1`. |
| Float input guard | PASS | Fixed descriptors contain no Python `float`. |
| `ctx.workprec` restoration | PASS | Restored after success and intentional exception. |
| Exact `arb` construction | PASS | All fixed balls finite, non-point where expected, midpoint included. |
| Rectangular `acb` construction | PASS | Fixed real and imaginary components kept nonzero width. |
| `dirichlet_char(3, 2)` identity | PASS | Metadata and values match the fixed `chi_3` smoke identity. |
| `chi.l_function(nonpoint_acb)` | PASS | Both fixed non-point inputs returned finite nonzero-width `acb` outputs. |

### Exact `arb` checks

| Label | Finite | Lower != Upper | Contains exact midpoint | Lower | Upper |
| --- | --- | --- | --- | --- | --- |
| `arb_A_one_third_radius_1_over_1000` | true | true | true | `[0.332333333329492 +/- 3.91e-16]` | `[0.334333333337175 +/- 2.05e-17]` |
| `arb_B_minus_two_fifths_radius_1_over_10000` | true | true | true | `[-0.400100000000316 +/- 7.49e-17]` | `[-0.399899999999684 +/- 8.25e-18]` |
| `arb_C_two_radius_1_over_1000000` | true | true | true | `[1.99999900000000 +/- 2.81e-15]` | `[2.00000100000000 +/- 2.81e-15]` |

### Rectangular `acb` checks

| Label | Finite | Real lower != upper | Imag lower != upper |
| --- | --- | --- | --- |
| `acb_S1` | true | true | true |
| `acb_S2` | true | true | true |

Observed component bounds:

```text
acb_S1.real_lower = [0.498999999997977 +/- 2.84e-16]
acb_S1.real_upper = [0.501000000002023 +/- 2.84e-16]
acb_S1.imag_lower = [1.39949999999808 +/- 9.42e-16]
acb_S1.imag_upper = [1.40050000000192 +/- 7.65e-16]

acb_S2.real_lower = [0.749499999998989 +/- 3.59e-16]
acb_S2.real_upper = [0.750500000001011 +/- 3.59e-16]
acb_S2.imag_lower = [1.99899999999798 +/- 2.72e-15]
acb_S2.imag_upper = [2.00100000000202 +/- 2.72e-15]
```

### `chi_3` identity

```text
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

### Native `l_function` fixed non-point checks

Both calls used `ctx.workprec(96)` and restored the previous context after the
call.

| Label | Output type | Finite | Real width nonzero | Imag width nonzero | Result |
| --- | --- | --- | --- | --- | --- |
| `acb_S1` | `acb` | true | true | true | PASS |
| `acb_S2` | `acb` | true | true | true | PASS |

Observed output bounds:

```text
acb_S1.output_real_lower = [0.559427222516187 +/- 4.84e-16]
acb_S1.output_real_upper = [0.618490659445324 +/- 1.10e-16]
acb_S1.output_imag_lower = [0.355214949523921 +/- 2.42e-16]
acb_S1.output_imag_upper = [0.416471770383774 +/- 4.76e-16]

acb_S2.output_real_lower = [0.765176502557899 +/- 7.02e-17]
acb_S2.output_real_upper = [0.796540318558420 +/- 2.24e-16]
acb_S2.output_imag_lower = [0.459664271262785 +/- 8.47e-17]
acb_S2.output_imag_upper = [0.491247939053768 +/- 1.25e-17]
```

These values are not zero-free evidence, not a zero certificate, and not a
mathematical proof.

## 7. Evidencia de restauracion de contexto

`ctx.prec` before the checks was `53`.

| Bits | Success before | Inside | Success after | Success restored | Exception before | Exception inside | Exception after | Exception restored |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 64 | 53 | 64 | 53 | true | 53 | 64 | 53 | true |
| 96 | 53 | 96 | 53 | true | 53 | 96 | 53 | true |

For `l_function` calls:

| Label | Context before | Inside before call | Inside after call | Context after | Restored |
| --- | --- | --- | --- | --- | --- |
| `acb_S1` | 53 | 96 | 96 | 53 | true |
| `acb_S2` | 53 | 96 | 96 | 53 | true |

## 8. Pruebas explicitamente no realizadas

```text
contours = not_executed
Lambda_3 = not_evaluated
zero_isolation = not_executed
zero_counting = not_executed
zero_tables = not_generated
adaptive_search = not_executed
precision_chasing_for_certification = not_executed
project_backend = not_invoked
H2_pipeline = not_invoked
H2_certification = not_performed
006F_opening = not_performed
downstream_use = forbidden
novelty_claim = false
new_dependencies = not_installed
network = not_used
```

No result from 006E23 is permitted to become downstream evidence.

## 9. Limite de identidad Arb no versionada por separado

006E23 observed:

```text
python-flint = 0.8.0
flint.__version__ = 0.8.0
flint.__FLINT_VERSION__ = 3.3.1
```

No separate Arb version accessor was used or discovered in this phase. Arb
functionality was exercised through python-flint 0.8.0 with observed FLINT
3.3.1 metadata. Therefore:

```text
Arb_native_identity = bounded_by_python_flint_and_FLINT_metadata
Arb_independent_version_seal = false
```

This is acceptable only for this narrow non-certifying semantic smoke. It is
not acceptable as a probative version seal for contours, zero certification,
H2 certification, or 006F readiness.

## 10. Veredicto limitado

```text
006E23_RESULT = 006E23_NARROW_SMOKE_PASS_LIMITED
REAL_FLINT_IMPORT = passed
FLINT_VERSION_SEAL_LIMITED = passed
ARB_SEMANTIC_NARROW_SMOKE = passed_limited
ACB_SEMANTIC_NARROW_SMOKE = passed_limited
NATIVE_L_NONPOINT_ACB_NARROW_SMOKE = passed_limited
MATHEMATICAL_PROOF = false
H2_CERTIFIED = false
H2_CERTIFIED_TRUE = false
006F = blocked
006F_OPENED = false
ZERO_CERTIFICATION = forbidden
ZERO_CERTIFICATION_COMPLETED = false
ZERO_TABLES = not_generated
DOWNSTREAM_USE = forbidden
DOWNSTREAM_USE_ALLOWED = false
NOVELTY_CLAIM = false
```

006E23 shows only that the authorized runtime passed the fixed narrow semantic
contracts above. It does not prove general Arb/acb semantics, general native
L-function inclusion, zero-free regions, H2, or any downstream theorem.

## 11. Recomendacion no vinculante para Yonnah

Recommended next step:

```text
NEXT_STEP = 006E24_document_narrow_semantic_result_and_boundaries
```

Do not proceed directly to contours or zero work. The next useful step is a
documentary interpretation layer that records exactly what 006E23 means, what
it still does not mean, and whether another narrow non-adaptive semantic phase
is needed before any broader real route is discussed.
