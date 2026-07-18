# ATHENA DOMAIN-E005 — Protocolo **PRERREGISTRADO** (no ejecutado)

**Clase:** dominio Athena · asesinato limpio de material vs Cramér  
**Versión:** **1.1 PRERREGISTRADO** (enmienda pre-sello: dos mitades · alinea issue GitLab #1)  
**Fecha:** 2026-07-17  
**Candado remoto:** https://gitlab.com/athena-group321329/athena/-/issues/1  
**Anclas:** MD-034 · MD-035 · MD-036 · addendum E004 · MD-039 · MD-040  

**Candado:** este archivo fija C1, C2, \(k\), \(B\), \(p\), **dos mitades** **antes** de mirar resultados de E005.

**Enmienda 1.0→1.1 (antes de datos, no post-hoc):**  
criterio extra del issue #1 — replicación en \(\{1..N/2\}\) y \(\{N/2..N\}\).

---

## 1. Pregunta

> ¿\(M_2(G[S])\) con \(G\) ordinal discrimina \(P\) frente a **Cramér** (densidad local) y controles MD-036 corregidos?

---

## 2. Congelado idéntico a E004 (salvo lo listado)

| Campo | Valor |
| ----- | ----- |
| \(N\) principal (réplica de escala) | \(10^5\) |
| \(N\) satélite (mismo régimen que E004) | \(10^4\) (opcional, misma política \(k\)) |
| \(G\) | \(V=\{1..N\}\), \((i,j)\in E \iff 0<\|i-j\|\le k\) |
| \(M\) | \(M_2\) segundo momento espectral Laplaciano inducido (forma cerrada E004) |
| MD-035 | sin \(p\mid n\), \(\gcd\), factores en \(E\) |

---

## 3. Política de \(k\) — **PRERREGISTRADA: B (réplica de escala)**

\[
k(N) = \max\!\big(1,\; \mathrm{round}(c \cdot \log N)\big)
\qquad
c = 1
\qquad
\log = \ln\text{ (natural)}
\]

| \(N\) | \(\ln N\) | \(k(N)\) |
| ----- | --------- | -------- |
| \(10^4\) | \(\approx 9.21\) | **9** |
| \(10^5\) | \(\approx 11.51\) | **12** |

**Motivo:** \(k\) fijo en E004 operaba en la escala del gap medio; subir \(N\) con \(k=10\) **no** replica, cambia régimen.

### Política A (satélite, no principal)

Si se corre \(k\equiv 10\) en \(N=10^5\):

**Predicción prerregistrada (dirección):**  
como \(k < \ln N\), el grafo inducido de primos se vuelve **más disperso** relativo al gap medio  
→ \(M(P)\) tiende a **bajar** respecto al régimen \(k\sim\ln N\);  
la comparación relevante sigue siendo vs Cramér con el **mismo** \(k=10\), no vs E004 absoluto.

Política A **no** decide el veredicto de campaña 1; solo documenta régimen.

---

## 4. Controles (MD-036 corregidos)

### C1★ — Cramér (asesino de H-00)

Para seed \(s=0..B-1\):

1. Para cada \(n=2..N\), incluir \(n\) en \(C_s\) con probabilidad  
   \[
   p_n = \min\!\big(1,\; 1/\ln n\big) \quad (n\ge 3);\quad
   p_2 = 1
   \]
   (Bernoulli independiente; RNG seed \(s\)).  
2. Si se desea equicardinalidad estricta (opción congelada **ON**):  
   - generar pool Cramér con \(p_n\) hasta obtener un conjunto;  
   - **alternativa condicional (adoptada):** muestreo de tamaño exacto \(m=\pi(N)\) con pesos proporcionales a \(1/\ln n\) (sin reemplazo, algoritmo de weighted sampling / sequential), seed \(s\).  

**Adoptado en v1.0:** equicardinal **weighted without replacement**, pesos \(w_n = 1/\ln n\) (\(n\ge 3\)), \(w_2=1\), tamaño \(m=\pi(N)\).

Nombre: **C1-Cramér equicardinal**.

### C2★ — Semiprimos equicardinales en soporte \(\le N\)

1. Enumerar \(S_{\mathrm{all}}=\{x\le N: \Omega(x)=2\}\).  
2. Si \(|S_{\mathrm{all}}|\ge m\): sample \(m\) elementos **uniformes** de \(S_{\mathrm{all}}\) (seed \(s\) fijo 0 para el punto; réplicas opcionales \(s=0..9\)).  
3. **No** usar el prefijo de los primeros \(m\) semiprimos (error E004).

### C3 — Artificial (Ulam)

Como E004, con emparejamiento de cardinalidad documentado si \(\#U < m\).

### Réplicas

\[
B = 2000
\]

(\(M_2\) forma cerrada → barato; no \(B=100\)).

---

## 5. Estadísticos y \(p\) de rango (sin “\(p=0\)”)

Sea \(M_P = M_2(P)\), \(M_s = M_2(C1_s)\).

\[
p_{\mathrm{range}}
=
\frac{1 + \#\{s: |M_s - \mathrm{median}_t M_t| \ge |M_P - \mathrm{median}_t M_t|\}}{B+1}
\]

(versión bilateral respecto a la mediana nula; alternativa aceptable documentada en código: cola unilateral si se fija dirección a priori).

**Dirección a priori (opcional, si se usa cola unilateral):**  
E004 vs uniforme dio \(M_P < \mu_{C1}\).  
Vs Cramér **no** se asume dirección: **bilateral** obligatorio en veredicto principal.

**Prohibido como veredicto:** \(z\)-score gaussiano.  
**Permitido en ficha:** \(z\) descriptivo con nota “no normalidad asumida”.

También:

\[
D_{P,C2} = |M_P - M(C2^\star)|
\qquad
D_{P,C3} = |M_P - M(C3)|
\qquad
D_{C1}^{\mathrm{med}} = \mathrm{median}_s |M_s - \mathrm{median}_t M_t|
\]

---

## 6. Dos mitades (enmienda issue #1 — prerregistrada)

Para que una señal global no dependa de un solo régimen de densidad:

| Mitad | Universo |
| ----- | -------- |
| **Low** | \(V_L = \{1,\ldots,\lfloor N/2\rfloor\}\) |
| **High** | \(V_H = \{\lfloor N/2\rfloor+1,\ldots,N\}\) |

En cada mitad \(H\in\{L,H\}\):

1. \(P_H = P\cap V_H\), \(m_H = |P_H|\).  
2. Cramér equicardinal de tamaño \(m_H\) con pesos \(w_n=1/\ln n\) **restringidos a** \(V_H\) (misma receta, seeds \(s=0..B-1\)).  
3. \(k\) global \(k(N)\) (no se re-escala por mitad — misma lámpara).  
4. \(p_{\mathrm{range}}^{(H)}\) bilateral como en §5 sobre \(M_2(P_H)\) vs \(\{M_2(C1_s^{(H)})\}\).

**Código de consistencia de mitades:**

| Código | Condición |
| ------ | --------- |
| **HALF_BOTH_EXTREME** | \(p_{\mathrm{range}}^{(L)}\le 0.05\) **y** \(p_{\mathrm{range}}^{(H)}\le 0.05\) |
| **HALF_BOTH_NULL** | \(p_{\mathrm{range}}^{(L)}>0.10\) **y** \(p_{\mathrm{range}}^{(H)}>0.10\) |
| **HALF_SPLIT** | resto (una mitad extrema, la otra no) |

---

## 7. Criterios de veredicto (congelados)

Umbral global \(p_{\mathrm{range}}\le 0.01\) como en issue/protocolo 1.0.

| Resultado | Condición |
| --------- | --------- |
| **H-01 PERSISTE** (material > Cramér) | \(p_{\mathrm{range}}\le 0.01\) **y** \(D_{P,C2} > 2 D_{C1}^{\mathrm{med}}\) **y** \(D_{P,C3} > 2 D_{C1}^{\mathrm{med}}\) **y** **HALF_BOTH_EXTREME** |
| **H-00 DESAPARECE** / `MATERIAL_DISSOLVED_BY_CRAMER` | \(p_{\mathrm{range}} > 0.10\) **o** \(M_P\) en banda central 80% de \(\{M_s\}\) **o** (**HALF_BOTH_NULL** y no se cumplen las tres condiciones globales de H-01) |
| **NO_SABEMOS** | resto — en particular: H-01 global sin mitades, o **HALF_SPLIT**, o C2/C3 grises |

Lectura preferente del programa si H-00:

```text
M₂ ordinal no ve nada más allá de densidad (+ independencia tipo Cramér)
MATERIAL_DISSOLVED_BY_CRAMER
```

Primer resultado limpio posible del dominio espectral-grafo.

---

## 8. Ficha de salida

```text
N, k(N), c:     …
B:              2000
C1:             Cramér weighted equicardinal
C2:             sample m of semiprimes ≤ N (not prefix)
p_range:        …   (≥ 1/(B+1) floor)
M_P, med_C1:    …
D_P,C2 / thr:   …
D_P,C3 / thr:   …
p_range_L / H:  …
half_code:      HALF_BOTH_EXTREME | HALF_BOTH_NULL | HALF_SPLIT
z (descriptivo): …  [no veredicto]
Interpretación: PERSISTE | DESAPARECE | NO_SABEMOS
verdict_code:   … | MATERIAL_DISSOLVED_BY_CRAMER
protocol_sha256: …
issue:          gitlab athena#1
```

---

## 9. No-afirmaciones

Igual que E004 + explícito:

- sobrevivir Cramér **no** es Hilbert–Pólya  
- morir vs Cramér **no** es “no hay estructura en primos”  
- solo: este instrumento \(M_2\)+ordinal

---

## 10. Ejecución (secuencia de sello)

```text
1. push artefactos a origin (gitlab.com/athena-group321329/athena)
2. comentar en issue #1 el sha256 de ESTE archivo
3. scripts/run_athena_domain_e005.py
   ATHENA_DOMAIN_E005/resultados/
```

**No ejecutar** el paso 3 sin 1–2.

---

## 11. Checklist pre-run

- [x] MD-039 / MD-040 en log  
- [x] Enmienda 1.1 dos mitades **antes** de datos  
- [ ] Código C1★ / C2★ / mitades vs MD-035  
- [x] \(B=2000\), \(c=1\), bilateral, \(p\le 0.01\) global  
- [ ] Commit + sha256 en issue #1  

---

# FIN — DOMAIN-E005 PROTOCOL 1.1 PREREGISTERED

*Si Cramér mata el ladrillo, el programa gana claridad.  
Si no, entonces — y solo entonces — hay algo que mirar con lupa.*
