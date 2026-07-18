# Plan de Implementacion Inerte del Backend Matematico Real L3

> **Para trabajadores agenticos:** SUB-HABILIDAD OBLIGATORIA: usar `superpowers:subagent-driven-development` (recomendado) o `superpowers:executing-plans` para ejecutar este plan tarea por tarea. Los pasos usan casillas `- [ ]` para seguimiento.

**Objetivo:** Construir, en una futura fase autorizada, la arquitectura probatoria real definida por 006E6 usando una API falsa de bolas inclusivas, sin importar FLINT real, recorrer contornos reales ni calcular ceros.

**Arquitectura:** Los certificados reales serán tipos opacos separados de los fixtures sintéticos. Un adaptador de operaciones de bolas inyectable implementará la ruta nativa de `L(s,chi_3)`, la evaluación de `Lambda_3`, la imagen rectangular completa de segmentos, la separación por semiplano y el incremento de argumento. `PythonFlintBackend` seguirá bloqueado; la fase solo demostrará contratos y flujo de datos con un `FakeRigorousBallRuntime` determinista.

**Tecnologías:** Python 3, `dataclasses`, `Decimal`, `unittest`, SHA-256, contratos `Protocol`; sin red, sin FLINT real y sin escritura en `artifacts/`.

---

## 1. Estado y límites de 006E7

```text
experiment_id = G5B-006E7
status = inert_real_backend_tdd_plan_only
006E6_SHA256 = dbfcda51f1edca9efc502ab9de9ab7cd470bdf3f3f70ff5ce758767fe7acdbca
code_authorization = false
execution_authorization = false
real_flint_import = forbidden
real_flint_execution = forbidden
real_contour_execution = forbidden
zero_certification = forbidden
zero_tables = not_generated
artifacts = none
network = forbidden
H2_certified = false
006F = blocked
C05_RERUN = forbidden
C35 = frozen
C15 = frozen
novelty_claim = false
```

Este documento contiene un plan ejecutable futuro, no autorización para
modificar código. La futura fase de código deberá recibir un identificador
separado y una autorización explícita.

El espacio de trabajo no es un repositorio Git. Por eso cada tarea sustituye
el paso de commit por un punto de control SHA-256 de los archivos modificados.

## 2. Mapa de archivos futuro

**Crear:**

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

**Modificar:**

```text
athena_azr/h2_zero_certifier/backend.py
athena_azr/h2_zero_certifier/python_flint_backend.py
athena_azr/h2_zero_certifier/authorization.py
athena_azr/h2_zero_certifier/pipeline.py
tests/test_h2_pipeline_guard.py
tests/test_h2_real_flint_guarded.py
```

Responsabilidades:

1. `real_evidence.py`: tipos opacos y procedencia de evidencia real;
2. `rigorous_ball_runtime.py`: protocolo mínimo de bolas, sin importar FLINT;
3. `real_completed_l3.py`: composición nativa de `Lambda_3`;
4. `real_segment_enclosure.py`: caja completa de segmento y evaluación inclusiva;
5. `real_argument.py`: semiplano, logaritmo, suma angular y entero único;
6. `python_flint_backend.py`: adaptador aún inerte que no implementa operaciones;
7. `pipeline.py`: guardias que impiden mezclar evidencia sintética y real.

## 3. Convenciones obligatorias

1. Ningún módulo nuevo importará `flint`.
2. Ningún test instalará, importará o simulará el módulo `flint` real.
3. La API falsa operará con cadenas decimales y objetos inmutables.
4. Ningún dato probatorio se convertirá a `float` o `complex` de Python.
5. La ruta principal de L será `native_entire_Dirichlet_L`.
6. La envolvente principal será `whole_rectangular_complex_ball`.
7. Hurwitz regularizada y Taylor permanecerán fuera del código principal.
8. La única salida permitida durante pruebas serán directorios temporales.
9. `argument_principle.py`, basado en flotantes sintéticos, no podrá ser
   importado por ningún módulo real.
10. Todo fallo de contrato devolverá excepción inconclusa; nunca conteo cero.

### Tarea 1: Crear tipos opacos de evidencia real

**Archivos:**
- Crear: `athena_azr/h2_zero_certifier/real_evidence.py`
- Crear: `tests/test_h2_real_evidence.py`

- [ ] **Paso 1: escribir la prueba roja de construcción no autorizada**

```python
def test_real_evidence_cannot_be_constructed_without_factory_capability():
    with self.assertRaises(InvalidRealEvidence):
        RealCompletedL3PointEvidence(
            value=ComplexBallRecord("1", "2", "3", "4"),
            precision_bits=192,
            backend_id="fake",
            authorization_digest="a" * 64,
            runtime_code_digest="b" * 64,
            parent_evidence_hashes=(),
        )
```

- [ ] **Paso 2: ejecutar la prueba y observar el rojo correcto**

```powershell
& $python -m unittest tests.test_h2_real_evidence.H2RealEvidenceTests.test_real_evidence_cannot_be_constructed_without_factory_capability -v
```

Esperado: error de importación porque `real_evidence.py` aún no existe.

- [ ] **Paso 3: implementar registros y fábrica interna mínimos**

```python
@dataclass(frozen=True)
class ComplexBallRecord:
    real_lower: str
    real_upper: str
    imag_lower: str
    imag_upper: str


class InvalidRealEvidence(RuntimeError):
    pass


_EVIDENCE_CAPABILITY = object()


@dataclass(frozen=True)
class RealCompletedL3PointEvidence:
    value: ComplexBallRecord
    precision_bits: int
    backend_id: str
    authorization_digest: str
    runtime_code_digest: str
    parent_evidence_hashes: tuple[str, ...]
    _capability: object = field(default=None, repr=False, compare=False)

    def __post_init__(self) -> None:
        if self._capability is not _EVIDENCE_CAPABILITY:
            raise InvalidRealEvidence("real evidence requires the internal factory")
```

La fábrica interna validará intervalos finitos, orden, hashes SHA-256,
precisión positiva y nombres no vacíos. Se crearán además:

```text
RealSegmentImageEvidence
RealHalfPlaneEvidence
RealArgumentIncrementEvidence
RealWindingEvidence
```

La API de fábrica queda fijada para todo el plan:

```python
class RealEvidenceFactory:
    def completed_l3_point(self, value: ComplexBallRecord, *,
                           precision_bits: int,
                           segment_id: str = "") -> RealCompletedL3PointEvidence:
        raise NotImplementedError

    def segment_image(self, *, value: ComplexBallRecord, segment_id: str,
                      precision_bits: int) -> RealSegmentImageEvidence:
        raise NotImplementedError

    def half_plane(self, *, segment: RealSegmentImageEvidence,
                   rotation_real: str, rotation_imag: str,
                   rotated_real_lower: str) -> RealHalfPlaneEvidence:
        raise NotImplementedError

    def argument_increment(self, half_plane: RealHalfPlaneEvidence,
                           lower: str, upper: str) -> RealArgumentIncrementEvidence:
        raise NotImplementedError

    def winding(self, increments: tuple[RealArgumentIncrementEvidence, ...],
                winding_ball: RealBallRecord,
                winding_number: int) -> RealWindingEvidence:
        raise NotImplementedError
```

- [ ] **Paso 4: agregar pruebas de cadena parental y rechazo sintético**

```python
def test_real_half_plane_requires_the_exact_segment_parent():
    first = factory.segment_image(
        value=ComplexBallRecord("1", "2", "3", "4"),
        segment_id="segment-1",
        precision_bits=192,
    )
    second = factory.segment_image(
        value=ComplexBallRecord("5", "6", "7", "8"),
        segment_id="segment-2",
        precision_bits=192,
    )
    with self.assertRaises(InvalidRealEvidence):
        factory.half_plane(segment=first, claimed_parent_hash=second.digest)
```

- [ ] **Paso 5: ejecutar el módulo completo**

```powershell
& $python -m unittest tests.test_h2_real_evidence -v
```

Esperado: todas las pruebas en verde, sin importar FLINT.

- [ ] **Paso 6: registrar punto de control SHA-256**

```powershell
Get-FileHash -Algorithm SHA256 athena_azr\h2_zero_certifier\real_evidence.py,tests\test_h2_real_evidence.py
```

### Tarea 2: Definir el runtime inyectable de bolas rigurosas

**Archivos:**
- Crear: `athena_azr/h2_zero_certifier/rigorous_ball_runtime.py`
- Crear: `tests/test_h2_rigorous_ball_runtime.py`

- [ ] **Paso 1: escribir la prueba roja del contrato de radio no nulo**

```python
def test_native_l_receives_the_full_input_ball_not_its_midpoint():
    runtime = FakeRigorousBallRuntime()
    ball = runtime.complex_ball("0.4", "0.6", "7", "8")
    runtime.native_dirichlet_l(ball, modulus=3, conrey_number=2, precision_bits=192)
    self.assertEqual(runtime.native_l_inputs, [ball])
```

- [ ] **Paso 2: ejecutar y confirmar que falla por API ausente**

```powershell
& $python -m unittest tests.test_h2_rigorous_ball_runtime -v
```

- [ ] **Paso 3: crear el protocolo mínimo**

```python
class RigorousBallRuntime(Protocol):
    def complex_ball(self, real_lower: str, real_upper: str,
                     imag_lower: str, imag_upper: str) -> object:
        raise NotImplementedError
    def pi_ball(self, precision_bits: int) -> object:
        raise NotImplementedError
    def divide_exact_integer(self, numerator: int, denominator,
                             precision_bits: int) -> object:
        raise NotImplementedError
    def real_log(self, value, precision_bits: int) -> object:
        raise NotImplementedError
    def scale_and_shift_exponent(self, input_ball, log_base,
                                 precision_bits: int) -> object:
        raise NotImplementedError
    def affine_half_plus_half(self, input_ball, precision_bits: int) -> object:
        raise NotImplementedError
    def complex_exp(self, value, precision_bits: int) -> object:
        raise NotImplementedError
    def complex_gamma(self, value, precision_bits: int) -> object:
        raise NotImplementedError
    def native_dirichlet_l(self, value, *, modulus: int,
                           conrey_number: int,
                           precision_bits: int) -> object:
        raise NotImplementedError
    def multiply(self, *values, precision_bits: int) -> object:
        raise NotImplementedError
    def multiply_complex_scalar(self, scalar, value,
                                precision_bits: int) -> object:
        raise NotImplementedError
    def complex_log(self, value, precision_bits: int) -> object:
        raise NotImplementedError
    def subtract(self, left, right, precision_bits: int) -> object:
        raise NotImplementedError
    def imaginary_interval(self, value) -> tuple[str, str]:
        raise NotImplementedError
    def real_interval(self, value) -> tuple[str, str]:
        raise NotImplementedError
    def sum_real_balls(self, values, precision_bits: int) -> object:
        raise NotImplementedError
    def divide_by_two_pi(self, value, pi_ball,
                         precision_bits: int) -> object:
        raise NotImplementedError
    def audit_ball_semantics(self) -> Mapping[str, bool]:
        raise NotImplementedError
```

El fake registrará todas las llamadas y devolverá bolas predeterminadas. No
aproximará funciones especiales.

- [ ] **Paso 4: probar que una API que colapsa al centro es rechazada**

```python
def test_runtime_audit_rejects_midpoint_only_semantics():
    runtime = MidpointOnlyRuntime()
    with self.assertRaises(UnsupportedBallSemantics):
        audit_runtime_semantics(runtime)
```

- [ ] **Paso 5: ejecutar pruebas y registrar hashes**

```powershell
& $python -m unittest tests.test_h2_rigorous_ball_runtime -v
Get-FileHash -Algorithm SHA256 athena_azr\h2_zero_certifier\rigorous_ball_runtime.py,tests\test_h2_rigorous_ball_runtime.py
```

### Tarea 3: Componer Lambda_3 con la ruta L nativa

**Archivos:**
- Crear: `athena_azr/h2_zero_certifier/real_completed_l3.py`
- Crear: `tests/test_h2_real_completed_l3.py`
- Modificar: `athena_azr/h2_zero_certifier/backend.py`

- [ ] **Paso 1: escribir la prueba roja del orden de operaciones**

```python
def test_completed_l3_uses_native_entire_l_and_exact_character_identity():
    runtime = FakeRigorousBallRuntime.fixed_completed_l3_fixture()
    result = evaluate_completed_l3(
        runtime,
        input_ball=runtime.input_ball,
        precision_bits=192,
        evidence_factory=factory,
    )
    self.assertEqual(runtime.native_l_character, (3, 2))
    self.assertEqual(runtime.calls, [
        "pi_ball", "real_log", "complex_exp",
        "complex_gamma", "native_dirichlet_l", "multiply",
    ])
    self.assertEqual(result.value, runtime.expected_product)
```

- [ ] **Paso 2: ejecutar y verificar el rojo**

```powershell
& $python -m unittest tests.test_h2_real_completed_l3 -v
```

- [ ] **Paso 3: implementar la composición sin FLINT**

```python
def evaluate_completed_l3(runtime, *, input_ball, precision_bits, evidence_factory):
    pi_value = runtime.pi_ball(precision_bits)
    log_base = runtime.real_log(runtime.divide_exact_integer(3, pi_value), precision_bits)
    exponent = runtime.scale_and_shift_exponent(input_ball, log_base, precision_bits)
    power = runtime.complex_exp(exponent, precision_bits)
    gamma_arg = runtime.affine_half_plus_half(input_ball, precision_bits)
    gamma_value = runtime.complex_gamma(gamma_arg, precision_bits)
    l_value = runtime.native_dirichlet_l(
        input_ball,
        modulus=3,
        conrey_number=2,
        precision_bits=precision_bits,
    )
    product = runtime.multiply(power, gamma_value, l_value, precision_bits=precision_bits)
    return evidence_factory.completed_l3_point(product, precision_bits=precision_bits)
```

Los nombres auxiliares se incorporarán al protocolo de la Tarea 2 con firmas
exactas. No se implementará la ruta Hurwitz.

- [ ] **Paso 4: probar fallos cerrados**

```python
def test_completed_l3_rejects_nonfinite_native_l_ball():
    runtime = FakeRigorousBallRuntime.fixed_completed_l3_fixture()
    runtime.native_l_result = NonFiniteBall()
    with self.assertRaises(InconclusiveRealEvaluation):
        evaluate_completed_l3(runtime, input_ball=runtime.input_ball,
                              precision_bits=192, evidence_factory=factory)


def test_completed_l3_rejects_wrong_character_metadata():
    runtime = FakeRigorousBallRuntime.fixed_completed_l3_fixture()
    runtime.character_metadata = {"modulus": "5", "number": "2"}
    with self.assertRaises(InconclusiveRealEvaluation):
        evaluate_completed_l3(runtime, input_ball=runtime.input_ball,
                              precision_bits=192, evidence_factory=factory)


def test_completed_l3_rejects_effective_precision_below_request():
    runtime = FakeRigorousBallRuntime.fixed_completed_l3_fixture()
    runtime.effective_precision_bits = 128
    with self.assertRaises(InconclusiveRealEvaluation):
        evaluate_completed_l3(runtime, input_ball=runtime.input_ball,
                              precision_bits=192, evidence_factory=factory)
```

- [ ] **Paso 5: ejecutar y registrar hashes**

```powershell
& $python -m unittest tests.test_h2_real_completed_l3 -v
Get-FileHash -Algorithm SHA256 athena_azr\h2_zero_certifier\real_completed_l3.py,athena_azr\h2_zero_certifier\backend.py,tests\test_h2_real_completed_l3.py
```

### Tarea 4: Encerrar la imagen completa de un segmento

**Archivos:**
- Crear: `athena_azr/h2_zero_certifier/real_segment_enclosure.py`
- Crear: `tests/test_h2_real_segment_enclosure.py`

- [ ] **Paso 1: escribir la prueba roja de caja rectangular completa**

```python
def test_segment_enclosure_evaluates_the_full_rectangular_hull():
    segment = DirectedSegment(
        RationalComplexPoint("-0.5", "3"),
        RationalComplexPoint("1.5", "7"),
    )
    result = enclose_completed_l3_segment(runtime, segment, 192, factory)
    self.assertEqual(runtime.completed_l3_inputs, [
        ComplexBallRecord("-0.5", "1.5", "3", "7")
    ])
    self.assertTrue(result.entire_segment_covered)
    self.assertEqual(result.mechanism, "whole_rectangular_complex_ball")
```

- [ ] **Paso 2: observar el rojo**

```powershell
& $python -m unittest tests.test_h2_real_segment_enclosure -v
```

- [ ] **Paso 3: implementar el hull exacto y la evidencia**

```python
def rectangular_hull(segment: DirectedSegment) -> ComplexBallRecord:
    return ComplexBallRecord(
        real_lower=str(min(segment.start.real_decimal, segment.end.real_decimal)),
        real_upper=str(max(segment.start.real_decimal, segment.end.real_decimal)),
        imag_lower=str(min(segment.start.imag_decimal, segment.end.imag_decimal)),
        imag_upper=str(max(segment.start.imag_decimal, segment.end.imag_decimal)),
    )
```

Para segmentos horizontales o verticales, el runtime representará el radio
cero de una coordenada mediante su tipo de bola interno. El registro
serializado podrá conservar extremos iguales únicamente en este tipo real;
no reutilizará `RealInterval`, que exige anchura positiva.

- [ ] **Paso 4: agregar falsificadores**

```python
def test_segment_enclosure_rejects_endpoint_sampling_runtime():
    runtime = EndpointSamplingRuntime()
    with self.assertRaises(UnsupportedBallSemantics):
        enclose_completed_l3_segment(runtime, segment, 192, factory)


def test_segment_enclosure_rejects_a_hull_outside_frozen_domain():
    outside = DirectedSegment(
        RationalComplexPoint("-2", "3"),
        RationalComplexPoint("1.5", "7"),
    )
    with self.assertRaises(InconclusiveRealEvaluation):
        enclose_completed_l3_segment(runtime, outside, 192, factory)


def test_segment_enclosure_rejects_entire_segment_covered_false():
    runtime.segment_coverage_proved = False
    with self.assertRaises(InconclusiveRealEvaluation):
        enclose_completed_l3_segment(runtime, segment, 192, factory)
```

- [ ] **Paso 5: ejecutar y registrar hashes**

```powershell
& $python -m unittest tests.test_h2_real_segment_enclosure -v
Get-FileHash -Algorithm SHA256 athena_azr\h2_zero_certifier\real_segment_enclosure.py,tests\test_h2_real_segment_enclosure.py
```

### Tarea 5: Certificar semiplano e incremento de argumento

**Archivos:**
- Crear: `athena_azr/h2_zero_certifier/real_argument.py`
- Crear: `tests/test_h2_real_argument.py`

- [ ] **Paso 1: escribir pruebas rojas para la rotación determinista**

```python
def test_nearest_rectangle_rotation_separates_a_right_upper_box():
    image = ComplexBallRecord("2", "3", "4", "5")
    evidence = certify_real_half_plane(runtime, image, factory)
    self.assertEqual(evidence.rotation_real, "2")
    self.assertEqual(evidence.rotation_imag, "-4")
    self.assertGreater(Decimal(evidence.rotated_real_lower), 0)


def test_half_plane_is_inconclusive_if_delta_ball_touches_zero():
    runtime.rotated_real_interval = ("0", "9")
    with self.assertRaises(InconclusiveRealArgument):
        certify_real_half_plane(runtime, image, factory)
```

- [ ] **Paso 2: ejecutar y observar el rojo**

```powershell
& $python -m unittest tests.test_h2_real_argument -v
```

- [ ] **Paso 3: implementar selección de q y rotación sin normalizar**

```python
def nearest_coordinate(lower: Decimal, upper: Decimal) -> Decimal:
    if lower > 0:
        return lower
    if upper < 0:
        return upper
    return Decimal(0)
```

`rotation_real=q_x` y `rotation_imag=-q_y`. El runtime realizará la
multiplicación intervalar y entregará el intervalo de la parte real.

- [ ] **Paso 4: implementar el incremento de logaritmo mediante el runtime**

```python
def real_argument_increment(runtime, *, half_plane, start_value, end_value,
                            precision_bits, evidence_factory):
    rotated_start = runtime.multiply_complex_scalar(half_plane.rotation, start_value)
    rotated_end = runtime.multiply_complex_scalar(half_plane.rotation, end_value)
    start_log = runtime.complex_log(rotated_start, precision_bits)
    end_log = runtime.complex_log(rotated_end, precision_bits)
    difference = runtime.subtract(end_log, start_log, precision_bits)
    lower, upper = runtime.imaginary_interval(difference)
    return evidence_factory.argument_increment(half_plane, lower, upper)
```

- [ ] **Paso 5: agregar pruebas de identidad y rama**

```python
def test_argument_increment_rejects_endpoints_from_another_segment():
    foreign_start = factory.completed_l3_point(
        ComplexBallRecord("1", "2", "0", "1"),
        precision_bits=192,
        segment_id="foreign-segment",
    )
    with self.assertRaises(InvalidRealEvidence):
        real_argument_increment(runtime, half_plane=half_plane,
                                start_value=foreign_start,
                                end_value=end_value,
                                precision_bits=192,
                                evidence_factory=factory)


def test_argument_increment_rejects_log_ball_crossing_branch_cut():
    runtime.log_branch_certified = False
    with self.assertRaises(InconclusiveRealArgument):
        real_argument_increment(runtime, half_plane=half_plane,
                                start_value=start_value,
                                end_value=end_value,
                                precision_bits=192,
                                evidence_factory=factory)


def test_argument_increment_rejects_float_or_atan2_runtime():
    runtime = FloatPhaseRuntime()
    with self.assertRaises(UnsupportedBallSemantics):
        real_argument_increment(runtime, half_plane=half_plane,
                                start_value=start_value,
                                end_value=end_value,
                                precision_bits=192,
                                evidence_factory=factory)
```

- [ ] **Paso 6: ejecutar y registrar hashes**

```powershell
& $python -m unittest tests.test_h2_real_argument -v
Get-FileHash -Algorithm SHA256 athena_azr\h2_zero_certifier\real_argument.py,tests\test_h2_real_argument.py
```

### Tarea 6: Acumular winding real y aislarlo del camino sintético

**Archivos:**
- Modificar: `athena_azr/h2_zero_certifier/real_argument.py`
- Modificar: `athena_azr/h2_zero_certifier/backend.py`
- Modificar: `athena_azr/h2_zero_certifier/pipeline.py`
- Crear o modificar: `tests/test_h2_real_argument.py`
- Modificar: `tests/test_h2_pipeline_guard.py`

- [ ] **Paso 1: escribir la prueba roja de pi riguroso**

```python
def test_real_winding_uses_runtime_pi_ball_not_decimal_constants():
    runtime = FakeRigorousBallRuntime.with_pi_ball("3.1415", "3.1416")
    result = accumulate_real_winding(runtime, increments, 192, factory)
    self.assertEqual(runtime.pi_requests, [192])
    self.assertEqual(result.winding_number, 1)
```

- [ ] **Paso 2: escribir la prueba roja contra mezcla sintética**

```python
def test_real_pipeline_rejects_synthetic_argument_certificate():
    with self.assertRaises(InvalidRealEvidence):
        accumulate_real_winding(runtime, [synthetic_increment], 192, factory)
```

- [ ] **Paso 3: ejecutar y confirmar los rojos**

```powershell
& $python -m unittest tests.test_h2_real_argument tests.test_h2_pipeline_guard -v
```

- [ ] **Paso 4: implementar suma y entero único como bolas del runtime**

```python
def accumulate_real_winding(runtime, increments, precision_bits, evidence_factory):
    total = runtime.sum_real_balls(
        [item.delta_ball for item in increments],
        precision_bits=precision_bits,
    )
    pi_value = runtime.pi_ball(precision_bits)
    winding_ball = runtime.divide_by_two_pi(total, pi_value, precision_bits)
    lower, upper = runtime.real_interval(winding_ball)
    first = Decimal(lower).to_integral_value(rounding=ROUND_CEILING)
    last = Decimal(upper).to_integral_value(rounding=ROUND_FLOOR)
    if first != last or first < 0:
        raise InconclusiveRealArgument("winding ball has no unique nonnegative integer")
    return evidence_factory.winding(increments, winding_ball, int(first))
```

- [ ] **Paso 5: retirar el módulo flotante del inventario probatorio futuro**

No se borrará `argument_principle.py`. Se modificará `RUNTIME_CODE_FILES` para
separar explícitamente:

```python
PROBATIVE_RUNTIME_CODE_FILES = (
    "athena_azr/h2_zero_certifier/authorization.py",
    "athena_azr/h2_zero_certifier/backend.py",
    "athena_azr/h2_zero_certifier/real_evidence.py",
    "athena_azr/h2_zero_certifier/rigorous_ball_runtime.py",
    "athena_azr/h2_zero_certifier/real_completed_l3.py",
    "athena_azr/h2_zero_certifier/real_segment_enclosure.py",
    "athena_azr/h2_zero_certifier/real_argument.py",
    "athena_azr/h2_zero_certifier/python_flint_backend.py",
    "athena_azr/h2_zero_certifier/pipeline.py",
    "scripts/run_h2_zero_certification.py",
)
SYNTHETIC_TEST_ONLY_FILES = ("athena_azr/h2_zero_certifier/argument_principle.py",)
```

La futura autorización de ejecución solo aprobará el inventario probatorio.

- [ ] **Paso 6: ejecutar módulos afectados y registrar hashes**

```powershell
& $python -m unittest tests.test_h2_real_argument tests.test_h2_pipeline_guard tests.test_h2_authorization -v
Get-FileHash -Algorithm SHA256 athena_azr\h2_zero_certifier\real_argument.py,athena_azr\h2_zero_certifier\backend.py,athena_azr\h2_zero_certifier\pipeline.py,athena_azr\h2_zero_certifier\authorization.py
```

### Tarea 7: Mantener PythonFlintBackend completamente inerte

**Archivos:**
- Modificar: `athena_azr/h2_zero_certifier/python_flint_backend.py`
- Modificar: `tests/test_h2_real_flint_guarded.py`
- Modificar: `tests/test_h2_pipeline_guard.py`

- [ ] **Paso 1: escribir pruebas rojas para los nuevos endpoints**

```python
def test_real_math_endpoints_remain_unimplemented_after_fake_authorization():
    backend = PythonFlintBackend()
    with self.assertRaises(ExecutionNotAuthorized):
        backend.real_completed_l3_point(None, 192)
    with self.assertRaises(ExecutionNotAuthorized):
        backend.real_completed_l3_segment(None, 192)
```

- [ ] **Paso 2: añadir endpoints inertes**

```python
def real_completed_l3_point(self, point_ball, precision_bits):
    return self._blocked_until_reviewed_real_backend()

def real_completed_l3_segment(self, segment, precision_bits):
    return self._blocked_until_reviewed_real_backend()
```

Incluso tras inicialización, `_blocked_until_reviewed_real_backend` levantará
`NotImplementedError`. Esta tarea no importará FLINT en ninguna prueba.

- [ ] **Paso 3: probar que un objeto de autorización fabricado sigue fallando**

```python
def test_direct_execution_authorization_construction_cannot_initialize_backend():
    backend = PythonFlintBackend()
    with self.assertRaises(ExecutionNotAuthorized):
        forged = ExecutionAuthorization(
            experiment_id="G5B-006F",
            execution_authorized=True,
            max_height=500,
            requested_heights=(143, 200, 300, 500),
            protocol_006b_sha256="a" * 64,
            plan_006c_sha256="b" * 64,
            spec_006e2_sha256="c" * 64,
            plan_006e3_sha256="d" * 64,
            approved_code_hashes={"module.py": "e" * 64},
            output_directory=Path("artifacts"),
        )
        backend.initialize(authorization=forged)
```

- [ ] **Paso 4: ejecutar guardias**

```powershell
& $python -m unittest tests.test_h2_real_flint_guarded tests.test_h2_pipeline_guard -v
```

- [ ] **Paso 5: confirmar una sola importación perezosa**

```powershell
rg -n "import flint|from flint" athena_azr\h2_zero_certifier scripts\run_h2_zero_certification.py
```

Esperado: una única línea dentro de `PythonFlintBackend.initialize`.

### Tarea 8: Auditoría integral y documento de cierre de la fase de código

**Archivos:**
- Crear en la fase futura: `docs/experimentos/experimento-006e8-c03b-l3-real-backend-inert-code-report.md`
- Revisar: todos los archivos de las tareas 1 a 7

- [ ] **Paso 1: ejecutar la suite H2 completa**

```powershell
& $python -m unittest discover -s tests -p 'test_h2_*.py' -v
```

Esperado: cero fallos; la prueba de integración real continúa omitida.

- [ ] **Paso 2: compilar la superficie H2**

```powershell
& $python -m compileall -q athena_azr\h2_zero_certifier scripts\run_h2_zero_certification.py
```

- [ ] **Paso 3: auditar llamadas prohibidas**

```powershell
rg -n --glob '*.py' "acb\.zeta_zero|chi\.hardy_z|chi\.l_function|acb\.integral|requests|urllib|socket|subprocess" athena_azr\h2_zero_certifier scripts\run_h2_zero_certification.py
```

Esperado: cero coincidencias en runtime probatorio.

- [ ] **Paso 4: auditar floats y módulo sintético**

```powershell
rg -n "float|complex\(|atan2|argument_principle" athena_azr\h2_zero_certifier\real_*.py athena_azr\h2_zero_certifier\rigorous_ball_runtime.py
```

Esperado: cero coincidencias probatorias.

- [ ] **Paso 5: confirmar ausencia de efectos laterales**

Registrar:

```text
real_flint_calls = 0
network_access = 0
real_contours = 0
zero_tables = 0
artifact_writes = 0
H2_certified = false
006F_readiness = false
```

- [ ] **Paso 6: generar inventario SHA-256 completo**

El informe futuro listará cada archivo de runtime probatorio y cada test nuevo.
No modificará 006E2–006E7.

## 4. Criterios de aceptación de una futura fase de código

La futura implementación inerte solo podrá aceptarse si:

1. todos los tipos reales son opacos y trazables;
2. la L nativa recibe la bola completa;
3. la envolvente evalúa una caja que contiene todo el segmento;
4. semiplano y logaritmo conservan identidad parental;
5. `pi` proviene del runtime de bolas;
6. no se usan `float`, `complex`, `atan2` ni muestreo finito;
7. evidencia sintética y real son incompatibles por tipo y capacidad;
8. `PythonFlintBackend` continúa sin operaciones matemáticas implementadas;
9. no se importa FLINT durante las pruebas;
10. no se generan tablas, artefactos ni conteos reales.

Si cualquiera falla:

```text
real_backend_inert_code_status = rejected
006F_readiness = false
```

## 5. Estado final del plan

```text
006E7_PLAN = complete_pending_review_and_freeze
IMPLEMENTATION_STYLE = strict_TDD
PRIMARY_L_ROUTE = native_entire_Dirichlet_L
PRIMARY_SEGMENT_ROUTE = whole_rectangular_complex_ball
REAL_EVIDENCE_TYPES = separate_and_opaque
PYTHON_FLINT_BACKEND = remains_inert
CODE_AUTHORIZATION = false
EXECUTION_AUTHORIZATION = false
REAL_FLINT_EXECUTION = forbidden
ZERO_CERTIFICATION = forbidden
H2_CERTIFIED = false
006F_READINESS = false
006F_EXECUTION = forbidden
C05_RERUN = forbidden
C35 = frozen
C15 = frozen
NOVELTY_CLAIM = false
```
