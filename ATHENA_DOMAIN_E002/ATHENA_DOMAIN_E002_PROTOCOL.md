# ATHENA DOMAIN-E002 — Protocolo **CONGELADO**

**Clase:** dominio Athena · simetría candidata mínima  
**Versión:** **1.0 CONGELADO**  
**Fecha:** 2026-07-17  
**No es:** operador de Riemann · catedral geométrica · reabrir E001  

---

## 1. Pregunta

> ¿Existe una cantidad global \(P\) **aproximadamente conservada** bajo una familia predeclarada \(\mathcal{R}\) de representaciones legítimas del sistema Goldbach/primos residual,  
> de forma **diferencial** respecto a nulos que rompen la estructura del objeto?

No: “¿hay alguna invariancia cualquiera?”  
Sí: conservación **interesante** bajo \(T\in\mathcal{R}\), no bajo nulos.

---

## 2. Objeto \(X\)

```text
X = (G(N))_{N par ∈ [4, N_max]}
N_max = 10000
fuente: artifacts/goldbach/goldbach_partitions_4_10000.csv
```

---

## 3. Familia \(\mathcal{R}\) de representaciones legítimas (congelada)

Cada \(T\in\mathcal{R}\) produce una serie residual \(r_T\) sobre la que se evalúa \(P\):

| ID | \(T\) | Descripción |
| -- | ----- | ----------- |
| **T0** | residual media | \(G-\overline{G}\) en ventana completa |
| **T1** | subventana baja | residual media en primera mitad de índices |
| **T2** | subventana alta | residual media en segunda mitad |
| **T3** | detrend lineal | residual de regresión lineal \(G\sim a+b\cdot t\) |
| **T4** | escala log | residual media de \(\log(1+G)\) |

**Restricción:** \(\mathcal{R}\) = formas alternativas de mirar el **mismo** objeto \(G\), no transformaciones arbitrarias.

---

## 4. Propiedad \(P\) (una, no débil)

**No** media, rango ni conteo total (demasiado gruesos).

**Sí — \(P\) = entropía espectral normalizada del residual** (excl. DC):

Sea \(S_k\) la potencia FFT en bins \(k=1,\ldots,K\).  
\[
p_k = \frac{S_k}{\sum_j S_j},\quad
P = -\frac{1}{\log K}\sum_k p_k\log p_k
\]
(con \(0\log 0:=0\)).  
\(P\in[0,1]\): cerca de 1 = espectro plano; bajo = energía concentrada.

**Por qué interesante:** mide la **forma** de la distribución de energía espectral, no un pico aislado (E001 ya mató extremidad de un bin bajo residual media).

---

## 5. Estadístico de estabilidad

\[
\Delta = \max_{T\in\mathcal{R}} |P(T(X)) - \mathrm{median}_{T'} P(T'(X))|
\]

Pequeño \(\Delta\) ⇒ alta estabilidad de \(P\) bajo \(\mathcal{R}\).

---

## 6. Nulos (ataques)

| ID | Nulo | Procedimiento |
| -- | ---- | ------------- |
| **N1** | Permutación de \(G\) | Barajar \(G\) (seed \(s\)); aplicar \(\mathcal{R}\) y \(\Delta_s\) |
| **N2** | Bootstrap de bloques | Reordenar bloques de longitud \(B=50\) de \(G\); \(\Delta_s\) |

Seeds: \(s=0..99\).

Sea \(p = \) fracción de nulos con \(\Delta_s \le \Delta_0\) (nulo **tan o más estable** que los datos).

---

## 7. Criterios de veredicto

| Resultado | Condición |
| --------- | --------- |
| **H-01 PERSISTE** (candidato estructural) | \(\Delta_0\) es **pequeño** en sentido predeclarado: \(\Delta_0 \le 0.08\) **y** \(p \le 0.05\) (estabilidad real **extrema** vs nulos) |
| **H-00 DESAPARECE** (artefacto / no diferencial) | \(p > 0.10\) **o** \(\Delta_0 > 0.15\) |
| **NO_SABEMOS** | resto |

Interpretación:

- PERSISTE: \(P\) se conserva bajo \(\mathcal{R}\) **más** que bajo nulos que rompen orden → pista de simetría.  
- DESAPARECE: o no se conserva, o los nulos se conservan igual → no hay conservación diferencial interesante bajo este \(P,\mathcal{R}\).

---

## 8. Ficha de salida (obligatoria)

```text
Propiedad P:     entropía espectral normalizada
Familia T:       T0–T4 (arriba)
Rango probado:   N∈[4,10000]
Nulos:           N1 permutación, N2 bloques
Estabilidad Δ0:  …
p vs nulos:      …
Interpretación:  PERSISTE | DESAPARECE | NO_SABEMOS
```

---

## 9. No-afirmaciones

Incluso PERSISTE:

- no geometría de Riemann  
- no operador  
- no “estructura fundamental → primos”  
- solo: conservación diferencial de **esta** \(P\) bajo **esta** \(\mathcal{R}\)

---

## 10. Ejecución

```text
scripts/run_athena_domain_e002.py
ATHENA_DOMAIN_E002/resultados/
```

---

# FIN — DOMAIN-E002 PROTOCOL 1.0

*Simetría mínima. Un ladrillo. No una catedral.*
