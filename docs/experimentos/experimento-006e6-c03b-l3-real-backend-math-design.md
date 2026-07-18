# Experimento 006E6: diseno matematico del backend real L3

## 1. Estado y alcance

```text
experiment_id = G5B-006E6
target = L3_real_backend_mathematical_design
status = real_backend_math_design_only
method = pure_argument_principle
code_authorization = false
execution_authorization = false
real_flint_execution = forbidden
contour_execution = forbidden
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

Este documento disena la futura capa matematica real que debera reemplazar
los certificados sinteticos de 006E4. No autoriza modificar codigo, importar
FLINT, evaluar funciones especiales, recorrer contornos ni calcular ceros.

La separacion es estricta:

```text
006E6 = formula + contratos + reglas de fallo
fase futura de codigo = implementacion inerte revisable
006F = ejecucion real, todavia no autorizada
```

## 2. Base congelada

```text
006E2_SHA256 = 4b14ba44d08d80941a4ab69776c41479453f0f08661ffec9fcb304204f1212c5
006E3_SHA256 = 4b7a277e939fab39ac6a9ce95cfe771944964a90a37dab12d005908ab849e931
006E4_SHA256 = fc60928a11f917f771dbcf296ef832398edb635211d96bd7fadcf2bfc395a77a
006E5_SHA256 = 7c527e921cf41081d46800474b6c1026dba904d80a274617cb4004f7637f981e
```

006E5 acepta el flujo de control sintetico, pero mantiene sin implementar:

1. `Lambda_3(s)` con bolas complejas reales;
2. la imagen completa de un segmento;
3. el logaritmo complejo con rama certificada;
4. la acumulacion angular con redondeo dirigido;
5. el conteo completo de L3 hasta altura 500.

## 3. Funcion completada y dominio

Para el caracter primitivo real impar `chi_3` modulo 3 se usara:

```text
Lambda_3(s)
= exp(((s+1)/2) * log(3/pi))
  * Gamma((s+1)/2)
  * L(s,chi_3).
```

El rectangulo congelado es:

```text
-1/2 <= Re(s) <= 3/2
0 <= Im(s) <= T
T in {143, 200, 300, 500}.
```

En este dominio:

```text
1/4 <= Re((s+1)/2) <= 5/4.
```

Por tanto, `Gamma((s+1)/2)` no atraviesa polos. La base `3/pi` es real y
positiva, asi que la potencia se define mediante el logaritmo real de esa
base y no introduce una eleccion de rama compleja. La funcion L de un caracter
primitivo no principal es entera. En consecuencia, `Lambda_3` es holomorfa en
todo rectangulo y en todas las cajas internas autorizadas por 006E2.

No se extendera el contorno hacia `Re(s) <= -1` sin una nueva derivacion de
polos aparentes y cancelaciones de factores Gamma.

## 4. Evaluacion rigurosa de L(s,chi_3)

La identidad de control es:

```text
L(s,chi_3)
= 3^(-s) * (HurwitzZeta(s,1/3) - HurwitzZeta(s,2/3)).
```

Cada zeta de Hurwitz posee un polo en `s=1`, aunque la diferencia es entera.
Por ello queda prohibido evaluar cerca de una bola que contenga `s=1`
mediante la resta ingenua de dos evaluaciones meromorfas.

006E6 congela la Ruta A como unica ruta probatoria principal. La Ruta B queda
como control independiente y como posible enmienda futura, no como fallback
dentro de una corrida.

### Ruta A: funcion L nativa entera

Usar una operacion de la biblioteca de bolas cuyo contrato documentado e
inspeccionado acepte una bola compleja `s` y encierre directamente
`L(s,chi_3)` como funcion entera del caracter exacto `(3,2)`.

La revision de codigo debera demostrar:

1. identidad exacta del caracter;
2. soporte de entrada con radio no nulo;
3. semantica de inclusion para toda la bola de entrada;
4. ausencia de reduccion silenciosa a su punto medio;
5. propagacion outward-rounded del error.

### Ruta B: Hurwitz regularizada

Definir:

```text
H(s,a) = HurwitzZeta(s,a) - 1/(s-1).
```

`H(s,a)` es holomorfa en `s=1`, y entonces:

```text
L(s,chi_3)
= 3^(-s) * (H(s,1/3) - H(s,2/3)).
```

La implementacion no podra formar primero dos bolas infinitas o
indeterminadas y restarlas. Debera evaluar la continuacion regularizada como
un objeto holomorfo o mediante una serie local validada alrededor de `s=1`.

### Regla congelada

```text
primary_L_route = native_entire_Dirichlet_L
regularized_Hurwitz = independent_control_only
runtime_fallback_between_routes = forbidden
```

Si la Ruta A no demuestra inclusion para bolas de radio no nulo, la fase de
codigo quedara bloqueada. Usar la Ruta B como prueba principal requerira una
enmienda documental y una nueva autorizacion anteriores a cualquier dato.

En ese caso:

```text
completed_L3_status = inconclusive
```

## 5. Evaluacion puntual de Lambda_3

La operacion futura:

```text
completed_l3_point(s_ball, precision_bits)
-> RealCompletedL3PointEvidence
```

debera ejecutar, en este orden conceptual:

1. construir exactamente `chi_3`;
2. obtener una bola rigurosa para `pi`;
3. calcular `log(3/pi)` como bola real;
4. evaluar el factor exponencial;
5. evaluar Gamma en una bola libre de polos;
6. evaluar `L(s,chi_3)` por la ruta congelada;
7. multiplicar con redondeo dirigido;
8. devolver una bola compleja finita y procedencia completa.

Se rechazara el resultado si:

1. cualquier componente es no finita;
2. la operacion pierde la bola de entrada y usa solo su centro;
3. el radio se sustituye por una tolerancia inventada;
4. el caracter, conductor o paridad no coinciden con 006E2;
5. la precision efectiva es menor que la solicitada.

## 6. Envolvente de un segmento completo

Para un segmento dirigido `[a,b]`, sea:

```text
m = (a+b)/2
h = (b-a)/2
s(u) = m + u*h,  -1 <= u <= 1.
```

La operacion futura:

```text
completed_l3_segment(segment, precision_bits)
-> RealSegmentImageEvidence
```

debera encerrar:

```text
{ Lambda_3(s(u)) : -1 <= u <= 1 }.
```

No basta evaluar extremos ni una malla finita.

006E6 congela S1 como mecanismo probatorio. S2 queda documentado solo como
posible enmienda futura.

### Mecanismo S1: evaluacion sobre la bola que contiene el segmento

Construir la caja compleja rectangular exacta:

```text
D = hull(Re(a),Re(b)) + i*hull(Im(a),Im(b)),
```

que contiene todo el segmento sin inflar la direccion perpendicular. Evaluar
`Lambda_3(D)` mediante operaciones que acepten entradas con radios real e
imaginario no nulos. El resultado puede ser ancho, pero es valido si la
biblioteca garantiza la inclusion de la imagen de toda la caja.

Antes de evaluar, `D` debe permanecer dentro del dominio analitico congelado.
Si una caja intermedia excede ese dominio, se subdivide; no se evalua Gamma
sobre una caja que pueda tocar sus polos.

### Mecanismo S2: extension de Taylor o valor medio validado

Si S1 no cierra, usar una expansion validada alrededor de `m`. Una forma
minima admisible es:

```text
Lambda_3(m+u*h)
= Lambda_3(m)
  + u*h * integral_0^1 Lambda_3'(m+t*u*h) dt.
```

Una envolvente rigurosa de `Lambda_3'` sobre una bola que contenga el segmento
produce una envolvente de toda la imagen. Tambien se admite una serie de
Taylor con resto de Cauchy probado. Los coeficientes, derivadas y resto deben
ser bolas; no se admiten diferencias finitas ordinarias.

### Politica determinista

```text
primary_segment_enclosure = S1_whole_rectangular_complex_ball
S2_Taylor = amendment_only
runtime_fallback_between_S1_and_S2 = forbidden
```

La subdivision adaptativa de 006E2 sera la unica respuesta dentro de la ruta
principal a una envolvente ancha. Si S1 no puede demostrar semantica de
inclusion, la implementacion queda bloqueada y S2 exigira una nueva revision.

Un certificado de segmento conservara:

```text
segment_exact_endpoints
input_hull
evaluation_mechanism
precision_bits
image_real_ball
image_imag_ball
entire_segment_covered = true
backend_provenance
```

## 7. Separacion del origen y semiplano real

Sea la caja rectangular de imagen:

```text
E = [x_l,x_u] + i[y_l,y_u].
```

Primero se exige que no ocurra simultaneamente:

```text
0 in [x_l,x_u]
and
0 in [y_l,y_u].
```

Si la caja contiene el origen, el segmento se subdivide o queda inconcluso.

Para una caja que no contiene el origen se usara una separacion determinista.
Definir el punto de la caja mas cercano al origen por coordenadas:

```text
q_x = x_l, si x_l > 0
      x_u, si x_u < 0
      0,   en otro caso

q_y = y_l, si y_l > 0
      y_u, si y_u < 0
      0,   en otro caso.
```

Como la caja no contiene el origen, `(q_x,q_y) != (0,0)`. Elegir la rotacion
no normalizada:

```text
r = q_x - i*q_y.
```

Entonces se calcula con bolas:

```text
delta = inf Re(r*E).
```

El semiplano queda certificado solo si:

```text
delta > 0.
```

No es necesario normalizar `r`; evitar la raiz cuadrada reduce dependencia y
anchura. Si la aritmetica de bolas no separa `delta` de cero, se subdivide.
No se reemplaza la prueba por el signo del punto medio.

## 8. Incremento de argumento con rama validada

Una vez probado que `r*Lambda_3(s(u))` permanece en el semiplano derecho, el
logaritmo principal es holomorfo en toda la imagen del subsegmento.

Sean `A` y `B` bolas puntuales rigurosas para los extremos. Se calculara:

```text
Delta_ab
contains
Im(Log(r*B) - Log(r*A)).
```

La rotacion se cancela en la diferencia. La operacion solo es admisible si:

1. `A` y `B` pertenecen al mismo segmento certificado;
2. sus imagenes rotadas estan estrictamente en el semiplano derecho;
3. el logaritmo usado tiene semantica de bola compleja y rama principal;
4. el intervalo final se obtiene con redondeo dirigido;
5. no aparece `atan2`, phase unwrap ni conversion a `float`.

El certificado guardara referencias criptograficas a la imagen del segmento,
las bolas de extremos, la rotacion y el intervalo angular.

## 9. Acumulacion angular y entero unico

La ruta real no reutilizara las constantes decimales sinteticas de `pi`.
Obtendra una bola rigurosa `P` para `pi` desde el backend.

Los incrementos se sumaran en el orden orientado del contorno:

```text
A = sum Delta_ab
W = A / (2*P).
```

Todo el calculo se mantendra como bola real. El entero queda certificado solo
si:

```text
ceil(inf(W)) = floor(sup(W)) = N
and N >= 0.
```

Si el intervalo contiene cero y otro entero, ningun entero, o mas de un
entero, el resultado sera inconcluso. No se redondeara el punto medio.

## 10. Precision y subdivision congeladas

Se conserva la secuencia:

```text
precision_bits = 192, 256, 384, 512, 768, 1024
max_contour_depth = 40
max_root_isolation_depth = 60
```

Para cada precision se intentara el contorno completo con subdivision
determinista. Al agotar profundidad se pasa a la siguiente precision desde el
contorno original. No se mezclaran certificados creados con distintas
precisiones dentro de un mismo winding final, salvo que una futura derivacion
demuestre y congele una regla de promocion de bolas.

El orden de procesamiento permanece:

```text
borde inferior
borde derecho
borde superior
borde izquierdo
```

y dentro de cada biseccion se procesa primero la mitad inicial.

## 11. Procedencia y separacion sintetico/real

Los tipos publicos usados por los fixtures sinteticos no son evidencia
probatoria real. La futura ruta real usara tipos separados y opacos:

```text
RealCompletedL3PointEvidence
RealSegmentImageEvidence
RealHalfPlaneEvidence
RealArgumentIncrementEvidence
RealWindingEvidence
```

Cada objeto real se construira mediante una fabrica interna del backend y
contendra una capacidad de procedencia no emitida por constructores publicos.
Como minimo conservara:

```text
backend_id
backend_version
precision_bits
authorization_digest
runtime_code_digest
parent_evidence_hashes
serialized_ball_bounds
```

La tuberia real rechazara los tipos sinteticos incluso si tienen campos con
los mismos nombres. El modulo flotante `argument_principle.py` no sera
importado por la ruta real y debera salir del inventario probatorio antes de
006F o moverse a ayudantes de pruebas.

Esta capacidad evita ejecucion accidental o certificados fabricados por la
aplicacion. No pretende ser una frontera de seguridad contra codigo hostil
que ya controle el proceso Python o el sistema de archivos.

## 12. Contratos del backend futuro

El backend matematico real debera satisfacer contratos equivalentes a:

```text
completed_l3_point(point_ball, precision)
    -> RealCompletedL3PointEvidence

completed_l3_segment(segment, precision)
    -> RealSegmentImageEvidence

validate_half_plane(segment_evidence)
    -> RealHalfPlaneEvidence | inconclusive

argument_increment(half_plane_evidence, precision)
    -> RealArgumentIncrementEvidence | inconclusive

accumulate_winding(increments, pi_ball)
    -> RealWindingEvidence | inconclusive

l3_box_winding_count(box, precision)
    -> nonnegative_integer_certificate | inconclusive
```

`unique_integer` pertenecera a la capa de aritmetica real rigurosa, no a un
backend que pueda devolver un entero sin adjuntar el intervalo del que se
dedujo.

## 13. Estados de fallo cerrado

El resultado sera inconcluso si ocurre cualquiera de estas condiciones:

1. la API elegida no certifica entradas con radio no nulo;
2. una bola cruza `s=1` y la cancelacion de Hurwitz no esta regularizada;
3. Gamma puede tocar un polo;
4. la imagen del segmento puede contener cero;
5. no se demuestra un semiplano comun;
6. un extremo puede tocar el corte del logaritmo;
7. el incremento angular no es finito;
8. el winding no contiene exactamente un entero no negativo;
9. se agota precision o profundidad;
10. falta procedencia o se mezcla evidencia sintetica y real;
11. no coinciden hashes, identidad del caracter o precision;
12. cualquier operacion convierte una bola probatoria a `float`;
13. la evaluacion usa muestreo finito como sustituto de inclusion;
14. la biblioteca o version real no satisface el contrato revisado.

Ningun estado inconcluso se transformara en cero, ausencia de ceros o conteo
parcial.

## 14. Pruebas exigidas a una futura fase de codigo

Antes de ejecutar contornos reales deberan existir pruebas estructurales y de
aritmetica de bolas sobre funciones analiticas simples:

1. `F(s)=1`: imagen constante, winding cero;
2. `F(s)=s-rho`: una raiz interior, winding uno;
3. `F(s)=(s-rho)^2`: multiplicidad global dos;
4. raiz exterior: winding cero;
5. raiz sobre frontera: inconcluso;
6. segmento cuya caja contiene cero: subdivision obligatoria;
7. caja separable por la rotacion del punto mas cercano;
8. caja que no separa delta de cero: inconcluso;
9. logaritmo de extremos en semiplano derecho con intervalo certificado;
10. winding cuyo intervalo contiene un unico entero;
11. winding ambiguo: inconcluso;
12. rechazo de evidencia sintetica en la ruta real;
13. rechazo de objetos reales sin capacidad de procedencia;
14. rechazo de una API simulada que usa solo el centro de la bola;
15. rechazo de la resta meromorfa ingenua al cruzar `s=1`.

Estas pruebas no autorizaran evaluar `Lambda_3` real. La autorizacion de codigo
y la autorizacion de ejecucion continuaran separadas.

## 15. Criterios para una futura autorizacion de codigo

Antes de modificar el backend real se requerira:

1. revision y congelamiento de 006E6;
2. verificacion documental de que la Ruta A nativa satisface el contrato;
3. verificacion documental de que S1 acepta cajas complejas con radio;
4. verificacion documental de la semantica de bolas de la API concreta;
5. lista exacta de archivos y contratos a modificar;
6. plan TDD con pruebas rojas y fallos esperados;
7. politica de procedencia de evidencia real;
8. confirmacion de que no se ejecutaran contornos ni ceros durante esa fase.

La futura fase de codigo no sera 006F. 006F seguira reservada para una
autorizacion de ejecucion posterior a una nueva revision del backend real.

## 16. Veredicto de diseno

```text
006E6_DESIGN = complete_pending_review_and_freeze
ANALYTIC_FUNCTION = completed_L3
L_EVALUATION = native_entire_Dirichlet_L
REGULARIZED_HURWITZ = independent_control_only
SEGMENT_ENCLOSURE = whole_rectangular_complex_ball
VALIDATED_TAYLOR = amendment_only
HALF_PLANE = nearest_rectangle_point_rotation
ARGUMENT_INCREMENT = rigorous_complex_log_on_validated_right_half_plane
PI_SOURCE = rigorous_backend_ball
SYNTHETIC_REAL_SEPARATION = mandatory
REAL_BACKEND_CODE = not_authorized
REAL_FLINT_EXECUTION = forbidden
RIGOROUS_L3_COMPLETENESS = unresolved
H2_CERTIFIED = false
006F_READINESS = false
006F_EXECUTION = forbidden
C05_RERUN = forbidden
C35 = frozen
C15 = frozen
NOVELTY_CLAIM = false
```

006E6 define el motor matematico sobre planos. No construye ni enciende ese
motor y no aporta evidencia sobre ningun cero real.
