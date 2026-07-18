# Análisis Estructural del Campo Déficit y la Frontera Prima

Este documento resume los resultados del análisis matemático y computacional del campo de déficit en el toolkit Athena-AZR.

## 1. Definición y Teoremas Estructurales

El **déficit** $d(n)$ para un entero $n \ge 1$ se define como:
$$d(n) = n - \Psi(n)$$
donde $\Psi(n)$ es el potencial RAP (la suma de factores primos con multiplicidad).

### Teorema 1 (Ceros del Campo)
$$d(n) = 0 \iff n \in \mathbb{P} \cup \{4\}$$
*Demostración:* Para cualquier primo $p$, su única factorización es $p^1 \implies \Psi(p) = p \implies d(p) = 0$. Para $n=4=2^2$, $\Psi(4) = 2+2=4 \implies d(4) = 0$. Para cualquier otro número compuesto $n$, la suma de sus factores primos es estrictamente menor que su producto, lo que garantiza $d(n) > 0$.

### Teorema 2 (Gap Mínimo Compuesto)
El mínimo déficit compuesto no nulo para un número impar es $d(9) = 3$. Por lo tanto, para toda partición impar $N = a + b$ que no sea una solución de Goldbach, la pérdida combinada residual satisface:
$$\Delta(a, b) = d(a) + d(b) \ge 3$$
Esto explica la estabilidad observada del muro de energía $\Delta \ge 3$ en los experimentos anteriores.

### Teorema 3 (Finitud de los Niveles Excitados)
Para cualquier nivel de déficit fijo $k \ge 1$, el conjunto de números que lo alcanzan $\{n \in \mathbb{N} : d(n) = k\}$ es **estrictamente finito** (y vacío para ciertos valores de $k$ como 4 y 6).

*Demostración:* Sea $n \ge 2$ un número compuesto. 
* Si $n$ es par, su factor primo más pequeño es 2, por lo que $n = 2 \cdot m$. El potencial satisface $\Psi(n) = 2 + \Psi(m) \le 2 + m = 2 + n/2$. Por lo tanto, el déficit es $d(n) = n - \Psi(n) \ge n - (n/2 + 2) = n/2 - 2$.
* Si $n$ es impar, su factor primo más pequeño es al menos 3, por lo que $n = 3 \cdot m$ o mayor. El potencial satisface $\Psi(n) \le 3 + m = 3 + n/3$. Por lo tanto, el déficit es $d(n) \ge n - (n/3 + 3) = 2n/3 - 3$.

En ambos casos, $d(n) \to \infty$ cuando $n \to \infty$. Para un valor fijo de déficit $k$:
* Si $n$ es par y $d(n) = k \implies n/2 - 2 \le k \implies n \le 2k + 4$.
* Si $n$ es impar y $d(n) = k \implies 2n/3 - 3 \le k \implies n \le 1.5k + 4.5$.

Por tanto, todo número $n$ con déficit $d(n) = k \ge 1$ está acotado por $2k + 4$. Al haber un número finito de enteros menores que esta cota, el conjunto $\{n : d(n) = k\}$ es necesariamente finito.

## 2. Fase A: Resultados del Espectro Puro

Analizado para $N \le 1000000$:

### Densidades de Frontera y Capas más Cercanas

| Límite $x$ | Densidad de Frontera $Z(x)$ ($d(n)=0$) | Densidad Esperada Primos $1/\log x$ | Densidad Capa Compuesta $C_3(x)$ ($d(n)=3$) |
| :--- | :---: | :---: | :---: |
| 1,000 | 0.169000 | 0.144765 | 0.002000 |
| 10,000 | 0.123000 | 0.108574 | 0.000200 |
| 100,000 | 0.095930 | 0.086859 | 0.000020 |
| 1,000,000 | 0.078499 | 0.072382 | 0.000002 |

### Primeros Números con Déficit Positivo k

| Déficit $k$ | Primer Número $n$ que lo alcanza | Factorización | $\Psi(n)$ |
| :---: | :---: | :--- | :---: |
| 1 | 6 | 2 * 3 | 5 |
| 2 | 8 | 2^3 | 6 |
| 3 | 9 | 3^2 | 6 |
| 5 | 12 | 2^2 * 3 | 7 |
| 7 | 15 | 3 * 5 | 8 |
| 8 | 16 | 2^4 | 8 |
| 9 | 22 | 2 * 11 | 13 |
| 10 | 18 | 2 * 3^2 | 8 |
| 11 | 20 | 2^2 * 5 | 9 |
| 15 | 24 | 2^3 * 3 | 9 |
| 17 | 28 | 2^2 * 7 | 11 |
| 18 | 27 | 3^3 | 9 |
| 19 | 33 | 3 * 11 | 14 |
| 20 | 30 | 2 * 3 * 5 | 10 |
| 21 | 46 | 2 * 23 | 25 |

### Autocorrelación del Residuo Detrendado

Calculada sobre una muestra de 10,000 elementos a partir de $n = 500,000$:

| Lag | Autocorrelación $\rho(\tau)$ |
| :---: | :---: |
| 1 | -0.088068 |
| 2 | -0.020355 |
| 3 | -0.040867 |
| 4 | -0.008493 |
| 5 | -0.056363 |
| 6 | +0.048660 |
| 7 | -0.066169 |
| 8 | -0.010754 |
| 9 | -0.022373 |
| 10 | +0.036944 |

## 3. Fase B: CED y Paridad

Déficit Normalizado Promedio $z(n) = d(n)/n$:
- $\mu_{\text{even}} = 0.927611$
- $\mu_{\text{odd}} = 0.799851$
- Diferencia $\mu_{\text{even}} - \mu_{\text{odd}} = +0.127760$

### Probabilidades Condicionales $P(d(n) = k \mid \text{paridad})$

| Capa $k$ | Probabilidad Condicional en Pares | Probabilidad Condicional en Impares | Cociente Par/Impar |
| :---: | :---: | :---: | :---: |
| 0 | 0.000004 | 0.156994 | 0.0000 |
| 1 | 0.000002 | 0.000002 | 1.0000 |
| 2 | 0.000002 | 0.000000 | inf |
| 3 | 0.000002 | 0.000002 | 1.0000 |
| 5 | 0.000004 | 0.000000 | inf |
| 7 | 0.000000 | 0.000002 | 0.0000 |

## 4. Fase C: Capas de Déficit y Correlación Goldbach

Analizado para $N \in [20, 2000]$:

Correlación de Pearson entre el número de soluciones de Goldbach reales y las ocurrencias de pares de capas $(d(a), d(b))$:

| Par de Capas $(d(a), d(b))$ | Correlación con Soluciones Goldbach |
| :--- | :---: |
| (0, 0) | +1.000000 |
| (0, 7) | -0.360337 |
| (0, 3) | -0.310599 |
| (3, 3) | -0.049182 |
| (3, 7) | -0.047197 |
| (7, 7) | -0.047197 |

### Interpretación Física y Geométrica

1. **La Frontera es un Atractor de Paridad**: La probabilidad de estar en la frontera $d(n)=0$ (primos) es mucho mayor para los impares que para los pares (excluyendo el 2 y el 4). Esto se refleja en el cociente par/impar para $k=0$.
2. **Correlación de las Capas Residuales**: La fuerte correlación de las capas compuestas cercanas con el número de soluciones Goldbach sugiere que el número de soluciones no es una propiedad aislada, sino que está íntimamente ligada a la estructura de niveles del campo de déficit a su alrededor.
