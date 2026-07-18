# ATHENA DOMAIN-E007 — Protocolo **CONGELADO** (replicación)

**Clase:** dominio Athena · **réplica**, no descubrimiento  
**Versión:** **1.0 CONGELADO**  
**Fecha:** 2026-07-18  
**Padre:** E006 v1.0 (issue #2) · MD-048 · MD-049  
**Finalidad única:** comprobar **reproducibilidad** de la curva \(S(W)\) y de la clasificación vs rueda 30 — **no** mejorarla ni explicarlas.

---

## 1. Pregunta

**No:**

> ¿Aparece una señal más fuerte?  
> ¿Se acerca más a una teoría?

**Sí:**

> **¿La relación observada en E006 se reproduce bajo un cambio de escala del dominio?**

En una línea:

> **¿Lo que vimos una vez vuelve a ocurrir bajo las mismas reglas, con otro \(N\)?**

---

## 2. Principio de una sola variable

| Elemento | Estado |
| -------- | ------ |
| Definición de \(S(W)\) | **Idéntica** a E006 |
| Valores de \(W\) | **Idénticos:** \(1,2,6,30\) |
| Construcción del grafo | **Idéntica** (ordinal \(0<\|i-j\|\le k\)) |
| Observable \(M_2\) | **Idéntico** |
| Controles C2★ / C3 | **Idénticos** |
| Mitades / p de rango / § veredicto W=30 | **Idénticos** a E006 |
| Pipeline / seeds scheme por rueda | **Idéntico** (mismos `seed_base` relativos) |
| MD-035 | **Idéntico** (gcd solo en \(U_W\)) |
| **Único cambio permitido** | **\(N\)** |

Si entra cualquier otro cambio → **no es E007**; nuevo ID.

---

## 3. Definiciones (copia operativa E006)

\[
S(W)
:=
\big|M_2(P) - \mathrm{median}_s\, M_2\big(C^{(W)}_s\big)\big|
\]

donde \(C^{(W)}_s\) es Cramér-rueda equicardinal sobre \(U_W=\{\gcd(n,W)=1\}\), pesos \(1/\ln n\) en \(U_W\).

\[
k(N)=\mathrm{round}(\ln N),\quad c=1
\]

\(B=2000\). Mitades: universo nulo \(U_W\cap\) mitad.

---

## 4. Escala de réplica (única variable)

| Campo | Valor |
| ----- | ----- |
| \(N_{\mathrm{E006}}\) (referencia, no re-ejecutar aquí) | \(10^5\) |
| \(N_{\mathrm{E007}}\) **principal** | \(\mathbf{5\cdot 10^4}\) |
| \(k(N_{\mathrm{E007}})\) | \(\mathrm{round}(\ln 50000)=\mathbf{11}\) |

**Por qué \(5\cdot 10^4\):** cambio de escala **hacia abajo** (no “más grande”); barato; prueba si el fenómeno era un artefacto de \(N=10^5\).  
Un satélite \(N=2\cdot 10^5\) **no** forma parte de E007 v1.0 (sería E007b / nuevo ID si se desea).

---

## 5. Criterios de reproducción (escritos **antes** de ejecutar)

No se exige igualdad numérica de \(S(W)\) ni de \(M_2\).

### Clasificación protocolar en \(N_{\mathrm{E007}}\)

Misma tabla que E006 §5, nulo principal \(W=30\):

| Código local | Condición |
| ------------ | --------- |
| **PERSISTE** | \(p_{\mathrm{range}}^{(30)}\le 0.01\) **y** \(D_{P,C2}>2D_{\mathrm{med},30}\) **y** \(D_{P,C3}>2D_{\mathrm{med},30}\) **y** HALF_BOTH_EXTREME |
| **DESAPARECE** | \(p^{(30)}>0.10\) **o** central 80% **o** (HALF_BOTH_NULL sin H-01 global) |
| **NO_SABEMOS** | resto (incl. gray \(0.01<p\le 0.10\)) |

### Orden de la curva

\[
S(1) > S(2) > S(6) > S(30)
\]

### Régimen

Ningún punto “cambia de régimen” en el sentido:  
no se exige mapear cada \(W\) a PERSISTE/DESAPARECE (el veredicto es solo W=30);  
sí se exige que **no** ocurra el patrón absurdo de informe: p.ej. declarar éxito de orden si \(S\) se reordena por completo.

### Veredicto de réplica E007 (congelado)

| Resultado E007 | Condición |
| -------------- | --------- |
| **REPRODUCIDA** | Clasificación local = **PERSISTE** **y** orden \(S(1)>S(2)>S(6)>S(30)\) |
| **SENAL_SIN_CURVA** | Clasificación = **PERSISTE** **pero** el orden de \(S(W)\) **falla** |
| **NO_REPRODUCIDA** | Clasificación ≠ **PERSISTE** (DESAPARECE o NO_SABEMOS) |
| **AMBIGUA** | Cualquier fallo técnico / cardinalidad insuficiente en \(U_W\) / incumplimiento de pipeline — **no** se reinterpreta E006 |

---

## 6. Lecturas de desenlace (pre-escritas)

| Resultado | Lectura |
| --------- | ------- |
| **REPRODUCIDA** | Evidencia de **estabilidad** del fenómeno bajo cambio de \(N\). No es teoría. |
| **SENAL_SIN_CURVA** | Hay señal vs rueda 30, pero la **forma** de \(S(W)\) no es estable. |
| **NO_REPRODUCIDA** | E006 pudo depender del tamaño de muestra o de fluctuaciones del observable **a esa escala**. |
| **AMBIGUA** | La pregunta sigue abierta; no se reinterpreta E006 retrospectivamente. |

---

## 7. Regla de interpretación (obligatoria)

> **E007 no modifica retrospectivamente la lectura de E006.**

- Si E007 **falla** (NO_REPRODUCIDA): no convierte E006 en “falso”; indica que el fenómeno **no fue estable** bajo la condición probada (\(N=5\cdot 10^4\)).  
- Si E007 **reproduce**: no convierte E006 en teoría; **aumenta la confianza** en que la observación es reproducible.

El veredicto protocolar de E006 (`H01_MATERIAL_BEYOND_WHEEL_30` a \(N=10^5\)) **permanece** en su ficha.

---

## 8. Prohibido en E007

- nuevos grafos  
- nuevos observables  
- nuevos controles  
- nuevas ruedas  
- suavizados  
- métricas alternativas  
- “mejorar” \(S(W)\) o ajustar \(k\) post-hoc  

---

## 9. Ficha de salida

```text
N_E007, k:         50000, 11
pipeline:          idéntico E006
M_P:               …
S(1),S(2),S(6),S(30): …
orden:             OK | FAIL
class_W30:         PERSISTE | DESAPARECE | NO_SABEMOS
replica_verdict:   REPRODUCIDA | SENAL_SIN_CURVA | NO_REPRODUCIDA | AMBIGUA
protocol_sha256:   …
md035:             PASS (heredado)
E006_status:       no reescrito
```

---

## 10. Ejecución

```text
scripts/run_athena_domain_e007.py
  → llama al pipeline E006 con N=50000 (sin cambiar lógica)
ATHENA_DOMAIN_E007/resultados/classification.json
```

---

## 11. Checklist pre-run

- [x] Solo cambia \(N\)  
- [x] Criterios de reproducción escritos pre-datos  
- [x] Regla anti-retrospectiva  
- [ ] SHA-256 del protocolo en issue/sello si se usa candado remoto  
- [ ] Ejecutar → lectura mecánica de la tabla §5–§6  

---

# FIN — DOMAIN-E007 PROTOCOL 1.0

*De exploración a replicación.  
¿Vuelve a ocurrir?*
