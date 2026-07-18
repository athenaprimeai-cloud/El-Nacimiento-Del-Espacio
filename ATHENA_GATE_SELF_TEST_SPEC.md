# ATHENA — Gate Self-Test Spec

**Capa:** calibración formal del ATHENA MEMORY AXIS GATE
**Estado inicial:** UNRESOLVED — diseño definido, no congelado y no evaluado.
**Objeto:** verificar que el Gate rechaza tautologías estructurales deliberadas
y reconoce dos certificados positivos mínimos.

**No autoriza:** T-06, T-08, Intake, E008, código de motor, H2 real, FLINT
real, ceros, 006F ni inferencias de dominio.

> Un criterio que no puede rechazar su propia tautología todavía no es un
> criterio.

## 1. Alcance y nomenclatura

Esta especificación calibra únicamente:

~~~text
R0 → M4/M5-Gate → R5 → R4
~~~

**M4/M5-Gate** significa aquí confinamiento estructural no degenerado:

\[
\varnothing\neq\mathcal M=\{z:C(z)=0\}\subsetneq X\times H,
\qquad
\widetilde F(\mathcal M)\subseteq\mathcal M.
\]

No significa M4/M5 de ATHENA_MECHANISM_DISCOVERY_SYNTHESIS_v3.md, donde M4
es ceguera Phase III y M5 es posibilidad estructural de P*. Ningún resultado
de esta suite satisface por sí solo los M4/M5 de Discovery, ni a la inversa.

La suite es documental y formal. No se permite simulación, código, consulta de
raw previos, cálculo numérico, exploración de parámetros ni inferencia sobre
Athena.

## 2. Dos estados por caso

Cada caso registra dos resultados independientes:

| Campo | Valores | Significado |
| --- | --- | --- |
| criterion_verdict | PASS / FAIL / UNRESOLVED | Resultado del criterio atacado o ilustrado por el juguete. |
| calibration_status | PASS / FAIL / UNRESOLVED | Si el Gate produjo exactamente el resultado pre-registrado. |

Un FAIL esperado del criterio es un PASS de calibración:

~~~text
G-01: R0 = FAIL                  → calibration_status = PASS
G-03: M4/M5-Gate = PASS          → calibration_status = PASS
~~~

Un caso queda UNRESOLVED si falta una definición, un testigo, una prueba de
dependencia, un orden temporal o un registro de congelación necesario. Nunca
se eleva a PASS mediante interpretación narrativa.

## 3. Pre-registro: R4 activo desde el inicio

Antes de revisar, derivar, comentar o resolver un caso, se congela:

1. la versión completa de esta suite;
2. la matriz de decisión de la sección 4;
3. los seis juguetes y testigos de la sección 5;
4. el orden de revisión G-01 a G-06;
5. el identificador de versión, fecha/hora, hash y referencia inmutable;
6. el rol de revisión, sin autoridad para editar la especificación;
7. la declaración \(\Omega=\varnothing\): no hay variaciones libres.

Para cada caso \(j\) se vincula:

\[
\mathcal S_j=
(M_j,X_{0,j},F_j,H_j,O_j,\mu_j,\tau^+_j,\tau^-_j,\Omega_j,\Gamma_j).
\]

En esta suite \(H_j=0\): no existe trayectoria numérica que ejecutar. El
observable es un certificado formal o un ledger sintético; la métrica es
igualdad algebraica, implicación lógica o orden temporal. Un campo que no
aplica debe declararse N/A, no dejarse vacío.

Modificar cualquier elemento congelado crea una nueva versión. Nunca se
corrige una versión revisada en sitio.

## 4. Matriz de decisión congelada

| Caso | Criterio objetivo | Veredicto esperado | Calibración esperada |
| --- | --- | --- | --- |
| G-01 | R0, independencia fuerte | FAIL | PASS |
| G-02 | M4/M5-Gate, confinamiento | FAIL | PASS |
| G-03 | M4/M5-Gate, confinamiento | PASS | PASS |
| G-04 | R5-B, factor dinámico propio | FAIL | PASS |
| G-05 | R5-B, factor dinámico propio | PASS | PASS |
| G-06 | R4, congelación precomputacional | FAIL | PASS |

La suite completa solo puede terminar en:

~~~text
PASS
    los seis casos coinciden con la matriz y R4 de la propia suite está intacto.

FAIL
    un caso tiene un veredicto definitivo distinto del esperado, se acepta una
    tautología, se rechaza un certificado positivo o la suite cambia post-freeze.

UNRESOLVED
    falta un requisito necesario para decidir o para verificar integridad R4.
~~~

## 5. Casos de calibración

### G-01 — Circularidad de R0

**Objetivo:** R0 debe rechazar una predicción escondida en una premisa no
demostrada.

Se toma una premisa marcada como afirmación no demostrada:

\[
U:\quad\forall n\;Q(n),
\qquad
P^*:=Q(\bar 7).
\]

La derivación propuesta es \(U\Rightarrow P^*\). Al retirar \(U\), debe quedar
un contra-modelo de las definiciones limpias donde \(Q\) sea vacío.

**Testigos obligatorios:** mapa \(U\rightarrow P^*\), marca explícita de U
como no demostrada, derivación y contra-modelo limpio.

~~~text
criterion_verdict  = R0: FAIL
calibration_status = PASS
~~~

G-01 falla como calibración si R0 acepta la derivación o no distingue la
premisa que ya contiene la conclusión.

### G-02 — Acumulador sin confinamiento

**Objetivo:** una memoria de acumulación no debe confundirse con estructura.

Se toma:

\[
X=H=\mathbb Z_2,
\qquad
\widetilde F(x,h)=(x+1\pmod 2,\;h+x\pmod 2).
\]

El certificado superficial es \(C_0(x,h)\equiv0\), por lo que
\(\mathcal M_0=X\times H\). La órbita:

\[
(0,0)\to(1,0)\to(0,1)\to(1,1)\to(0,0)
\]

cubre todo el espacio. No existe un confinamiento no vacío, propio e invariante
para este juguete.

**Testigos obligatorios:** definición exacta, enumeración de la órbita, prueba
de cobertura y comprobación de que \(C_0\) no excluye ningún estado.

~~~text
criterion_verdict  = M4/M5-Gate: FAIL
calibration_status = PASS
~~~

Este caso no afirma que todo acumulador imaginable carezca de invariantes:
prueba solamente que acumulación por sí sola no certifica confinamiento.

### G-03 — Confinamiento conservativo genuino

**Objetivo:** el Gate debe reconocer un certificado analítico, propio y fijado
antes de toda revisión.

\[
X=H=\mathbb R,
\qquad
\widetilde F(x,h)=(-h,x),
\]

\[
C(x,h)=x^2+h^2-1,
\qquad
\mathcal M=\{(x,h):x^2+h^2=1\}.
\]

La prueba local es:

\[
C(\widetilde F(x,h))=(-h)^2+x^2-1=C(x,h).
\]

Además, \((1,0)\in\mathcal M\) y \((0,0)\notin\mathcal M\).

**Testigos obligatorios:** definiciones previas, igualdad local, un testigo de
no-vaciedad, uno de propiedad y declaración de que C no fue ajustada desde una
órbita.

~~~text
criterion_verdict  = M4/M5-Gate: PASS
calibration_status = PASS
~~~

### G-04 — Identidad disfrazada de factor

**Objetivo:** R5-B debe rechazar una conmutatividad que conserva toda la
información.

\[
X=\mathbb R^2,
\qquad
F(x,y)=(x+y,y),
\qquad
I=\operatorname{id}_X,
\qquad
\Phi=F.
\]

Entonces \(I\circ F=\Phi\circ I\), pero I es inyectiva y no reduce información.

**Testigos obligatorios:** igualdad de conmutatividad, prueba de inyectividad y
declaración de que el caso pretende R5-B, no R5-A ni R5-C.

~~~text
criterion_verdict  = R5-B: FAIL
calibration_status = PASS
~~~

### G-05 — Factor dinámico propio

**Objetivo:** R5-B debe reconocer reducción real con evolución cerrada.

\[
X=\mathbb R^2,
\qquad
F(x,y)=(x+1,2y),
\qquad
Y=\mathbb R,
\]

\[
I(x,y)=x,
\qquad
\Phi(u)=u+1.
\]

Por tanto:

\[
I\circ F(x,y)=x+1=\Phi\circ I(x,y).
\]

La reducción no es inyectiva porque
\((0,0)\ne(0,1)\) y \(I(0,0)=I(0,1)=0\).

**Testigos obligatorios:** igualdad exacta, par de no inyectividad, definición
de Y y \(\Phi\), y declaración congelada de R5-B.

~~~text
criterion_verdict  = R5-B: PASS
calibration_status = PASS
~~~

### G-06 — Búsqueda retrospectiva

**Objetivo:** R4 debe rechazar un resultado elegido después de observar los
datos.

Este caso contiene dos objetos: la suite actual, que sí está preregistrada, y
un protocolo objetivo sintético \(S_{\mathrm{sub}}\), diseñado para violar R4.
El ledger de \(S_{\mathrm{sub}}\) debe declarar:

~~~text
L0  No existe S_sub congelada: observable, métrica, umbrales, espacio de
    búsqueda y multiplicidad no están fijados.
L1  Se observan resultados D.
L2  Después se introducen U = {u1,u2,u3}, W = {w1,w2} y se elige el máximo.
L3  Se reclama coincidencia local sin umbral global ni corrección declarada.
~~~

**Testigos obligatorios:** ledger con \(L0\prec L1\prec L2\prec L3\), evidencia
de ausencia de especificación previa y lista de campos no congelados
\((O,\mu,\tau^+,\tau^-,\Omega,\Gamma)\).

~~~text
criterion_verdict  = R4: FAIL
calibration_status = PASS
~~~

R4 es UNRESOLVED, no FAIL, si el orden temporal no puede demostrarse.

## 6. Reingreso y límites

Un fallo de la suite no se arregla cambiando expectativas, juguetes o
testigos de la misma versión:

~~~text
suite v1
  → calibration FAIL, UNRESOLVED o ruptura R4
  → diagnóstico archivado
  → nueva versión de Gate o spec
  → suite v2, nuevo freeze, G-01…G-06 desde el inicio
~~~

Un PASS de esta suite solo calibra seis casos mínimos. No significa que exista
un mecanismo Athena, una P*, R5-C, una ley global, una autorización de T-06,
una certificación H2 ni una ejecución real de FLINT.

---

*La autoprueba no busca producir un patrón. Busca demostrar que la aduana sabe
rechazar una reformulación y reconocer una restricción cuando ambas aparecen en
forma mínima.*
