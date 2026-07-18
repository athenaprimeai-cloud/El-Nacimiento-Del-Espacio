# Experimento 006C: plan de implementacion del certificador H2

> **Para agentes ejecutores:** SUB-SKILL OBLIGATORIA EN UNA FASE AUTORIZADA:
> usar `superpowers:test-driven-development` y
> `superpowers:subagent-driven-development` o `superpowers:executing-plans`.
> Este documento no autoriza ejecutar ninguno de sus pasos.

**Objetivo:** disenar la construccion de un certificador H2 que produzca, en
una fase posterior, aislamiento riguroso de cada cero y conteo completo de
`zeta(s)` y `L(s,chi_3)` hasta altura `T=500`.

**Arquitectura:** un paquete Python aislado separara modelos inmutables,
aritmetica de bolas, certificacion de zeta, evaluacion de `L3`, conteo por
principio del argumento, aislamiento, validacion y serializacion. Los tests de
la fase de codigo usaran backends falsos y funciones sinteticas; el backend
FLINT real quedara detras de una autorizacion de ejecucion separada.

**Stack previsto:** Python 3.12, biblioteca estandar, `unittest`,
`python-flint==0.8.0` con FLINT 3.3.1 incluido en sus ruedas, SHA-256 y formatos
CSV/JSON canonicos.

---

## 1. Estado y limites de 006C

```text
experiment_id = G5B-006C
target = H2_zero_certifier_implementation_plan
status = implementation_plan_only
code_authorization = pending
execution_authorization = false
zero_tables = not_generated
artifacts = none
tests_executed = none
rerun = false
novelty_claim = false
005F = frozen_protocol_only
006A = H3_resolved_as_exact_zero
006B = frozen_zero_certification_protocol_only
C05 = provisional_quarantined
C05_RERUN = forbidden
C35 = frozen
C15 = frozen
```

006C describe archivos, interfaces, algoritmos, pruebas y puertas de seguridad.
No crea codigo, no instala dependencias, no calcula ceros y no genera tablas.

La regla heredada de 006B es inalterable:

```text
Certificacion H2
= aislamiento riguroso de cada cero
+ conteo completo hasta T=500.
```

## 2. Decisiones arquitectonicas

### 2.1 Opcion seleccionada

Se usara una arquitectura Python con backend intercambiable:

```text
dominio y validacion puros
        |
        +-- FakeBallBackend para tests estructurales 006D
        |
        +-- PythonFlintBackend para ejecucion real 006F
```

Ventajas:

1. sigue el lenguaje y el estilo `unittest` del repositorio;
2. permite probar toda la logica sin calcular ceros reales;
3. evita enlazar manualmente una DLL de FLINT mediante `ctypes`;
4. aprovecha las bolas rigurosas, `acb.zeta_zero`, caracteres de Dirichlet,
   `hardy_z`, `l_function` e integracion validada de python-flint;
5. mantiene el motor numerico fuera de la logica de aceptacion.

### 2.2 Alternativas descartadas

**Ejecutable C directo contra FLINT:** ofrece acceso total a la API C, pero
introduce compilador, ABI, cabeceras y empaquetado especifico de Windows antes
de demostrar que el enlace Python cubre la altura 500.

**SageMath/LMFDB como generador:** facilitaria listas exploratorias, pero no
proporciona por si solo el paquete autocontenido de intervalos y completitud
exigido por 006B.

Si durante 006D se demuestra documentalmente que python-flint no expone una
operacion indispensable, el codigo debera detenerse y solicitar una revision de
006C. No se introducira `ctypes`, CFFI ni un ejecutable C sin una nueva
autorizacion.

## 3. Estructura futura de archivos

La fase 006D, si se autoriza, podra crear exclusivamente:

```text
requirements-h2-certifier.txt

athena_azr/h2_zero_certifier/
    __init__.py
    models.py
    config.py
    authorization.py
    backend.py
    python_flint_backend.py
    zeta_certifier.py
    chi3_function.py
    argument_principle.py
    l3_certifier.py
    validation.py
    serialization.py
    pipeline.py

scripts/
    run_h2_zero_certification.py

tests/
    test_h2_models.py
    test_h2_authorization.py
    test_h2_zeta_certifier.py
    test_h2_argument_principle.py
    test_h2_l3_certifier.py
    test_h2_validation.py
    test_h2_serialization.py
    test_h2_pipeline_guard.py

tests/fixtures/h2_zero_certifier/
    synthetic_zeta_intervals.json
    synthetic_l3_boxes.json
    invalid_overlapping_intervals.json
    fake_execution_authorization.json
```

Responsabilidades:

| Archivo | Responsabilidad unica |
| --- | --- |
| `models.py` | tipos inmutables de intervalos, cajas, ceros, conteos y paquetes |
| `config.py` | parametros congelados y validacion de configuracion |
| `authorization.py` | bloqueo de ejecucion y verificacion de hashes |
| `backend.py` | protocolo abstracto del motor de bolas |
| `python_flint_backend.py` | adaptador perezoso a python-flint |
| `zeta_certifier.py` | aislamiento y completitud del canal zeta |
| `chi3_function.py` | definicion certificada de chi3, L3 y Lambda3 |
| `argument_principle.py` | conteo riguroso en contornos y cajas sinteticas/reales |
| `l3_certifier.py` | aislamiento de L3 y concordancia con conteo global |
| `validation.py` | reglas 006B sin acceso a FLINT ni disco |
| `serialization.py` | CSV/JSON canonicos y SHA-256 |
| `pipeline.py` | orquestacion sin argumentos numericos ocultos |
| `run_h2_zero_certification.py` | CLI bloqueada por autorizacion 006F |

No se modificaran los modulos historicos de C00, C03, C03-B o C05.

## 4. Contratos de dominio

### 4.1 Intervalos y cajas

`models.py` definira dataclasses congeladas con extremos decimales almacenados
como cadenas canonicas. No se serializaran `float` binarios.

```python
@dataclass(frozen=True)
class RealInterval:
    lower: str
    upper: str

    def width_decimal(self) -> Decimal: ...
    def contains_decimal(self, value: Decimal) -> bool: ...
    def is_disjoint_from(self, other: "RealInterval") -> bool: ...


@dataclass(frozen=True)
class ComplexBox:
    real: RealInterval
    imag: RealInterval
```

### 4.2 Certificado individual

```python
@dataclass(frozen=True)
class ZeroCertificate:
    index: int
    function_id: Literal["zeta", "L3"]
    conductor: int
    character_id: str
    parity: int
    box: ComplexBox
    multiplicity: int
    isolation_method: str
    working_precision_bits: int
    certificate_reference: str
    critical_line_certified: bool
```

Aunque el CSV final autorizado por 006B presenta principalmente la altura, el
modelo interno conservara tambien el intervalo real. Para L3 no se descartara
informacion que pudiera revelar un cero fuera de la recta critica.

### 4.3 Certificado de conteo

```python
@dataclass(frozen=True)
class CountCertificate:
    function_id: Literal["zeta", "L3"]
    requested_height: int
    counting_boundary: str
    boundary_zero_free: bool
    certified_total_count: int
    isolated_count_with_multiplicity: int
    counting_method: str
    working_precision_bits: int
    parameters: Mapping[str, str]

    @property
    def counts_match(self) -> bool: ...
```

### 4.4 Resultado global

```python
@dataclass(frozen=True)
class CertificationBundle:
    protocol_sha256: str
    dependency_versions: Mapping[str, str]
    zeros: tuple[ZeroCertificate, ...]
    counts: tuple[CountCertificate, ...]
    protected_hashes: Mapping[str, str]
    cross_references: tuple[CrossReferenceResult, ...]
```

Los constructores rechazaran intervalos invertidos, multiplicidades no
positivas, indices repetidos y precisiones no positivas.

## 5. Configuracion congelada

`config.py` no permitira parametros libres desde la linea de comandos salvo
rutas de entrada/salida y ruta de autorizacion.

```python
REQUESTED_HEIGHTS = (143, 200, 300, 500)
MAX_HEIGHT = 500
TARGET_INTERVAL_WIDTH = Decimal("1e-20")
INITIAL_PRECISION_BITS = 192
PRECISION_STEPS_BITS = (192, 256, 384, 512, 768, 1024)
L3_CONDUCTOR = 3
L3_CONREY_NUMBER = 2
L3_PARITY = 1
CONTOUR_SIGMA_LEFT = Decimal("-0.5")
CONTOUR_SIGMA_RIGHT = Decimal("1.5")
MAX_CONTOUR_DEPTH = 40
MAX_ROOT_ISOLATION_DEPTH = 60
```

Los valores de precision son techos de trabajo, no afirmaciones de suficiencia.
Si `1024` bits no resuelve una frontera, intervalo o multiplicidad, la salida
sera `inconclusive`; no se ampliara el limite despues de observar resultados.

## 6. Backend riguroso

`backend.py` definira un `Protocol` sin importar FLINT:

```python
class BallBackend(Protocol):
    def metadata(self) -> Mapping[str, str]: ...
    def zeta_zero(self, index: int, precision_bits: int) -> ComplexBox: ...
    def chi3_hardy_z(self, t: RealInterval, precision_bits: int) -> ComplexBox: ...
    def chi3_completed_l(self, s: ComplexBox, precision_bits: int) -> ComplexBox: ...
```

`python_flint_backend.py` importara `flint` solamente cuando una instancia real
sea construida despues de superar `authorization.py`. Importar el paquete
`athena_azr.h2_zero_certifier` no podra cargar FLINT ni iniciar calculos.

La version prevista queda fijada en:

```text
python-flint==0.8.0
embedded FLINT expected by wheel = 3.3.1
```

La fase 006E debera verificar las versiones reales expuestas por el entorno y
rechazar cualquier diferencia antes de pedir 006F.

## 7. Guardia de autorizacion

`authorization.py` sera llamado antes de construir el backend real o crear el
directorio de salida.

La futura autorizacion 006F debera ser un JSON separado con, al menos:

```json
{
  "experiment_id": "G5B-006F",
  "execution_authorized": true,
  "max_height": 500,
  "requested_heights": [143, 200, 300, 500],
  "protocol_006b_sha256": "4f110d0926067e9e1eb44cbbfe78ee1acc93f85f526176c81d98446eafd492cb",
  "plan_006c_sha256_pattern": "^[0-9a-f]{64}$",
  "approved_code_hashes": {},
  "output_directory": "artifacts/goldbach_cesaro/c03b_h2_zero_certification"
}
```

El archivo real de 006F usara la clave `plan_006c_sha256` con el hash literal
congelado; el sufijo `_pattern` solo expresa la regla dentro de este esquema no
ejecutable. 006D debera probar que cualquier autorizacion incompleta, falsa, vencida,
incompatible o con hashes distintos falla antes de llamar al backend.

## 8. Certificador zeta

### 8.1 Algoritmo

`zeta_certifier.py` usara la operacion rigurosa que devuelve el n-esimo cero no
trivial de zeta. El algoritmo futuro sera:

1. solicitar ceros consecutivos desde `n=1`;
2. refinar cada bola hasta ancho imaginario `<=1e-20`;
3. detenerse solo cuando el extremo inferior del siguiente cero sea mayor que
   `500`;
4. verificar orden estricto y disjuncion;
5. para cada altura, exigir que ningun intervalo la atraviese;
6. derivar el conteo del indice certificado del ultimo cero bajo la altura;
7. comprobar que el siguiente indice queda rigurosamente por encima.

El uso de `acb.zeta_zero(n)` es admisible porque FLINT documenta que entrega el
n-esimo cero mediante aislamiento y metodos de Turing. No se aceptara buscar
minimos de `|zeta|` ni usar valores de mpmath como certificado.

### 8.2 Contrato

```python
def certify_zeta(
    backend: BallBackend,
    config: CertificationConfig,
) -> FunctionCertification:
    """Return consecutive isolated zeros and counts at all frozen heights."""
```

Si una bola atraviesa una altura solicitada, se refinara usando la siguiente
precision congelada. Si sigue atravesandola a 1024 bits, el proceso fallara.

## 9. Funcion completada L3

`chi3_function.py` fijara el caracter `dirichlet_char(3, 2)` y verificara antes
de usarlo:

```text
modulus = 3
conductor = 3
number = 2
primitive = true
real = true
principal = false
parity = 1
```

La evaluacion principal usara la funcion de Dirichlet de python-flint. Como
control interno independiente, en puntos preregistrados se comparara con:

```text
L(s,chi_3) = 3^(-s) [HurwitzZeta(s,1/3) - HurwitzZeta(s,2/3)].
```

La funcion completada sera:

```text
Lambda_3(s)
= (3/pi)^((s+1)/2) Gamma((s+1)/2) L(s,chi_3).
```

No se evaluara mediante logaritmos con ramas ocultas sobre el contorno. Las
potencias y Gamma deberan usar las opciones analiticas de FLINT cuando el
backend reciba una caja compleja.

## 10. Conteo L3 por principio del argumento

### 10.1 Region

Para cada altura solicitada se contaran ceros dentro del rectangulo:

```text
-1/2 < Re(s) < 3/2
0 < Im(s) < T.
```

El borde inferior forma parte del contorno y debera certificarse libre de
ceros. El borde superior se usara solo si esta certificado libre de ceros. Las
fronteras verticales incluyen toda la franja critica y excluyen los ceros
triviales negativos del caracter impar.

### 10.2 Algoritmo de contorno

`argument_principle.py` implementara subdivisiones adaptativas de cada lado:

1. evaluar `Lambda_3` sobre una caja que encierre el segmento completo;
2. exigir que la imagen no contenga el origen;
3. exigir una variacion angular local menor que `pi/4`;
4. subdividir si cualquiera de las dos condiciones no queda certificada;
5. sumar incrementos de argumento con una rama continua local;
6. encerrar el total dividido por `2*pi`;
7. aceptar un conteo solo si el intervalo contiene un unico entero.

Contrato:

```python
def certified_winding_number(
    function: CertifiedComplexFunction,
    contour: RectangularContour,
    config: ContourConfig,
) -> WindingCertificate:
    """Certify a unique integer winding number or raise InconclusiveCount."""
```

No se redondeara un valor aproximado del cambio de argumento. Un intervalo que
contenga dos enteros, una imagen que pueda contener cero o el agotamiento de
profundidad producen `InconclusiveCount`.

## 11. Aislamiento individual L3

`l3_certifier.py` separara dos pruebas independientes:

1. **Aislamiento:** particionar la recta critica y certificar cajas con un unico
   cero usando Hardy Z, intervalos y refinamiento.
2. **Completitud:** comparar la suma de multiplicidades aisladas con el conteo
   del principio del argumento en toda la franja.

Los cambios de signo sirven para proponer intervalos, no para demostrar que no
faltan ceros. El particionado debera tambien certificar regiones sin cero. Una
multiplicidad par o un grupo que no pueda separarse producira
`unresolved_cluster` y fallara H2.

Para certificar que un cero aislado esta sobre la recta critica, se usara una
caja simetrica respecto de `Re(s)=1/2`. Si la caja contiene exactamente un cero,
la simetria funcional `rho -> 1-conjugate(rho)` fuerza que ese cero sea fijo por
la simetria. No se declarara `critical_line_certified=true` solo porque el punto
medio numerico tenga parte real `0.5`.

Contrato:

```python
def certify_l3(
    backend: BallBackend,
    config: CertificationConfig,
) -> FunctionCertification:
    """Isolate L3 zeros and match them to independent strip counts."""
```

La aceptacion exige igualdad de conteos en `143`, `200`, `300` y `500`.

## 12. Validacion pura

`validation.py` recibira objetos de dominio y devolvera una lista exhaustiva de
errores; no accedera a FLINT ni al sistema de archivos.

Reglas obligatorias:

```text
interval_width <= 1e-20
intervals_pairwise_disjoint = true
ordering_certified = true
unique_zero_in_interval = true
multiplicity >= 1
boundary_zero_free = true
certified_total_count = isolated_count_with_multiplicity
counts_close_at = [143, 200, 300, 500]
unresolved_clusters = 0
```

El validador rechazara:

1. indices duplicados o con huecos;
2. intervalos que atraviesan una altura congelada;
3. conteos decrecientes;
4. cajas L3 sin prueba de simetria o unicidad;
5. metadatos de dependencia incompletos;
6. referencias externas usadas como metodo primario;
7. cualquier estado distinto de `complete` para una funcion.

## 13. Serializacion y manifiesto

`serialization.py` implementara escritura atomica en un directorio temporal y
renombrado final solo despues de validar todo el paquete.

Archivos futuros, no creados en 006D:

```text
zeta_zeros_T500.csv
l3_zeros_T500.csv
zeta_isolation_report.json
l3_isolation_report.json
zeta_completeness_report.json
l3_completeness_report.json
H2_ZERO_CERTIFICATION_MANIFEST.json
```

Reglas:

```text
encoding = UTF-8
newlines = LF
csv_header = fixed
json_keys = sorted
json_separators = [",", ":"]
allow_nan = false
hash = SHA-256 over final bytes
```

Si la certificacion queda inconclusa, se podra escribir un reporte de fallo en
un directorio temporal de diagnostico solo si 006F lo autoriza expresamente;
nunca se escribiran tablas parciales con nombres finales.

## 14. Referencias cruzadas

Odlyzko y LMFDB se descargaran unicamente durante 006F, se conservaran como
copias locales hasheadas y se compararan despues de cerrar los certificados
internos.

La comparacion no podra modificar intervalos. Un desacuerdo devolvera:

```text
cross_reference_status = disagreement
H2_certification_status = failed_pending_review
```

Los tests 006D usaran fixtures sinteticos con nombres que no puedan confundirse
con copias reales de Odlyzko o LMFDB.

## 15. CLI futura y bloqueo fisico

`scripts/run_h2_zero_certification.py` aceptara solo:

```text
--authorization PATH
--output-dir PATH
--dry-validate-config
```

No aceptara `--max-height`, precisiones, profundidades ni caracter desde la
linea de comandos. Esos valores estan congelados en `config.py`.

Orden obligatorio de `main()`:

```text
1. leer autorizacion
2. validar protocolo, plan y hashes de codigo
3. comprobar directorio de salida vacio/inexistente
4. comprobar dependencias y versiones
5. construir PythonFlintBackend
6. certificar zeta
7. certificar L3
8. validar paquete completo
9. contrastar fuentes externas
10. serializar atomicamente
```

Los pasos 5-10 no podran alcanzarse con `execution_authorized=false`.
`--dry-validate-config` solo validara constantes y hashes; no importara FLINT.

## 16. Estrategia de pruebas para 006D

006D podra autorizar codigo y ejecucion de pruebas estructurales exclusivamente.
Ningun test llamara `acb.zeta_zero`, `chi.hardy_z`, `chi.l_function`,
`acb.integral`, red ni fuentes externas.

Las pruebas usaran:

1. un backend falso con intervalos predeterminados;
2. funciones sinteticas como `f(s)=s-rho` y polinomios de raices conocidas;
3. directorios temporales;
4. autorizaciones falsas que deben ser rechazadas;
5. serializacion de paquetes sinteticos pequenos.

Las pruebas de integracion real se escribiran marcadas y bloqueadas:

```python
@unittest.skipUnless(
    os.environ.get("ATHENA_H2_EXECUTION_AUTHORIZED") == "1",
    "requires separate 006F execution authorization",
)
class RealFlintCertificationTests(unittest.TestCase):
    ...
```

La variable de entorno por si sola no autorizara nada; el runner tambien
exigira el JSON 006F y los hashes correctos.

## 17. Tareas futuras de implementacion 006D

Cada tarea queda descrita para ejecucion TDD posterior. En este documento todas
las casillas permanecen sin marcar.

### Tarea 1: dependencia y paquete vacio

**Archivos:**

- Crear: `requirements-h2-certifier.txt`
- Crear: `athena_azr/h2_zero_certifier/__init__.py`

- [ ] Escribir un test que compruebe que importar el paquete no importa
  `flint` ni accede al disco.
- [ ] Ejecutar el test y comprobar que falla antes de crear el paquete.
- [ ] Fijar `python-flint==0.8.0` y exportaciones minimas sin efectos laterales.
- [ ] Ejecutar el test y comprobar que pasa.
- [ ] Registrar hashes del checkpoint; el workspace no es un repositorio Git y
  no se inventara un commit inexistente.

### Tarea 2: modelos inmutables

**Archivos:**

- Crear: `athena_azr/h2_zero_certifier/models.py`
- Crear: `tests/test_h2_models.py`

- [ ] Escribir tests de intervalos validos, invertidos, disjuntos y solapados.
- [ ] Escribir tests de multiplicidad, indices y `counts_match`.
- [ ] Ejecutar los tests y verificar fallos por simbolos ausentes.
- [ ] Implementar las dataclasses y validaciones minimas.
- [ ] Ejecutar los tests y verificar que pasan.
- [ ] Registrar hashes del checkpoint.

### Tarea 3: configuracion congelada

**Archivos:**

- Crear: `athena_azr/h2_zero_certifier/config.py`
- Ampliar: `tests/test_h2_models.py`

- [ ] Escribir tests que exijan exactamente alturas, ancho, precisiones,
  conductor, numero Conrey y limites de profundidad fijados en 006C.
- [ ] Ejecutar los tests y verificar que fallan.
- [ ] Implementar `CertificationConfig.frozen_default()` sin overrides
  numericos externos.
- [ ] Ejecutar los tests y verificar que pasan.
- [ ] Registrar hashes del checkpoint.

### Tarea 4: guardia de autorizacion

**Archivos:**

- Crear: `athena_azr/h2_zero_certifier/authorization.py`
- Crear: `tests/test_h2_authorization.py`
- Usar fixture: `tests/fixtures/h2_zero_certifier/fake_execution_authorization.json`

- [ ] Escribir tests para autorizacion ausente, falsa, hash incorrecto, ruta de
  salida incorrecta y campos adicionales no permitidos.
- [ ] Ejecutar y verificar fallos iniciales.
- [ ] Implementar parser estricto, hashes y `ExecutionNotAuthorized`.
- [ ] Ejecutar y verificar que todos los casos negativos pasan.
- [ ] Probar que el backend falso no recibe llamadas cuando la guardia falla.
- [ ] Registrar hashes del checkpoint.

### Tarea 5: interfaz de backend y backend falso

**Archivos:**

- Crear: `athena_azr/h2_zero_certifier/backend.py`
- Crear fixtures sinteticos de intervalos zeta y cajas L3.
- Ampliar: `tests/test_h2_zeta_certifier.py`

- [ ] Escribir tests del contrato `BallBackend` mediante un fake determinista.
- [ ] Ejecutar y verificar fallos iniciales.
- [ ] Implementar protocolo, errores y fake solo dentro de tests.
- [ ] Verificar que ningun test importa python-flint.
- [ ] Registrar hashes del checkpoint.

### Tarea 6: adaptador python-flint perezoso

**Archivos:**

- Crear: `athena_azr/h2_zero_certifier/python_flint_backend.py`
- Ampliar: `tests/test_h2_pipeline_guard.py`

- [ ] Escribir tests con importacion simulada para verificar que FLINT se carga
  solo despues de autorizacion valida.
- [ ] Ejecutar y verificar el fallo inicial.
- [ ] Implementar el adaptador y conversiones `arb/acb -> RealInterval/ComplexBox`.
- [ ] No llamar funciones matematicas reales en 006D.
- [ ] Ejecutar tests estructurales y registrar hashes.

### Tarea 7: certificador zeta con fake

**Archivos:**

- Crear: `athena_azr/h2_zero_certifier/zeta_certifier.py`
- Crear: `tests/test_h2_zeta_certifier.py`

- [ ] Probar secuencia consecutiva, refinamiento, siguiente cero sobre 500,
  cierre de cuatro alturas y fallo por intervalo atravesando frontera.
- [ ] Ejecutar y verificar fallos iniciales.
- [ ] Implementar `certify_zeta` contra `BallBackend`.
- [ ] Verificar que los tests pasan solo con datos sinteticos.
- [ ] Registrar hashes del checkpoint.

### Tarea 8: definicion L3

**Archivos:**

- Crear: `athena_azr/h2_zero_certifier/chi3_function.py`
- Crear: `tests/test_h2_l3_certifier.py`

- [ ] Probar metadatos exactos del caracter mediante fake.
- [ ] Probar que una discrepancia entre evaluacion principal y Hurwitz cancela
  la certificacion.
- [ ] Implementar interfaces para `L3`, `Lambda3` y Hardy Z sin evaluarlas en
  tests reales.
- [ ] Ejecutar pruebas sinteticas y registrar hashes.

### Tarea 9: principio del argumento sintetico

**Archivos:**

- Crear: `athena_azr/h2_zero_certifier/argument_principle.py`
- Crear: `tests/test_h2_argument_principle.py`

- [ ] Probar conteos 0, 1, 2 y multiplicidad 2 con polinomios sinteticos.
- [ ] Probar fallo cuando la frontera contiene una raiz o el intervalo angular
  contiene mas de un entero.
- [ ] Implementar subdivisiones, acumulacion angular y cierre entero riguroso.
- [ ] Ejecutar tests sinteticos y registrar hashes.

### Tarea 10: certificador L3 con backends falsos

**Archivos:**

- Crear: `athena_azr/h2_zero_certifier/l3_certifier.py`
- Ampliar: `tests/test_h2_l3_certifier.py`

- [ ] Probar aislamiento completo, conteo coincidente, conteo discrepante,
  grupo no resuelto y simetria insuficiente.
- [ ] Implementar `certify_l3` sin asumir GRH.
- [ ] Exigir igualdad en las cuatro alturas.
- [ ] Ejecutar tests sinteticos y registrar hashes.

### Tarea 11: validador global

**Archivos:**

- Crear: `athena_azr/h2_zero_certifier/validation.py`
- Crear: `tests/test_h2_validation.py`
- Usar: `invalid_overlapping_intervals.json`

- [ ] Escribir un test por cada criterio de la seccion 14 de 006B.
- [ ] Ejecutar y verificar fallos iniciales.
- [ ] Implementar validacion exhaustiva sin salida temprana.
- [ ] Verificar que un solo error mantiene `H2` no certificado.
- [ ] Registrar hashes del checkpoint.

### Tarea 12: serializacion canonica

**Archivos:**

- Crear: `athena_azr/h2_zero_certifier/serialization.py`
- Crear: `tests/test_h2_serialization.py`

- [ ] Probar bytes exactos, LF, orden de claves, ausencia de NaN, escritura
  atomica, hashes y rechazo de paquetes parciales.
- [ ] Ejecutar y verificar fallos iniciales.
- [ ] Implementar serializadores sobre directorios temporales.
- [ ] Confirmar que ningun test escribe en `artifacts/`.
- [ ] Registrar hashes del checkpoint.

### Tarea 13: pipeline y CLI bloqueada

**Archivos:**

- Crear: `athena_azr/h2_zero_certifier/pipeline.py`
- Crear: `scripts/run_h2_zero_certification.py`
- Crear: `tests/test_h2_pipeline_guard.py`

- [ ] Probar que la CLI sin autorizacion termina antes de importar FLINT y antes
  de crear el directorio de salida.
- [ ] Probar que `--dry-validate-config` no ejecuta matematica.
- [ ] Implementar el orden fijo de diez pasos de la seccion 15.
- [ ] Mantener las llamadas reales detras de la guardia 006F.
- [ ] Ejecutar solo tests estructurales y registrar hashes.

### Tarea 14: auditoria de aislamiento

**Archivos:**

- Revisar todos los archivos creados por 006D.
- No crear tablas ni reportes finales.

- [ ] Buscar importaciones de C03-B, C05, red o escritura fuera de temporales.
- [ ] Verificar que no existen constantes de ceros reales en codigo o fixtures.
- [ ] Verificar que las pruebas reales estan saltadas y doblemente bloqueadas.
- [ ] Ejecutar la suite estructural completa autorizada por 006D.
- [ ] Registrar lista y SHA-256 de todo el codigo para la revision 006E.

## 18. Comandos futuros de 006D

Estos comandos son parte del plan y no se ejecutan en 006C:

```powershell
python -m unittest tests.test_h2_models tests.test_h2_authorization tests.test_h2_zeta_certifier tests.test_h2_argument_principle tests.test_h2_l3_certifier tests.test_h2_validation tests.test_h2_serialization tests.test_h2_pipeline_guard -v
```

Resultado esperado en 006D:

```text
tests estructurales = passed
real_flint_calls = 0
real_zero_tables = 0
artifacts_written = 0
protected_files_modified = 0
```

No se ejecutara la suite historica completa sin que 006D lo autorice
explicitamente, porque ejecutar pruebas tambien es una accion separada del mero
permiso de escribir codigo.

## 19. Revision 006E

006E debera revisar antes de autorizar cualquier calculo:

1. correspondencia literal entre 006B, 006C y el codigo;
2. ausencia de parametros ajustables no preregistrados;
3. pereza real de importacion y construccion de FLINT;
4. cierre de la guardia antes de todo efecto lateral;
5. cobertura de fallos y estados inconclusos;
6. ninguna tabla, frecuencia o conteo real incrustado;
7. hashes de codigo, tests y dependencias;
8. inmutabilidad de 005F, 006A, 006B, C03-B y C05;
9. viabilidad matematica del principio del argumento para L3;
10. suficiencia de los tests sinteticos sin confundirlos con certificacion.

Si la auditoria descubre que el algoritmo L3 no puede certificar la variacion
angular o la frontera con la API publica disponible, 006E devolvera
`implementation_not_ready`; no se autorizara 006F.

## 20. Ejecucion 006F y revision 006G

006F sera la primera fase que podra:

1. instalar o cargar python-flint en el entorno autorizado;
2. invocar operaciones matematicas rigurosas;
3. descargar copias de contraste de Odlyzko y LMFDB;
4. generar las tablas y reportes previstos;
5. crear el manifiesto final.

006F necesitara un JSON de autorizacion independiente, posterior a 006E y con
todos los hashes aprobados. Una ejecucion inconclusa no se repetira cambiando
parametros: cualquier cambio requerira un nuevo protocolo.

006G revisara conteos, intervalos, procedencia, referencias cruzadas y hashes.
Solo 006G podra declarar:

```text
H2 = certified_for_future_005F_use
```

Incluso entonces, 005F no se ejecutara automaticamente y C05 seguira bloqueado.

## 21. Criterios de aceptacion de 006C

El plan queda listo para revision si:

1. cada requisito de 006B tiene un modulo y una prueba futura identificables;
2. zeta y L3 tienen conteos independientes de sus aislamientos;
3. no se asume RH ni GRH;
4. el backend real no puede construirse antes de la guardia;
5. 006D no calcula ceros reales;
6. 006F y 006G permanecen como autorizaciones posteriores;
7. no se modifica ni desbloquea ningun experimento existente;
8. no se crea ningun artefacto experimental durante 006C.

## 22. Estado final

```text
experiment_id = G5B-006C
target = H2_zero_certifier_implementation_plan
status = implementation_plan_only
architecture = isolated_python_package_with_rigorous_ball_backend
code_authorization = pending
execution_authorization = false
zero_tables = not_generated
artifacts = none
tests_executed = none
rerun = false
novelty_claim = false
006D = future_code_authorization
006E = future_code_review
006F = future_execution_authorization
006G = future_table_review_and_freeze
005F = frozen_protocol_only
006A = H3_resolved_as_exact_zero
006B = frozen_zero_certification_protocol_only
C05 = provisional_quarantined
C05_RERUN = forbidden
C35 = frozen
C15 = frozen
```

## Referencias tecnicas

1. Protocolo H2 congelado:
   `docs/experimentos/experimento-006b-c03b-protocolo-certificacion-ceros-500.md`.
2. python-flint 0.8.0,
   [documentacion de `acb`](https://python-flint.readthedocs.io/en/latest/acb.html),
   para bolas complejas, integracion validada y ceros de zeta.
3. python-flint 0.8.0,
   [caracteres de Dirichlet](https://python-flint.readthedocs.io/en/latest/dirichlet.html),
   para `dirichlet_char`, `hardy_z` y `l_function`.
4. FLINT,
   [acb_dirichlet.h](https://flintlib.org/doc/acb_dirichlet.html), para la base
   rigurosa de aislamiento y Turing usada por los ceros de zeta.
