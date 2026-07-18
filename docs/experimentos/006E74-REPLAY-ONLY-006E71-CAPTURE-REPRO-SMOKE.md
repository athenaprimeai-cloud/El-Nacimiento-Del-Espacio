# 006E74 / Replay-Only 006E71 Capture Repro Smoke

## 1. Estado inicial y autorizacion

006E74 fue autorizada como ejecucion real estrecha, fija y no adaptativa,
siguiendo el gate documental 006E73.

```text
input_gate = 006E73-PREAUTHORIZATION-GATE-FOR-NEXT-REAL-EXECUTION
source_006E73_result = 006E73_PREAUTHORIZATION_GATE_DOCUMENT_COMPLETED
source_runtime_phase = 006E71
matrix_id = 006E74_REPLAY_ONLY_006E71_CAPTURE_REPRO
scope = narrow_fixed_non_adaptive_l_function_replay_only_smoke
capture_discipline = patched_capture_from_start
```

Bloqueos preservados:

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

## 2. Runtime usado

Runtime autorizado:

```text
runtime_authorized = C:\Users\johnn\AppData\Local\Temp\athena-006e20r\Scripts\python.exe
runtime_exists = true
runtime_sys_executable = C:\Users\johnn\AppData\Local\Temp\athena-006e20r\Scripts\python.exe
runtime_matches_authorized = true
```

No se instalaron dependencias. No se uso red. No se invoco backend del proyecto
ni pipeline H2.

## 3. Versiones observadas

Versiones observadas:

```text
python = 3.12.13 (main, Mar  3 2026, 15:01:35) [MSC v.1944 64 bit (AMD64)]
platform = Windows-11-10.0.26200-SP0
python-flint distribution = 0.8.0
flint.__version__ = 0.8.0
flint.__FLINT_VERSION__ = 3.3.1
arb_independent_version_seal = false
```

La identidad FLINT sigue sellada de forma limitada. Arb sigue sin sello de
version independiente separado.

## 4. Matriz fija ejecutada

006E74 ejecuto solo el replay exacto de la matriz 006E71:

```text
matrix_id = 006E74_REPLAY_ONLY_006E71_CAPTURE_REPRO
source_matrix_id = 006E71_REPLAY_PLUS_CENTER_YOCTO_TIGHT
total_inputs = 45
replay_inputs_from_006E71 = 45
new_inputs = 0
```

Disciplina de entrada:

```text
all_inputs_constructed_from_exact_rational_descriptors = true
float_inputs_present = false
complex_inputs_present = false
decimal_float_literals_present = false
adaptive_inputs_present = false
new_center_layer = false
```

006E74 no agrega una nueva familia de cajas. Su funcion es reproducibilidad
estrecha de runtime/captura sobre la matriz 006E71.

## 5. Precisiones fijas ejecutadas

006E74 uso solo las precisiones fijas autorizadas:

```text
precision_values = [96, 128]
precision_chasing = not_executed
```

No se agrego ninguna precision durante la fase.

## 6. Llamadas semanticas realizadas

006E74 ejecuto exactamente:

```text
expected_l_function_records = 90
observed_l_function_records = 90
records_pass = 90
```

Resultados por contrato:

```text
ctx_restored_for_all_calls = true
output_type_acb_for_all_calls = true
output_finite_for_all_calls = true
output_width_nonzero_for_all_calls = true
input_width_nonzero_for_all_calls = true
```

El 90/90/90 significa solamente que, para este replay fijo y estas precisiones
fijas, `chi.l_function` acepto las entradas `acb` no puntuales predeclaradas y
devolvio salidas `acb` finitas, con anchuras real e imaginaria no nulas,
restaurando el contexto.

## 7. Diagnosticos madre/hijo

006E74 ejecuto exactamente los diagnosticos smoke replay de 006E71:

```text
expected_diagnostics = 84
observed_diagnostics = 84
diagnostics_pass = 84
diagnostic_pairs = 42
```

Bloques diagnosticos:

```text
parent_to_existing_children = 30
center_to_tight_children = 6
tight_to_ultra_tight_children = 6
ultra_tight_to_micro_tight_children = 6
micro_tight_to_nano_tight_children = 6
nano_tight_to_pico_tight_children = 6
pico_tight_to_femto_tight_children = 6
femto_tight_to_atto_tight_children = 6
atto_tight_to_zepto_tight_children = 6
zepto_tight_to_yocto_tight_children = 6
```

El 84/84/84 diagnostico significa solo que los checks smoke madre/hijo
declarados reportaron `contains = true` y `overlaps = true` en las parejas fijas.
No prueba inclusion general de `chi.l_function`.

## 8. Captura parcheada y autoridad de artefactos

Artefactos persistidos en:

```text
artifact_directory = artifacts/006E74-replay-only-006E71-capture-repro/
```

Archivos persistidos:

```text
ledger.jsonl
ledger.csv
ledger-compact.md
diagnostics.jsonl
diagnostics.csv
manifest.json
SHA256SUMS.txt
```

Reglas de autoridad:

```text
JSONL_AUTHORITY = primary
CSV_AUTHORITY = secondary
MARKDOWN_COMPACT_AUTHORITY = summary_only
MANIFEST_AUTHORITY = identity_and_counts
SHA256SUMS_AUTHORITY = file_integrity_only
CONSOLE_SCROLLBACK_AUTHORITY = none
```

Estado del orden de captura:

```text
manifest_initial_write_before_files_present_check = true
files_present_computed_after_manifest_initial_write = true
manifest_final_written_before_final_SHA256SUMS = true
SHA256SUMS_written_after_final_manifest = true
hashes_computed_after_manifest_finalization = true
hashes_verified_after_SHA256SUMS_write = true
capture_warning = none
unresolved_capture_warning = false
semantic_rerun_performed_for_capture_correction = false
```

## 9. Conteos y hashes

Checks de artefactos posteriores a la corrida:

```text
files_present = true
hash_verified = true
fresh_hash_verification = true
hash_records = 6
ledger_jsonl_lines = 90
diagnostics_jsonl_lines = 84
unique_input_labels = 45
```

SHA-256 verifica integridad de archivos, no matematica.

## 10. Pruebas explicitamente no realizadas

006E74 no ejecuto:

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
```

006E74 no instalo dependencias y no uso la red.

## 11. Verificacion contractual local

La prueba contractual estrecha fue ejecutada antes y despues de la corrida real:

```text
tests.test_006e74_replay_only_capture_repro_contract = passed
contract_tests = 3/3
py_compile = passed
```

La suite completa del proyecto no fue requisito de exito para 006E74.

## 12. Interpretacion permitida

Interpretacion permitida:

```text
fixed_006E74_replay_l_function_smoke = passed_limited
patched_capture_order = passed_limited
runtime_context_restoration = observed_for_fixed_calls
finite_acb_outputs = observed_for_fixed_calls
nonzero_output_widths = observed_for_fixed_calls
parent_child_diagnostics = smoke_only_passed
REPLAY_ONLY_006E71 = reproducibility_and_capture_only
```

006E74 reproduce la matriz 006E71 sin entradas nuevas. No amplia alcance
matematico.

## 13. Inferencias prohibidas

006E74 no implica:

```text
MATHEMATICAL_PROOF = false
H2_CERTIFIED_TRUE = false
006F_OPENED = false
ZERO_CERTIFICATION_COMPLETED = false
ZERO_TABLES_GENERATED = false
ZERO_FREE_REGION_PROVED = false
GENERAL_L_FUNCTION_SEMANTICS_PROVED = false
GENERAL_ARB_ACB_SEMANTICS_PROVED = false
DOWNSTREAM_USE_ALLOWED = false
NOVELTY_CLAIM_ALLOWED = false
```

El 90/90/90, el 84/84/84, los ledgers completos y los hashes son evidencia
runtime/captura estrecha y reproducible. No son prueba matematica.

## 14. Recomendacion no vinculante para Yonnah

Recomendacion:

```text
NEXT_STEP = 006E75_DOCUMENT_006E74_REPLAY_CAPTURE_REPRO_RESULT
AUTHORIZE_CONTOURS = false
AUTHORIZE_LAMBDA_3 = false
AUTHORIZE_ZERO_WORK = false
AUTHORIZE_H2 = false
AUTHORIZE_006F = false
AUTHORIZE_DOWNSTREAM = false
AUTHORIZE_NOVELTY_CLAIM = false
```

El siguiente movimiento razonable es una capa documental interpretativa que fije
el significado de la reproducibilidad de 006E74, no una ampliacion de alcance.

## 15. Resultado

```text
006E74_RESULT = 006E74_REPLAY_ONLY_CAPTURE_REPRO_SMOKE_PASS_LIMITED
RESULT_MAXIMUM = 006E74_REPLAY_ONLY_CAPTURE_REPRO_SMOKE_PASS_LIMITED
VALID_RUNTIME_SEMANTIC_RESULT = 006E74_REPLAY_ONLY_CAPTURE_REPRO_SMOKE_PASS_LIMITED
RUNTIME_AUTHORIZED_EXISTS = true
RUNTIME_MATCHES_AUTHORIZED = true
REAL_FLINT_IMPORT = passed
PYTHON_FLINT_DISTRIBUTION = 0.8.0
FLINT_VERSION = 0.8.0
FLINT_NATIVE_VERSION_LIMITED = 3.3.1
ARB_INDEPENDENT_VERSION_SEAL = false
MATRIX_ID = 006E74_REPLAY_ONLY_006E71_CAPTURE_REPRO
SOURCE_MATRIX_ID = 006E71_REPLAY_PLUS_CENTER_YOCTO_TIGHT
INPUTS_TOTAL = 45
REPLAY_INPUTS_FROM_006E71 = 45
NEW_INPUTS = 0
PRECISION_VALUES = [96, 128]
L_FUNCTION_CALLS_EXPECTED = 90
L_FUNCTION_CALLS_OBSERVED = 90
L_FUNCTION_CALLS_PASS = 90
DIAGNOSTICS_EXPECTED = 84
DIAGNOSTICS_OBSERVED = 84
DIAGNOSTICS_PASS = 84
FILES_PRESENT = true
HASH_VERIFIED = true
FRESH_HASH_VERIFICATION = true
CAPTURE_WARNING = none
UNRESOLVED_CAPTURE_WARNING = false
PATCHED_CAPTURE_ORDER_APPLIED = true
CTX_RESTORED_FOR_ALL_CALLS = true
OUTPUT_TYPE_ACB_FOR_ALL_CALLS = true
OUTPUT_FINITE_FOR_ALL_CALLS = true
OUTPUT_WIDTH_NONZERO_FOR_ALL_CALLS = true
SCOPE_LEAK = false
MATHEMATICAL_PROOF = false
H2_CERTIFIED = false
006F = blocked
ZERO_CERTIFICATION = forbidden
ZERO_TABLES = not_generated
DOWNSTREAM_USE = forbidden
NOVELTY_CLAIM = false
```

006E74 cierra como `006E74_REPLAY_ONLY_CAPTURE_REPRO_SMOKE_PASS_LIMITED`.
