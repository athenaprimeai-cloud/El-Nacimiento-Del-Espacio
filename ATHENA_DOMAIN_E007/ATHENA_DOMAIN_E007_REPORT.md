# ATHENA DOMAIN-E007 — Informe de cierre (replicación)

**Protocolo:** v1.0 **CONGELADO** · SHA-256 `eacc3f54e9d7bd768416bc7d93ffd577767d21b88e15403a66aac883a256ab0b`  
**Clase:** réplica, no descubrimiento  
**Único cambio:** \(N=5\cdot 10^4\) (E006: \(N=10^5\))  
**Fuente:** `resultados/classification.json`  

---

## Pregunta

> ¿La relación observada en E006 se reproduce bajo un cambio de escala del dominio?

---

## Ficha

| Campo | Valor |
| ----- | ----- |
| \(N\), \(k\), \(B\) | 50000, 11, 2000 |
| \(M(P)\) | 5.84687317 |
| class_W30 | **PERSISTE** |
| orden \(S(1)>S(2)>S(6)>S(30)\) | **sí** |
| **replica_verdict** | **REPRODUCIDA** |
| E006_status | **unchanged** (regla anti-retrospectiva) |

### Curva \(S(W)\) en \(N=5\cdot 10^4\)

| \(W\) | \(S(W)\) |
| ----- | -------- |
| 1 | 3.950 |
| 2 | 2.300 |
| 6 | 0.840 |
| 30 | 0.592 |

Orden: \(3.950 > 2.300 > 0.840 > 0.592\) · CURVE_MONOTONE.

### W=30 (criterios heredados E006)

| Condición | ¿OK? |
| --------- | ---- |
| \(p_{\mathrm{range}}^{(30)}\le 0.01\) | sí (\(1/2001\)) |
| C2 / C3 vs thr | sí |
| HALF_BOTH_EXTREME | sí |

---

## Lectura pre-escrita (aplicada)

| Resultado | Lectura |
| --------- | ------- |
| **REPRODUCIDA** | Evidencia de **estabilidad** del fenómeno bajo cambio de \(N\). **No** es teoría. |

E007 **no** convierte E006 en teoría.  
E006 **no** se reescribe.

---

## Comparación de forma (descriptiva, no criterio)

| | E006 \(N=10^5\) | E007 \(N=5\cdot 10^4\) |
| - | --------------- | ---------------------- |
| \(S(1)\) | 2.114 | 3.950 |
| \(S(2)\) | 1.798 | 2.300 |
| \(S(6)\) | 1.506 | 0.840 |
| \(S(30)\) | 0.996 | 0.592 |
| orden | monótono | monótono |
| class W=30 | PERSISTE | PERSISTE |

Los valores numéricos **no** coinciden (no se exigía).  
Clasificación y **orden** sí.

---

## No-afirmaciones

- No geometría generativa · no operador · no RH  
- No “señal más fuerte” como objetivo  
- REPRODUCIDA ≠ derecho a catedral  

---

## Montaña

```text
¿mecanismo mínimo E004+E006 (sin contrabando)?
        ↑
E007: S(W) REPRODUCIDA a N=5e4
        ↑
E006: PERSISTE rueda 30 + curva
```

---

# FIN — DOMAIN-E007 REPORT

*¿Vuelve a ocurrir? Sí — bajo este N y estas reglas.  
Aún no es una teoría.*
