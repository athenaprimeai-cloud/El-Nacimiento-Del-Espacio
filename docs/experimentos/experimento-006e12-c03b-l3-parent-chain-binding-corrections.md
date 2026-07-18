# Experimento 006E12: Correccion de Vinculo de Cadena Parental L3

## 1. Estado y alcance

```text
experiment_id = G5B-006E12
status = corrections_completed_pending_independent_review
target = fix_006E11_blocking_finding
code_authorization = structural_only
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

006E12 corrige exclusivamente la adopcion de evidencia parental probatoria.
No completa el backend matematico real, no importa FLINT y no calcula,
aisla, cuenta ni certifica ceros.

## 2. Hallazgo heredado de 006E11

006E11 demostro que una fabrica validada podia adoptar un padre creado por
una fabrica no validada si este copiaba tres identificadores publicos:

```text
backend_id
authorization_digest
runtime_code_digest
```

La comprobacion no exigia `parent.probative = true`, no comparaba
`review_chain_digest` y el pipeline solo verificaba el hijo superior. La
secuencia adversarial observada fue:

```text
untrusted_parent_probative = false
adopted_child_probative = true
pipeline_accepted = true
```

## 3. Desarrollo TDD

Antes de modificar la implementacion se agregaron cinco falsificadores:

```text
RED: validated factory adopts non-probative segment parent
RED: validated factory adopts parent with wrong review_chain_digest
RED: validated factory adopts matching-id non-probative half-plane
RED: winding adopts one bad increment among valid increments
RED: pipeline receives a probative child with non-probative ancestry
```

Los cinco fallaron inicialmente porque la adopcion fue aceptada. Despues de
la correccion, los cinco pasan como rechazos cerrados.

## 4. Correccion implementada

Se agrego una validacion recursiva de evidencia que exige, para cada nodo de
la genealogia:

```text
evidence.probative = expected probative status
evidence.backend_id = sealed backend_id
evidence.authorization_digest = sealed authorization_digest
evidence.runtime_code_digest = sealed runtime_code_digest
evidence.review_chain_digest = sealed review_chain_digest
evidence.digest = sha256 recomputado desde contenido y padres
parent_evidence_hashes = digests exactos de los padres incorporados
```

La validacion recorre:

```text
RealSegmentImageEvidence
RealHalfPlaneEvidence -> segment
RealArgumentIncrementEvidence -> half_plane -> segment
RealWindingEvidence -> every increment -> half_plane -> segment
```

Tambien rechaza ciclos, raices con padres declarados y segmentos que no
certifiquen cobertura rectangular completa.

La fabrica validada obtiene la identidad esperada desde su procedencia
privada sellada, no desde atributos publicos mutables. Las fabricas sinteticas
continuan disponibles para pruebas, pero solo pueden adoptar una genealogia
sintetica completa con `probative = false` y cadena de revision nula.

## 5. Defensa del pipeline

`require_probative_evidence` ya no acepta un objeto por observar solamente el
booleano del hijo. Antes de admitirlo recorre toda la ascendencia, recomputa
los digests y exige una unica procedencia probatoria exacta.

La reproduccion directa del ataque de 006E11 ahora produce:

```text
untrusted_parent_probative False
adoption_rejected InvalidRealEvidence parent evidence has incompatible probative status
```

No se crea el hijo blanqueado y el pipeline conserva una segunda barrera para
objetos alterados despues de su creacion.

## 6. Archivos modificados

Runtime probatorio:

```text
athena_azr/h2_zero_certifier/real_evidence.py 516432846faa9dc5bf1081aff0365079f4bcfdfa2a82c422799faf9783c2cc1a
athena_azr/h2_zero_certifier/pipeline.py 5cca6b38530d551ed5764479927e2cf169134fe5d6e8bd425c096073d7797f1d
```

Pruebas:

```text
tests/test_h2_real_evidence.py f98da7f7f7655ea648a72d95940ecfe0b885df9e22ffaf1e82e39c7a9ad409c9
tests/test_h2_pipeline_guard.py 189e0e13d77bc065b258c30ccc1d565ea9f6aceda418ebe03edb8ea0c68bad73
```

Documento historico actualizado para reflejar el inventario vigente:

```text
docs/experimentos/experimento-006e8-c03b-l3-real-backend-inert-code-report.md
SHA256 = d8e1243deb65cceae907c37eb313b43f36ad350dae1dd9a71db3cbeda767d482
status = corrected_by_006e12_pending_recheck
```

## 7. Verificacion

Suite estructural completa:

```text
tests_run = 112
tests_passed = 111
real_integration_tests_skipped = 1
failures = 0
errors = 0
compileall = passed
```

Auditoria negativa:

```text
real_flint_calls = 0
real_flint_imports_executed = 0
network_access = 0
real_contours = 0
zero_tables = 0
artifact_writes = 0
lazy_flint_imports_present = 1
lazy_flint_import_location = python_flint_backend.py:22
prohibited_real_api_matches = 0
probative_float_complex_atan2_matches = 0
probative_argument_principle_imports = 0
```

Sellos antecedentes consultados:

```text
006E7_SHA256 = 4f51a71107d16b037a589d948082669a0c993245e28154d8fb68c36603ef33e4
006E9_SHA256 = 905eed6c485c6b67b54cc0ebaf197784ec3da7b81bdddb45d468a728fa927cef
006E10_SHA256 = 911a1dc2a5b21d20093f60907bda6e3131b9c64c798240b9e3ce355246aeaefb
006E11_SHA256 = f02eb2c59946c333b4cce6f409e0bfeee5258753c3edf0db603a5ef8d7618d75
```

## 8. Limites y siguiente revision

Esta fase afirma una correccion implementada, no su aceptacion independiente:

```text
006E12_CORRECTION = completed_pending_independent_review
006E11_BLOCKING_FINDING = corrected_claimed
006E8_FINAL_ACCEPTANCE = pending_recheck
006E10_FINAL_ACCEPTANCE = pending_recheck
006E8_FORMAL_FREEZE = not_approved
006E10_FORMAL_FREEZE = not_approved
H2_CERTIFIED = false
006F_READINESS = false
006F_EXECUTION = forbidden
DOWNSTREAM_USE = forbidden
NOVELTY_CLAIM = false
```

Una revision posterior debe intentar nuevamente blanquear padres no
probatorios, mezclar cadenas de revision, alterar digests y esconder un unico
incremento invalido dentro de un winding. Solo esa revision puede aceptar o
rechazar definitivamente la correccion 006E12.
