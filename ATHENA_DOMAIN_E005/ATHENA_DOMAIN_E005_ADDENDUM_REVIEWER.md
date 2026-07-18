# ATHENA DOMAIN-E005 — Addendum de revisor (post-veredicto)

**Fecha:** 2026-07-18  
**Veredicto protocolar (intacto):** `PERSISTE` / `H01_MATERIAL_BEYOND_CRAMER`  
**Predicción a priori del revisor (pre-E005):** Cramér disuelve el ladrillo → **FALSADA**  
**No reescribe** `classification.json`.

---

## 1. Registro sin maquillaje

| Afirmación | Estado |
| ---------- | ------ |
| Bajo sello #1 y §7, H-01 protocolar | **SOPORTADA** |
| “Cramér mata \(M_2\) ordinal” (predicción a priori) | **FALSADA** |
| “Material nuevo / más allá de aritmética trivial” | **NO afirmado** por el veredicto |

El andamiaje mató la predicción con la misma frialdad con que habría matado el ladrillo.

---

## 2. Sospechoso conocido: Cramér como hombre de paja

El modelo de Cramér **no** es el nulo más afilado.

Hechos clásicos:

- Todo primo \(>2\) es **impar** → gaps entre primos \(>2\) son **pares**.  
- Un conjunto de Cramér admite pares consecutivos y gaps impares imposibles para primos.  
- En grafo ordinal \(k=12\), eso altera la estructura local de vecinos y por tanto \(M_2\).  
- Dirección observada \(M(P)=7.93 < \mathrm{med\,Cramér}=10.04\): compatible con espaciado **más regular** / sin vecinos a distancia 1 (impares).

Crítica clásica: correcciones de Hardy–Littlewood, teorema de Maier — la desviación de Cramér incluye estructura de **residuos módulo primos pequeños**, conocida desde hace un siglo.

```text
MATERIAL_BEYOND_CRAMER  ≠  material nuevo
```

Hasta E006, es **compatible** con:

```text
el instrumento detectó que los primos son impares
(+ filtrado mod 6 / 30, si se prueba)
```

---

## 3. MD-035 no se contradice

- Las **aristas** no contienen aritmética (auditoría PASS).  
- El instrumento **puede detectar** aritmética.  
- No puede **presuponerla** en \(E\).

E006 pregunta: ¿detectó **más** que la aritmética trivial de residuos pequeños?

---

## 4. Escalera de nulos (programa)

| Peldaño | Nulo | Estado |
| ------- | ---- | ------ |
| 1 | Uniforme | E004 — nulo débil; H-00 no muerta |
| 2 | Cramér | E005 — **muerto** como asesino del ladrillo |
| 3 | **Cramér-rueda** \(W\in\{2,6,30\}\) | **E006** |
| 4 | Correlaciones Hardy–Littlewood | solo si sobrevive rueda 30 |

---

## 5. Predicción a priori E006 (escrita antes de datos)

La señal **colapsa sustancialmente** en rueda mod 2; el residuo se **encoge** al subir a mod 6 y mod 30.

Si \(p_{\mathrm{range}}\) sigue en el suelo \(1/(B+1)\) con `HALF_BOTH_EXTREME` **contra rueda 30**, entonces sí hay algo que mirar con lupa.

---

# FIN — E005 ADDENDUM REVIEWER
