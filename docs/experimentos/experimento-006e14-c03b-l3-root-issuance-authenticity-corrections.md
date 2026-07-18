# Experimento 006E14: Correccion de Autenticidad de Emision Raiz L3

## 1. Estado y alcance

```text
experiment_id = G5B-006E14
status = corrections_completed_pending_independent_review
target = fix_006E13_blocking_finding
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

006E14 corrige exclusivamente la autenticidad de emision de evidencia
probatoria. No implementa matematica real, no importa FLINT y no calcula,
aisla, cuenta ni certifica ceros.

## 2. Hallazgo heredado de 006E13

006E13 comprobo que la genealogia y los digests podian ser coherentes sin que
la raiz hubiera sido emitida por una fabrica validada. El ataque combinaba:

```text
global shared _EVIDENCE_CAPABILITY
dataclasses.replace preserving capability
publicly recomputable SHA-256 digest
copied backend/auth/runtime/review-chain fields
```

La secuencia anterior terminaba con:

```text
synthetic_root_probative False
forged_root_probative True
trusted_factory_adopted True
pipeline_root_accepted True
pipeline_child_accepted True
capability_preserved True
```

## 3. Desarrollo TDD

Se agregaron siete falsificadores antes de modificar produccion:

```text
RED: dataclasses.replace promotes synthetic root to probative
RED: forged root copies provenance and recomputes digest
RED: validated factory adopts unregistered forged root
RED: pipeline accepts forged root directly
RED: pipeline accepts child descending from forged root
RED: synthetic and validated factories share capability
RED: public digest recomputation creates accepted issuance
```

Los siete fallaron inicialmente por aceptacion indebida. Despues de la
correccion, todos pasan como rechazos.

## 4. Separacion de conceptos

006E14 fija explicitamente:

```text
content_consistency != trusted_issuance
```

La consistencia sigue verificando procedencia, contenido, digest y
genealogia. La autenticidad de emision agrega una condicion independiente:
el mismo objeto debe constar en un registro de emisiones creado por una
fabrica validada.

## 5. Correccion implementada

### 5.1 Capacidad unica por fabrica

La capacidad global compartida fue eliminada. Cada `RealEvidenceFactory`
recibe un objeto de capacidad unico. Una fabrica sintetica y una validada no
comparten identidad interna.

### 5.2 Permiso efimero de construccion

La construccion usa un `ContextVar` que solo esta activo durante
`RealEvidenceFactory._construct`. El permiso liga:

```text
factory capability
probative status
backend_id
authorization_digest
runtime_code_digest
review_chain_digest
```

`_EvidenceBase.__post_init__` rechaza cualquier creacion fuera de ese
contexto o incompatible con el permiso. Como `_capability` tiene
`init = false`, `dataclasses.replace` no puede conservar una credencial valida
y falla antes de producir el objeto reemplazado.

### 5.3 Registro cerrado por identidad

Las emisiones probatorias se registran despues de la construccion en un
registro privado que conserva:

```text
weak reference to the exact object
factory capability identity
sealed provenance tuple
digest at issuance
```

El registro usa identidad de objeto, no igualdad estructural. Una clonacion
sin constructor puede copiar todos los campos y recalcular el SHA-256, pero
su identidad no esta registrada.

Las referencias debiles eliminan registros cuando la evidencia deja de
existir y el callback comprueba la identidad de la referencia antes de borrar.

### 5.4 Defensa en profundidad

`_require_evidence_chain` exige el registro de emision para cada nodo
probatorio antes de validar digest y ascendencia. Por tanto, la fabrica y el
pipeline verifican:

```text
registered issuance identity
factory capability identity
sealed provenance
issuance-time digest
current recomputed digest
recursive parental genealogy
```

## 6. Resultado adversarial

La reproduccion posterior a la correccion produce:

```text
synthetic_root_probative False
forged_root_creation REJECTED
trusted_factory_adoption REJECTED
pipeline_root_accepted False
pipeline_child_accepted False
capability_shared False
```

Una clonacion directa mediante `object.__new__` tambien es rechazada aunque
copie la capacidad, la procedencia y un digest recomputado correcto, porque no
existe una emision registrada para su identidad.

## 7. Archivos modificados

Runtime probatorio:

```text
athena_azr/h2_zero_certifier/real_evidence.py 36b22255f107a987bcd5af25ac20b7811c5fa0f21f673ae81df9ca16572e7e32
```

Pruebas:

```text
tests/test_h2_root_issuance.py 0183206673e8b5d136690de09762de16f091d66eb0d212f6a44ffc2916edc0c2
tests/test_h2_real_evidence.py 755f61c7dd8129484fa1130debbb06b400063f4d6b5f026abde7b40b3cca868d
tests/test_h2_pipeline_guard.py 80806d9f87873fa4e478b939b399f647281afcb102cb9b8dc3a9e7205fb709fa
```

Inventario historico actualizado:

```text
docs/experimentos/experimento-006e8-c03b-l3-real-backend-inert-code-report.md
SHA256 = 4ce8e9a4cb597eb14c19db45a7df7f1d11b36199077ef270ea7285b06f28f16b
status = corrected_by_006e14_pending_recheck
```

## 8. Verificacion

```text
tests_run = 119
tests_passed = 118
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
artifact_writes_by_006E14 = 0
lazy_flint_imports_present = 1
lazy_flint_import_location = python_flint_backend.py:22
prohibited_real_api_matches = 0
probative_float_complex_atan2_matches = 0
probative_argument_principle_imports = 0
shared_global_evidence_capability_matches = 0
```

Sellos antecedentes:

```text
006E13_SHA256 = ce9c57b5d25c07e15599b0b2fad82bc4f886fcd36222aaea0570bd57d3ae98fa
```

## 9. Limite del modelo de amenaza

Esta correccion protege las rutas publicas y estructurales frente a
`dataclasses.replace`, copia de campos, recomputacion publica de digests,
clonacion sin constructor y mezcla de genealogias. No presenta el proceso de
Python como una frontera criptografica frente a codigo que deliberadamente
use introspeccion para invocar o alterar privados internos del mismo modulo.

Una revision independiente debe evaluar si este limite coincide con el modelo
de amenaza preregistrado antes de aceptar la correccion.

## 10. Veredicto de fase

```text
006E14_CORRECTION = completed_pending_independent_review
006E13_BLOCKING_FINDING = corrected_claimed
006E12_FINAL_ACCEPTANCE = pending_recheck
006E10_FINAL_ACCEPTANCE = pending_recheck
006E8_FINAL_ACCEPTANCE = pending_recheck
006E8_FORMAL_FREEZE = not_approved
006E10_FORMAL_FREEZE = not_approved
006E12_FORMAL_FREEZE = not_approved
H2_CERTIFIED = false
006F_READINESS = false
006F_EXECUTION = forbidden
DOWNSTREAM_USE = forbidden
NOVELTY_CLAIM = false
```

006E14 afirma una correccion implementada, no su aceptacion independiente.
Ningun congelamiento ni ejecucion real queda autorizado por esta fase.
