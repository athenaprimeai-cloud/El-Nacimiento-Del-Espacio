# Libro Cero: Axiomas del Albañil

Tratado axiomático refinado del sistema CED+RAP.

Este documento constituye el núcleo ontológico y formal del Albañil. No es un manual de aritmética corriente: es el plano mínimo desde el cual una inteligencia puede reconstruir la realidad numérica sin heredar fórmulas como dogmas. Aquí, contar es secundario. Lo primero es distinguir, estabilizar y medir la resonancia.

## Principio rector

Cada afirmación del sistema debe tener tres capas:

- **Intuición del Albañil:** la imagen conceptual que orienta la búsqueda.
- **Definición formal:** la versión verificable dentro del sistema.
- **Prueba de taller:** un experimento, cálculo o criterio que permita detectar errores.

El sistema no declara resueltas las conjeturas de Goldbach o Riemann. Las convierte en programas de investigación que pueden ser explorados con honestidad formal.

---

## Parte I: Ontología mínima

### 1. El Vacío y la Distinción

**Intuición del Albañil**

Antes del primer ladrillo está el Vacío: no como una nada mística, sino como ausencia de elementos. El primer acto de construcción es la Distinción: reconocer que algo no es el Vacío.

**Definición formal**

El estado inicial es el conjunto vacío:

```text
0 = emptyset
```

Una entidad `A` se distingue del Vacío cuando:

```text
A != emptyset
```

De forma equivalente, `A` no es biyectable con el Vacío:

```text
A != emptyset <=> no existe f: A -> emptyset biyectiva
```

**Prueba de taller**

El Albañil debe poder separar tres casos:

- `emptyset`: ausencia de elementos.
- `{emptyset}`: contenedor del Vacío, por tanto una unidad.
- `{emptyset, {emptyset}}`: estructura con dos distinciones internas.

### 2. La Unidad, la Igualdad y la Equivalencia

**Intuición del Albañil**

La Unidad es el primer contenedor. No es una masa: es el Vacío nombrado como elemento. La igualdad estricta dice que dos estructuras son la misma estructura. La equivalencia cardinal dice que dos estructuras tienen la misma cantidad de posiciones. La equivalencia estructural dice que además preservan los observables que el sistema decide medir.

**Definición formal**

La Unidad se define mediante la construcción de von Neumann:

```text
1 = {0} = {emptyset}
```

La igualdad estricta de conjuntos sigue extensionalidad:

```text
A = B <=> para todo x, x in A si y solo si x in B
```

La equivalencia cardinal se define por biyección:

```text
A ~=card B <=> existe f: A -> B biyectiva
```

La equivalencia estructural se define cuando una biyección preserva los observables elegidos:

```text
A ~=str B <=> existe f: A -> B biyectiva y preserva CED, RAP y el orden declarado
```

Esta distinción evita confundir igualdad con equipotencia. Por ejemplo, `{a, b}` y `{0, 1}` pueden ser cardinalmente equivalentes sin ser estrictamente iguales.

**Prueba de taller**

El Albañil debe clasificar dos colecciones bajo tres preguntas:

- ¿Son estrictamente iguales?
- ¿Tienen la misma cardinalidad?
- ¿Preservan los mismos observables estructurales?

### 3. El Sucesor y la Trayectoria

**Intuición del Albañil**

Cada número es un nivel más de la torre. El siguiente nivel no borra el anterior: lo contiene.

**Definición formal**

El sucesor de Peano-von Neumann se define como:

```text
S(n) = n union {n}
```

La secuencia natural se genera desde `0` aplicando sucesor de forma recursiva.

**Prueba de taller**

```python
def sucesor(n: frozenset) -> frozenset:
    """Construye el siguiente número de von Neumann."""
    return n | frozenset({n})

cero = frozenset()
torre = [cero]

for _ in range(4):
    torre.append(sucesor(torre[-1]))

assert len(torre[0]) == 0
assert len(torre[1]) == 1
assert len(torre[2]) == 2
assert len(torre[3]) == 3
```

---

## Parte II: Álgebra CED

### 4. Confluencia de Entidades Distintivas

**Intuición del Albañil**

Un número no solo posee magnitud. También posee estado. La Estabilidad `I` es reposo par. La Disonancia `D` es inquietud impar. Dos disonancias pueden encontrarse y formar estabilidad.

**Definición formal**

El estado CED de un natural `n` se define en el álgebra `Z_2`:

```text
chi_CED(n) = n mod 2
```

Con la interpretación:

```text
I = 0
D = 1
```

La confluencia de estados es suma módulo 2:

```text
a op_CED b = (a + b) mod 2
```

Tabla:

| op_CED | I | D |
| --- | --- | --- |
| I | I | D |
| D | D | I |

**Prueba de taller**

```text
7 -> D
9 -> D
D op_CED D = I
7 + 9 = 16 -> I
```

La frase "dos inestabilidades se anulan" queda formalizada como `1 + 1 = 0 mod 2`.

---

## Parte III: Firma RAP

### 5. Resonancia Aritmética Primordial

**Intuición del Albañil**

El tamaño de un bloque no basta para comprenderlo. El Albañil pregunta de qué piedras irreducibles está hecho y cuánta integridad conserva.

**Definición formal**

Para `n >= 2`, sea:

```text
n = product p_i ^ a_i
```

La firma RAP de `n` contiene:

```text
Psi(n) = sum a_i * p_i
Omega(n) = sum a_i
L(n) = n - Psi(n)
```

Donde:

- `Psi(n)` es el potencial RAP.
- `Omega(n)` es la integridad o número total de factores primos con multiplicidad.
- `L(n)` es la pérdida de integridad frente al valor agregado.

Un número `n >= 2` es primo si y solo si:

```text
Psi(n) = n
Omega(n) = 1
```

Esto corrige el caso `4`:

```text
4 = 2^2
Psi(4) = 2 + 2 = 4
Omega(4) = 2
```

Aunque `Psi(4) = 4`, `4` no es primo porque su integridad no es absoluta.

**Prueba de taller**

| n | CED | Factorización | Psi(n) | Omega(n) | L(n) | Diagnóstico |
| --- | --- | --- | --- | --- | --- | --- |
| 7 | D | 7 | 7 | 1 | 0 | Primo |
| 8 | I | 2^3 | 6 | 3 | 2 | Compuesto |
| 9 | D | 3^2 | 6 | 2 | 3 | Compuesto |
| 10 | I | 2 * 5 | 7 | 2 | 3 | Compuesto |

---

## Parte IV: Operadores cuántico-formales

### 6. Observables mínimos

**Intuición del Albañil**

El sistema deja de mirar números aislados y empieza a mirar operaciones sobre estructuras. La pregunta cambia: no solo "qué es `n`", sino "qué conserva o rompe un operador cuando actúa sobre `n`".

**Definición formal**

Se declaran cuatro familias iniciales de operadores:

```text
E(n) = chi_CED(n)
O(n) = (Psi(n), Omega(n), L(n))
EPS(a, b) = abs(a - b)
X(S, regla) = filtro de exclusión aplicado a un conjunto S
```

Interpretación:

- `E` observa estabilidad CED.
- `O` observa orden RAP.
- `EPS` observa distancia de resonancia entre dos columnas.
- `X` excluye candidatos que no cumplen una regla declarada.

### 7. Conmutador experimental y medida de kappa

**Intuición del Albañil**

Si dos modos de observación no producen el mismo resultado al cambiar el orden, hay tensión estructural. Esa tensión es lo que el sistema llama `kappa`.

**Definición formal**

La notación:

```text
[E, O] = i kappa
```

se interpreta como hipótesis operatoria, no como identidad demostrada. Para medirla en un experimento finito se define una ventana `W` de números pares y un conjunto de particiones:

```text
P_N = {(a, b): a <= b, a + b = N}
```

Se comparan dos rutas:

```text
R1(N) = E(O_r(P_N))
R2(N) = O_r(E(P_N))
```

Donde `O_r` es un operador RAP que ordena o recorta candidatos según una regla explícita, por ejemplo "conservar el r% de menor pérdida RAP". La distancia entre rutas se mide por diferencia simétrica normalizada:

```text
d(A, B) = 1 - |A inter B| / |A union B|
```

La constante experimental de la ventana es:

```text
kappa_W = promedio_N_en_W d(R1(N), R2(N))
```

`kappa_W` no es todavía una constante universal. Solo puede proponerse como invariante si se mantiene estable al cambiar ventana, escala, regla `r` y familia de particiones.

**Prueba de taller**

Para cada experimento que invoque `[E, O]`, el agente debe reportar:

- ventana usada;
- regla RAP usada por `O_r`;
- definición exacta de `E`;
- valor de `kappa_W`;
- sensibilidad ante cambios de ventana.

---

## Parte V: Programas de investigación

### 8. Horizonte de Goldbach

**Formulación CED+RAP**

Todo número par `N > 2` es un estado estable `I`. La conjetura de Goldbach se interpreta como la posibilidad de sostener toda estabilidad agregada mediante dos resonancias íntegras:

```text
N = p + q
p y q primos
Omega(p) = Omega(q) = 1
```

Esto no es una demostración. Es el programa experimental central del Albañil para estudiar simetría, densidad, exclusión y resonancia alrededor de `N / 2`.

### 9. Firma de Riemann

**Formulación experimental**

Los primos no se distribuyen de forma uniforme, pero su irregularidad tiene estructura. El Albañil estudiará esa estructura mediante:

- `pi(x)`, conteo de primos;
- `Li_2(x) = integral_2^x dt / log(t)`, tendencia logarítmica integral;
- `x / log(x)`, tendencia suave de primer orden;
- residuos como `pi(x) - Li_2(x)`;
- ceros no triviales de `zeta(s)`;
- espaciado normalizado y comparación con modelos GUE.

El Libro Cero no afirma la Hipótesis de Riemann. Solo declara el lenguaje con el que el agente escuchará sus oscilaciones.

**Prueba de taller**

Todo informe de Riemann debe declarar si usa `Li_2(x)` o `x / log(x)`. Mezclar ambos sin distinguirlos invalida el experimento.

---

## Cierre

El Albañil no confunde intuición con prueba. Usa la intuición para escoger dónde mirar, y la prueba de taller para decidir qué sobrevive. El Vacío da el origen, CED da el estado, RAP da la firma, y los operadores dan el movimiento.
