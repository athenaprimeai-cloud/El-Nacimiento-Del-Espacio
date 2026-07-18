# Experimento 006E17: Protocolo de Semantica Real FLINT/Arb para L3

## 1. Estado y alcance

```text
experiment_id = G5B-006E17
status = protocol_only
target = real_FLINT_Arb_semantics_for_L3_backend
code_authorization = false
execution_authorization = false
real_flint_import = forbidden
real_flint_execution = forbidden
real_contour_execution = forbidden
zero_certification = forbidden
zero_tables = not_generated
artifacts = none
network_during_future_runtime = forbidden
H2_certified = false
006F = blocked
downstream_use = forbidden
novelty_claim = false
```

006E17 define el significado que debera tener el primer contacto futuro con
python-flint/FLINT/Arb. No autoriza codigo, instalaciones, importaciones,
pruebas reales, evaluacion de `Lambda_3`, contornos ni calculo de ceros.

Frase rectora:

```text
Ahora pasamos de arquitectura inerte congelada a diseno semantico del primer
contacto real, sin ejecutar todavia.
```

## 2. Estado heredado y cadena congelada

```text
006E16_STATUS = formal_joint_freeze_completed
006E16_SHA256 = 9deb49e89764909b7af91c94c5e3593d71edbd35676fcca97a91a51436e309f2
006E8 = frozen_by_006E16
006E10 = frozen_by_006E16
006E12 = frozen_by_006E16
006E14 = frozen_by_006E16
006E15 = incorporated_by_006E16
H2_CERTIFIED = false
006F_EXECUTION = forbidden
```

006E17 no reabre ni modifica esa cadena. Su funcion es convertir las
abstracciones matematicas de 006E6 y los contratos inertes de 006E7-006E14
en requisitos verificables para una API real futura.

## 3. Versiones y fuentes normativas

La fase futura debera fijar antes de importar:

```text
python_flint_version = exact
flint_version = exact
arb_backend_version = exact_or_bundled
python_version = exact
platform = exact
runtime_code_digest = exact
```

Este protocolo fue contrastado documentalmente el 15 de junio de 2026 con:

1. python-flint 0.8.0, conceptos generales:
   https://python-flint.readthedocs.io/en/latest/general.html
2. python-flint 0.8.0, `arb`:
   https://python-flint.readthedocs.io/en/latest/arb.html
3. python-flint 0.8.0, `acb`:
   https://python-flint.readthedocs.io/en/latest/acb.html
4. python-flint 0.8.0, caracteres de Dirichlet:
   https://python-flint.readthedocs.io/en/latest/dirichlet.html
5. FLINT, `acb_dirichlet`:
   https://flintlib.org/doc/acb_dirichlet.html
6. Arb 2.23, `acb_dirichlet` como contraste historico:
   https://arblib.org/acb_dirichlet.html

La documentacion `latest` no sustituye un pin de version. Si las firmas o
garantias cambian, el resultado sera `blocked_version_mismatch` hasta una
revision documental nueva.

## 4. Tipos reales y representacion canonica

### 4.1 Bola real

El tipo candidato es:

```text
flint.arb(mid, rad)
```

Una instancia representa un intervalo `[m-r, m+r]`. La precision del punto
medio depende de `flint.ctx.prec`; el radio se redondea hacia afuera segun la
implementacion.

Contrato requerido:

```text
RealBall = arb
lower_bound = value.lower()
upper_bound = value.upper()
finite = value.is_finite()
unique_integer = value.unique_fmpz()
```

No se serializaran certificados probatorios mediante decimales impresos. Los
limites canonicos deberan guardarse como datos binarios/dyadicos exactos del
backend, por ejemplo pares mantisa-exponente obtenidos de limites exactos, o
un formato equivalente revisado. `str()` solo podra usarse para lectura
humana.

### 4.2 Bola compleja

El tipo candidato es:

```text
flint.acb(real_ball, imag_ball)
```

`acb` representa una caja rectangular formada por una bola real y otra
imaginaria:

```text
ComplexBall = [re_lower,re_upper] + i[im_lower,im_upper]
real_part = value.real
imag_part = value.imag
finite = value.is_finite()
contains_zero = value.contains(0)
```

Una caja no es un disco. Para un segmento diagonal, el casco rectangular
incluye puntos fuera del segmento. Esa sobreaproximacion es rigurosa, aunque
puede impedir una conclusion. No se describira como una envolvente sin
inflacion perpendicular.

### 4.3 Entradas exactas

Quedan prohibidos `float` y `complex` de Python para constantes probatorias.
Se admitiran enteros, racionales exactos, cadenas racionales revisadas o
datos dyadicos exactos. La propia documentacion advierte que `arb(0.1)`
encierra el binario de Python, no necesariamente el decimal matematico 1/10.

## 5. Contexto de precision

python-flint controla la precision real y compleja mediante el contexto
global `flint.ctx`.

La futura ruta debera usar un bloque equivalente a `ctx.workprec(bits)` y
restaurar el contexto incluso ante excepciones. Como el contexto es global:

```text
probative_concurrency = forbidden_until_separately_proved_safe
one_probative_precision_scope_at_a_time = required
context_restoration = mandatory
ctx.prec_before_and_after = recorded
```

`showgood`, `dps` y refinamiento adaptativo destinado a presentacion no son
primitivas probatorias. La precision seguira la secuencia preregistrada y no
se elegira mirando el resultado esperado.

## 6. Caracter exacto chi_3

Constructor candidato:

```text
chi = flint.dirichlet_char(3, 2)
```

Antes de aceptar el objeto, una futura prueba real sin contornos debera
certificar todos estos metadatos y valores:

```text
chi.modulus() = 3
chi.number() = 2
chi.conductor() = 3
chi.is_primitive() = true
chi.is_principal() = false
chi.is_real() = true
chi.order() = 2
chi.parity() = odd
chi(0) contains 0
chi(1) contains 1
chi(2) contains -1
```

Si la numeracion concreta de la version fijada no produce exactamente este
caracter, no se buscara otro indice automaticamente:

```text
status = blocked_character_identity
```

## 7. API candidata para L(s,chi_3)

La API publica candidata es:

```text
chi.l_function(s_ball)
```

Alias documentado:

```text
chi.l(s_ball)
```

El alias no se usara en la ruta probatoria para evitar ambiguedad. La ruta
congelada nombrara siempre `l_function`.

La documentacion publica confirma evaluacion en un numero complejo, pero no
explicita por si sola todos los puntos necesarios para una entrada `acb` con
radio no nulo. Por tanto, antes de autorizar codigo real se exigira:

```text
1. inspeccion de la version exacta del enlace python-flint;
2. prueba de que pasa el acb completo a acb_dirichlet_l o equivalente;
3. prueba de que no extrae midpoints;
4. prueba de que no convierte a float/complex;
5. confirmacion del contrato inclusivo de la funcion C subyacente;
6. pruebas de regresion con radios no nulos como evidencia suplementaria.
```

Las pruebas numericas suplementarias no sustituyen la inspeccion del
contrato. Si esa semantica no puede demostrarse:

```text
status = blocked_native_L_ball_semantics
```

No se habilitara automaticamente la resta de zetas de Hurwitz como fallback.

## 8. Evaluacion de Lambda_3(s)

La funcion completada permanece:

```text
Lambda_3(s)
= exp(((s+1)/2) * log(3/pi))
  * Gamma((s+1)/2)
  * L(s,chi_3).
```

Primitivas candidatas:

```text
pi_ball = arb.pi()
log_base = (arb(3) / pi_ball).log()
shifted = (s_ball + 1) / 2
scale = (shifted * log_base).exp()
gamma_factor = shifted.gamma()
l_value = chi.l_function(s_ball)
result = scale * gamma_factor * l_value
```

No se usara `pow(3/pi, shifted)`, porque introduciria semantica de potencia
compleja y ramas innecesarias. `log_base` es una bola real positiva.

### 8.1 Dominio analitico

El dominio congelado sigue siendo:

```text
-1/2 <= Re(s) <= 3/2
0 <= Im(s) <= T
T in {143, 200, 300, 500}
```

Entonces `(s+1)/2` tiene parte real entre 1/4 y 5/4, fuera de los polos de
Gamma. Cada caja de entrada debera demostrar inclusion completa en este
dominio antes de evaluar.

### 8.2 Resultado admisible

El resultado solo sera admisible si:

```text
input_ball_preserved = true
all_intermediates_finite = true
output_is_acb = true
character_identity_verified = true
working_precision_verified = true
no_midpoint_extraction = true
no_float_or_complex_conversion = true
```

Un resultado `nan`, infinito, indeterminado o excesivamente ancho produce
`inconclusive`, nunca cero.

## 9. Semantica del segmento completo

Para el segmento dirigido `[a,b]`, se construira la caja rectangular:

```text
D = hull(Re(a),Re(b)) + i hull(Im(a),Im(b)).
```

La caja `D` contiene todo el segmento. Para segmentos diagonales tambien
contiene un area adicional; esto es una sobreaproximacion aceptada y debe
figurar en la evidencia.

Ruta primaria:

```text
segment_method = whole_rectangular_acb_input
segment_image = Lambda_3(D)
```

No se aceptan extremos, malla finita ni muestreo adaptativo como prueba de
cobertura. La ruta solo sera probatoria si la semantica inclusiva de todas las
operaciones, incluida `chi.l_function(D)`, fue aprobada en la seccion 7.

Un certificado futuro debera registrar:

```text
exact_start
exact_end
input_rectangle_exact_bounds
diagonal_overapproximation = true_or_false
precision_bits
output_rectangle_exact_bounds
entire_segment_covered = true
backend_and_version
parent_evidence_digest
```

Si la caja es demasiado ancha, se subdivide segun la politica congelada. No
se recorta manualmente el radio.

## 10. Separacion del origen y semiplano

Para una imagen rectangular `E`, el origen queda excluido solo si no pertenece
a la vez a sus intervalos real e imaginario.

La separacion por semiplano usara el punto rectangular mas cercano al origen,
como en 006E6. Todas las decisiones se tomaran con limites rigurosos `lower()`
y `upper()` o predicados de certeza equivalentes.

Condicion final:

```text
rotated = r * E
delta = lower(rotated.real)
half_plane_certified iff delta > 0 is certainly true
```

Los predicados de python-flint sobre numeros inexactos pueden devolver falso
tanto por falsedad como por indeterminacion. Por ello:

```text
false_is_not_disproof
undetermined_comparison = inconclusive_or_subdivide
```

No se usara el signo del midpoint.

## 11. Logaritmo complejo y rama

API candidata:

```text
z_ball.log(analytic=True)
```

La opcion analitica es preferida porque obliga a tratar el corte de rama como
parte del contrato. No obstante, la futura fase debera verificar su semantica
exacta en la version fijada y no inferirla solo del nombre del parametro.

La llamada sera admisible unicamente despues de certificar que la imagen
rotada completa esta en el semiplano derecho abierto. En tal dominio, el
logaritmo principal es holomorfo y la rama es comun a todo el segmento.

Estados de fallo:

```text
branch_cut_touched = inconclusive
zero_possible = inconclusive
nonfinite_log = inconclusive
analytic_semantics_unverified = blocked_complex_log_semantics
```

`arg()`, `atan2`, desempaquetado de fase y correcciones manuales por `2*pi`
quedan fuera de la ruta probatoria.

## 12. Incremento angular e entero unico

Para extremos certificados `A` y `B` del mismo subsegmento:

```text
Delta contains Im(Log(r*B) - Log(r*A)).
```

Los incrementos se sumaran como bolas `arb`. `pi` procedera de `arb.pi()` en
el mismo contexto de precision. El winding sera:

```text
W = sum(Delta) / (2*pi_ball).
```

Metodo candidato de unicidad:

```text
N = W.unique_fmpz()
```

La aceptacion exige ademas `N >= 0`. Si `unique_fmpz()` devuelve `None`, el
resultado es inconcluso. No se redondeara el midpoint.

## 13. Serializacion y evidencia

Toda evidencia futura conservara limites outward-rounded de forma canonica.
Queda prohibido reconstruir una bola probatoria desde una cadena decimal
redondeada para presentacion.

Campos minimos:

```text
backend_id
python_flint_version
flint_version
python_version
platform
ctx_precision_bits
operation_name
exact_character_metadata
exact_input_bounds
exact_output_bounds
parent_evidence_digests
authorization_digest
runtime_code_digest
issuance_registry_identity
```

La autenticidad estructural congelada en 006E14-006E16 se mantiene. No se
eleva a frontera criptografica.

## 14. Estados de fallo cerrado

Estados obligatorios:

```text
blocked_version_mismatch
blocked_character_identity
blocked_native_L_ball_semantics
blocked_complex_log_semantics
blocked_serialization_semantics
inconclusive_nonfinite
inconclusive_domain_not_proved
inconclusive_origin_not_excluded
inconclusive_half_plane
inconclusive_branch
inconclusive_precision_exhausted
inconclusive_subdivision_exhausted
inconclusive_unique_integer
inconclusive_context_integrity
```

Regla:

```text
blocked = contrato no demostrado; no ejecutar
inconclusive = ejecucion futura rigurosa sin conclusion
neither blocked nor inconclusive may be coerced to zero or success
```

## 15. Pruebas minimas de una futura fase real sin contornos

Estas pruebas se definen, pero no se ejecutan en 006E17.

### 15.1 Identidad y contexto

1. pin y reporte exacto de versiones;
2. identidad completa de `chi_3`;
3. restauracion de `ctx.prec` tras exito y excepcion;
4. rechazo de concurrencia probatoria no autorizada;
5. rechazo de constantes `float` y `complex`.

### 15.2 Semantica de bolas

1. construccion y serializacion exacta de bolas reales;
2. construccion de `acb` con radios real e imaginario no nulos;
3. round-trip de limites sin perdida de inclusion;
4. rechazo de serializacion decimal como fuente probatoria;
5. comprobacion de resultados finitos y tipos esperados.

### 15.3 Funcion L nativa

1. inspeccion del binding de `l_function` de la version fijada;
2. prueba de ausencia de extraccion de midpoint;
3. entrada `acb` no puntual;
4. comparacion de inclusion entre una caja y subcajas como regresion;
5. contraste con Hurwitz solo en cajas alejadas de `s=1`;
6. fallo cerrado si las dos rutas no se solapan.

Las pruebas 4 y 5 son controles, no demostraciones independientes de
completitud semantica.

### 15.4 Lambda_3 puntual

1. puntos exactos sencillos;
2. cajas no puntuales dentro del dominio;
3. rechazo de caja que salga del dominio;
4. rechazo de intermedio no finito;
5. control de ecuacion funcional como consistencia, no como certificacion;
6. monotonia de inclusion al subdividir como diagnostico.

### 15.5 Segmentos, rama e integer

1. caja horizontal y vertical;
2. caja diagonal con marca de sobreaproximacion;
3. imagen sintetica separada del origen;
4. imagen que contiene el origen: inconclusa;
5. log analitico en semiplano derecho;
6. caja que toca corte de rama: inconclusa;
7. `unique_fmpz` con un entero;
8. intervalo con dos enteros: inconcluso.

Estas pruebas reales sin contornos requeriran autorizacion separada. No
aislaran ceros ni certificaran H2.

## 16. Criterios para 006E18 y 006E19

006E18 debera revisar documentalmente:

```text
1. correspondencia entre APIs candidatas y version oficial;
2. suficiencia de los bloqueos de semantica no documentada;
3. correccion del modelo rectangular de acb;
4. contexto global y politica de concurrencia;
5. rama del logaritmo;
6. serializacion exacta;
7. estados blocked frente a inconclusive;
8. preservacion de 006E16 y bloqueo de 006F.
```

Solo tras aceptacion y congelamiento separados de 006E17/006E18 podra
proponerse 006E19 como plan TDD. 006E19 tampoco autorizara importar FLINT.

## 17. Veredicto del protocolo

```text
006E17_STATUS = protocol_completed_pending_independent_review
BALL_TYPES = arb_and_acb_rectangular_enclosures
CHARACTER_API = dirichlet_char_3_2_pending_version_identity_check
NATIVE_L_API = chi.l_function_pending_nonzero_radius_semantics_check
COMPLETED_L3 = explicit_exp_gamma_L_composition
SEGMENT_ENCLOSURE = whole_rectangular_acb_with_declared_overapproximation
ORIGIN_EXCLUSION = rigorous_rectangular_bounds
HALF_PLANE = rigorous_rotation_and_positive_real_lower_bound
COMPLEX_LOG = log_analytic_pending_exact_version_semantics_check
UNIQUE_INTEGER = arb.unique_fmpz
GLOBAL_CONTEXT = serialized_and_restored
CODE_AUTHORIZATION = false
EXECUTION_AUTHORIZATION = false
REAL_FLINT_IMPORT = forbidden
REAL_FLINT_EXECUTION = forbidden
REAL_CONTOUR_EXECUTION = forbidden
ZERO_CERTIFICATION = forbidden
ZERO_TABLES = not_generated
ARTIFACTS = none
H2_CERTIFIED = false
006F = blocked
DOWNSTREAM_USE = forbidden
NOVELTY_CLAIM = false
```

006E17 fija el significado de una futura operacion real. No demuestra que la
API instalada satisfaga ese significado y no produce evidencia matematica.
