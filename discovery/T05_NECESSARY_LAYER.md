# T-05 — Capa de consecuencias necesarias

**Fecha:** 2026-07-18  
**MD:** MD-073  
**Pregunta:** ¿Qué **no puede dejar de ocurrir** si esta máquina es exactamente la que dice ser?  
**No:** “¿Se parece a los primos?” · Athena · T-01/T-03/T-04  

---

## NECESSARY

| ID | Afirmación |
| -- | ---------- |
| N1 | min dist entre aceptados \(\ge\varepsilon\) (por construcción) |
| N2 | si \(\varepsilon>\sqrt{d}\), a lo sumo un punto en \([0,1]^d\) |
| N3 | la regla es **métrica**, no ordinal (índices = etiquetas) |
| N4 | cardinalidad \(O(\varepsilon^{-d})\) (packing) |

## EMPIRICAL / SEED / UNKNOWN

| ID | Clase | Nota |
| -- | ----- | ---- |
| E1 | EMPIRICAL | densidad ↓ al subir \(\varepsilon\) (ola 1) |
| E2 | EMPIRICAL | 0 violaciones hard-core numéricas |
| S1 | SEED_DEPENDENT | init + orden |
| U1 | UNKNOWN | intensidad límite tipo Matérn exacta |

## ¿P\* / Intake?

N1–N4 son **geometría de packing**, no apuesta Athena.

```text
¿Consecuencia necesaria cuantificable → P* Athena?
        └── NO

T05_STATUS = REFERENCE_COMPLETE
PSTAR       = NONE
INTAKE      = NOT_ELIGIBLE
```

**Resultado de mapa:** tercera representación (métrica en \(\mathbb{R}^d\)) cartografiada;  
tampoco produce por sí sola una hipótesis Athena → **reduce el espacio de \(\mathcal{M}\)**.

---

# FIN — T-05 NECESSARY LAYER
