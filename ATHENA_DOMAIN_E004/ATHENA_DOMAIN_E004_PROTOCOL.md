# ATHENA DOMAIN-E004 — Protocolo **CONGELADO** (quirúrgico)

**Clase:** dominio Athena · material espectral no aritmético vs controles  
**Versión:** **1.0 CONGELADO**  
**Fecha:** 2026-07-17  
**No es:** Hilbert–Pólya · Hamiltoniano · modularidad · Riemann · catedral  

**Anclas:** MD-034 (dualidad) · MD-035 (anti-contrabando) · MD-036 (controles negativos)

---

## 1. Pregunta

> ¿Existe una estructura espectral emergente, en un grafo de \(\mathbb{N}\) definido **sin** conocimiento primo,  
> cuya métrica \(M\) discrimine el conjunto de primos \(P\) frente a controles de misma cardinalidad / impostores?

En una línea:

> **¿Hay material para una pared, o solo la forma del ladrillo que ya pusimos (densidad/orden)?**

---

## 2. Entrada

```text
X = {1, 2, …, N}
N = 10000          # campaña 1 quirúrgica (escala baja)
```

No se usa primalidad para definir la geometría de \(G\).

---

## 3. Familia de grafos (una sola)

**Vecindad ordinal** (MD-035 — permitida):

\[
V = \{1,\ldots,N\}
\qquad
(i,j)\in E \iff 0 < |i-j| \le k
\qquad
k = 10
\]

Grafo no dirigido, simple, sin pesos.

**Prohibido en \(E\):** \(p\mid n\), \(\gcd\), factores, criba como geometría.

---

## 4. Conjuntos (MD-036 — congelados antes de mirar)

Sea \(\pi(N)=\#P\). Todos los controles se recortan o construyen a **cardinalidad** \(m=\pi(N)\) salvo indicación.

| ID | Conjunto | Construcción |
| -- | -------- | ------------ |
| **P** | Primos | \(\{p\le N: p\text{ primo}\}\) |
| **C1** | Impostor densidad | \(m\) enteros **uniformes distintos** en \(\{1,\ldots,N\}\), seed \(s\) (réplicas) |
| **C2** | Semiprimos | primeros \(m\) enteros \(\le N\) con **exactamente dos** factores primos contando multiplicidad (p.ej. \(4,6,9,10,\ldots\)); si hay menos de \(m\), completar con semiprimos siguientes no usados (si \(N\) no basta: reportar y usar todos los disponibles + nota) |
| **C3** | Artificial | números de **Ulam** \(\le N\); si \(\#U<m\), completar con los enteros restantes de la secuencia Ulam extendida o, si insuficiente, los \(m\) primeros Ulam truncando \(m\) (documentar \(m_3=\min(m,\#U)\)); comparar con cardinalidad efectiva emparejada |

**Réplicas C1:** seeds \(s=0..99\) (100 impostores de densidad).

**Emparejamiento:** para C2/C3, si \(|S|\ne m\), se usa \(m'=\min(|S|,m)\) y se **re-muestrea** también un subconjunto aleatorio de \(P\) de tamaño \(m'\) solo para ese contraste (seed fijo 0), documentado en ficha. Preferencia: elegir \(N\) tal que C2 tenga \(\ge m\) elementos cuando sea posible.

---

## 5. Inducción y Laplaciano

Para cada conjunto \(S\subset V\):

1. Grafo inducido \(G[S]=(S, E\cap(S\times S))\).  
2. Laplaciano combinatorio \(L = D - A\) (simétrico, \(L_{ii}=\deg_S(i)\)).

No se suaviza. No se rewirea con reglas aritméticas.

---

## 6. Una métrica espectral \(M\) (campaña 1)

**No** lista de propiedades bonitas. **Una:**

### Segundo momento espectral (forma cerrada)

Sea \(\lambda_1,\ldots,\lambda_{n}\) los autovalores de \(L\) (\(n=|S|\)).  
Sin diagonalizar:

\[
\sum_i \lambda_i = \mathrm{tr}(L) = \sum_{v\in S}\deg(v) = 2|E_S|
\]

\[
\sum_i \lambda_i^2 = \|L\|_F^2 = \sum_{v}\deg(v)^2 + 2|E_S|
\]

(para grafo simple no dirigido).

\[
M(S)
=
\begin{cases}
\dfrac{1}{n}\displaystyle\sum_i \lambda_i^2
=
\dfrac{1}{n}\Big(\sum_v \deg(v)^2 + 2|E_S|\Big)
& n\ge 1\\[6pt]
0 & n=0
\end{cases}
\]

**Nombre en informes:** *segundo momento espectral del Laplaciano inducido* \(M_2\).  
**No** se afirma GUE, semicírculo, ni operador.

**Por qué esta y no otra:** es genuinamente espectral (momento del espectro), barata, reproducible sin eigensolver, no es solo “¿hay aristas?” (usa \(\sum\deg^2\)).

---

## 7. Discrepancias y nulos

\[
D(S,T) = |M(S)-M(T)|
\]

Sobre réplicas C1:

\[
D_{\mathrm{nulo}}
=
\mathrm{median}_{s}\,
D(C1_s,\, C1_{s'})
\]

(o, equivalente operativo: distribución de \(M(C1_s)\); ver estadísticos abajo).

### Estadísticos congelados

| Símbolo | Definición |
| ------- | ---------- |
| \(M_P\) | \(M(P)\) |
| \(\mu_{C1},\,\sigma_{C1}\) | media y desv. muestral de \(M(C1_s)\), \(s=0..99\) |
| \(z_{P}\) | \((M_P - \mu_{C1}) / \sigma_{C1}\) si \(\sigma_{C1}>0\); else \(0\) |
| \(p_{C1}\) | fracción de seeds con \(\|M(C1_s)-\mu_{C1}\| \ge \|M_P-\mu_{C1}\|\) (cola bilateral empírica) |
| \(D_{P,C2}\) | \(\|M_P - M(C2)\|\) (con emparejamiento de cardinalidad si aplica) |
| \(D_{P,C3}\) | \(\|M_P - M(C3)\|\) idem |
| \(D_{C1}^{\mathrm{med}}\) | mediana de \(\|M(C1_s)-\mu_{C1}\|\) |

---

## 8. Criterios de veredicto (congelados antes de ejecutar)

| Resultado | Condición |
| --------- | --------- |
| **H-01 PERSISTE** (material candidato) | \(p_{C1}\le 0.05\) **y** \(D_{P,C2} > 2\cdot D_{C1}^{\mathrm{med}}\) **y** \(D_{P,C3} > 2\cdot D_{C1}^{\mathrm{med}}\) |
| **H-00 DESAPARECE** (solo densidad/orden / no firma) | \(p_{C1}>0.10\) **o** (\(D_{P,C2}\le 2\cdot D_{C1}^{\mathrm{med}}\) **y** \(D_{P,C3}\le 2\cdot D_{C1}^{\mathrm{med}}\)) **o** \(\|z_P\|<2\) y \(p_{C1}>0.05\) |
| **NO_SABEMOS** | resto (p.ej. gana solo vs C1 pero no vs C2/C3, o zona gris) |

Lectura:

- **PERSISTE:** \(M(P)\) extremo vs misma densidad **y** separado de semiprimos y artificial más allá de la dispersión C1.  
- **DESAPARECE:** no hay material diferencial bajo este \(G\), este \(k\), este \(M\).

---

## 9. Ficha de salida (obligatoria)

```text
N, k:              10000, 10
G:                 vecindad ordinal |i-j|≤k
M:                 M_2 segundo momento espectral Laplaciano inducido
m = π(N):          …
M(P):              …
μ_C1 ± σ_C1:       …
z_P, p_C1:         …
M(C2), D_P,C2:     …
M(C3), D_P,C3:     …
D_C1^med:          …
Interpretación:    PERSISTE | DESAPARECE | NO_SABEMOS
MD-035 audit:      E sin p|n, gcd, factores  OK
```

---

## 10. No-afirmaciones

Incluso PERSISTE:

- no “los primos son un espectro”  
- no inversión de la dualidad ceros→primos  
- no operador · no Hilbert–Pólya · no GUE demostrado  
- solo: **esta** \(M_2\) en **este** grafo ordinal discrimina **estos** controles a **este** \(N\)

---

## 11. Ejecución

```text
scripts/run_athena_domain_e004.py
ATHENA_DOMAIN_E004/resultados/
```

---

## 12. Deuda / no-campaña-1

| Tema | Estado |
| ---- | ------ |
| Otras \(k\), otras familias (embebidas, \(T\) geométrico) | nuevo ID |
| Espectro completo / GUE / espaciados | nuevo ID + justificación MD-034 |
| \(N=10^5\) | réplica de escala, mismo protocolo si H-01 o interés |
| Contrabando aritmético en \(E\) | **prohibido** (MD-035) |

---

# FIN — DOMAIN-E004 PROTOCOL 1.0

*Primero el ladrillo.  
La catedral no se discute sin material.*
