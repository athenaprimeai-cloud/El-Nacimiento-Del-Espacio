# ATHENA DOMAIN-E004 — Informe de cierre (campaña 1 quirúrgica)

**Protocolo:** v1.0 **CONGELADO**  
**Ejecución:** `scripts/run_athena_domain_e004.py`  
**Fuente:** `resultados/classification.json`  
**Anclas:** MD-034 · MD-035 · MD-036 · MD-037  

---

## 1. Pregunta

> ¿El segundo momento espectral \(M_2\) del Laplaciano del grafo **inducido** por vecindad ordinal (\(k=10\))  
> discrimina el conjunto de primos frente a impostores de densidad, semiprimos y Ulam?

No: operador · GUE · “primos = espectro”.  
Sí: **¿hay material** bajo linterna no aritmética y controles obligatorios?

---

## 2. Ficha de salida

| Campo | Valor |
| ----- | ----- |
| **\(N\), \(k\)** | 10000, 10 |
| **\(G\)** | vecindad ordinal \(0<\|i-j\|\le k\) (MD-035 OK) |
| **\(M\)** | \(M_2\) segundo momento espectral Laplaciano inducido |
| **\(m=\pi(N)\)** | 1229 |
| **\(M(P)\)** | **7.740** |
| **\(\mu_{C1}\pm\sigma_{C1}\)** | **10.611 ± 0.492** |
| **\(z_P\), \(p_{C1}\)** | **−5.84**, **0.00** |
| **\(M(C2)\), \(D_{P,C2}\)** | **36.013**, **28.273** |
| **\(M(C3)\), \(D_{P,C3}\)** | **6.046**, **1.316** (Ulam \(m_3=827\); \(P\) submuestreado) |
| **\(2\cdot D_{C1}^{\mathrm{med}}\)** | **0.630** |
| **Interpretación** | **PERSISTE** |

### Condiciones H-01

| Condición | ¿OK? |
| --------- | ---- |
| \(p_{C1}\le 0.05\) | sí (0.00) |
| \(D_{P,C2} > 2 D_{C1}^{\mathrm{med}}\) | sí (28.27 > 0.63) |
| \(D_{P,C3} > 2 D_{C1}^{\mathrm{med}}\) | sí (1.32 > 0.63) |

---

## 3. Veredicto

### 3.a Histórico (protocolo v1.0 tal como escrito — C1 uniforme)

| ID | Estado histórico de corrida |
| -- | --------------------------- |
| **H-ATH-D004-01** | SOPORTADA vs **C1 uniforme** bajo umbrales v1.0 |
| **H-ATH-D004-00** | marcada MUERTA en corrida — **enmendada abajo** |

**Código histórico:** `H01_SPECTRAL_MATERIAL_VS_CONTROLS`

### 3.b Enmendado tras revisor (addendum) — **gobierna la lectura**

| ID | Estado enmendado |
| -- | ---------------- |
| **H-ATH-D004-01** | **SOPORTADA_BAJO_CONTROL_C1_UNIFORME** únicamente |
| **H-ATH-D004-00** | **NO_MUERTA** — nulo legítimo = **Cramér** (E005) |

**Código enmendado:** `H01_VS_UNIFORM_ONLY__H00_PENDING_CRAMER`

Ver `ATHENA_DOMAIN_E004_ADDENDUM_REVIEW.md`.

---

## 4. Lecturas

### Permitido

- Bajo C1 **uniforme** equicardinal, \(M(P)\) es extremo (con la salvedad de \(p\) de rango, no \(p=0\)).  
- Lectura sobria: firma de **gaps/clustering ordinal** (y/o gradiente de densidad), no Hamiltoniano.  
- MD-035/034 respetados en la geometría del grafo.  
- Los cuatro puntos del revisor quedan anclados; H-00 se juega en **E005 vs Cramér**.

### Prohibido

- Declarar H-00 **muerta** con nulo uniforme.  
- Reportar \(p=0\); el honesto es \(p\le 1/101\) en E004.  
- Usar \(z\) gaussiano como veredicto.  
- Tratar \(D_{P,C2}\) del prefijo de semiprimos como control de estructura multiplicativa limpio.  
- “Réplica” \(N=10^5\) con \(k=10\) fijo sin prerregistrar política de \(k\).  
- “Los primos son un espectro” / Hilbert–Pólya / GUE.

### Objeciones del revisor (resumen)

1. **C1 uniforme** no mata H-00 → hace falta **Cramér**.  
2. **\(p=0\)** no existe → p de rango; más réplicas.  
3. **C2 prefijo** confunde densidad → sample equicardinal en \(\le N\).  
4. **\(k=10\)** ≈ gap medio en \(N=10^4\) → réplica con \(k=c\ln N\) o predicción si \(k\) fijo.

---

## 5. Montaña

```text
¿estructura generativa → primos?
        ↑
¿material no aritmético vs controles?  ← E004: sí, bajo control (ladrillo)
        ↑
E003 / E002 / E001: tres ilusiones de señal muertas
```

Siguiente (solo con disciplina):

- réplica \(N=10^5\) mismo protocolo, **o**  
- otra familia de grafo permitida (embebida / \(T\) geométrico) con **nuevo ID**, **o**  
- otra \(M\) (espectro completo) solo si se justifica sin contrabando y sin catedral prematura  

No: saltar a Riemann porque “por fin algo persistió”.

---

## 6. Lab

Tres linternas mataron sombras pintadas.  
La cuarta no busca la pared: encontró **un ladrillo** que no es solo la forma del molde (densidad).  

Era II: el instrumento mereció existir.  
La catedral **no** se discute todavía.

---

# FIN — DOMAIN-E004 REPORT

*Material ≠ muro.  
PERSISTE ≠ teorema.*
