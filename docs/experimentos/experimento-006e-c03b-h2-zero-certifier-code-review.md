# Experimento 006E: revision de codigo del certificador H2

## 1. Estado y alcance

```text
experiment_id = G5B-006E
target = H2_zero_certifier_code_review
status = completed_structural_review
006D_structural_layer = accepted_after_review_patches
real_flint_backend = incomplete_and_inert
rigorous_L3_argument_principle = not_implemented
H2_certified = false
006F_readiness = blocked
006F_execution = forbidden
zero_tables = not_generated
artifacts = none
network_access = 0
novelty_claim = false
C05_RERUN = forbidden
C35 = frozen
C15 = frozen
```

006E revisa la correspondencia entre 006B, 006C y el codigo construido en
006D. Autoriza parches estructurales y pruebas sinteticas, pero no autoriza
calculo real, importacion efectiva de FLINT, certificacion de ceros, tablas ni
escritura en `artifacts/`.

## 2. Base documental verificada

Los documentos congelados conservaron sus hashes esperados:

```text
005F = 148816b8375d42e4a19cf67d0c14e53e54a07f0a518754fc0a1b6d1e35042216
006A = 546f502b2907a9e125df6b07ffff5a07aa7f1147765196ab3e4523097d2a67d8
006B = 4f110d0926067e9e1eb44cbbfe78ee1acc93f85f526176c81d98446eafd492cb
006C = cbf9e6ef8d39032cefdd467fab274d6cd7e1569978292ecfd1fb9da70768db3f
006D = 4ee69ecfd461b381913ba413c9941379a589f90260f5c6b06a88080b3f8ff051
```

## 3. Hallazgos corregidos durante 006E

### 3.1 Intervalos degenerados

`RealInterval` permitia inicialmente `lower == upper`. Eso no constituye un
encierro intervalar riguroso y contradice la regla `lower < gamma < upper` de
006B. Ahora todos los intervalos exigen ancho estrictamente positivo. Las
pruebas sinteticas usan `Decimal` para evitar que radios pequenos colapsen por
redondeo binario.

### 3.2 Conteo sintetico confundible con certificacion rigurosa

El acumulador angular original usaba `float` y `complex`. Era util para probar
ramas logicas, pero no podia certificar un cambio de argumento. La funcion fue
renombrada `synthetic_winding_number`. El punto de entrada
`certified_winding_number` permanece inerte y lanza `NotImplementedError` hasta
que exista una implementacion con bolas complejas revisada.

### 3.3 Contrato incompleto de aislamiento L3

Las cajas L3 ahora llegan como `IsolatedZeroBox`, con multiplicidad, indicador
explicito de unicidad y referencia de certificado. `certify_l3` rechaza cajas
sin unicidad, secuencias vacias, cajas no simetricas respecto de la recta
critica, solapamientos, fronteras atravesadas y conteos independientes que no
coincidan.

### 3.4 Conteo de zeta no independiente

006D obtenia el conteo en cada altura contando la misma lista aislada. Eso no
satisfacia la condicion de 006B/006C de contrastar aislamiento y completitud.
El backend ahora debe entregar `zeta_count_certificate` por separado. La capa
de dominio exige identidad, frontera libre de ceros, coherencia interna e
igualdad con la suma de multiplicidades aisladas.

### 3.5 Ruta de salida elegible por la CLI

La autorizacion comprobaba que el JSON y la CLI coincidieran, pero la CLI podia
proponer cualquier ruta. El pipeline ahora acepta exclusivamente:

```text
artifacts/goldbach_cesaro/c03b_h2_zero_certification/
```

resuelta bajo la raiz del proyecto. La comprobacion ocurre antes de construir
el backend o crear salida.

### 3.6 Integracion real sin prueba doblemente bloqueada

Se agrego una prueba de integracion real visible pero omitida. Solo puede dejar
de estar omitida si coinciden dos llaves independientes:

1. `ATHENA_H2_EXECUTION_AUTHORIZED=1`;
2. un archivo legible que declare `G5B-006F` y
   `execution_authorized=true`.

Incluso con ambas llaves, la prueba falla de forma segura porque la integracion
real no esta implementada ni autorizada.

### 3.7 Contrastes externos opcionales

El validador global ahora exige referencias separadas `odlyzko` y `lmfdb`,
ambas con estado `match` y SHA-256 valido. Un contraste ausente, no revisado o
en desacuerdo impide aceptar el paquete.

## 4. Auditoria negativa posterior a los parches

```text
structural_tests_run = 38
structural_tests_passed = 37
real_integration_tests_skipped = 1
real_flint_calls = 0
real_flint_imports_executed = 0
network_access = 0
embedded_real_zero_constants = 0
zero_tables = 0
artifact_writes = 0
H2_certified = false
```

La unica sentencia `import flint` sigue dentro de
`PythonFlintBackend.initialize()` y esta despues de la validacion 006F. Las
operaciones matematicas reales del adaptador permanecen como
`NotImplementedError`. Las escrituras ejercitadas por las pruebas ocurren solo
en directorios temporales.

## 5. Viabilidad del backend real

### 5.1 Zeta

La API publica de python-flint documenta una ruta viable para aislar ceros
consecutivos de zeta y obtener conteos rigurosos. El contrato estructural ya
separa ambas pruebas. Falta implementar y revisar las conversiones
`arb/acb -> RealInterval/ComplexBox` y la procedencia exacta del certificado de
conteo. No se ejecutaron esas funciones en 006E.

### 5.2 L(s, chi_3)

La API publica permite construir el caracter modulo 3 y evaluar su funcion de
Hardy y su funcion L con bolas. No ofrece una operacion de alto nivel que, por
si sola, aisle todos los ceros y certifique el conteo completo hasta 500.

Por tanto, el cierre L3 requiere aun:

1. definir la funcion completada usada en el contorno;
2. implementar evaluacion intervalar de su imagen sobre segmentos;
3. certificar que cada imagen de segmento evita el origen;
4. subdividir adaptativamente sin usar fases `float`;
5. encerrar el cambio total de argumento en un unico entero;
6. producir un certificado de conteo independiente de las cajas aisladas;
7. demostrar unicidad individual, incluidas multiplicidades pares y posibles
   ceros fuera de la recta critica.

El principio del argumento sintetico no cubre estos puntos. Usarlo como prueba
real invalidaria H2.

## 6. Inventario SHA-256 posterior a 006E

```text
requirements-h2-certifier.txt = a98869ee84ec316349fde0f110b1c02f2479d81073de3e0e758f9d88417566f3
athena_azr/h2_zero_certifier/__init__.py = 4f4535cd57ec9cd35ec8196f25e58beefe19a52356ec15f5271d3f911ebc12cc
athena_azr/h2_zero_certifier/argument_principle.py = 444769e5cfae1a4bafd6cd26b87edf444b4857e75e7c863e000bb2aab0e30387
athena_azr/h2_zero_certifier/authorization.py = 19875d50f55a34152121277ec8c2e9db939a55978ea15794e8f229608080a74a
athena_azr/h2_zero_certifier/backend.py = 613a683cdb2021072012dc5914265d5a9ff3ddd50a274c05f65d38904fc24f7d
athena_azr/h2_zero_certifier/chi3_function.py = 38e151320ba9cc900df4650b40e5a84349587cef26d6f2f0c7a5130783828716
athena_azr/h2_zero_certifier/config.py = 7b799efbeb198cad71cd77a8981909c4f9fb2ed495a053dbb94da5efcd637d44
athena_azr/h2_zero_certifier/l3_certifier.py = 6ae912bd032ee4ff5d27374f6a87f6ff62976e91ef3ed2c0a47963c0a0815fb2
athena_azr/h2_zero_certifier/models.py = 7330dad69e16a21d2cd44928aedc4b0f992195b4cf609112654ec4be053b6ce7
athena_azr/h2_zero_certifier/pipeline.py = d1d0e445dd4deddaba0be3bc44c13ea96c36e07a6892cd80aba7b2928c450bc1
athena_azr/h2_zero_certifier/python_flint_backend.py = d2a5fd58b0e29e37cb7a029f2e6722e836625e553dfb38c870fcfea3b3e47c4a
athena_azr/h2_zero_certifier/serialization.py = b507e3e67a28142d6366e0df874be083562076abe258bc0c2ef0b9faa9babd2a
athena_azr/h2_zero_certifier/validation.py = 4ff6d0dc973c4538aaae2f12d329ebed251932bd997db73d43be517d1144c688
athena_azr/h2_zero_certifier/zeta_certifier.py = 4999c79342880b5cdba610fcd7b284c3a236c6f0000d24e7fb40ced9bdc25932
scripts/run_h2_zero_certification.py = 3e517c2424fafc91f8f3a8a25ff7a4f989f72d75ac9e32b9e0da920d78a88212
tests/test_h2_argument_principle.py = ca922735586b8dc96d4ac92e2568f3015effe1b1eedc47d197e3f840416354ae
tests/test_h2_authorization.py = a253dfe2efa852ab09ddbca48439ba2ceac9d8b4e3a77812c3423e618027de32
tests/test_h2_l3_certifier.py = 3ddabda1920010a2762ecec7c77cccaf1dc5511a120d35845ed0363045f5d852
tests/test_h2_models.py = fac2b12958e20fc7bc79da0732cc65180a93165d7a40ce3991e27ea31df28f4c
tests/test_h2_pipeline_guard.py = dcaaf5c55975eac9cb4c645c26f9800039910ee639c9586980c1edad12014a91
tests/test_h2_real_flint_guarded.py = c9357eea46acba7e326ea29961489c8ae6ff17db1c3220203dfd0be5def341b9
tests/test_h2_serialization.py = b909582631066fd7f02ffdd216d45ab3e51c10ad47425980589b3ef7192d34c6
tests/test_h2_validation.py = 2fbcf4ba77a0ce2cb720314d76d3889c0bdc0a5bef1baaa4aeb4e104455feccf
tests/test_h2_zeta_certifier.py = 0468c36efc4fa185d83261a4bb40f99fe1d5bdf4566e09e496e1f732bb0b60e9
```

Este inventario describe el codigo posterior a los parches 006E. El inventario
historico de 006D conserva el estado previo y no fue reescrito.

## 7. Veredicto

```text
006E_CODE_REVIEW = completed
006D_STRUCTURAL_CODE = accepted_after_review_patches
STRUCTURAL_GUARDS = passed
REAL_BACKEND_IMPLEMENTATION = incomplete
RIGOROUS_L3_COMPLETENESS = unresolved
006F_READINESS = false
006F_EXECUTION = forbidden
H2 = protocol_defined_not_executed
005F_EXECUTABLE_UNLOCK = false
C05_RERUN = forbidden
```

No se autoriza 006F. El siguiente trabajo permitido debera completar y revisar
el backend real, especialmente el conteo L3 por aritmetica de bolas, sin
ejecutarlo. Despues sera necesaria una nueva revision de codigo antes de pedir
autorizacion de calculo real.

## Referencias tecnicas

1. Protocolo 006B congelado:
   `docs/experimentos/experimento-006b-c03b-protocolo-certificacion-ceros-500.md`.
2. Plan 006C congelado:
   `docs/experimentos/experimento-006c-c03b-h2-zero-certifier-implementation-plan.md`.
3. python-flint, [bolas complejas, integracion y zeta](https://python-flint.readthedocs.io/en/latest/acb.html).
4. python-flint, [caracteres de Dirichlet y funciones L](https://python-flint.readthedocs.io/en/latest/dirichlet.html).
