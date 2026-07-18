# ATHENA DOMAIN-E006 — Informe de cierre (lectura mecánica §5)

**Protocolo:** v1.0 sellado · SHA-256 `12b9c1b7ec6930472efc2a774d484a90ea64e9db9f15270394c24e15161f9e5b`  
**Issue:** https://gitlab.com/athena-group321329/athena/-/issues/2  
**Fuente:** `resultados/classification.json`  
**Ejecución:** `scripts/run_athena_domain_e006.py` · N=10⁵ · B=2000 · ~13 min  

---

## Candado pre-run

| Casilla | Estado |
| ------- | ------ |
| Hash `origin/main` blob = sello | **MATCH** `12b9c1b7…9e5b` |
| MD-035 runner (gcd solo \(U_W\); aristas ordinales; mitades \(U_W\cap\) half) | **PASS** |

---

## Ficha

| Campo | Valor |
| ----- | ----- |
| \(N\), \(k\), \(B\) | 100000, 12, 2000 |
| diseño | directa + curva \(W\in\{1,2,6,30\}\) |
| \(M(P)\) | **7.92994162** |
| principal | **W=30** |

### Por rueda

| \(W\) | med nulo | \(p_{\mathrm{range}}\) | señal | half_code | thr \(2D\) |
| ----- | -------- | ---------------------- | ----- | --------- | ---------- |
| 1 | 10.0438 | \(1/2001\) | **2.1138** | HALF_BOTH_EXTREME | 0.2469 |
| 2 | 9.7279 | \(1/2001\) | **1.7980** | HALF_BOTH_EXTREME | 0.2106 |
| 6 | 9.4356 | \(1/2001\) | **1.5056** | HALF_BOTH_EXTREME | 0.1631 |
| **30** | **8.9264** | **\(1/2001\)** | **0.9965** | **HALF_BOTH_EXTREME** | **0.1410** |

| C2 / C3 (vs thr W=30) | |
| --------------------- | - |
| \(D_{P,C2}\) | 1.2433 **>** 0.1410 |
| \(D_{P,C3}\) | 0.3834 **>** 0.1410 |
| curve_code | **CURVE_MONOTONE** |

---

## Lectura mecánica §5 (solo W=30 decide)

| Condición H-01 | ¿OK? |
| -------------- | ---- |
| \(p_{\mathrm{range}}^{(30)}\le 0.01\) | **sí** (\(1/2001\)) |
| \(D_{P,C2} > 2 D_{C1}^{\mathrm{med},30}\) | **sí** |
| \(D_{P,C3} > 2 D_{C1}^{\mathrm{med},30}\) | **sí** |
| half_code\(^{(30)}\)=HALF_BOTH_EXTREME | **sí** |

| Condición H-00 `MATERIAL_DISSOLVED_BY_WHEEL_30` | ¿OK? |
| ---------------------------------------------- | ---- |
| \(p>0.10\) / central 80% / HALF_BOTH_NULL sin H-01 | **no** |

| NO_SABEMOS gray \(0.01<p\le 0.10\) | **no** |

### Veredicto

```text
interpretation: PERSISTE
verdict:        H01_MATERIAL_BEYOND_WHEEL_30
H-ATH-D006-01:  SOPORTADA_BAJO_CONTROL
H-ATH-D006-00:  MUERTA
```

**No** es `MATERIAL_DISSOLVED_BY_WHEEL_30`.  
**No** es `NO_SABEMOS`.

---

## Curva (secundaria; no decide H-01)

\[
\mathrm{señal}(1)=2.11 > \mathrm{señal}(2)=1.80 > \mathrm{señal}(6)=1.51 > \mathrm{señal}(30)=1.00
\]

→ **CURVE_MONOTONE** (dirección de la predicción a priori de “encogerse”).

La predicción de **disolución** en W=30 queda **falsada** (protocolar).  
La predicción de colapso “sustancial” ya en W=2: la señal baja ~15%, no al suelo — no es disolución.

---

## No-afirmaciones

- No Hardy–Littlewood · no operador · no catedral  
- PERSISTE vs rueda 30 = material **bajo este instrumento y este nulo**, no “geometría profunda demostrada”  
- Siguiente lupa (si se abre): nulos con correlaciones HL — **nuevo ID**

---

# FIN — DOMAIN-E006 REPORT
