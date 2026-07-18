# Experimento 006E4: autorizacion de integracion inerte L3

## 1. Autorizacion

El mensaje del usuario `puedes continuar.. procede con lo que sigue` se toma
como autorizacion explicita para ejecutar el plan TDD 006E3 dentro de los
limites de 006E2.

```text
experiment_id = G5B-006E4
status = authorized_inert_code_phase
method = pure_argument_principle
code = authorized_inert_only
synthetic_tests = authorized
real_flint_execution = forbidden
zero_certification = forbidden
zero_tables = not_generated
artifacts = none
network = forbidden
H2_certified = false
006F = blocked
C05_RERUN = forbidden
C35 = frozen
C15 = frozen
```

## 2. Base congelada

```text
006E2_SHA256 = 4b14ba44d08d80941a4ab69776c41479453f0f08661ffec9fcb304204f1212c5
006E3_SHA256 = 4b7a277e939fab39ac6a9ce95cfe771944964a90a37dab12d005908ab849e931
```

006E3 queda congelado como plan. Su texto puede contener descripciones de
pruebas y codigo futuro, pero no constituye evidencia de que la implementacion
sea rigurosa ni de que las pruebas hayan sido ejecutadas.

## 3. Acciones permitidas

1. completar los tipos y contratos inertes definidos por 006E2;
2. crear o modificar exclusivamente el paquete `h2_zero_certifier` y sus
   pruebas H2;
3. usar TDD con funciones y certificados sinteticos;
4. corregir implementaciones parciales encontradas al iniciar 006E4;
5. conservar todas las operaciones FLINT reales como inaccesibles o
   `NotImplementedError`;
6. ejecutar la suite estructural H2;
7. producir un informe documental 006E4 con hashes.

## 4. Acciones prohibidas

1. importar o ejecutar FLINT real;
2. evaluar `zeta`, `L(s,chi_3)`, Gamma o contornos reales;
3. usar Hardy o Turing para L3;
4. calcular o incrustar ceros reales;
5. generar tablas, manifiestos o archivos en `artifacts/`;
6. usar red;
7. declarar H2 certificado;
8. autorizar 006F;
9. tocar C05, C35 o C15.

## 5. Estado inicial observado

Al comenzar 006E4 ya existia una implementacion parcial de los archivos
previstos en 006E3. La prueba base registro:

```text
tests_run = 59
failures = 1
errors = 4
skipped = 1
```

006E4 tratara ese codigo como trabajo no aceptado: auditara sus garantias,
reproducira cada fallo y aplicara correcciones mediante ciclos TDD. No se
presupondra que una prueba verde equivale a aritmetica rigurosa.

## 6. Correcciones realizadas

La revision de la implementacion parcial encontro y corrigio estas diferencias
respecto de 006E2:

1. los fixtures antiguos fueron migrados al conteo recursivo por cajas;
2. una secuencia L3 vacia vuelve a producir estado inconcluso;
3. el modulo angular dejo de usar `float`, `complex`, `atan2` y margenes de
   error inventados como si fueran certificados;
4. la rotacion de semiplano se valida con intervalos `Decimal` y el incremento
   trascendental solo puede envolverse si llega ya certificado por el backend;
5. el winding se acepta solo si su intervalo contiene exactamente un entero
   no negativo, no por proximidad menor que medio entero;
6. la division intervalar por `2*pi` considera todas las combinaciones de
   extremos;
7. la subdivision adaptativa del contorno quedo conectada a los contratos de
   imagen, semiplano e incremento;
8. los limites de contorno y profundidad provienen de la configuracion;
9. contener `Re(s)=1/2` ya no certifica la recta critica: se exige una
   declaracion probatoria separada del backend;
10. los fixtures de aislamiento usan coordenadas decimales, no `complex` ni
    comparaciones binarias;
11. los modulos nuevos se incorporaron al inventario obligatorio de hashes;
12. una futura autorizacion 006F debe coincidir tambien con los hashes de 006E2
    y 006E3;
13. `PythonFlintBackend.initialize` ya no acepta un booleano: exige el objeto
    de autorizacion validado por el parser.

## 7. Arquitectura inerte resultante

```text
CompletedL3 identity
    -> exact rectangular contour
    -> full segment image certificate
    -> strict right-half-plane certificate
    -> backend-supplied rigorous argument interval
    -> adaptive segment subdivision
    -> interval winding with unique integer
    -> recursive box isolation
    -> independent counts at frozen heights
```

La capa sintetica demuestra el flujo de control y los fallos cerrados. No
implementa Gamma, funciones L, logaritmos complejos rigurosos ni envolventes
reales de segmentos. Esas operaciones permanecen inertes y bloqueadas.

## 8. Verificacion

La verificacion final registro:

```text
tests_run = 68
tests_passed = 67
real_integration_tests_skipped = 1
failures = 0
errors = 0
compileall = passed
static_audit = passed
real_flint_execution = 0
network_access = 0
zero_tables = 0
artifacts_newer_than_006E4 = 0
embedded_real_zero_constants_in_runtime = 0
```

La prueba omitida exige simultaneamente la puerta de entorno y un archivo de
autorizacion 006F, y aun asi conserva un fallo seguro porque la integracion
real no existe.

La unica sentencia `import flint` permanece dentro de la inicializacion
perezosa, posterior a la validacion del objeto de autorizacion.

## 9. Inventario SHA-256 del runtime

```text
athena_azr/h2_zero_certifier/__init__.py = 4f4535cd57ec9cd35ec8196f25e58beefe19a52356ec15f5271d3f911ebc12cc
athena_azr/h2_zero_certifier/argument_principle.py = 444769e5cfae1a4bafd6cd26b87edf444b4857e75e7c863e000bb2aab0e30387
athena_azr/h2_zero_certifier/authorization.py = 6eea933dd4a5bb1bc2931e3a8cbedaf6022216269a87792e2f256456c2ea7de3
athena_azr/h2_zero_certifier/backend.py = 3fb0f532b5e09fa2eee32b1eb3d95c954b610dea63a689ff4d4bd0d8a9b351ef
athena_azr/h2_zero_certifier/ball_argument.py = a92efc31d7a43ed9d25e307b34f3d1bb489a33e5d454af586b4d807426835954
athena_azr/h2_zero_certifier/chi3_function.py = 38e151320ba9cc900df4650b40e5a84349587cef26d6f2f0c7a5130783828716
athena_azr/h2_zero_certifier/completed_l3.py = 6daf2e486dcac2226171cc0d169abdc3414d83c9dbd9802fb24b4754c7513ad7
athena_azr/h2_zero_certifier/config.py = 7b799efbeb198cad71cd77a8981909c4f9fb2ed495a053dbb94da5efcd637d44
athena_azr/h2_zero_certifier/contour.py = ab68dbb6c7c5d44da4f1c2d5fec159ec3bba292574f449dca570d7a2563646b6
athena_azr/h2_zero_certifier/l3_argument_count.py = 128289f0825551241d70c6ad1e3278a160e9002968964e079a2a23d5927b4d91
athena_azr/h2_zero_certifier/l3_certifier.py = 3241105f699adb4794a98f3889f1e4ac1071ea721ec17de2fa177881806ff741
athena_azr/h2_zero_certifier/models.py = 447c33d5c133ec899e89bc7be411f5b57a38a687e9d071659f8e3f2988024993
athena_azr/h2_zero_certifier/pipeline.py = 78056bb77460f9ffc07bba73c587e5c603da20949dfdca4ca18cad2f36bf895c
athena_azr/h2_zero_certifier/python_flint_backend.py = a6a7f864dc4f2b71f8501f537ff8cdbb35935e0a26c04b5315423ed5ade7fd25
athena_azr/h2_zero_certifier/serialization.py = b507e3e67a28142d6366e0df874be083562076abe258bc0c2ef0b9faa9babd2a
athena_azr/h2_zero_certifier/validation.py = f555b5a9c19a6940234cfcaf6049a3ae62164e1295726ef4e5eec477576e080a
athena_azr/h2_zero_certifier/zeta_certifier.py = 4999c79342880b5cdba610fcd7b284c3a236c6f0000d24e7fb40ced9bdc25932
scripts/run_h2_zero_certification.py = 3e517c2424fafc91f8f3a8a25ff7a4f989f72d75ac9e32b9e0da920d78a88212
```

## 10. Veredicto

```text
006E4_STATUS = inert_integration_completed_pending_review
006E2_METHOD = preserved
PURE_ARGUMENT_PRINCIPLE_STRUCTURE = implemented_synthetically
STRUCTURAL_GUARDS = passed
REAL_BACKEND_IMPLEMENTATION = still_incomplete
REAL_SEGMENT_ENCLOSURE = not_implemented
RIGOROUS_COMPLEX_LOG_INCREMENT = not_implemented
RIGOROUS_L3_COMPLETENESS = unresolved
H2_CERTIFIED = false
006F_READINESS = false
006F_EXECUTION = forbidden
C05_RERUN = forbidden
C35 = frozen
C15 = frozen
NOVELTY_CLAIM = false
```

006E4 completa la integracion inerte, no el backend matematico real. El
siguiente paso permitido es revisar y congelar esta fase. Una futura fase de
backend real debera implementar envolventes completas de segmento y logaritmos
complejos con bolas sin ejecutar todavia el contorno de altura 500.
