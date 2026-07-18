# ATHENA DOMAIN-E005 — Informe de cierre (lectura mecánica §7)

**Protocolo:** v1.1 sellado · SHA-256 `762483fd72bc45586193beac556ba86fe935b645176e3d17b3b1fc1a5ab6689c`  
**Issue:** https://gitlab.com/athena-group321329/athena/-/issues/1  
**Fuente:** `resultados/classification.json`  
**Ejecución:** `scripts/run_athena_domain_e005.py` · N=10⁵ · B=2000  

---

## Candado pre-run

| Casilla | Estado |
| ------- | ------ |
| Hash `origin/main` blob = sello | **MATCH** `762483fd…689c` |
| MD-035 runner (aristas solo ordinales) | **PASS** · `MD035_RUNNER_AUDIT.md` |

---

## Ficha

| Campo | Valor |
| ----- | ----- |
| \(N\), \(k\) | 100000, **12** (\(=\mathrm{round}(\ln N)\)) |
| \(m=\pi(N)\) | 9592 |
| \(M(P)\) | **7.92994162** |
| med \(M(\mathrm{Cramér})\) | **10.04378649** |
| \(p_{\mathrm{range}}\) | **0.00049975** \(= 1/(B+1)\) |
| banda central 80% | **no** |
| \(D_{P,C2}\) / thr | **1.24333** / **0.24687** |
| \(D_{P,C3}\) / thr | **0.38344** / **0.24687** |
| \(p_L\), \(p_H\) | **0.00049975**, **0.00049975** |
| half_code | **HALF_BOTH_EXTREME** |
| gray \(0.01<p\le 0.10\) | false |

---

## Lectura mecánica §7 (sin margen)

| Condición H-01 | ¿OK? |
| -------------- | ---- |
| \(p_{\mathrm{range}}\le 0.01\) | **sí** |
| \(D_{P,C2} > 2 D_{C1}^{\mathrm{med}}\) | **sí** |
| \(D_{P,C3} > 2 D_{C1}^{\mathrm{med}}\) | **sí** |
| HALF_BOTH_EXTREME | **sí** |

| Condición H-00 / `MATERIAL_DISSOLVED_BY_CRAMER` | ¿OK? |
| ---------------------------------------------- | ---- |
| \(p_{\mathrm{range}}>0.10\) | no |
| \(M_P\) en central 80% | no |
| HALF_BOTH_NULL sin H-01 global | no |

| Condición NO_SABEMOS | ¿OK? |
| -------------------- | ---- |
| franja \(0.01 < p \le 0.10\) | no |
| resto (SPLIT / C2·C3 grises) | no aplica |

### Veredicto

```text
interpretation: PERSISTE
verdict:        H01_MATERIAL_BEYOND_CRAMER
H-ATH-D005-01:  SOPORTADA_BAJO_CONTROL
H-ATH-D005-00:  MUERTA
```

**No** es `MATERIAL_DISSOLVED_BY_CRAMER`.  
**No** es `NO_SABEMOS`.

---

## No-afirmaciones (obligatorias)

- No Hilbert–Pólya · no “primos = espectro” · no GUE/Riemann  
- Solo: **esta** \(M_2\) + grafo ordinal + **este** Cramér equicardinal + controles C2★/C3 + mitades, bajo sello #1  

---

# FIN — DOMAIN-E005 REPORT
