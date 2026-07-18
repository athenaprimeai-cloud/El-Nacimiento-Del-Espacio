# Experimento 006D: autorizacion de construccion estructural H2

## 1. Estado

```text
experiment_id = G5B-006D
status = authorized_structural_code_phase
code = authorized_structural_only
structural_tests = authorized
real_zero_certification = forbidden
real_flint_math = forbidden
zero_tables = not_generated
artifacts = none
network = forbidden
novelty_claim = false
C05_RERUN = forbidden
C35 = frozen
C15 = frozen
```

006D autoriza en una sola fase la construccion del instrumento estructural y la
ejecucion de sus pruebas sinteticas. No autoriza certificar ceros reales.

## 2. Base congelada

```text
005F_SHA256 = 148816b8375d42e4a19cf67d0c14e53e54a07f0a518754fc0a1b6d1e35042216
006A_SHA256 = 546f502b2907a9e125df6b07ffff5a07aa7f1147765196ab3e4523097d2a67d8
006B_SHA256 = 4f110d0926067e9e1eb44cbbfe78ee1acc93f85f526176c81d98446eafd492cb
006C_SHA256 = cbf9e6ef8d39032cefdd467fab274d6cd7e1569978292ecfd1fb9da70768db3f
```

Los cuatro documentos deben permanecer byte por byte inmutables.

## 3. Acciones autorizadas

1. crear `athena_azr/h2_zero_certifier/`;
2. crear `requirements-h2-certifier.txt` sin instalar dependencias;
3. crear una CLI bloqueada en `scripts/run_h2_zero_certification.py`;
4. crear pruebas estructurales y fixtures sinteticos;
5. usar backends falsos y funciones de raices conocidas;
6. probar serializacion solo en directorios temporales;
7. probar que la CLI falla sin autorizacion 006F;
8. probar que FLINT no se importa antes de una autorizacion valida;
9. ejecutar exclusivamente la suite estructural 006D;
10. generar un informe documental 006D con hashes del codigo construido.

## 4. Acciones prohibidas

1. calcular ceros reales de `zeta` o `L(s,chi_3)`;
2. llamar `acb.zeta_zero`, `chi.hardy_z`, `chi.l_function` o `acb.integral`;
3. instalar, importar o inicializar FLINT para calculo real;
4. usar red o descargar Odlyzko, LMFDB u otras fuentes;
5. escribir tablas finales CSV/JSON;
6. escribir dentro de `artifacts/`;
7. modificar C00, C03, C03-B, C05 o sus artefactos;
8. abrir C35 o C15;
9. declarar H2 certificado;
10. crear una autorizacion 006F.

## 5. Regla de aislamiento

```text
006D construye la jaula.
006F, si se autoriza despues, introduce el calculo real.
```

El adaptador `python_flint_backend.py` debe ser perezoso. Importar el paquete no
puede importar `flint`. Las operaciones reales deben permanecer bloqueadas por
la ausencia de una autorizacion 006F valida.

## 6. Pruebas permitidas

Las pruebas 006D pueden verificar:

1. modelos, configuracion y validadores;
2. guardias de autorizacion y hashes;
3. aislamiento y conteo usando datos sinteticos;
4. principio del argumento sobre funciones sinteticas;
5. serializacion canonica en temporales;
6. ausencia de escrituras en `artifacts/`;
7. ausencia de importaciones y llamadas reales de FLINT.

No se ejecutara la suite matematica historica ni pruebas de integracion real.

## 7. Estado posterior esperado

```text
si structural_tests = passed y isolation_audit = passed:
    006D = structurally_built_pending_006E_review
    H2 = protocol_defined_not_executed
    real_zero_certification = forbidden

en otro caso:
    006D = incomplete_or_failed
    006E = blocked
```

Solo 006E podra aceptar el codigo estructural y preparar una solicitud separada
de ejecucion 006F.

## 8. Resultado de construccion estructural

```text
006D_BUILD_STATUS = structurally_built_pending_006E_review
structural_tests = 29 passed
real_flint_calls = 0
network_access = 0
zero_tables = 0
artifacts_written = 0
artifacts_modified = 0
protected_documents_modified = 0
real_zero_certification = forbidden
```

Se ejecutaron exclusivamente:

```text
tests.test_h2_models
tests.test_h2_authorization
tests.test_h2_zeta_certifier
tests.test_h2_argument_principle
tests.test_h2_l3_certifier
tests.test_h2_validation
tests.test_h2_serialization
tests.test_h2_pipeline_guard
```

Las pruebas usan intervalos, contornos, polinomios y conteos sinteticos. No
incluyen ceros reales ni frecuencias publicadas.

## 9. Auditoria negativa

La revision estatica posterior a las pruebas registro:

```text
forbidden_real_math_calls = 0
network_imports = 0
directed_artifact_writes = 0
flint_import_statements = 1
artifacts_modified_since_006d_start = 0
protected_documents_unchanged = true
```

La unica sentencia `import flint` se encuentra dentro de
`PythonFlintBackend.initialize()`, despues de comprobar
`authorization_validated=true`. Ninguna prueba alcanza esa linea.

El adaptador real conserva deliberadamente sus operaciones matematicas como
`NotImplementedError`. 006D construye y prueba la arquitectura, pero no declara
que la integracion FLINT necesaria para 006F este terminada. 006E debera decidir
si esa integracion puede autorizarse y revisarse sin ejecutar calculo real.

## 10. Inventario SHA-256 de 006D

```text
requirements-h2-certifier.txt = a98869ee84ec316349fde0f110b1c02f2479d81073de3e0e758f9d88417566f3
athena_azr/h2_zero_certifier/__init__.py = a9288b5cff0c9dc963f557b79af412a3fb9b8118c1af0444f8fe936bd70d3c9c
athena_azr/h2_zero_certifier/argument_principle.py = 0fa4511f1401bb2ada700d043f0992dc04424acfff8b68605733dc5059e82b47
athena_azr/h2_zero_certifier/authorization.py = 19875d50f55a34152121277ec8c2e9db939a55978ea15794e8f229608080a74a
athena_azr/h2_zero_certifier/backend.py = db90c7c5e6fc0d605afd57362f0194c68db5b9064d75f5277ef45b8a744f7212
athena_azr/h2_zero_certifier/chi3_function.py = 38e151320ba9cc900df4650b40e5a84349587cef26d6f2f0c7a5130783828716
athena_azr/h2_zero_certifier/config.py = 7b799efbeb198cad71cd77a8981909c4f9fb2ed495a053dbb94da5efcd637d44
athena_azr/h2_zero_certifier/l3_certifier.py = aba4837161f371bf933d9e811c7dd0f7c0b94f3ea98f99b54504f2d420775e49
athena_azr/h2_zero_certifier/models.py = a69770612b4cf699b4591c26e2a05b6bfd5c1c40c7fbb6d4455c4d08db3a1a3f
athena_azr/h2_zero_certifier/pipeline.py = 6714fb97c96487d71af38ccfd8334d324ee0a80d9f9ebff383da7f072e80e7a6
athena_azr/h2_zero_certifier/python_flint_backend.py = ad6931af0d1937aa22d9b919862ead664ed2ebd44872dfdfb5138372b74682a7
athena_azr/h2_zero_certifier/serialization.py = b507e3e67a28142d6366e0df874be083562076abe258bc0c2ef0b9faa9babd2a
athena_azr/h2_zero_certifier/validation.py = 5abaca69e894eaf55e1a84e550b5c10f9bafb6577526ba5b618024cf8a1d83e5
athena_azr/h2_zero_certifier/zeta_certifier.py = 686ed4b419795ab3d2697b12ddb009db14a90ddf88cbb388834470a230fa9855
scripts/run_h2_zero_certification.py = 3e517c2424fafc91f8f3a8a25ff7a4f989f72d75ac9e32b9e0da920d78a88212
tests/test_h2_argument_principle.py = 10b1aa659182c7ee8ffb1b1e83227c52ff9c6154df9f096c955329acf4a24ba3
tests/test_h2_authorization.py = a253dfe2efa852ab09ddbca48439ba2ceac9d8b4e3a77812c3423e618027de32
tests/test_h2_l3_certifier.py = 7280bf09c3996b41a064f2d6ed95a2218d1d3d32ae8a2fdb00898cda48b3f870
tests/test_h2_models.py = 433373040084df16054114fd0e57fe357799d769883a17d9be71c28510fa048f
tests/test_h2_pipeline_guard.py = ab1a8b65a4802220a0d4306c79038ac59e2b3d73d83f36959340fda63677817b
tests/test_h2_serialization.py = fd8ea926e431a97f82fda7131dcdfae7addb8cd1c4614c9bf15ea040a857eef7
tests/test_h2_validation.py = 90290d7f93e50f54245700b7e4560de940b969ed74fe353e8e86a65f2cacfa64
tests/test_h2_zeta_certifier.py = 410b0cf1cdda8e587ea3b16ebd3d3878e8f0fcfbd22617dd7ef14fb333e5f3ae
```

## 11. Estado para 006E

```text
006D = structurally_built_pending_006E_review
H2 = protocol_defined_not_executed
real_zero_certification = forbidden
real_flint_backend = intentionally_incomplete
006E = authorized_next_review_stage_only
006F = not_authorized
C05_RERUN = forbidden
C35 = frozen
C15 = frozen
```
