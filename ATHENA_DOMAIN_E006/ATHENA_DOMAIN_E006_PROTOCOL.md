# ATHENA DOMAIN-E006 — Protocolo **PRERREGISTRADO** (no ejecutado)

**Clase:** dominio Athena · Cramér-rueda vs material ordinal \(M_2\)  
**Versión:** **1.0 PRERREGISTRADO**  
**Fecha:** 2026-07-18  
**Padre:** E005 sello #1 · addendum revisor Cramér-hombre-de-paja  
**Diseño:** **opción directa con curva** (no escalera secuencial)

**Candado:** este archivo fija ruedas, pesos, §7, predicciones **antes** de mirar resultados E006.

---

## 1. Pregunta

> ¿\(M_2\) del Laplaciano inducido (grafo ordinal) discrimina \(P\) frente a Cramér-rueda \(W=30\),  
> con curva de señal en \(W\in\{1,2,6,30\}\)?

---

## 2. Heredado de E005 (congelado idéntico salvo nulo)

| Campo | Valor |
| ----- | ----- |
| \(N\) | \(10^5\) |
| \(k(N)\) | \(\mathrm{round}(\ln N)=12\) (\(c=1\)) |
| \(G\) | \(0 < \|i-j\| \le k\) (MD-035: sin aritmética en \(E\)) |
| \(M\) | \(M_2\) segundo momento espectral Laplaciano inducido |
| \(B\) | 2000 por rueda |
| Mitades | \(\{1..N/2\}\), \(\{N/2..N\}\) como E005 |
| C2★ | sample \(m\) semiprimos \(\le N\) (no prefijo) |
| C3 | Ulam, emparejamiento de cardinalidad como E005 |
| \(p\) | rango bilateral; floor \(1/(B+1)\); \(z\) no veredicto |
| Gray band | \(0.01 < p_{\mathrm{range}} \le 0.10\) → **NO_SABEMOS** (salvo dissolve por otras vías) |

---

## 3. Nulo principal y satélites — Cramér-rueda

### Universo rueda

\[
U_W = \{ n \in \{1,\ldots,N\} : \gcd(n,W)=1 \}
\]

(\(W=1\): \(U_1=\{1,\ldots,N\}\) = Cramér puro, réplica descriptiva de E005.)

### Pesos renormalizados **dentro** de la rueda

Para \(n\in U_W\):

\[
w_n^{(W)} = \frac{1}{\ln n}\quad (n\ge 3),\quad w_2^{(W)}=1\text{ si }2\in U_W
\]

Muestreo equicardinal **sin reemplazo**, tamaño \(m=\pi(N)\) (o \(m_H\) en mitades),  
algoritmo Efraimidis–Spirakis con pesos \(w_n^{(W)}\) **solo sobre** \(U_W\)  
(renormalización implícita al restringir el soporte; no se mezclan no-coprimos).

**Importante:** \(\gcd(n,W)=1\) define el **universo de muestreo del nulo**, no las aristas del grafo (MD-035 intacto: \(E\) sigue siendo solo ordinal).

### Ruedas de la corrida

| ID | \(W\) | Rol |
| -- | ----- | --- |
| **R1** | 1 | satélite: Cramér puro (ancla E005) |
| **R2** | 2 | satélite: solo impares (+1 si aplica) |
| **R6** | 6 | satélite: coprimos a 6 |
| **R30** | 30 | **nulo principal del veredicto** |

Cada rueda: \(B=2000\) réplicas globales + \(B\) por mitad (como E005).

---

## 4. Estadísticos

Para cada rueda \(W\):

- \(M_P = M_2(P)\) (único; el objeto no cambia)  
- \(\{M_s^{(W)}\}_{s=0}^{B-1}\)  
- \(p_{\mathrm{range}}^{(W)}\), \(\mathrm{med}^{(W)}\), \(D_{C1}^{\mathrm{med},W}\), half_code\(^{(W)}\)  
- \(D_{P,C2}\), \(D_{P,C3}\) vs thr de **esa** rueda (misma definición E005)

### Señal (para curva)

\[
\mathrm{señal}(W)
:=
|M_P - \mathrm{median}_s M_s^{(W)}|
\]

(descriptivo; el veredicto principal **no** usa monotonía como requisito de H-01, solo la reporta).

Predicción secundaria prerregistrada:

\[
\mathrm{señal}(1) > \mathrm{señal}(2) > \mathrm{señal}(6) > \mathrm{señal}(30)
\]

Códigos de curva:

| Código | Condición |
| ------ | --------- |
| **CURVE_MONOTONE** | las tres desigualdades estrictas |
| **CURVE_WEAK** | no creciente: \(\mathrm{señal}(1)\ge\mathrm{señal}(2)\ge\mathrm{señal}(6)\ge\mathrm{señal}(30)\) con al menos un \(=\) |
| **CURVE_NONMONOTONE** | resto |

---

## 5. Criterios de veredicto §7 (heredados; nulo = R30)

| Resultado | Condición |
| --------- | --------- |
| **H-01 PERSISTE** / `H01_MATERIAL_BEYOND_WHEEL_30` | \(p_{\mathrm{range}}^{(30)}\le 0.01\) **y** \(D_{P,C2} > 2 D_{C1}^{\mathrm{med},30}\) **y** \(D_{P,C3} > 2 D_{C1}^{\mathrm{med},30}\) **y** half_code\(^{(30)}=\) **HALF_BOTH_EXTREME** |
| **H-00 DESAPARECE** / `MATERIAL_DISSOLVED_BY_WHEEL_30` | \(p_{\mathrm{range}}^{(30)} > 0.10\) **o** \(M_P\) en banda central 80% de \(\{M_s^{(30)}\}\) **o** (HALF_BOTH_NULL en \(W=30\) y no H-01 global) |
| **NO_SABEMOS** | resto — en particular \(0.01 < p_{\mathrm{range}}^{(30)} \le 0.10\), HALF_SPLIT, C2/C3 grises |

R1/R2/R6: **solo ficha y curva**; no cambian el veredicto principal si R30 disuelve o persiste.

---

## 6. Predicción a priori (revisor + lab) — escrita pre-datos

1. La señal **colapsa sustancialmente** en \(W=2\) respecto a \(W=1\).  
2. El residuo **se encoge** al subir a \(W=6\) y \(W=30\).  
3. Escenario más probable: **H-00** / `MATERIAL_DISSOLVED_BY_WHEEL_30`.  
4. Si H-01 con \(p_{\mathrm{range}}^{(30)}=1/(B+1)\) y HALF_BOTH_EXTREME: **entonces** lupa (siguiente peldaño HL), no catedral.

Falsar (1)–(3) es un éxito del candado, no un fracaso del revisor.

---

## 7. Ficha de salida

```text
N, k, B:           100000, 12, 2000
design:            directa + curva W∈{1,2,6,30}
principal:         W=30
M_P:               …
per W:             med, p_range, D_med, half_code, señal
D_P,C2 / D_P,C3:   … (thr de W=30)
curve_code:        CURVE_MONOTONE | CURVE_WEAK | CURVE_NONMONOTONE
interpretation:    PERSISTE | DESAPARECE | NO_SABEMOS
verdict:           H01_MATERIAL_BEYOND_WHEEL_30 | MATERIAL_DISSOLVED_BY_WHEEL_30 | NO_SABEMOS
protocol_sha256:   …
md035:             E ordinal only; gcd only for null universe U_W
```

---

## 8. No-afirmaciones

- Sobrevivir rueda 30 **no** es Hardy–Littlewood ni operador  
- Disolverse en rueda 30 **no** es “no hay estructura en primos”  
- Solo: \(M_2\)+ordinal vs este nulo de residuos  

---

## 9. Ejecución (secuencia de sello)

```text
1. push este protocolo + issue GitLab E006
2. comentar sha256 del protocolo en el issue
3. scripts/run_athena_domain_e006.py
4. classification.json + lectura mecánica §5
```

---

## 10. Checklist pre-run

- [ ] Issue-candado E006 creado  
- [ ] SHA-256 del protocolo en el issue  
- [ ] Runner: \(U_W\) por \(\gcd(n,W)=1\); pesos solo en \(U_W\); \(E\) ordinal  
- [ ] MD-035 audit: gcd **no** entra en aristas  
- [ ] No ejecutar hasta sello  

---

# FIN — DOMAIN-E006 PROTOCOL 1.0 PREREGISTERED

*Si la rueda 30 disuelve el ladrillo: claridad — M₂ ordinal ve residuos pequeños y poco más.  
Si no: lupa, no catedral.*
