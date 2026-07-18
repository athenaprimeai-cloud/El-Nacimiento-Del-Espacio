# ATHENA DOMAIN-E006 — Pregunta (Cramér-rueda: ¿más que impares?)

**Estado:** pregunta **prerregistrada** · no ejecutada  
**Después de:** E005 PERSISTE vs Cramér + addendum revisor (Cramér = hombre de paja conocido)  
**No es:** Hardy–Littlewood completo · Hilbert–Pólya · catedral  

---

## Pregunta

> Bajo el mismo grafo ordinal y la misma \(M_2\),  
> ¿el conjunto de primos sigue siendo extremo frente a **Cramér-rueda**  
> (muestreo equicardinal con pesos \(1/\ln n\) **restringido a enteros coprimos con \(W\)**, densidad renormalizada dentro de la rueda),  
> en particular contra \(W=30\), con \(W=2,6\) como satélites de curva?

En una línea:

> **¿\(M_2\) ordinal ve más que aritmética de residuos pequeños, o la rueda disuelve el ladrillo?**

---

## Decisión de diseño (lab)

**Opción adoptada: directa con curva** (recomendación revisor).

| Rol | \(W\) |
| --- | ----- |
| **Veredicto principal** | \(W=30\) |
| Satélites descriptivos (misma corrida) | \(W=1\) (Cramér puro, réplica E005), \(W=2\), \(W=6\) |

Predicción secundaria prerregistrada (monotonía de señal):

\[
\mathrm{señal}(W{=}1) \;\;>\;\; \mathrm{señal}(W{=}2) \;\;>\;\; \mathrm{señal}(W{=}6) \;\;>\;\; \mathrm{señal}(W{=}30)
\]

(si la curva **no** es monótona, también es información).

**No** escalera secuencial: una campaña, \(B=2000\) por rueda, barata con \(M_2\) cerrada.

---

## Hipótesis

| ID | Enunciado |
| -- | --------- |
| **H-ATH-D006-00** | Rueda \(W=30\) disuelve el material: \(M(P)\) compatible con Cramér-rueda-30 bajo §7. Código: `MATERIAL_DISSOLVED_BY_WHEEL_30` |
| **H-ATH-D006-01** | Material persiste vs rueda 30 (p_range ≤ 0.01, C2/C3, HALF_BOTH_EXTREME). Código: `H01_MATERIAL_BEYOND_WHEEL_30` |

Predicción a priori del revisor: **H-00** (colapso ya en \(W=2\), residuo menguante).

---

## Montaña

```text
¿más que residuos pequeños?
        ↑
E006 Cramér-rueda (W=30 principal)
        ↑
E005 vs Cramér: PERSISTE (protocolar) · sospechoso = impares
        ↑
E004 vs uniforme: nulo débil
```

---

# FIN — DOMAIN-E006 PREGUNTA
