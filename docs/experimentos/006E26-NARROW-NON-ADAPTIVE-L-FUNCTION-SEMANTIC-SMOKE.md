# 006E26-NARROW-NON-ADAPTIVE-L-FUNCTION-SEMANTIC-SMOKE

## 1. Estado inicial y bloqueos preservados

```text
phase_id = 006E26
status = narrow_non_adaptive_l_function_semantic_smoke_completed_with_warnings
result = 006E26_L_FUNCTION_SEMANTIC_SMOKE_PASS_WITH_WARNINGS
maximum_allowed_result = 006E26_L_FUNCTION_SEMANTIC_SMOKE_PASS_LIMITED
source = 006E25-NARROW-NON-ADAPTIVE-L-FUNCTION-SEMANTICS-PLAN
scope = fixed_non_adaptive_l_function_semantic_smoke
adaptive_search = not_executed
precision_chasing = not_executed
project_backend_invocation = not_executed
H2_pipeline_invocation = not_executed
contour_execution = forbidden
Lambda_3_evaluation = forbidden
zero_isolation = forbidden
zero_counting = forbidden
zero_tables = not_generated
new_dependencies = not_installed
network = not_used
MATHEMATICAL_PROOF = false
H2_CERTIFIED = false
006F = blocked
ZERO_CERTIFICATION = forbidden
ZERO_TABLES = not_generated
DOWNSTREAM_USE = forbidden
NOVELTY_CLAIM = false
```

006E26 executed only the fixed `chi.l_function` semantic smoke matrix defined
by 006E25: 15 predeclared `acb` inputs and 2 fixed precision values.

## 2. Runtime usado

```text
runtime_authorized = C:\Users\johnn\AppData\Local\Temp\athena-006e20r\Scripts\python.exe
runtime_sys_executable = C:\Users\johnn\AppData\Local\Temp\athena-006e20r\Scripts\python.exe
runtime_exists = true
runtime_matches_authorized = true
import_flint = PASS
```

## 3. Versiones observadas

```text
python = 3.12.13 (main, Mar  3 2026, 15:01:35) [MSC v.1944 64 bit (AMD64)]
platform = Windows-11-10.0.26200-SP0
python-flint_distribution = 0.8.0
flint.__version__ = 0.8.0
flint.__FLINT_VERSION__ = 3.3.1
```

## 4. Lista fija exacta de entradas

Parent boxes:

| Label | Real midpoint | Real radius | Imag midpoint | Imag radius |
| --- | --- | --- | --- | --- |
| `LBOX_P1` | `1/2` | `1/1000` | `7/5` | `1/2000` |
| `LBOX_P2` | `3/4` | `1/2000` | `2/1` | `1/1000` |
| `LBOX_P3` | `1/3` | `1/1500` | `5/3` | `1/1500` |

Subboxes used exactly as expanded in 006E25:

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

Input discipline:

```text
float_inputs_present = false
complex_inputs_present = false
adaptive_inputs_present = false
all_inputs_constructed_from_exact_rational_descriptors = true
```

## 5. Precisiones fijas

```text
ctx_workprec_values = [96, 128]
adaptive_precision = forbidden
precision_chasing = not_executed
```

## 6. Resultados contrato por contrato

| Contract | Result | Notes |
| --- | --- | --- |
| Authorized runtime | PASS | Runtime exists and matches authorized path. |
| `import flint` | PASS | Import succeeded. |
| Version precheck | PASS | python-flint 0.8.0, `flint.__version__` 0.8.0, FLINT 3.3.1. |
| Exact input discipline | PASS | No `float`, no `complex`, no adaptive descriptors. |
| Fixed matrix size | PASS | 15 inputs x 2 precisions = 30 records. |
| `chi.l_function` output type | PASS | All 30 outputs were `acb`. |
| Output finiteness | PASS | All 30 outputs finite. |
| Nonzero real output width | PASS | All 30 real output components had lower != upper. |
| Nonzero imaginary output width | PASS | All 30 imaginary output components had lower != upper. |
| Context restoration | PASS | All calls restored `ctx.prec` to 53. |
| Parent/subbox diagnostic | PASS_DIAGNOSTIC | 24/24 diagnostic comparisons had `contains=true` and `overlaps=true`. |
| Plan consistency warning | WARNING | 006E25 formula/table tension; exact expanded table was used. |

Summary:

```text
records = 30
records_pass = 30
diagnostics = 24
diagnostics_pass = 24
result = 006E26_L_FUNCTION_SEMANTIC_SMOKE_PASS_WITH_WARNINGS
```

## 7. Ledger por entrada y precision

Column key:

```text
label = input_label
bits = precision_bits
in_rl/in_ru = input real lower/upper
in_il/in_iu = input imaginary lower/upper
out_rl/out_ru = output real lower/upper
out_il/out_iu = output imaginary lower/upper
rw/iw = output real/imag lower_ne_upper
ctx = ctx_before/ctx_inside/ctx_after
```

```text
label|bits|in_rl|in_ru|in_il|in_iu|out_type|finite|out_rl|out_ru|out_il|out_iu|rw|iw|ctx|restored|result
LBOX_P1|96|[0.498999999997977 +/- 2.84e-16]|[0.501000000002023 +/- 2.84e-16]|[1.39949999999808 +/- 9.42e-16]|[1.40050000000192 +/- 7.65e-16]|acb|true|[0.559427222516187 +/- 4.84e-16]|[0.618490659445324 +/- 1.10e-16]|[0.355214949523921 +/- 2.42e-16]|[0.416471770383774 +/- 4.76e-16]|true|true|53/96/53|true|PASS
LBOX_P1|128|[0.498999999997977 +/- 2.84e-16]|[0.501000000002023 +/- 2.84e-16]|[1.39949999999808 +/- 9.42e-16]|[1.40050000000192 +/- 7.65e-16]|acb|true|[0.551224179575808 +/- 1.74e-16]|[0.626693774373859 +/- 2.42e-16]|[0.345763799608881 +/- 4.29e-16]|[0.425922933025482 +/- 8.97e-18]|true|true|53/128/53|true|PASS
LBOX_P2|96|[0.749499999998989 +/- 3.59e-16]|[0.750500000001011 +/- 3.59e-16]|[1.99899999999798 +/- 2.72e-15]|[2.00100000000202 +/- 2.72e-15]|acb|true|[0.765176502557899 +/- 7.02e-17]|[0.796540318558420 +/- 2.24e-16]|[0.459664271262785 +/- 8.47e-17]|[0.491247939053768 +/- 1.25e-17]|true|true|53/96/53|true|PASS
LBOX_P2|128|[0.749499999998989 +/- 3.59e-16]|[0.750500000001011 +/- 3.59e-16]|[1.99899999999798 +/- 2.72e-15]|[2.00100000000202 +/- 2.72e-15]|acb|true|[0.762513764186462 +/- 4.74e-18]|[0.799203073997216 +/- 1.81e-17]|[0.456966245348580 +/- 3.25e-16]|[0.493945986474414 +/- 3.77e-16]|true|true|53/128/53|true|PASS
LBOX_P3|96|[0.332666666664712 +/- 1.60e-16]|[0.334000000001955 +/- 2.12e-16]|[1.66599999999805 +/- 4.96e-15]|[1.66733333333529 +/- 2.01e-15]|acb|true|[0.550460991440364 +/- 3.55e-16]|[0.636922109280736 +/- 2.18e-16]|[0.452574820701485 +/- 1.93e-16]|[0.539027413564255 +/- 2.09e-16]|true|true|53/96/53|true|PASS
LBOX_P3|128|[0.332666666664712 +/- 1.60e-16]|[0.334000000001955 +/- 2.12e-16]|[1.66599999999805 +/- 4.96e-15]|[1.66733333333529 +/- 2.01e-15]|acb|true|[0.519906073462762 +/- 3.70e-16]|[0.667477020880751 +/- 1.16e-16]|[0.422009155534797 +/- 4.54e-16]|[0.569593076043421 +/- 3.13e-16]|true|true|53/128/53|true|PASS
LBOX_P1_S1|96|[0.499249999998079 +/- 1.20e-16]|[0.500250000001921 +/- 1.20e-16]|[1.39949999999904 +/- 5.99e-16]|[1.40000000000096 +/- 2.55e-16]|acb|true|[0.574085283694401 +/- 4.83e-16]|[0.603607601185175 +/- 1.31e-16]|[0.370506841684813 +/- 4.60e-16]|[0.401127435233333 +/- 5.18e-17]|true|true|53/96/53|true|PASS
LBOX_P1_S1|128|[0.499249999998079 +/- 1.20e-16]|[0.500250000001921 +/- 1.20e-16]|[1.39949999999904 +/- 5.99e-16]|[1.40000000000096 +/- 2.55e-16]|acb|true|[0.569979864644371 +/- 2.19e-16]|[0.607713038457110 +/- 4.44e-16]|[0.365775091764829 +/- 8.57e-17]|[0.405859180044229 +/- 1.62e-16]|true|true|53/128/53|true|PASS
LBOX_P1_S2|96|[0.499249999998079 +/- 1.20e-16]|[0.500250000001921 +/- 1.20e-16]|[1.39999999999904 +/- 4.32e-16]|[1.40050000000096 +/- 4.22e-16]|acb|true|[0.574182766193223 +/- 4.96e-16]|[0.603682105482255 +/- 4.62e-16]|[0.370654692017779 +/- 1.03e-16]|[0.401255636930073 +/- 1.22e-16]|true|true|53/96/53|true|PASS
LBOX_P1_S2|128|[0.499249999998079 +/- 1.20e-16]|[0.500250000001921 +/- 1.20e-16]|[1.39999999999904 +/- 4.32e-16]|[1.40050000000096 +/- 4.22e-16]|acb|true|[0.570089656850901 +/- 3.91e-17]|[0.607775233036951 +/- 1.99e-16]|[0.365937171554460 +/- 2.95e-16]|[0.405973152249853 +/- 3.03e-16]|true|true|53/128/53|true|PASS
LBOX_P1_S3|96|[0.499749999998079 +/- 1.20e-16]|[0.500750000001921 +/- 1.75e-16]|[1.39949999999904 +/- 5.99e-16]|[1.40000000000096 +/- 2.55e-16]|acb|true|[0.574247777970140 +/- 4.83e-16]|[0.603721121659601 +/- 9.89e-17]|[0.370447018874148 +/- 3.82e-16]|[0.401015316011655 +/- 2.57e-16]|true|true|53/96/53|true|PASS
LBOX_P1_S3|128|[0.499749999998079 +/- 1.20e-16]|[0.500750000001921 +/- 1.75e-16]|[1.39949999999904 +/- 5.99e-16]|[1.40000000000096 +/- 2.55e-16]|acb|true|[0.570152808210182 +/- 6.16e-18]|[0.607816109896007 +/- 9.52e-17]|[0.365726405054665 +/- 4.72e-16]|[0.405735928330905 +/- 1.61e-16]|true|true|53/128/53|true|PASS
LBOX_P1_S4|96|[0.499749999998079 +/- 1.20e-16]|[0.500750000001921 +/- 1.75e-16]|[1.39999999999904 +/- 4.32e-16]|[1.40050000000096 +/- 4.22e-16]|acb|true|[0.574345237163853 +/- 2.18e-16]|[0.603795640428344 +/- 2.16e-16]|[0.370594809919840 +/- 2.30e-16]|[0.401143492065149 +/- 1.24e-17]|true|true|53/96/53|true|PASS
LBOX_P1_S4|128|[0.499749999998079 +/- 1.20e-16]|[0.500750000001921 +/- 1.75e-16]|[1.39999999999904 +/- 4.32e-16]|[1.40050000000096 +/- 4.22e-16]|acb|true|[0.570262549262271 +/- 3.79e-16]|[0.607878346802910 +/- 8.57e-17]|[0.365888393719193 +/- 7.25e-17]|[0.405849906734635 +/- 2.76e-16]|true|true|53/128/53|true|PASS
LBOX_P2_S1|96|[0.749499999999039 +/- 4.91e-16]|[0.750000000000960 +/- 3.43e-16]|[1.99899999999808 +/- 1.02e-15]|[2.00000000000192 +/- 6.86e-16]|acb|true|[0.772840714127653 +/- 9.46e-17]|[0.788514841713606 +/- 3.08e-16]|[0.467531738307529 +/- 3.66e-16]|[0.483316101424366 +/- 4.04e-16]|true|true|53/96/53|true|PASS
LBOX_P2_S1|128|[0.749499999999039 +/- 4.91e-16]|[0.750000000000960 +/- 3.43e-16]|[1.99899999999808 +/- 1.02e-15]|[2.00000000000192 +/- 6.86e-16]|acb|true|[0.771512890259709 +/- 3.88e-17]|[0.789842669557055 +/- 4.00e-16]|[0.466185645432070 +/- 4.73e-16]|[0.484662200061231 +/- 3.81e-16]|true|true|53/128/53|true|PASS
LBOX_P2_S2|96|[0.749499999999039 +/- 4.91e-16]|[0.750000000000960 +/- 3.43e-16]|[1.99999999999808 +/- 1.14e-15]|[2.00100000000192 +/- 5.76e-16]|acb|true|[0.773105093586566 +/- 2.39e-16]|[0.788778774661552 +/- 1.07e-16]|[0.467729074576881 +/- 3.79e-16]|[0.483512348890316 +/- 3.65e-16]|true|true|53/96/53|true|PASS
LBOX_P2_S2|128|[0.749499999999039 +/- 4.91e-16]|[0.750000000000960 +/- 3.43e-16]|[1.99999999999808 +/- 1.14e-15]|[2.00100000000192 +/- 5.76e-16]|acb|true|[0.771770709012677 +/- 3.64e-16]|[0.790113163231914 +/- 2.83e-16]|[0.466377747966599 +/- 1.99e-16]|[0.484863681246916 +/- 3.68e-16]|true|true|53/128/53|true|PASS
LBOX_P2_S3|96|[0.749999999999040 +/- 4.54e-16]|[0.750500000000960 +/- 3.99e-16]|[1.99899999999808 +/- 1.02e-15]|[2.00000000000192 +/- 6.86e-16]|acb|true|[0.772949991974681 +/- 3.84e-16]|[0.788602363661564 +/- 1.35e-18]|[0.467410710878317 +/- 4.07e-16]|[0.483173087564642 +/- 5.47e-17]|true|true|53/96/53|true|PASS
LBOX_P2_S3|128|[0.749999999999040 +/- 4.54e-16]|[0.750500000000960 +/- 3.99e-16]|[1.99899999999808 +/- 1.02e-15]|[2.00000000000192 +/- 6.86e-16]|acb|true|[0.771625346476859 +/- 4.31e-16]|[0.789927013540357 +/- 4.52e-16]|[0.466067815555263 +/- 3.90e-16]|[0.484515987284950 +/- 2.67e-16]|true|true|53/128/53|true|PASS
LBOX_P2_S4|96|[0.749999999999040 +/- 4.54e-16]|[0.750500000000960 +/- 3.99e-16]|[1.99999999999808 +/- 1.14e-15]|[2.00100000000192 +/- 5.76e-16]|acb|true|[0.773214317973630 +/- 6.13e-17]|[0.788866247282290 +/- 3.79e-16]|[0.467607956436412 +/- 2.69e-16]|[0.483369249383402 +/- 3.67e-16]|true|true|53/96/53|true|PASS
LBOX_P2_S4|128|[0.749999999999040 +/- 4.54e-16]|[0.750500000000960 +/- 3.99e-16]|[1.99999999999808 +/- 1.14e-15]|[2.00100000000192 +/- 5.76e-16]|acb|true|[0.771883126566584 +/- 1.99e-16]|[0.790197443086120 +/- 3.88e-16]|[0.466259839892362 +/- 3.62e-16]|[0.484717370307979 +/- 3.77e-16]|true|true|53/128/53|true|PASS
LBOX_P3_S1|96|[0.332833333332356 +/- 7.05e-17]|[0.333500000000977 +/- 4.04e-16]|[1.66599999999902 +/- 2.49e-15]|[1.66666666666764 +/- 3.96e-15]|acb|true|[0.571959651735652 +/- 4.47e-16]|[0.615171936360694 +/- 1.07e-16]|[0.474133150072329 +/- 3.13e-16]|[0.517343311340109 +/- 1.36e-16]|true|true|53/96/53|true|PASS
LBOX_P3_S1|128|[0.332833333332356 +/- 7.05e-17]|[0.333500000000977 +/- 4.04e-16]|[1.66599999999902 +/- 2.49e-15]|[1.66666666666764 +/- 3.96e-15]|acb|true|[0.556708026053107 +/- 1.43e-17]|[0.630423562675438 +/- 3.57e-16]|[0.458878843464814 +/- 1.66e-16]|[0.532597617713660 +/- 2.35e-16]|true|true|53/128/53|true|PASS
LBOX_P3_S2|96|[0.332833333332356 +/- 7.05e-17]|[0.333500000000977 +/- 4.04e-16]|[1.66666666666569 +/- 9.22e-16]|[1.66733333333431 +/- 5.53e-16]|acb|true|[0.572124749646881 +/- 1.88e-17]|[0.615308688188796 +/- 3.60e-16]|[0.474348552540162 +/- 3.84e-16]|[0.517530374011242 +/- 8.85e-17]|true|true|53/96/53|true|PASS
LBOX_P3_S2|128|[0.332833333332356 +/- 7.05e-17]|[0.333500000000977 +/- 4.04e-16]|[1.66666666666569 +/- 9.22e-16]|[1.66733333333431 +/- 5.53e-16]|acb|true|[0.556842431881156 +/- 4.37e-16]|[0.630591006589744 +/- 9.64e-17]|[0.459063552509184 +/- 4.03e-16]|[0.532815373808268 +/- 4.47e-17]|true|true|53/128/53|true|PASS
LBOX_P3_S3|96|[0.333166666665689 +/- 2.27e-16]|[0.333833333334311 +/- 3.00e-16]|[1.66599999999902 +/- 2.49e-15]|[1.66666666666764 +/- 3.96e-15]|acb|true|[0.572084235828921 +/- 1.28e-16]|[0.615248565665066 +/- 2.73e-17]|[0.474081687327771 +/- 1.05e-16]|[0.517243895203637 +/- 4.50e-16]|true|true|53/96/53|true|PASS
LBOX_P3_S3|128|[0.333166666665689 +/- 2.27e-16]|[0.333833333334311 +/- 3.00e-16]|[1.66599999999902 +/- 2.49e-15]|[1.66666666666764 +/- 3.96e-15]|acb|true|[0.556855306076942 +/- 3.31e-16]|[0.630477485760240 +/- 3.47e-16]|[0.458850084360057 +/- 3.02e-16]|[0.532475496780426 +/- 4.94e-16]|true|true|53/128/53|true|PASS
LBOX_P3_S4|96|[0.333166666665689 +/- 2.27e-16]|[0.333833333334311 +/- 3.00e-16]|[1.66666666666569 +/- 9.22e-16]|[1.66733333333431 +/- 5.53e-16]|acb|true|[0.572249307784442 +/- 1.71e-16]|[0.615385331060462 +/- 2.18e-16]|[0.474297022639133 +/- 3.70e-16]|[0.517430930415925 +/- 2.78e-17]|true|true|53/96/53|true|PASS
LBOX_P3_S4|128|[0.333166666665689 +/- 2.27e-16]|[0.333833333334311 +/- 3.00e-16]|[1.66666666666569 +/- 9.22e-16]|[1.66733333333431 +/- 5.53e-16]|acb|true|[0.556989727593436 +/- 4.57e-16]|[0.630644901590831 +/- 3.09e-16]|[0.459034768170209 +/- 3.29e-16]|[0.532693183519410 +/- 2.49e-16]|true|true|53/128/53|true|PASS
```

## 8. Diagnostico madre/subcajas

The parent/subbox comparison is smoke-only. It is not mathematical proof,
coverage proof, zero-free evidence, or contour evidence.

```text
parent|subbox|bits|contains|overlaps|result
LBOX_P1|LBOX_P1_S1|96|true|true|PASS_DIAGNOSTIC
LBOX_P1|LBOX_P1_S2|96|true|true|PASS_DIAGNOSTIC
LBOX_P1|LBOX_P1_S3|96|true|true|PASS_DIAGNOSTIC
LBOX_P1|LBOX_P1_S4|96|true|true|PASS_DIAGNOSTIC
LBOX_P2|LBOX_P2_S1|96|true|true|PASS_DIAGNOSTIC
LBOX_P2|LBOX_P2_S2|96|true|true|PASS_DIAGNOSTIC
LBOX_P2|LBOX_P2_S3|96|true|true|PASS_DIAGNOSTIC
LBOX_P2|LBOX_P2_S4|96|true|true|PASS_DIAGNOSTIC
LBOX_P3|LBOX_P3_S1|96|true|true|PASS_DIAGNOSTIC
LBOX_P3|LBOX_P3_S2|96|true|true|PASS_DIAGNOSTIC
LBOX_P3|LBOX_P3_S3|96|true|true|PASS_DIAGNOSTIC
LBOX_P3|LBOX_P3_S4|96|true|true|PASS_DIAGNOSTIC
LBOX_P1|LBOX_P1_S1|128|true|true|PASS_DIAGNOSTIC
LBOX_P1|LBOX_P1_S2|128|true|true|PASS_DIAGNOSTIC
LBOX_P1|LBOX_P1_S3|128|true|true|PASS_DIAGNOSTIC
LBOX_P1|LBOX_P1_S4|128|true|true|PASS_DIAGNOSTIC
LBOX_P2|LBOX_P2_S1|128|true|true|PASS_DIAGNOSTIC
LBOX_P2|LBOX_P2_S2|128|true|true|PASS_DIAGNOSTIC
LBOX_P2|LBOX_P2_S3|128|true|true|PASS_DIAGNOSTIC
LBOX_P2|LBOX_P2_S4|128|true|true|PASS_DIAGNOSTIC
LBOX_P3|LBOX_P3_S1|128|true|true|PASS_DIAGNOSTIC
LBOX_P3|LBOX_P3_S2|128|true|true|PASS_DIAGNOSTIC
LBOX_P3|LBOX_P3_S3|128|true|true|PASS_DIAGNOSTIC
LBOX_P3|LBOX_P3_S4|128|true|true|PASS_DIAGNOSTIC
```

## 9. Advertencia

```text
warning = 006E25 subbox formula/table tension noted; exact expanded table used
```

The warning is documentary. It does not indicate a runtime failure: all 30
fixed `l_function` records passed and all 24 parent/subbox diagnostics passed.
It prevents using the stronger `006E26_L_FUNCTION_SEMANTIC_SMOKE_PASS_LIMITED`
label because the table/formula tension should remain visible before any next
phase.

## 10. Pruebas explicitamente no realizadas

```text
contours = not_executed
Lambda_3 = not_evaluated
zero_isolation = not_executed
zero_counting = not_executed
zero_tables = not_generated
adaptive_search = not_executed
precision_chasing = not_executed
project_backend = not_invoked
H2_pipeline = not_invoked
H2_certification = not_performed
006F_opening = not_performed
downstream_use = forbidden
novelty_claim = false
new_dependencies = not_installed
network = not_used
```

## 11. Limite de identidad Arb

```text
python-flint = 0.8.0
flint.__version__ = 0.8.0
flint.__FLINT_VERSION__ = 3.3.1
Arb_independent_version_seal = false
```

Arb functionality was exercised through python-flint 0.8.0 with observed FLINT
3.3.1 metadata. Arb remains not independently versioned by the recorded
metadata chain.

## 12. Veredicto limitado

```text
006E26_RESULT = 006E26_L_FUNCTION_SEMANTIC_SMOKE_PASS_WITH_WARNINGS
MAXIMUM_ALLOWED_RESULT = 006E26_L_FUNCTION_SEMANTIC_SMOKE_PASS_LIMITED
REAL_FLINT_IMPORT = passed
FLINT_VERSION_SEAL_LIMITED = passed
FIXED_NONADAPTIVE_L_FUNCTION_INPUTS = passed_limited_with_warning
PARENT_SUBBOX_DIAGNOSTIC = passed_limited_smoke_only
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

006E26 is a narrow semantic smoke result only. It does not prove general
`chi.l_function` inclusion semantics, Arb semantics, acb semantics, zero-free
regions, H2, or any downstream theorem.

## 13. Recomendacion no vinculante para Yonnah

Recommended next step:

```text
NEXT_STEP = 006E27_document_l_function_smoke_result_and_plan_tension
```

Do not proceed to contours, `Lambda_3`, zero work, H2 certification, 006F, or
downstream use. The next phase should document exactly what the 006E26 smoke
means and either patch or explicitly accept the 006E25 subbox formula/table
tension before any broader semantic phase.
