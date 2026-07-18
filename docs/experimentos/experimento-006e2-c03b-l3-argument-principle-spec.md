# Experimento 006E2: especificacion del principio del argumento para L3

## 1. Estado y alcance

```text
experiment_id = G5B-006E2
target = rigorous_L3_argument_principle_design
status = specification_only
method = pure_argument_principle
hybrid_hardy_argument = rejected_for_now
L3_turing_method = rejected_for_now
code_authorization = false
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

Este documento fija el diseno matematico y los contratos que debera cumplir
una futura integracion inerte del backend real. No autoriza crear o modificar
codigo, importar FLINT, evaluar funciones L reales, recorrer contornos,
calcular ceros ni generar archivos experimentales.

La decision metodologica es exclusiva:

```text
L3 completeness method = pure argument principle only.
```

No se usaran valores de Hardy para localizar candidatos reales y no se
introducira un metodo de Turing especifico para L3 durante esta fase.

## 2. Estado heredado

006E acepto la capa estructural despues de parches, pero mantuvo bloqueado
006F porque el principio del argumento riguroso para `L(s,chi_3)` no estaba
implementado.

```text
006E_CODE_REVIEW = completed
006D_STRUCTURAL_CODE = accepted_after_review_patches
STRUCTURAL_GUARDS = passed
REAL_BACKEND_IMPLEMENTATION = incomplete
RIGOROUS_L3_COMPLETENESS = unresolved
006F_READINESS = false
H2_CERTIFIED = false
```

La regla central de 006B permanece inalterada:

```text
Certificacion H2
= aislamiento riguroso de cada cero
+ conteo completo hasta T=500.
```

006E2 disena el mecanismo de conteo completo y la base para el aislamiento
bidimensional. No certifica ninguno de los dos.

## 3. Funcion analitica que se contara

Sea `chi_3` el caracter primitivo real impar modulo 3. Se usara la funcion
completada:

```text
Lambda_3(s)
= (3/pi)^((s+1)/2)
  * Gamma((s+1)/2)
  * L(s,chi_3).
```

La potencia se definira mediante la exponencial y el logaritmo real de la base
positiva `3/pi`:

```text
(3/pi)^((s+1)/2)
= exp(((s+1)/2) * log(3/pi)).
```

Esto evita introducir una rama compleja arbitraria. Para un caracter primitivo
no principal, la funcion completada es entera despues de las cancelaciones
analiticas correspondientes. La implementacion futura no podra tratar los
factores por separado en una region que atraviese un polo aparente sin
certificar la cancelacion.

El rectangulo principal usa:

```text
sigma_left  = -1/2
sigma_right =  3/2
t_bottom    =  0
t_top       =  T
T in {143, 200, 300, 500}.
```

En esta franja, el argumento de Gamma tiene parte real entre `1/4` y `5/4`,
por lo que no atraviesa polos de Gamma. Cada frontera, incluida `t=0`, debera
certificarse libre de ceros. Si una frontera no puede certificarse, el
resultado sera `inconclusive`; no se desplazara despues de observar el
resultado salvo mediante una regla de frontera previamente congelada en una
autorizacion posterior.

La ecuacion funcional y las simetrias podran usarse como controles de
consistencia. No sustituiran el conteo del contorno y no se asumira GRH.

## 4. Contorno y orientacion

Cada rectangulo se recorrera con orientacion positiva, en este orden:

```text
1. (-1/2, 0)   -> ( 3/2, 0)   borde inferior
2. ( 3/2, 0)   -> ( 3/2, T)   borde derecho
3. ( 3/2, T)   -> (-1/2, T)   borde superior
4. (-1/2, T)   -> (-1/2, 0)   borde izquierdo
```

Los vertices y parametros geometricos se representaran mediante racionales o
decimales exactos. No se usaran coordenadas binarias `float` para construir
el contorno.

Los modelos futuros seran inmutables y distinguiran:

```text
RationalComplexPoint
DirectedSegment
RectangularContour
SegmentImageCertificate
ArgumentIncrementCertificate
WindingCertificate
RectangleZeroCountCertificate
```

El certificado final conservara el orden de los segmentos, la orientacion, la
precision usada, la profundidad de subdivision y referencias verificables a
los certificados locales.

## 5. Regla local de exclusion del origen

Para cada subsegmento dirigido `[a,b]`, el backend riguroso debera evaluar una
extension intervalar de `Lambda_3` sobre todo el segmento, no solo en sus
extremos:

```text
E_ab contains { Lambda_3((1-u)a + ub) : 0 <= u <= 1 }.
```

Un muestreo finito de puntos no satisface esta condicion. El certificado local
solo sera admisible si demuestra simultaneamente:

```text
0 not_in E_ab
entire_segment_covered = true
arithmetic = rigorous_ball
```

Para fijar una rama local del argumento se buscara una rotacion compleja `r`
que cumpla, con aritmetica de bolas:

```text
Re(r * E_ab) > 0.
```

La rotacion puede proponerse a partir del punto medio de la bola, pero queda
aceptada unicamente por la desigualdad intervalar anterior. La eleccion
heuristica de `r` no tiene valor probatorio.

Si toda la imagen rotada esta en el semiplano derecho, existe una rama
continua del logaritmo sobre la imagen del subsegmento. El incremento local se
encerrara mediante:

```text
Delta_ab
contains Im(log(r * Lambda_3(b)) - log(r * Lambda_3(a))).
```

La rotacion se cancela en la diferencia. El certificado debera guardar las
bolas de los extremos, la envolvente del segmento, la rotacion validada y el
intervalo resultante. No se aceptaran fases escalares, `atan2` sobre puntos ni
desenvoltura de fase basada en redondeo.

## 6. Subdivision adaptativa

La subdivision de frontera sera determinista:

1. intentar certificar el segmento completo;
2. si la envolvente contiene cero, no cabe en un semiplano validado o el
   incremento es ambiguo, bisecar exactamente en el punto medio;
3. procesar primero la mitad inicial y luego la mitad final;
4. repetir hasta `max_contour_depth = 40`;
5. aumentar precision solo en la secuencia congelada
   `192, 256, 384, 512, 768, 1024` bits;
6. si ninguna combinacion cierra, devolver `inconclusive`.

No se podran cambiar profundidades, precisiones ni orden de recorrido despues
de observar un conteo. Alcanzar el limite no autoriza extrapolar ni redondear.

La condicion de cierre local es estricta: una caja que apenas toca el origen o
un semiplano cuyo limite puede contener parte de la imagen se considera no
certificada.

## 7. Acumulacion y entero unico

Los intervalos `Delta_ab` se sumaran en el orden orientado del contorno usando
aritmetica intervalar dirigida. Sea `A` el intervalo acumulado. Se calculara:

```text
W = A / (2*pi),
```

donde `pi` tambien sera una bola rigurosa. El conteo queda certificado solo si
`W` contiene exactamente un entero `N`:

```text
unique_integer(W) = N
N >= 0.
```

El resultado `N` cuenta ceros con multiplicidad dentro del rectangulo, porque
`Lambda_3` es entera en la region y la frontera ha sido certificada libre de
ceros.

Si `W` contiene cero o varios enteros, si no puede separarse de un semientero,
o si cualquier certificado local esta ausente, el resultado obligatorio es:

```text
count_status = inconclusive
certified_count = none
```

No se redondeara el punto medio de `W`.

## 8. Conteos anidados hasta altura 500

Se generara en una futura ejecucion un certificado independiente para cada
altura congelada:

```text
T = 143, 200, 300, 500.
```

Los cuatro conteos deberan ser no decrecientes y sus fronteras superiores
deberan estar certificadas libres de ceros. El certificado de `T=500` no
sustituye a los tres conteos intermedios.

Cada `RectangleZeroCountCertificate` debera contener al menos:

```text
function_id = L3
conductor = 3
character_id = 3.2
parity = 1
rectangle
orientation = positive
boundary_zero_free = true
certified_total_count
working_precision_bits
maximum_subdivision_depth_used
segment_certificate_hashes
method = pure_argument_principle
```

## 9. Aislamiento individual sin Hardy

El principio del argumento tambien sera la unica fuente futura de candidatos.
No se sembraran cajas con ceros publicados ni con cambios de signo de Hardy.

El rectangulo completo se particionara recursivamente. Para cada caja:

```text
count = 0  -> descartar caja;
count = 1  -> refinar hasta el ancho objetivo;
count > 1  -> subdividir;
inconclusive -> detener esa rama como unresolved_cluster.
```

La biseccion primaria se hara sobre el lado mas largo; en empate se divide
primero la direccion imaginaria. Una frontera interna que no pueda probarse
libre de ceros usara, en orden, desplazamientos racionales preregistrados
respecto del punto medio:

```text
0,
+1/8, -1/8,
+1/16, -1/16,
+1/32, -1/32,
+1/64, -1/64,
+1/128, -1/128,
+1/256, -1/256,
+1/512, -1/512,
+1/1024, -1/1024
```

Cada desplazamiento es una fraccion del ancho del lado que se divide. Se usa
el primer candidato cuya nueva frontera se certifique libre de ceros. Si todos
fallan, la caja queda inconclusa. Esta secuencia debera congelarse antes de una
autorizacion de codigo y no podra elegirse segun el resultado numerico.

El limite sera `max_root_isolation_depth = 60`. Una caja aceptada debera tener
anchos real e imaginario no mayores que `1e-20`, contener exactamente un cero
contado con multiplicidad y ser disjunta de todas las demas cajas aceptadas.

Si una caja pequena conserva conteo mayor que uno, el principio del argumento
no distingue por si solo una raiz multiple de varias raices proximas. El
resultado sera `unresolved_cluster`; no se inventara una multiplicidad. Por
ello, este metodo puede certificar automaticamente cajas individuales de
conteo uno, pero un cero multiple requeriria una futura ampliacion
explicitamente autorizada.

## 10. Recta critica y ausencia de GRH asumida

El algoritmo contara toda la franja rectangular, no solo `Re(s)=1/2`. Una caja
fuera de la recta critica no se descartara ni se proyectara sobre ella.

`critical_line_certified=true` solo podra declararse si se demuestra mediante
el propio certificado, por ejemplo:

1. la caja es invariante bajo la simetria funcional correspondiente;
2. contiene exactamente un cero;
3. la simetria obliga a ese cero a estar fijado en `Re(s)=1/2`.

En otro caso, la caja conservara su intervalo real completo y
`critical_line_certified=false`. La completitud no puede depender de asumir
GRH. Antes de una implementacion futura debera revisarse el validador actual,
que rechaza de forma global cajas L3 sin certificacion de recta critica.

## 11. Contratos de backend

La futura capa de dominio no recibira objetos FLINT directamente. El backend
riguroso debera ofrecer contratos equivalentes a:

```text
completed_l3_point(point, precision) -> rigorous complex ball
completed_l3_segment(segment, precision) -> rigorous range enclosure
validate_half_plane(enclosure) -> rotation certificate or inconclusive
argument_increment(segment_certificate) -> rigorous real interval
unique_integer(interval) -> integer certificate or inconclusive
```

La interfaz debera impedir que una envolvente de extremos se etiquete como
envolvente de todo el segmento. Los tipos y campos probatorios seran distintos.

El adaptador `PythonFlintBackend` continuara con importacion perezosa. Cada
operacion real permanecera detras de:

1. autorizacion 006F valida;
2. inventario exacto de hashes de codigo;
3. ruta de salida preregistrada;
4. inicializacion explicita posterior a las guardias.

Durante la futura fase de integracion inerte, estas operaciones deberan lanzar
`NotImplementedError` o un error cerrado equivalente. Los tests no podran
simular una autorizacion 006F para alcanzar FLINT real.

## 12. Arquitectura futura de archivos

Una autorizacion de codigo posterior podra proponer cambios limitados a:

```text
athena_azr/h2_zero_certifier/
    completed_l3.py
    contour.py
    ball_argument.py
    l3_argument_count.py
    models.py
    config.py
    backend.py
    python_flint_backend.py
    l3_certifier.py
    validation.py

tests/
    test_h2_completed_l3.py
    test_h2_contour.py
    test_h2_ball_argument.py
    test_h2_l3_argument_count.py
    test_h2_l3_isolation.py
    test_h2_real_flint_guarded.py
```

Cada archivo tendra una responsabilidad:

1. `completed_l3.py`: identidad y convenciones de `Lambda_3`;
2. `contour.py`: geometria exacta y orientacion;
3. `ball_argument.py`: certificados locales y acumulacion angular;
4. `l3_argument_count.py`: conteo rectangular y estados inconclusos;
5. `l3_certifier.py`: particion, aislamiento y comparacion global;
6. `python_flint_backend.py`: adaptacion perezosa, inicialmente inerte.

## 13. Pruebas sinteticas obligatorias

Una futura fase de codigo inerte debera usar TDD y demostrar, sin FLINT real:

1. contorno rectangular cerrado y orientado positivamente;
2. rechazo de contornos degenerados o de orientacion incorrecta;
3. conteo 0 para una funcion sintetica sin raices;
4. conteo 1 para una raiz simple interior;
5. conteo 2 para dos raices simples interiores;
6. conteo 2 para una raiz doble, conservando multiplicidad global;
7. exclusion de raices exteriores;
8. estado inconcluso si una raiz toca la frontera;
9. subdivision cuando una envolvente local contiene cero;
10. fallo cerrado al agotar profundidad o precision;
11. rechazo si el intervalo de winding contiene varios enteros;
12. aislamiento de cajas de conteo uno;
13. `unresolved_cluster` para una caja de conteo mayor que uno que no se
    separa;
14. ninguna suposicion implicita de recta critica;
15. importacion de paquete sin importar FLINT;
16. doble bloqueo de toda prueba de integracion real;
17. cero escrituras fuera de temporales;
18. cero constantes de ceros reales incrustadas.

Los polinomios sinteticos podran tener raices racionales conocidas. Sus
backends de prueba deberan producir envolventes rigurosas construidas para el
fixture, no muestreos numericos presentados como pruebas.

## 14. Criterios de fallo cerrado

El sistema devolvera `inconclusive` si ocurre cualquiera de estas condiciones:

1. una imagen de segmento puede contener el origen;
2. no se valida un semiplano comun;
3. una rama local de logaritmo no queda justificada;
4. el winding total no contiene un entero unico;
5. una frontera puede contener un cero;
6. se alcanza el maximo de precision o subdivision;
7. los conteos anidados decrecen;
8. el conteo global no coincide con la suma de cajas aisladas;
9. queda un grupo sin resolver;
10. falta procedencia o un hash requerido;
11. una operacion intenta usar `float` como dato probatorio;
12. una llamada real intenta ejecutarse sin 006F.

Ningun fallo puede transformarse en un conteo parcial aceptable.

## 15. Condiciones para una futura autorizacion de codigo

Antes de modificar codigo deberan aprobarse por separado:

1. esta especificacion congelada y su SHA-256;
2. un plan TDD con pruebas rojas y archivos exactos;
3. el contrato de envolvente de segmento completo;
4. el criterio de semiplano y logaritmo local;
5. la secuencia de divisiones internas;
6. la politica para cajas fuera de la recta critica;
7. la separacion entre integracion inerte y ejecucion 006F.

La autorizacion de codigo no autorizara instalar FLINT, ejecutar evaluaciones
reales, calcular ceros ni escribir artefactos.

## 16. Estado final

```text
006E2_SPECIFICATION = complete_pending_review_and_freeze
METHOD = pure_argument_principle
FUNCTION = completed_L3
GLOBAL_COUNT = rectangular_winding_with_ball_arithmetic
INDIVIDUAL_ISOLATION = recursive_argument_principle_partition
GRH_ASSUMED = false
HARDY_USED = false
L3_TURING_USED = false
REAL_BACKEND = inert
CODE_AUTHORIZATION = false
EXECUTION_AUTHORIZATION = false
H2_CERTIFIED = false
006F = blocked
C05_RERUN = forbidden
C35 = frozen
C15 = frozen
NOVELTY_CLAIM = false
```

## Referencias internas y tecnicas

1. `docs/experimentos/experimento-006b-c03b-protocolo-certificacion-ceros-500.md`.
2. `docs/experimentos/experimento-006c-c03b-h2-zero-certifier-implementation-plan.md`.
3. `docs/experimentos/experimento-006e-c03b-h2-zero-certifier-code-review.md`.
4. python-flint, documentacion de bolas complejas e integracion validada:
   <https://python-flint.readthedocs.io/en/latest/acb.html>.
5. python-flint, documentacion de caracteres de Dirichlet y funciones L:
   <https://python-flint.readthedocs.io/en/latest/dirichlet.html>.
