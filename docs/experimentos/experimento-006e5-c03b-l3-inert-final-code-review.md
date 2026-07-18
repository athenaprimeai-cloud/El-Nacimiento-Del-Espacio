# Experimento 006E5: revision final del codigo inerte L3

## 1. Alcance

006E5 audita la integracion inerte construida en 006E4. Esta fase permite
revisar y corregir guardias estructurales, pero no autoriza matematicas FLINT
reales, calculo de ceros, tablas, red ni escritura de artefactos.

```text
experiment_id = G5B-006E5
status = inert_code_review_completed_with_patches
method = pure_argument_principle
real_flint_execution = forbidden
zero_certification = forbidden
zero_tables = not_generated
H2_certified = false
006F_readiness = false
C05_RERUN = forbidden
C35 = frozen
C15 = frozen
novelty_claim = false
```

## 2. Base revisada

```text
006E2_SHA256 = 4b14ba44d08d80941a4ab69776c41479453f0f08661ffec9fcb304204f1212c5
006E3_SHA256 = 4b7a277e939fab39ac6a9ce95cfe771944964a90a37dab12d005908ab849e931
006E4_SHA256 = fc60928a11f917f771dbcf296ef832398edb635211d96bd7fadcf2bfc395a77a
```

Los tres documentos permanecieron sin cambios durante 006E5.

## 3. Hallazgos y correcciones

### 3.1 Contorno construido fuera del builder

Un `RectangularContour` podia construirse directamente con
`orientation="negative"` y llegar al contador sin repetir la validacion
geometrica. `count_contour_winding` ahora valida cierre, ejes y orientacion
positiva antes de solicitar un solo certificado al backend.

### 3.2 Identidad de la cadena de certificados

El flujo comprobaba la identidad de la imagen inicial, pero no exigia que el
certificado de semiplano y el incremento angular pertenecieran al mismo
segmento. Ahora se verifica la cadena completa:

```text
segmento solicitado
-> imagen rigurosa del mismo segmento
-> semiplano de esa misma imagen
-> incremento de ese mismo semiplano
```

Cualquier cruce devuelve estado inconcluso.

### 3.3 Semiplano fabricado sobre una imagen que contiene cero

`HalfPlaneCertificate` podia instanciarse manualmente con un valor positivo
declarado aunque su caja contuviera el origen. El modelo ahora rechaza esa
contradiccion en su constructor, ademas de exigir cobertura total y
aritmetica de bolas.

### 3.4 Conteos negativos del backend

El aislamiento recursivo no rechazaba de inmediato un winding negativo.
`_isolate_box` ahora falla cerrado antes de subdividir si `parent_count < 0`.

### 3.5 Capacidad de autorizacion construible directamente

`PythonFlintBackend.initialize` exigia un objeto `ExecutionAuthorization`,
pero ese objeto podia construirse directamente sin atravesar el parser de
hashes. La autorizacion incorpora ahora una capacidad privada emitida solo
por `require_execution_authorization` despues de validar esquema, documentos,
inventario de codigo y ruta de salida. La construccion directa falla cerrada.

## 4. Verificacion estructural

```text
tests_run = 74
tests_passed = 73
real_integration_tests_skipped = 1
failures = 0
errors = 0
compileall = passed
real_flint_calls = 0
network_access = 0
zero_tables = 0
artifact_writes = 0
```

Las seis pruebas agregadas cubren los cinco hallazgos anteriores y fueron
observadas en rojo antes de aplicar las correcciones.

La unica importacion de `flint` sigue siendo perezosa dentro de
`PythonFlintBackend.initialize`. Los metodos matematicos reales continuan
bloqueados mediante `NotImplementedError` aun despues de una futura
autorizacion valida.

## 5. Inventario SHA-256 posterior a 006E5

```text
athena_azr/h2_zero_certifier/__init__.py = 4f4535cd57ec9cd35ec8196f25e58beefe19a52356ec15f5271d3f911ebc12cc
athena_azr/h2_zero_certifier/argument_principle.py = 444769e5cfae1a4bafd6cd26b87edf444b4857e75e7c863e000bb2aab0e30387
athena_azr/h2_zero_certifier/authorization.py = 695dcf5b6d53e6f8ae8953ce6454b6a119f28bfa8cfe0fc649800c2760607702
athena_azr/h2_zero_certifier/backend.py = 3fb0f532b5e09fa2eee32b1eb3d95c954b610dea63a689ff4d4bd0d8a9b351ef
athena_azr/h2_zero_certifier/ball_argument.py = a92efc31d7a43ed9d25e307b34f3d1bb489a33e5d454af586b4d807426835954
athena_azr/h2_zero_certifier/chi3_function.py = 38e151320ba9cc900df4650b40e5a84349587cef26d6f2f0c7a5130783828716
athena_azr/h2_zero_certifier/completed_l3.py = 6daf2e486dcac2226171cc0d169abdc3414d83c9dbd9802fb24b4754c7513ad7
athena_azr/h2_zero_certifier/config.py = 7b799efbeb198cad71cd77a8981909c4f9fb2ed495a053dbb94da5efcd637d44
athena_azr/h2_zero_certifier/contour.py = 02809288c0815f0f80aeb2410e5cdc699fd5616bf0b390f4a2cafd900bd9ca1b
athena_azr/h2_zero_certifier/l3_argument_count.py = 42c9a7bc63ca865db32be600b29041f2897e694e0a05f3e8f1d86149725679ba
athena_azr/h2_zero_certifier/l3_certifier.py = ad5f2bc6a4b46da03411c9134efe16e39d2e26d65d58491ed7c7d1cd267ddb58
athena_azr/h2_zero_certifier/models.py = bf05509d8637d25eddfe77e6a1ce0a148131da2f3f660659476c5d54287a5989
athena_azr/h2_zero_certifier/pipeline.py = 78056bb77460f9ffc07bba73c587e5c603da20949dfdca4ca18cad2f36bf895c
athena_azr/h2_zero_certifier/python_flint_backend.py = a6a7f864dc4f2b71f8501f537ff8cdbb35935e0a26c04b5315423ed5ade7fd25
athena_azr/h2_zero_certifier/serialization.py = b507e3e67a28142d6366e0df874be083562076abe258bc0c2ef0b9faa9babd2a
athena_azr/h2_zero_certifier/validation.py = f555b5a9c19a6940234cfcaf6049a3ae62164e1295726ef4e5eec477576e080a
athena_azr/h2_zero_certifier/zeta_certifier.py = 4999c79342880b5cdba610fcd7b284c3a236c6f0000d24e7fb40ced9bdc25932
scripts/run_h2_zero_certification.py = 3e517c2424fafc91f8f3a8a25ff7a4f989f72d75ac9e32b9e0da920d78a88212
```

## 6. Bloqueos que permanecen

006E5 no convierte la estructura sintetica en una prueba rigurosa. Antes de
considerar 006F todavia faltan:

1. evaluacion rigurosa de `Lambda_3(s)` con cancelaciones analiticas;
2. envolvente de la imagen de un segmento completo, no muestreo puntual;
3. validacion de semiplano mediante bolas complejas reales;
4. incremento de logaritmo complejo con ramas certificadas;
5. acumulacion dirigida y bola rigurosa para `2*pi`;
6. implementacion y revision del conteo completo L3 hasta altura 500;
7. eliminar cualquier posibilidad de que el modulo sintetico basado en
   `float` participe en la ruta probatoria real.

## 7. Veredicto

```text
006E5_CODE_REVIEW = completed
006E4_INERT_CODE = accepted_after_review_patches
STRUCTURAL_GUARDS = passed
PURE_ARGUMENT_PRINCIPLE_CONTROL_FLOW = accepted_synthetically
REAL_BACKEND_IMPLEMENTATION = incomplete
RIGOROUS_L3_COMPLETENESS = unresolved
H2_CERTIFIED = false
006F_READINESS = false
006F_EXECUTION = forbidden
C05_RERUN = forbidden
C35 = frozen
C15 = frozen
NOVELTY_CLAIM = false
```

El proximo paso permitido no es ejecutar ceros. Es disenar y revisar una fase
separada para implementar el backend matematico real sin recorrer aun los
contornos de certificacion.
