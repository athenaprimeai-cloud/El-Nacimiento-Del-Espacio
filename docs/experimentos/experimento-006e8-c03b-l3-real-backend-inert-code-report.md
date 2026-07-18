# Experimento 006E8: Implementacion Inerte del Backend Real L3

## 1. Estado y alcance

```text
experiment_id = G5B-006E8
status = corrected_by_006e14_pending_recheck
scope = inert_code_plus_synthetic_tests_only
006E7_SHA256 = 4f51a71107d16b037a589d948082669a0c993245e28154d8fb68c36603ef33e4
real_flint_import = forbidden_during_tests
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

006E8 implemento la arquitectura probatoria inerte definida por 006E7. La
fase uso exclusivamente runtimes falsos deterministas y pruebas sinteticas.
No se evaluo `Lambda_3` con FLINT, no se recorrio ningun contorno real y no se
calculo, aislo ni certifico ningun cero.

## 2. Desarrollo TDD

La implementacion se realizo con ciclos rojo-verde:

1. Las cinco suites nuevas fallaron inicialmente porque los modulos reales no
   existian.
2. Los primeros contratos revelaron y corrigieron una incompatibilidad de
   campos heredados en las dataclasses de evidencia.
3. Falsificadores posteriores detectaron la ausencia de validacion de rama
   logaritmica, inventario probatorio separado, endpoints inertes y rechazo de
   evidencia sintetica.
4. La auditoria final agrego falsificadores para el contrato completo del
   runtime, mezcla de precisiones y mezcla de procedencias.
5. Cada fallo fue observado antes de aplicar el cambio minimo correspondiente.

## 3. Superficie implementada

Se crearon:

```text
athena_azr/h2_zero_certifier/real_evidence.py
athena_azr/h2_zero_certifier/rigorous_ball_runtime.py
athena_azr/h2_zero_certifier/real_completed_l3.py
athena_azr/h2_zero_certifier/real_segment_enclosure.py
athena_azr/h2_zero_certifier/real_argument.py
tests/test_h2_real_evidence.py
tests/test_h2_rigorous_ball_runtime.py
tests/test_h2_real_completed_l3.py
tests/test_h2_real_segment_enclosure.py
tests/test_h2_real_argument.py
```

Se modificaron dentro del alcance autorizado:

```text
athena_azr/h2_zero_certifier/authorization.py
athena_azr/h2_zero_certifier/backend.py
athena_azr/h2_zero_certifier/python_flint_backend.py
athena_azr/h2_zero_certifier/pipeline.py
tests/test_h2_authorization.py
tests/test_h2_pipeline_guard.py
tests/test_h2_real_flint_guarded.py
```

## 4. Propiedades verificadas

```text
real_evidence_types = opaque_immutable_and_traceable
parent_identity = enforced
precision_consistency = enforced
provenance_consistency = enforced
recursive_parent_chain_binding = enforced_pending_independent_recheck
root_issuance_authenticity = enforced_pending_independent_recheck
native_L_route = native_entire_Dirichlet_L_contract
segment_route = whole_rectangular_complex_ball_contract
log_branch = explicitly_certified
pi_source = rigorous_runtime_contract
synthetic_probative_mixing = rejected
PythonFlintBackend = inert
```

La evidencia real registra backend, autorizacion, inventario de codigo,
precision y hashes parentales. Una fabrica no puede adoptar evidencia de otra
procedencia. Los incrementos y el winding rechazan mezclas de precision.

`PROBATIVE_RUNTIME_CODE_FILES` excluye el modulo flotante
`argument_principle.py`, que permanece disponible unicamente para pruebas
sinteticas historicas.

## 5. Verificacion final

Comando de suite:

```text
python -m unittest discover -s tests -p "test_h2_*.py" -v
```

Resultado:

```text
tests_run = 119
tests_passed = 118
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
```

Auditorias estaticas:

```text
lazy_flint_imports_present = 1
lazy_flint_import_location = python_flint_backend.py:22
prohibited_real_api_matches = 0
probative_float_complex_atan2_matches = 0
probative_argument_principle_imports = 0
```

La unica sentencia `import flint` permanece dentro de
`PythonFlintBackend.initialize` y no fue ejecutada por la suite.

## 6. Inmutabilidad documental

```text
006E5_SHA256 = 7c527e921cf41081d46800474b6c1026dba904d80a274617cb4004f7637f981e
006E6_SHA256 = dbfcda51f1edca9efc502ab9de9ab7cd470bdf3f3f70ff5ce758767fe7acdbca
006E7_SHA256 = 4f51a71107d16b037a589d948082669a0c993245e28154d8fb68c36603ef33e4
```

Los tres hashes coinciden con sus sellos previos.

## 7. Inventario SHA-256 de 006E8

### Runtime probatorio

```text
athena_azr/h2_zero_certifier/__init__.py 4f4535cd57ec9cd35ec8196f25e58beefe19a52356ec15f5271d3f911ebc12cc
athena_azr/h2_zero_certifier/authorization.py 80758c8ab8759926a1b302e511c8ffadce13b72d2c9a91cb9a25dcb997867802
athena_azr/h2_zero_certifier/backend.py a049fef71d44ec130724b6fabbedb4be0106ba8b6b1269afe06c11895179f7fa
athena_azr/h2_zero_certifier/ball_argument.py a92efc31d7a43ed9d25e307b34f3d1bb489a33e5d454af586b4d807426835954
athena_azr/h2_zero_certifier/argument_increment.py cc4de6621b7006fe61f43fe7209015cfc1869570387ade0633fe60cfc09e973c
athena_azr/h2_zero_certifier/boundary_certifier.py 58fe227d07c290ef63376ae0bdbfdceed3b69fcb1b3a7d35f130218f35a5cbb3
athena_azr/h2_zero_certifier/chi3_function.py 4d300c4b4d26085be37fe030c21db5c54537a4b27b7e129a03aba518e31adf68
athena_azr/h2_zero_certifier/completed_l3.py 6daf2e486dcac2226171cc0d169abdc3414d83c9dbd9802fb24b4754c7513ad7
athena_azr/h2_zero_certifier/config.py 7b799efbeb198cad71cd77a8981909c4f9fb2ed495a053dbb94da5efcd637d44
athena_azr/h2_zero_certifier/contour.py bae15a7bb1d874cceb8e2869011e6f4063eb81650cad2937be2c8b5d551ee681
athena_azr/h2_zero_certifier/l3_argument_count.py 42c9a7bc63ca865db32be600b29041f2897e694e0a05f3e8f1d86149725679ba
athena_azr/h2_zero_certifier/l3_certifier.py 9fe62ab42b1ec80f96ad18869f46fecf8cdfc5ff3c86e11cdc9c072591c0c9b8
athena_azr/h2_zero_certifier/l3_isolator.py 6ce3f330d60721592725eba981e2d57fe9bda035ffd87daee209c453984bbca6
athena_azr/h2_zero_certifier/models.py bf05509d8637d25eddfe77e6a1ce0a148131da2f3f660659476c5d54287a5989
athena_azr/h2_zero_certifier/pipeline.py 3b35bc44312609cedbdd5628d6c8846b7e9280d6eb1baf5432c1c91b267e2eb2
athena_azr/h2_zero_certifier/python_flint_backend.py e273c8f2c568a94159036b23583ec1b7b47768b2bbaf96ec8a9e1d6c256d9100
athena_azr/h2_zero_certifier/serialization.py 1ff9d9db81d93b6712453b67fac421782552a292a1589661be27c4cd09dd50df
athena_azr/h2_zero_certifier/validation.py f555b5a9c19a6940234cfcaf6049a3ae62164e1295726ef4e5eec477576e080a
athena_azr/h2_zero_certifier/winding_certifier.py db66e4466a7f7a9129ab8c40662b6add898cf6cf13993f108875ce2791777c1c
athena_azr/h2_zero_certifier/zeta_certifier.py 4999c79342880b5cdba610fcd7b284c3a236c6f0000d24e7fb40ced9bdc25932
scripts/run_h2_zero_certification.py 3e517c2424fafc91f8f3a8a25ff7a4f989f72d75ac9e32b9e0da920d78a88212
athena_azr/h2_zero_certifier/real_evidence.py 36b22255f107a987bcd5af25ac20b7811c5fa0f21f673ae81df9ca16572e7e32
athena_azr/h2_zero_certifier/rigorous_ball_runtime.py 4a0f07357ffd506a6e46f03001d4911376309b5e15820cb2d684833a0cfc9ce5
athena_azr/h2_zero_certifier/real_completed_l3.py 848291ca3391085db7588121559a03ce8fd18bd9950e33d853317eff6e74d2ca
athena_azr/h2_zero_certifier/real_segment_enclosure.py 5e1e1d46e13e280fbb3a418c1c3f846bd17d899c5ad50654266adaa5d902bb72
athena_azr/h2_zero_certifier/real_argument.py 1cc4db86ede06bdffae6d5168d43ea22d28a20192d69b2f6cbda52485e1835e0
```

### Pruebas nuevas o ajustadas

```text
tests/h2_test_support.py             a48082b431654f51fd0bed16d89613f3cd33a1d95e6f1c402d02c570ce891a52
tests/test_h2_authorization.py        c4f5334cb6ea02883640482faaf5eedb94c42c062c596f723043913ad018a3e5
tests/test_h2_documented_inventory.py 4334d7feff79ba6a826c076b163ce69270babcf77b6b8dbc1c7d5f0b10a68492
tests/test_h2_pipeline_guard.py       80806d9f87873fa4e478b939b399f647281afcb102cb9b8dc3a9e7205fb709fa
test_h2_real_argument.py             e3af3d656bfd0e339fb07728f8049b1ca65d822deff9fb3a90a50f22088d549d
test_h2_real_completed_l3.py         ae478a2b3557cb010aa45800e6cc5e70b4b43a210bbd542b6e2576d07b41738a
tests/test_h2_real_evidence.py        755f61c7dd8129484fa1130debbb06b400063f4d6b5f026abde7b40b3cca868d
tests/test_h2_root_issuance.py        0183206673e8b5d136690de09762de16f091d66eb0d212f6a44ffc2916edc0c2
test_h2_real_flint_guarded.py        81250d9b2a8b1b9d19a8c80355976595b8e4559bb5b5fe03203cd7be067d87b6
test_h2_real_segment_enclosure.py    c22f36919081f2aa0f5dbb4ab591eda176a76b6f0488b29ca100cd342154367e
test_h2_rigorous_ball_runtime.py     b4d1534df3480bb4b5f15bec50ea211938cc609b673e61c460093e1d2d094d46
```

## 8. Limites que permanecen abiertos

### Correccion 006E10

La revision independiente 006E9 detecto dos bloqueos y una condicion abierta
de cadena. 006E10 incorporo:

1. procedencia probatoria emitida unicamente desde una autorizacion validada;
2. inventario completo de los 22 archivos de runtime probatorio;
3. campos obligatorios para los sellos 006E7, 006E8, 006E9 y 006E10 en una
   futura autorizacion 006F.

Estas correcciones no autorizan ejecucion real y requieren una nueva revision
antes del congelamiento final de 006E8.

### Correccion 006E12

El rechequeo 006E11 detecto que una fabrica validada aun podia adoptar un
padre no probatorio que copiara backend, autorizacion e inventario de runtime.
006E12 agrego validacion recursiva de la cadena parental completa:

```text
parent.probative = true
parent.backend_id = validated backend_id
parent.authorization_digest = validated authorization_digest
parent.runtime_code_digest = validated runtime_code_digest
parent.review_chain_digest = validated review_chain_digest
parent.digest = digest recomputado desde contenido y ascendencia
```

La misma regla se aplica a segmentos, semiplanos, incrementos y winding. El
pipeline vuelve a recorrer la genealogia antes de aceptar evidencia probatoria.
Esta correccion queda pendiente de revision independiente y no congela 006E8.

### Correccion 006E14

006E13 demostro que una raiz sintetica podia promoverse mediante
`dataclasses.replace`, copia de procedencia y recalculo de un digest publico.
006E14 separo consistencia de contenido y autenticidad de emision:

```text
factory_capability = unique per factory
construction_permit = context-local and ephemeral
dataclasses.replace = rejected outside active factory issuance
probative_issuance_registry = identity-bound weak registry
pipeline = genealogy + digest + provenance + registered issuance
```

Una clonacion sin constructor puede copiar todos los campos y recomputar el
SHA-256, pero no puede crear el registro de identidad emitido por una fabrica
validada. La correccion queda pendiente de revision independiente y no congela
006E8, 006E10 ni 006E12.

006E8 no demuestra que la API real de python-flint satisfaga los contratos
fijados. En particular, siguen sin verificarse:

1. la construccion real de bolas complejas con redondeo exterior;
2. la evaluacion nativa entera de `L(s, chi_3)` sobre bolas no degeneradas;
3. la evaluacion inclusiva de `Lambda_3` sobre cajas completas;
4. la certificacion real de semiplanos y ramas del logaritmo complejo;
5. la acumulacion rigurosa de argumentos sobre contornos reales;
6. el aislamiento y conteo completo de ceros hasta altura 500.

Por tanto:

```text
real_backend_mathematics = not_implemented
real_backend_semantics = not_verified
H2_certified = false
006F_readiness = false
006F_execution = forbidden
downstream_use = forbidden
```

## 9. Veredicto de fase

```text
006E8_STRUCTURAL_IMPLEMENTATION = completed
006E8_SYNTHETIC_VERIFICATION = passed
006E8_ACCEPTANCE = corrected_by_006e14_pending_recheck
REAL_FLINT_EXECUTION = forbidden
ZERO_CERTIFICATION = forbidden
H2_CERTIFIED = false
006F_READINESS = false
NOVELTY_CLAIM = false
```

006E8 construye y verifica la arquitectura inerte del backend probatorio. No
autoriza completar el adaptador matematico real, ejecutar FLINT ni avanzar a
006F.
