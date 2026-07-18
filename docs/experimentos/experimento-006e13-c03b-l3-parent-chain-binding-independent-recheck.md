# Experimento 006E13: Rechequeo Independiente de Cadena Parental L3

## 1. Estado y alcance

```text
experiment_id = G5B-006E13
status = independent_recheck_completed_with_blocking_finding
target = review_parent_chain_binding_correction
code_authorization = false
execution_authorization = false
real_flint_execution = forbidden
real_contour_execution = forbidden
zero_certification = forbidden
zero_tables = not_generated
artifacts = none
network = forbidden
H2_certified = false
006F = blocked
novelty_claim = false
```

006E13 reviso 006E12 sin modificar codigo. Los ataques se ejecutaron con
objetos efimeros y no generaron tablas, artefactos ni resultados matematicos.

## 2. Sellos e inmutabilidad

Sellos observados al inicio:

```text
006E8_SHA256 = d8e1243deb65cceae907c37eb313b43f36ad350dae1dd9a71db3cbeda767d482
006E9_SHA256 = 905eed6c485c6b67b54cc0ebaf197784ec3da7b81bdddb45d468a728fa927cef
006E10_SHA256 = 911a1dc2a5b21d20093f60907bda6e3131b9c64c798240b9e3ce355246aeaefb
006E11_SHA256 = f02eb2c59946c333b4cce6f409e0bfeee5258753c3edf0db603a5ef8d7618d75
006E12_SHA256 = 0f9b21b21e42662afea48dc00cd9d053f4175d7f25b0be06a37bc7374bb298f7
```

Los 22 archivos del runtime probatorio conservaron exactamente los hashes
registrados al comienzo de 006E13:

```text
expected_count = 22
current_count = 22
changed = {}
code_changes = 0
```

## 3. Checklist obligatorio

Los diez controles solicitados fueron ejecutados de forma independiente:

```text
01 non-probative parent whitening = rejected
02 mixed review_chain_digest = rejected
03 copied backend/auth/runtime with probative false = rejected
04 altered evidence digest = rejected
05 bad increment inside valid winding = rejected
06 pipeline recursive genealogy traversal = rejected
07 parental cycle = rejected
08 root declaring parent hashes = rejected
09 segment without complete rectangular coverage = rejected
10 freeze remains guarded by successful recheck = passed
```

Resultados observados:

```text
01 PASS_REJECTED: parent evidence has incompatible probative status
02 PASS_REJECTED: parent evidence has different sealed provenance
03 PASS_REJECTED: parent evidence has incompatible probative status
04 PASS_REJECTED: evidence digest does not match its content
05 PASS_REJECTED: parent evidence has incompatible probative status
06 PASS_REJECTED: parent evidence has incompatible probative status
07 PASS_REJECTED: evidence ancestry contains a cycle
08 PASS_REJECTED: root evidence cannot declare parents
09 PASS_REJECTED: segment evidence is not a whole-segment enclosure
10 PASS_GUARDED
checks = 10
passed = 10
failed = 0
```

El control 06 uso un hijo con digest recalculado y coherente. Por tanto, el
rechazo demuestra que `require_probative_evidence` alcanzo realmente al
ancestro no probatorio y no se limito a detectar un digest superior obsoleto.

El control 07 neutralizo temporalmente, solo dentro del proceso adversarial,
la comprobacion previa del digest para alcanzar el detector de ciclos. El
resultado explicito fue `evidence ancestry contains a cycle`.

## 4. Hallazgo bloqueante adicional

### Promocion de raiz sintetica con capacidad compartida

Aunque los diez controles pasan, una raiz sintetica puede promoverse a
probatoria sin una emision validada real:

1. una fabrica validada emite una raiz legitima, revelando los digests de
   backend, autorizacion, runtime y cadena de revision;
2. una fabrica directa no validada crea una raiz sintetica;
3. `dataclasses.replace` conserva `_capability`, porque fabricas validadas y
   sinteticas usan el mismo objeto global `_EVIDENCE_CAPABILITY`;
4. el atacante cambia `probative` a `true`, copia `review_chain_digest` y
   recalcula el digest desde los campos publicos;
5. la fabrica validada adopta la raiz promovida y el pipeline acepta tanto la
   raiz como su hijo.

Salida observada:

```text
synthetic_root_probative False
forged_root_probative True
trusted_factory_adopted True
child_probative True
pipeline_root_accepted True
pipeline_child_accepted True
capability_preserved True
```

Este ataque no rompe la coherencia de la genealogia. Construye una genealogia
internamente coherente cuya raiz no fue emitida por una autorizacion validada.
La validacion actual autentica campos y hashes, pero no autentica el acto de
emision.

## 5. Causa tecnica

```text
_EVIDENCE_CAPABILITY = one shared object for all factories
unvalidated factory evidence = carries the same internal capability
dataclasses.replace = preserves that capability
digest = unkeyed sha256 reproducible from public evidence fields
pipeline = validates consistency, not trusted issuance
```

El prefijo `_` de `_expected_digest` y `_capability` es una convencion de
Python, no una frontera de seguridad. El mismo digest tambien puede
reproducirse externamente sin importar la funcion privada.

## 6. Condicion para una correccion posterior

Una nueva correccion debe separar autenticidad de emision y coherencia de
contenido. Como minimo debe impedir que una evidencia creada por una fabrica
no validada se convierta en probatoria mediante copia de campos y recalculo de
SHA-256.

Opciones que requieren diseno previo:

```text
1. credencial de emision probatoria distinta de la capacidad sintetica;
2. registro cerrado de objetos o digests emitidos por una fabrica validada;
3. autenticador ligado al contenido que el llamador no pueda regenerar;
4. separacion explicita del modelo de amenaza:
   accidental mixing versus adversarial in-process mutation.
```

Una solucion basada solamente en otro campo publico o en otro SHA-256 sin
clave no cierra este hallazgo.

## 7. Verificacion general reproducida

```text
tests_run = 112
tests_passed = 111
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
lazy_flint_imports_present = 1
lazy_flint_import_location = python_flint_backend.py:22
prohibited_real_api_matches = 0
probative_float_complex_atan2_matches = 0
probative_argument_principle_imports = 0
```

La suite verde verifica los controles registrados, pero todavia no contiene
un falsificador permanente para la promocion de raiz sintetica descrita en la
seccion 4.

## 8. Veredicto

```text
006E13_RECHECK = completed
MANDATORY_CHECKLIST = 10_of_10_passed
ADDITIONAL_BLOCKING_FINDINGS = 1
006E12_PARENT_CHAIN_BINDING = passed_for_unmodified_evidence
006E12_ROOT_ISSUANCE_AUTHENTICITY = failed
006E12_FINAL_ACCEPTANCE = rejected_pending_correction
006E8_FINAL_ACCEPTANCE = rejected_pending_correction
006E10_FINAL_ACCEPTANCE = rejected_pending_correction
006E8_FORMAL_FREEZE = not_approved
006E10_FORMAL_FREEZE = not_approved
H2_CERTIFIED = false
006F_READINESS = false
006F_EXECUTION = forbidden
DOWNSTREAM_USE = forbidden
NOVELTY_CLAIM = false
```

006E12 cerro la rendija parental identificada por 006E11, pero el origen de
una raiz probatoria aun puede falsificarse dentro del proceso. Por ello 006E8
y 006E10 no son congelables y 006F permanece bloqueado.
