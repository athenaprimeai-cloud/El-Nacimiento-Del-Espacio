# 006H03: L3 backend completion code plan

```text
phase_id = 006H03
phase_name = L3_BACKEND_COMPLETION_CODE_PLAN
phase_type = documentary_technical_code_plan
code_modified = false
tests_executed = false
backend_invoked = false
FLINT_imported = false
Arb_or_Acb_imported = false
chi_l_function_called = false
Lambda_3_evaluated = false
contours_executed = false
zeros_isolated_or_counted = false
H2_opened = false
006F_opened = false
network_used = false
dependencies_installed = false
```

## 1. Alcance

006H03 disena el plan exacto de implementacion del backend L3 necesario para
satisfacer las obligaciones matematicas congeladas en 006H02. Este documento no
autoriza implementacion, no modifica codigo, no ejecuta pruebas y no abre una
fase H2/006F.

Fuentes usadas:

| Fuente | Uso |
| --- | --- |
| `006H01` | Contrato H2/006F congelado, artefactos canonicos y esquema de autorizacion. |
| `006H02` | Obligaciones matematicas L3: funcion completada, contornos, frontera, winding. |
| `006H00` | Brechas H2-R01..H2-R24 y cuello de botella H2-R06/H2-R07/H2-R08. |
| `006C` | Arquitectura original del certificador H2. |
| `006D/006E` | Estado estructural, backend real incompleto e inerte. |
| `006E7-006E17` | Rango confirmado: arquitectura probatoria inerte, evidencias reales selladas y semantica FLINT/Arb pendiente. |

## 2. Inventario del codigo actual

Inventario obtenido por lectura estatica de archivos locales, sin importar
modulos y sin ejecutar tests.

### 2.1 Archivos existentes del paquete `h2_zero_certifier`

```text
athena_azr/h2_zero_certifier/__init__.py
athena_azr/h2_zero_certifier/argument_principle.py
athena_azr/h2_zero_certifier/authorization.py
athena_azr/h2_zero_certifier/backend.py
athena_azr/h2_zero_certifier/ball_argument.py
athena_azr/h2_zero_certifier/chi3_function.py
athena_azr/h2_zero_certifier/completed_l3.py
athena_azr/h2_zero_certifier/config.py
athena_azr/h2_zero_certifier/contour.py
athena_azr/h2_zero_certifier/l3_argument_count.py
athena_azr/h2_zero_certifier/l3_certifier.py
athena_azr/h2_zero_certifier/models.py
athena_azr/h2_zero_certifier/pipeline.py
athena_azr/h2_zero_certifier/python_flint_backend.py
athena_azr/h2_zero_certifier/real_argument.py
athena_azr/h2_zero_certifier/real_completed_l3.py
athena_azr/h2_zero_certifier/real_evidence.py
athena_azr/h2_zero_certifier/real_segment_enclosure.py
athena_azr/h2_zero_certifier/rigorous_ball_runtime.py
athena_azr/h2_zero_certifier/serialization.py
athena_azr/h2_zero_certifier/validation.py
athena_azr/h2_zero_certifier/zeta_certifier.py
```

### 2.2 Clases y funciones ya implementadas

| Archivo | Inventario tecnico |
| --- | --- |
| `models.py` | `RealInterval`, `ComplexBox`, `IsolatedZeroBox`, `ZeroCertificate`, `CountCertificate`, `FunctionCertification`, `CertificationBundle`, `RationalComplexPoint`, `DirectedSegment`, `RectangularContour`, `SegmentImageCertificate`, `HalfPlaneCertificate`, `ArgumentIncrementCertificate`, `WindingCertificate`, `RectangleZeroCountCertificate`. |
| `config.py` | `CertificationConfig.frozen_default()` con alturas `(143, 200, 300, 500)`, ancho `1e-20`, precision escalonada, conductor L3 y contorno `[-0.5, 1.5]`. |
| `chi3_function.py` | `CHI3_METADATA`, `validate_chi3_metadata`, formulas simbolicas de `Lambda_3` y control Hurwitz. |
| `contour.py` | `bisect_segment`, `validate_contour_orientation`, `build_rectangular_contour`. |
| `ball_argument.py` | `verify_exclusion`, `certify_half_plane`, `certify_argument_increment`; no calcula transcendentes. |
| `l3_argument_count.py` | `_certify_segment`, `count_contour_winding`, `accumulate_winding`, `InconclusiveWindingCount`; ruta intervalar estructural con certificados del backend. |
| `l3_certifier.py` | `_isolate_box`, `certify_l3`, validacion de metadata L3, aislamiento recursivo sintetico/estructural y comparacion con conteos. |
| `real_evidence.py` | Registros probatorios sellados, `RealEvidenceFactory`, hashes parentales, prohibicion de evidencia probativa no emitida por fabrica validada. |
| `rigorous_ball_runtime.py` | `RigorousBallRuntime` y `audit_runtime_semantics` con semanticas requeridas. |
| `real_completed_l3.py` | `evaluate_completed_l3` contra runtime inyectado, compone factor conductor, exponencial, gamma y `native_dirichlet_l`. |
| `real_segment_enclosure.py` | `rectangular_hull`, `enclose_completed_l3_segment`, prueba de inclusion de caja completa. |
| `real_argument.py` | `certify_real_half_plane`, `real_argument_increment`, `accumulate_real_winding`. |
| `serialization.py` | JSON canonico, CSV de ceros, escritura atomica bajo raiz permitida. |
| `authorization.py` | Parser 006F validado, inventarios de hashes, procedencia probativa, bloqueo por autorizacion. |
| `pipeline.py` | Guardia de salida canonica, autorizacion, directorio vacio y backend factory antes de pipeline real. |
| `zeta_certifier.py` | Certificador estructural zeta con backend falso/real futuro. |

### 2.3 Funciones sinteticas o placeholders

| Archivo | Estado |
| --- | --- |
| `argument_principle.py` | `synthetic_winding_number` usa `complex`, `float`, `atan2` y `round` para pruebas sinteticas; debe permanecer fuera del inventario probativo. |
| `completed_l3.py` | Formula simbolica e inert stubs para punto/segmento real. |
| `l3_certifier.py` | Aislamiento y conteo estructural dependen de `backend.l3_box_winding_count` y `backend.l3_count_certificate`; no certifican sin backend real. |
| `real_completed_l3.py`, `real_segment_enclosure.py`, `real_argument.py` | Arquitectura probatoria inerte con runtime falso en tests; no contiene implementacion FLINT real. |

### 2.4 Rutas con `NotImplementedError`

| Ruta | Significado |
| --- | --- |
| `completed_l3.completed_l3_point_inert` | Evaluacion real de `Lambda_3` bloqueada. |
| `completed_l3.completed_l3_segment_inert` | Imagen real de segmento bloqueada. |
| `argument_principle.certified_winding_number` | Entrada rigurosa antigua reservada; no debe usarse como ruta probativa futura. |
| `python_flint_backend._blocked_until_006f` | Todas las operaciones matematicas FLINT reales permanecen reservadas para autorizacion futura. |
| `pipeline.run_certification_pipeline` | Pipeline real termina en `NotImplementedError` aun despues de preflight. |

### 2.5 Pruebas estructurales existentes

Pruebas H2 locales detectadas por lectura estatica:

```text
tests/test_h2_models.py
tests/test_h2_contour.py
tests/test_h2_argument_principle.py
tests/test_h2_ball_argument.py
tests/test_h2_l3_argument_count.py
tests/test_h2_l3_isolation.py
tests/test_h2_l3_certifier.py
tests/test_h2_real_completed_l3.py
tests/test_h2_real_segment_enclosure.py
tests/test_h2_real_argument.py
tests/test_h2_real_evidence.py
tests/test_h2_rigorous_ball_runtime.py
tests/test_h2_authorization.py
tests/test_h2_pipeline_guard.py
tests/test_h2_root_issuance.py
tests/test_h2_serialization.py
tests/test_h2_validation.py
tests/test_h2_zeta_certifier.py
tests/test_h2_real_flint_guarded.py
```

Estas pruebas son estructurales o sinteticas. 006H03 no las ejecuta.

### 2.6 Interfaces que no deben cambiar sin autorizacion separada

| Interfaz | Restriccion |
| --- | --- |
| `BallBackend` | Puede ampliarse solo de forma compatible; sus contratos actuales no deben debilitarse. |
| `CertificationConfig.frozen_default` | Alturas, ancho, contorno y presupuesto de precision no deben cambiarse dentro de 006H03. |
| `RealEvidenceFactory` y evidencias reales | La cadena de procedencia y hashes parentales no debe relajarse. |
| `require_execution_authorization` | Debe mantenerse como puerta antes de construir backend real; futura actualizacion debe migrar a esquema 006H01. |
| `PROBATIVE_RUNTIME_CODE_FILES` | Debe seguir excluyendo `argument_principle.py` sintetico. |
| `serialization.canonical_json_bytes` | Debe preservar UTF-8, LF, claves ordenadas, `allow_nan=False`. |
| `pipeline.run_certification_pipeline` | No puede producir artefactos ni construir backend antes de preflight completo. |

### 2.7 Codigo congelado o protegido por hashes

El proyecto ya tiene una politica de hashes en `authorization.py`:

```text
RUNTIME_CODE_FILES
PROBATIVE_RUNTIME_CODE_FILES
REVIEW_DOCUMENT_FILES
approved_code_hashes
review_chain_hashes
```

006H03 no congela hashes nuevos. La futura fase de codigo debe recalcular hashes
despues de modificar el backend y actualizar el esquema 006F a los protocolos
006H01/006H02. Cualquier ejecucion futura que use hashes antiguos 006E como si
fueran aprobacion 006H01/006H02 debe bloquearse.

## 3. Mapa de implementacion

### 3.1 Principios de implementacion

```text
no_float_for_probative_backend = true
no_hidden_complex_branches = true
no_T_star_adaptation = true
four_independent_contours = true
real_backend_requires_separate_code_authorization = true
real_execution_requires_separate_006F_authorization = true
```

La implementacion futura debe conservar dos mundos separados:

1. mundo sintetico: pruebas puras, backends falsos, curvas conocidas;
2. mundo probativo: evidencia emitida por fabrica validada, backend sellado,
   autorizacion 006F, hashes finales, sin `argument_principle.py` float.

### 3.2 Responsabilidades minimas por modulo

| Modulo | Accion futura | Reutilizacion | Trabajo faltante |
| --- | --- | --- | --- |
| `chi3_function.py` | Extender metadatos exactos y validacion. | Reutilizar `CHI3_METADATA`, formulas simbolicas. | Agregar campos 006H02: `character_type`, `conrey_index`, raiz funcional, normalizacion congelada. |
| `l3_completed_function.py` o `real_completed_l3.py` | Implementar fachada probativa de `Lambda_3`. | Reutilizar `evaluate_completed_l3`. | Agregar trazas de operaciones, derivada/log-derivada opcional, guardias de ramas y compatibilidad con 006H02. |
| `contour.py` | Congelar constructores `C_143`, `C_200`, `C_300`, `C_500`. | Reutilizar `build_rectangular_contour`. | Prohibir `T_star`, agregar validacion de alturas exactas y cobertura por segmento. |
| `boundary_certifier.py` | Certificar frontera libre de ceros por subdivision. | Reutilizar `real_segment_enclosure`, `ball_argument`. | Nuevo modulo: subdivision, certificados por caja, testigo de separacion, estados inconclusos. |
| `argument_increment.py` | Certificar incrementos locales. | Reutilizar `real_argument_increment`. | Nuevo modulo o separacion desde `real_argument.py`: ramas locales, endpoints, sumas con runtime. |
| `winding_certifier.py` | Resolver intervalo total a entero unico. | Reutilizar `accumulate_real_winding` y `accumulate_winding`. | Nuevo modulo/fachada que emita reporte por altura y estados 006H02. |
| `l3_isolator.py` | Aislar ceros individuales L3. | Reutilizar `_isolate_box` como punto de partida. | Separar de `l3_certifier.py`, soportar multiplicidades, clusters y certificados reales. |
| `l3_certifier.py` | Coordinar aislamiento y conteo completo. | Reutilizar validacion de metadata y comparacion de conteos. | Integrar certificados reales, cuatro alturas independientes y bloqueo por discrepancia. |
| `serialization.py` | Emitir artefactos canonicos L3. | Reutilizar JSON/CSV atomico. | Alinear columnas con 006H01, reportes L3 y hashes de certificados. |
| `pipeline.py` | Preflight H2/006F completo. | Reutilizar bloqueo antes de backend. | Migrar esquema a `G5B-006F-AUTHORIZATION.json`, validar 006H01/006H02, versiones, runtime, directorio vacio. |
| `python_flint_backend.py` | Implementar adaptador real solo en fase autorizada. | Reutilizar inicializacion perezosa. | Reemplazar stubs por operaciones Arb/Acb verificadas, sin importar FLINT al importar paquete. |

## 4. Funciones futuras requeridas

Cada funcion listada queda definida como tarea futura, no implementada en 006H03.

| function_name | module | purpose | inputs | outputs | preconditions | postconditions | mathematical_obligation_from_006H02 | H2_requirement_ids | failure_states | backend_operations_used | tests_required | real_execution_required |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `chi3_character_metadata` | `chi3_function.py` | Emitir identidad exacta de `chi_3`. | none | metadata dict canonico | No backend. | Metadata coincide con 006H02. | Definicion exacta de `chi_3`. | H2-R05, H2-R10, H2-R21 | `character_metadata_mismatch` | none | unit, contract | false |
| `validate_l3_contract_metadata` | `chi3_function.py` | Validar conductor, paridad, conrey y normalizacion. | metadata | none or error | Strings canonicos. | Rechaza variantes ambiguas. | No dependencia RH/GRH; caracter exacto. | H2-R10, H2-R21 | `completed_function_equivalence_unproved` | none | unit, contract | false |
| `evaluate_lambda3_ball` | `l3_completed_function.py` or `real_completed_l3.py` | Evaluar `Lambda_3` en bola compleja. | runtime, complex ball, precision, evidence factory | `RealCompletedL3PointEvidence` | Runtime auditado, metadata exacta. | Bola finita, probativa si autorizada. | Funcion completada congelada. | H2-R06, H2-R08, H2-R11, H2-R12 | `backend_semantics_insufficient`, `completed_function_equivalence_unproved` | pi ball, exact division, log, exp, gamma, native L, multiply | unit fake, real-blocked, contract | true |
| `evaluate_lambda3_segment_box` | `l3_completed_function.py` or `boundary_certifier.py` | Encerrar imagen de un segmento. | runtime, segment, precision | `RealSegmentImageEvidence` | Segmento dentro de contorno congelado. | `entire_segment_covered = true`. | Imagen de segmentos y exclusion del origen. | H2-R07, H2-R08, H2-R11 | `segment_image_contains_or_may_contain_zero` | whole-box L3 evaluation | synthetic, real-blocked | true |
| `build_l3_contours` | `contour.py` | Construir `C_143`, `C_200`, `C_300`, `C_500`. | none or frozen config | contour map | Alturas exactas. | Cuatro contornos positivos, vertices exactos. | Region y contorno exactos. | H2-R07, H2-R21 | `contour_accounting_ambiguous` | none | unit, contract | false |
| `subdivide_segment_cover` | `boundary_certifier.py` | Cubrir segmento sin huecos. | segment, max depth | subdivision list | Segmento valido. | Cobertura completa y ordenada. | Frontera libre de ceros. | H2-R07, H2-R08 | `boundary_not_certified_zero_free` | none | unit, synthetic | false |
| `certify_boundary_segment` | `boundary_certifier.py` | Probar `0 notin Lambda_3(segment_box)`. | backend/runtime, segment, precision | segment certificates | Backend autorizado en futuro. | Testigo de separacion positiva o inconcluso. | Boundary zero-free. | H2-R07, H2-R08, H2-R11 | `segment_image_contains_or_may_contain_zero` | segment box, zero exclusion, half-plane | synthetic, real-blocked | true |
| `certify_boundary_contour` | `boundary_certifier.py` | Certificar todos los segmentos de un contorno. | contour, precision, max depth | boundary report | Segmentos validos y orientados. | `boundary_zero_free = true` o estado inconcluso. | Cobertura completa de cada segmento. | H2-R07, H2-R08 | `boundary_not_certified_zero_free` | repeated segment certification | synthetic, real-blocked | true |
| `certify_argument_increment_local` | `argument_increment.py` | Encerrar `delta_arg_j`. | half-plane evidence, endpoint evidence | argument increment evidence | Rama local certificada. | Intervalo de incremento con inclusion. | Encierro del incremento de argumento. | H2-R06, H2-R08, H2-R11 | `argument_increment_not_certified` | rotate, complex_log, subtract, imag interval | unit fake, real-blocked | true |
| `sum_argument_intervals` | `argument_increment.py` | Sumar incrementos con redondeo dirigido. | increment list | total arg interval | Mismo backend/procedencia/precision. | Inclusion preservada. | Suma intervalar. | H2-R06, H2-R08 | `argument_increment_not_certified` | sum real balls | unit, synthetic | false |
| `certify_unique_integer_winding` | `winding_certifier.py` | Resolver `W_T` a entero unico. | total winding interval | winding certificate | Intervalo cerrado certificado. | Un unico entero o inconcluso. | Criterio de entero unico. | H2-R06, H2-R08 | `winding_interval_contains_multiple_integers` | divide by two pi, integer enclosure | unit, synthetic, real-blocked | true |
| `isolate_l3_zero_boxes` | `l3_isolator.py` | Aislar ceros individuales L3. | backend, region, precision | zero boxes | Winding local disponible. | Unicidad, ancho `<=1e-20`, disjuncion. | Multiplicidades y clusters. | H2-R05, H2-R06, H2-R09 | `multiplicity_unresolved`, `unresolved_cluster` | box winding count, subdivision | synthetic, real-blocked | true |
| `certify_l3_height` | `l3_certifier.py` | Cerrar una altura independiente. | T, contours, zero boxes, winding cert | count record | `C_T` certificado. | Conteos coinciden con multiplicidad. | Alturas intermedias. | H2-R05, H2-R06, H2-R07, H2-R08 | `count_mismatch`, `boundary_not_certified_zero_free` | winding, isolated count compare | synthetic, contract, real-blocked | true |
| `certify_l3_all_heights` | `l3_certifier.py` | Coordinar H2-L3 completo. | backend, config | L3 certification | Cuatro contornos independientes. | Reporte L3 completo o bloqueo. | Four independent contours. | H2-R05, H2-R06, H2-R07, H2-R08, H2-R10 | all 006H02 fail states | all L3 backend ops | synthetic, real-blocked | true |
| `l3_zero_csv_bytes` | `serialization.py` | Serializar `l3_zeros_T500.csv`. | L3 certification | bytes | Datos canonicos. | UTF-8/LF, strings decimales. | Artefactos canonicos 006H01. | H2-R16, H2-R21 | `serialization_semantics_invalid` | none | unit, contract | false |
| `l3_reports_json_bytes` | `serialization.py` | Serializar reportes L3. | reports | bytes | Claves ordenadas, no NaN. | JSON canonico hashable. | Reportes L3 006H01/006H02. | H2-R16, H2-R21 | `hash_or_serialization_mismatch` | none | unit, contract | false |
| `preflight_006f_authorization` | `pipeline.py` | Bloquear antes de backend si falta contrato. | auth path, code hashes, runtime seal | authorization object | Directorio vacio, hashes actuales. | Backend no se construye si hay bloqueo. | 006H01 schema. | H2-R12, H2-R13, H2-R14, H2-R17, H2-R21 | `authorization_schema_invalid`, `approved_code_hash_mismatch` | none | contract, real-blocked | false |

## 5. Plan de pruebas por niveles

### 5.1 Nivel 1: pruebas unitarias puras

Sin FLINT, Arb, Acb ni backend real.

| Area | Pruebas requeridas |
| --- | --- |
| Geometria de contornos | `C_143`, `C_200`, `C_300`, `C_500`; vertices exactos; orientacion positiva; rechazo de `T_star`. |
| Cobertura de subdivisiones | Segmentos cubiertos sin huecos; profundidad maxima; identidad de subsegmentos. |
| Entero unico | Intervalos con cero, uno, dos enteros; intervalos que tocan dos enteros; prohibicion de midpoint rounding. |
| Serializacion | UTF-8, LF, JSON sorted, `allow_nan=False`, extremos como strings. |
| Fallos | Cada estado 006H02 produce cierre bloqueado/inconcluso esperado. |
| Contratos | `argument_principle.py` permanece test-only y excluido de probative runtime. |

### 5.2 Nivel 2: pruebas sinteticas con backend falso

| Area | Pruebas requeridas |
| --- | --- |
| Imagenes de contorno conocidas | Curvas con winding `0`, `1`, `2`; multiplicidad simulada. |
| Cruce de cero | Segmento cuya imagen contiene o puede contener cero debe cerrar inconcluso. |
| Incrementos ambiguos | Winding interval con cero, uno, dos o ningun entero. |
| Subdivision | Backend falso que exige biseccion antes de certificar. |
| Clusters | Dos ceros cercanos, multiplicidad mayor que uno y cluster no resuelto. |
| Alturas | Cuatro alturas independientes; una falla intermedia bloquea L3 completo. |

### 5.3 Nivel 3: pruebas de integracion real bloqueadas

Estas pruebas deben existir en una futura fase de codigo, pero marcadas como
skip/bloqueadas hasta autorizacion separada.

Reglas:

```text
requires_G5B_006F_AUTHORIZATION_json = true
requires_validated_runtime_hashes = true
requires_backend_versions = true
requires_empty_artifact_directory = true
must_not_run_by_default = true
```

Debe verificarse que:

1. la bandera de entorno sola no abre la puerta;
2. un archivo de autorizacion incompleto no abre la puerta;
3. hashes antiguos o incompletos bloquean;
4. `PythonFlintBackend` no importa FLINT al importar el paquete;
5. operaciones reales no se ejecutan sin `ExecutionAuthorization` validada.

### 5.4 Nivel 4: pruebas contractuales

| Contrato | Prueba requerida |
| --- | --- |
| 006H01 | Artefactos canonicos, estados H2 y esquema `G5B-006F-AUTHORIZATION.json`. |
| 006H02 | Contornos exactos, `T_star` prohibido, frontera libre de ceros, entero unico. |
| Sin floats probativos | Buscar `float`, `complex`, `atan2`, `round` en modulos probativos; permitir solo en tests o `argument_principle.py` sintetico. |
| Sin red | Buscar `requests`, `urllib`, sockets o comandos de red en ruta H2. |
| Sin instalacion | Buscar `pip`, instaladores o subprocess de dependencias en ruta H2. |
| Sin downstream | Pipeline no puede emitir `H2_CERTIFIED_FOR_FUTURE_005F_USE` sin reportes L3/zeta completos y 006G posterior separada. |

## 6. Matriz obligacion 006H02 a implementacion

| obligacion_006H02 | modulo_responsable | funcion_responsable | prueba_sintetica | certificado_real_futuro | estado_actual | trabajo_faltante |
| --- | --- | --- | --- | --- | --- | --- |
| `completed_function_definition` | `chi3_function.py`, `real_completed_l3.py` | `chi3_character_metadata`, `evaluate_lambda3_ball` | Runtime falso compone factor, gamma y L nativa. | `RealCompletedL3PointEvidence` probativo. | partial | Agregar metadata 006H02, raiz funcional, trazas y proof hashes. |
| `equivalence_to_target_nontrivial_zeros` | docs/proof package + `l3_certifier.py` | `validate_l3_contract_metadata` | Contract tests de metadata y no RH/GRH. | Proof package local hasheado. | missing | Incorporar cita/prueba local y hash al manifest. |
| `contour_definition` | `contour.py` | `build_l3_contours` | Verificar cuatro contornos exactos. | Contour records en `l3_completeness_report.json`. | partial | Congelar constructores nominales `C_143..C_500` y prohibir `T_star`. |
| `boundary_zero_free_certificate` | `boundary_certifier.py` | `certify_boundary_contour` | Backend falso con imagen que excluye/incluye cero. | Segment certificates por subdivision. | missing | Crear modulo, estados y reportes. |
| `segment_image_excludes_zero` | `boundary_certifier.py`, `real_segment_enclosure.py` | `certify_boundary_segment` | Whole-box fake segment. | `RealSegmentImageEvidence` probativo. | partial | Unir evidencia real con subdivision completa y separacion positiva. |
| `ball_validated_subdivision` | `boundary_certifier.py` | `subdivide_segment_cover` | Cobertura sin huecos y max depth. | Hashes por subdivision. | missing | Crear estructura de certificados por subsegmento. |
| `argument_increment_enclosures` | `argument_increment.py`, `real_argument.py` | `certify_argument_increment_local` | Incrementos conocidos y ramas invalidas. | `RealArgumentIncrementEvidence`. | partial | Separar modulo, endpoints reales y estados 006H02. |
| `total_winding_unique_integer` | `winding_certifier.py`, `real_argument.py` | `certify_unique_integer_winding` | Intervalos con 0/1/2 enteros. | `RealWindingEvidence`. | partial | Emitir reporte por altura y prohibir midpoint rounding por contrato. |
| `multiplicity_accounting` | `l3_isolator.py`, `l3_certifier.py` | `isolate_l3_zero_boxes`, `certify_l3_height` | Multiplicidad y clusters simulados. | Isolation report y count match real. | partial | Separar isolator y soportar multiplicidad exacta real. |
| `symmetry_accounting` | `l3_certifier.py`, docs/proof package | `certify_l3_all_heights` | Contract no division by symmetry. | Manifest L3 con regla de no division. | missing | Agregar validacion documental y campos de reporte. |
| `four_independent_contours` | `contour.py`, `l3_certifier.py` | `build_l3_contours`, `certify_l3_all_heights` | Una altura falla y bloquea todo. | Cuatro winding certificates. | partial | Asegurar independencia, hashes por altura y no inferencia desde T=500. |
| `no_RH_or_GRH_dependency` | `l3_certifier.py`, tests contractuales | `certify_l3_all_heights` | Cero fuera de linea critica contado. | Reporte con `critical_line_certified` separado. | partial | Reforzar tests y campos en serializacion. |

## 7. Reutilizar vs escribir desde cero

### Reutilizable

```text
models.py
config.py
chi3_function.py metadata/formulas
contour.py geometry core
ball_argument.py structural half-plane wrapping
l3_argument_count.py interval accumulation core
real_evidence.py probative evidence factory
rigorous_ball_runtime.py protocol/audit shell
real_completed_l3.py composition skeleton
real_segment_enclosure.py whole-box segment skeleton
real_argument.py real half-plane/log/winding skeleton
authorization.py hash/provenance policy shell
pipeline.py fail-closed preflight shell
serialization.py canonical byte helpers
```

### Escribir desde cero o separar en modulos nuevos

```text
boundary_certifier.py
argument_increment.py
winding_certifier.py
l3_isolator.py
l3_completed_function.py facade, if chosen instead of extending real_completed_l3.py
006H01/006H02 aware authorization schema migration
l3_completeness_report serializers
l3_isolation_report serializers
```

### Mantener como test-only o inert

```text
argument_principle.py synthetic_winding_number
completed_l3.py inert point/segment stubs
PythonFlintBackend operations until separate code authorization
run_certification_pipeline final real pipeline body until 006F
```

## 8. Orden minimo de implementacion futura

Una futura fase separada de codigo, si se autoriza, debe seguir este orden:

1. Actualizar contratos de metadata y contorno sin backend real.
2. Crear `boundary_certifier.py`, `argument_increment.py`, `winding_certifier.py`
   con backends falsos.
3. Separar `l3_isolator.py` desde `l3_certifier.py`, preservando tests existentes.
4. Alinear serializacion L3 con 006H01.
5. Migrar autorizacion/pipeline al esquema 006H01/006H02 sin ejecutar backend.
6. Solo despues, en una fase separada, implementar adaptador FLINT/Arb real.
7. Mantener pruebas reales bloqueadas hasta autorizacion 006F independiente.

## 9. Bloqueos que permanecen

```text
real_backend_operations = not_implemented
NotImplementedError_present = true
G5B_006F_authorization_schema_migration = missing
ARB_INDEPENDENT_VERSION_SEAL = unresolved
native_L_ball_semantics = pending
complex_log_branch_semantics = pending
boundary_zero_free_real_certificates = absent
winding_unique_integer_real_certificates = absent
l3_zero_tables = absent
l3_completeness_report = absent
```

## 10. Decision final 006H03

```text
L3_BACKEND_CODE_PLAN = COMPLETE
EXISTING_CODE_INVENTORY = COMPLETE
IMPLEMENTATION_TASKS_DEFINED = true
SYNTHETIC_TEST_PLAN_DEFINED = true
REAL_INTEGRATION_REMAINS_BLOCKED = true
L3_READY_FOR_SEPARATE_CODE_AUTHORIZATION = true
L3_READY_FOR_REAL_EXECUTION = false
NEXT_PHASE_AUTHORIZED = false
```

Interpretacion:

```text
L3_READY_FOR_SEPARATE_CODE_AUTHORIZATION = true
```

significa que ya existe un mapa tecnico suficiente para que el usuario autorice
otra fase de implementacion separada. No autoriza esa fase.

```text
L3_READY_FOR_REAL_EXECUTION = false
```

queda fijado porque faltan implementacion backend real, sello Arb/Acb, pruebas
reales bloqueadas, certificados de frontera, certificados de winding y
autorizacion 006F.

## 11. Prohibiciones 006H03

```text
CODE_MODIFIED = false
TESTS_EXECUTED = false
FLINT_EXECUTED = false
ARB_EXECUTED = false
ACB_EXECUTED = false
CHI_L_FUNCTION_CALLED = false
LAMBDA_3_EVALUATED = false
CONTOURS_EXECUTED = false
ZEROS_ISOLATED = false
ZEROS_COUNTED = false
ZERO_TABLES_CREATED = false
NETWORK_USED = false
DEPENDENCIES_INSTALLED = false
H2_OPENED = false
006F_OPENED = false
DOWNSTREAM_AUTHORIZED = false
IMPLEMENTATION_AUTHORIZED = false
H2_PROOF_CLAIMED = false
NOVELTY_CLAIMED = false
```

Resultado:

```text
006H03_RESULT =
006H03_L3_BACKEND_COMPLETION_CODE_PLAN_COMPLETED
```
