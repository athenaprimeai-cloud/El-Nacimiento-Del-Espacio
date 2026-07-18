# Experimento 006E10: Correcciones del Backend Inerte L3

## 1. Estado y alcance

```text
experiment_id = G5B-006E10
status = corrections_completed_pending_review
target = fix_006E9_blocking_findings
code_authorization = structural_corrections_only
structural_test_execution = authorized
real_flint_execution = forbidden
real_contour_execution = forbidden
zero_certification = forbidden
zero_tables = not_generated
artifacts = none
network = forbidden
H2_certified = false
006F_readiness = false
006F_execution = forbidden
C05_RERUN = forbidden
C35 = frozen
C15 = frozen
novelty_claim = false
```

006E10 corrige los dos hallazgos bloqueantes de 006E9 y prepara la condicion
abierta de cadena 006F. No completa el backend matematico real y no autoriza
ninguna ejecucion probatoria.

## 2. Sellos heredados

```text
006E7_SHA256 = 4f51a71107d16b037a589d948082669a0c993245e28154d8fb68c36603ef33e4
006E8_CORRECTED_SHA256 = 8608a503203ad550dfa7800ab99e76e0a44ebae05d68b60842a9850d4f4c1a63
006E9_SHA256 = 905eed6c485c6b67b54cc0ebaf197784ec3da7b81bdddb45d468a728fa927cef
```

## 3. Correccion 1: procedencia probatoria validada

Se agrego `ValidatedEvidenceProvenance`, emitida exclusivamente por
`issue_evidence_provenance` cuando recibe un `ExecutionAuthorization` creado
por el parser con su capacidad privada.

La procedencia contiene:

```text
backend_id
authorization_digest
runtime_code_digest
review_chain_digest
```

`RealEvidenceFactory.from_authorization` conserva internamente esta capacidad.
La construccion directa de la fabrica sigue disponible para fixtures inertes,
pero toda evidencia que produce queda `probative = false`.

`require_probative_evidence` rechaza:

1. tipos sinteticos historicos;
2. evidencia de una fabrica no validada;
3. una fabrica no validada cuyos atributos publicos hayan sido manipulados.

La identidad del backend y los digests probatorios se leen siempre de la
procedencia sellada, no de atributos mutables de la fabrica.

## 4. Correccion 2: inventario SHA-256 completo

El informe 006E8 corregido enumera cada entrada de
`PROBATIVE_RUNTIME_CODE_FILES`. El inventario contiene exactamente 22 archivos
y excluye `argument_principle.py`.

Una prueba documental calcula los hashes actuales y exige que cada pareja
`ruta SHA-256` aparezca en 006E8. La prueba falla ante archivos ausentes o
hashes obsoletos.

## 5. Correccion 3: cadena futura 006F

El esquema de autorizacion agrega obligatoriamente:

```text
plan_006e7_sha256
report_006e8_sha256
review_006e9_sha256
corrections_006e10_sha256
```

`compute_review_document_hashes` calcula estos sellos directamente desde los
documentos del espacio de trabajo. El parser exige coincidencia exacta entre
el JSON futuro y los documentos presentes.

La eleccion dinamica evita referencias circulares entre documentos e
inventarios de codigo. No se creo ningun JSON 006F y el pipeline sigue
terminando en `NotImplementedError` despues de las guardias.

## 6. Evidencia TDD

Se observaron antes de implementar las correcciones:

```text
RED: una fabrica con hashes inventados atravesaba require_probative_evidence
RED: require_execution_authorization no aceptaba ni validaba la cadena posterior
RED: 006E8 no contenia los 22 archivos probatorios
RED: la marca probative mutable permitia auto-promocion de una fabrica falsa
RED: la identidad del backend validado podia mutarse despues de crear la fabrica
```

Despues de los cambios, todos estos falsificadores pasan.

## 7. Archivos modificados o creados

```text
athena_azr/h2_zero_certifier/authorization.py
athena_azr/h2_zero_certifier/pipeline.py
athena_azr/h2_zero_certifier/real_evidence.py
tests/h2_test_support.py
tests/test_h2_authorization.py
tests/test_h2_documented_inventory.py
tests/test_h2_pipeline_guard.py
tests/test_h2_real_evidence.py
docs/experimentos/experimento-006e8-c03b-l3-real-backend-inert-code-report.md
docs/experimentos/experimento-006e10-c03b-l3-inert-backend-corrections.md
```

## 8. Verificacion

```text
tests_run = 107
tests_passed = 106
real_integration_tests_skipped = 1
failures = 0
errors = 0
compileall = passed
real_flint_calls = 0
real_flint_imports_executed = 0
network_access = 0
real_contours = 0
zero_tables = 0
artifact_writes = 0
prohibited_real_api_matches = 0
probative_float_complex_atan2_matches = 0
```

La unica sentencia `import flint` permanece perezosa dentro de
`PythonFlintBackend.initialize` y no fue ejecutada.

## 9. Hashes principales de codigo

```text
athena_azr/h2_zero_certifier/authorization.py a6792a32be99772e0fa0adc22dffdb7f8c5868ee129da85ee3c1a8a7f1d8db13
athena_azr/h2_zero_certifier/pipeline.py 192f4ddd7e44a5cb7e51592c8c275a2f215c91818c0fb3f9a9a07e724866b3ac
athena_azr/h2_zero_certifier/real_evidence.py cbf417879b2cb492eaa29661b2ba9f5c57753f95d6dc01a3e51ed8d0bc09f835
tests/h2_test_support.py a48082b431654f51fd0bed16d89613f3cd33a1d95e6f1c402d02c570ce891a52
tests/test_h2_authorization.py c4f5334cb6ea02883640482faaf5eedb94c42c062c596f723043913ad018a3e5
tests/test_h2_documented_inventory.py 4334d7feff79ba6a826c076b163ce69270babcf77b6b8dbc1c7d5f0b10a68492
tests/test_h2_pipeline_guard.py b06de46de62139e9ba3e1d19d86ab5bf5189b5376d256f4c3ebd19de929d416b
tests/test_h2_real_evidence.py 9f477c0762ed06ae83ddb67b836c10518ff797f3fa26298907f2168f898f65c3
```

## 10. Limites y veredicto

006E10 no revisa la semantica real de python-flint, no implementa operaciones
matematicas del backend y no certifica ceros.

```text
006E10_CORRECTIONS = completed_pending_review
006E9_BLOCKING_FINDING_1 = corrected
006E9_BLOCKING_FINDING_2 = corrected
006E9_OPEN_CHAIN_FINDING = prepared_but_not_authorized
006E8_FINAL_ACCEPTANCE = pending_recheck
H2_CERTIFIED = false
006F_READINESS = false
006F_EXECUTION = forbidden
DOWNSTREAM_USE = forbidden
NOVELTY_CLAIM = false
```

El siguiente paso permitido es una revision documental y estructural de estas
correcciones. No se autoriza 006F ni calculo real.
