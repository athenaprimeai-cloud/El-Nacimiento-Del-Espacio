# Experimento 006E11: Rechequeo Independiente de las Correcciones 006E10

## 1. Estado y alcance

```text
experiment_id = G5B-006E11
status = independent_recheck_completed_with_blocking_finding
target = review_006E10_corrections
code_authorization = false
execution_authorization = false
real_flint_execution = forbidden
real_contour_execution = forbidden
zero_certification = forbidden
zero_tables = not_generated
artifacts = none
H2_certified = false
006F = blocked
novelty_claim = false
```

006E11 inspecciono codigo, documentos, pruebas y guardias sin modificar la
implementacion. Se realizaron comprobaciones adversariales con datos
temporales, pero no se importo FLINT ni se ejecuto matematica real.

## 2. Sellos revisados

```text
006E7_SHA256 = 4f51a71107d16b037a589d948082669a0c993245e28154d8fb68c36603ef33e4
006E8_CORRECTED_SHA256 = 8608a503203ad550dfa7800ab99e76e0a44ebae05d68b60842a9850d4f4c1a63
006E9_SHA256 = 905eed6c485c6b67b54cc0ebaf197784ec3da7b81bdddb45d468a728fa927cef
006E10_SHA256 = 911a1dc2a5b21d20093f60907bda6e3131b9c64c798240b9e3ce355246aeaefb
```

El estado de 006E8 es `corrected_by_006e10_pending_recheck`; no esta
congelado ni aceptado como final.

## 3. Resultado 1: procedencia probatoria

### Hallazgo bloqueante - adopcion de padre no probatorio

Referencias:

```text
real_evidence.py:179-185
real_evidence.py:232-247
pipeline.py:38-43
```

La correccion impide que una fabrica no validada se auto-promueva directamente
y sella los atributos de la evidencia raiz. Sin embargo, `_require_owned`
solo compara:

```text
backend_id
authorization_digest
runtime_code_digest
```

No exige que el padre sea probatorio ni compara `review_chain_digest`.

El rechequeo construyo esta cadena:

1. una fabrica validada emitio una evidencia raiz para obtener sus tres
   identificadores publicos;
2. una fabrica directa no validada copio esos identificadores y creo un
   `RealSegmentImageEvidence` con `probative = false`;
3. la fabrica validada adopto ese segmento al crear un semiplano;
4. el hijo resulto `probative = true` y `require_probative_evidence` lo acepto.

Salida observada:

```text
untrusted_parent_probative False
adopted_child_probative True
parent_review_chain 0000000000000000000000000000000000000000000000000000000000000000
child_review_chain 9fc0c398bce5e4145bb9f682872e693f52035951b9ee4b2f1077f75078bff2e7
pipeline_accepted True
```

Por tanto:

```text
root_evidence_binding = passed
parent_chain_binding = failed
006E9_BLOCKING_FINDING_1 = partially_corrected
```

La proxima correccion debe exigir en cada adopcion parental:

```text
parent.probative is true
parent.review_chain_digest == validated review_chain_digest
parent authorization/runtime/backend identity exacta
```

La misma regla debe aplicarse a semiplanos, incrementos y winding, y el
pipeline debe validar recursivamente la cadena o recibir un certificado
cerrado equivalente.

## 4. Resultado 2: inventario SHA-256

La seccion `Runtime probatorio` de 006E8 fue comparada contra
`PROBATIVE_RUNTIME_CODE_FILES`.

```text
expected_count = 22
documented_count = 22
missing = []
extra = []
stale = []
```

`argument_principle.py` permanece fuera del inventario probatorio.

```text
006E9_BLOCKING_FINDING_2 = corrected_verified
```

## 5. Resultado 3: cadena futura 006F

El esquema exige exactamente los campos:

```text
plan_006e7_sha256
report_006e8_sha256
review_006e9_sha256
corrections_006e10_sha256
```

El pipeline calcula los valores desde los documentos locales mediante
`compute_review_document_hashes` y los entrega al parser.

Controles adversariales:

```text
missing_review_006e9 = rejected: authorization schema mismatch
mismatched_006e10 = rejected: corrections_006e10_sha256 mismatch
```

No existe una autorizacion G5B-006F en el espacio de trabajo. La presencia del
protocolo sellado C05 no abre esta puerta.

```text
006E9_OPEN_CHAIN_FINDING = corrected_as_specified
006F_AUTHORIZATION = absent
006F_EXECUTION = forbidden
```

Una futura cadena final debera decidir ademas si incorpora el sello de la
revision que acepte definitivamente estas correcciones.

## 6. Verificacion reproducida

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

La suite verde no detecta actualmente la adopcion de padres no probatorios;
el hallazgo proviene de una prueba adversarial independiente ejecutada sin
modificar el codigo.

## 7. Veredicto

```text
006E11_RECHECK = completed
006E10_CORRECTION_1 = rejected_pending_parent_chain_binding
006E10_CORRECTION_2 = accepted_verified
006E10_CORRECTION_3 = accepted_as_specified_not_authorized
BLOCKING_FINDINGS = 1
006E10_FINAL_ACCEPTANCE = rejected_pending_correction
006E8_FINAL_ACCEPTANCE = rejected_pending_correction
006E8_FORMAL_FREEZE = not_approved
006E10_FORMAL_FREEZE = not_approved
H2_CERTIFIED = false
006F_READINESS = false
006F_EXECUTION = forbidden
DOWNSTREAM_USE = forbidden
NOVELTY_CLAIM = false
```

006E10 mejoro la procedencia raiz, completo el inventario y encadeno los
sellos requeridos. No obstante, la cadena probatoria aun puede blanquear un
padre no validado al crear un hijo validado. Esa rendija debe cerrarse antes
de aceptar o congelar 006E8 y 006E10.
