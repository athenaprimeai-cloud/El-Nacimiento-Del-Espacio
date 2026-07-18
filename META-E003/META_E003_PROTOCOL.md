# META-E003 — Protocolo experimental **CONGELADO**

**Clase:** investigación del **guardián** (Auditor)  
**Versión:** **1.0 CONGELADO**  
**Fecha:** 2026-07-17  
**No es:** “¿el Auditor funciona?” unitario · rediseño del Auditor · Selector v2  

---

## 1. Pregunta

> ¿Existen fallos metodológicos que **sobreviven** porque respetan la **forma externa** del sistema  
> (el Auditor comparte supuestos con lo que vigila)?

Zona peligrosa:

```text
Proceso incorrecto → parece correcto → Auditor → PASS
```

---

## 2. Hipótesis

| ID | Enunciado |
| -- | --------- |
| **H-META-E003-01** | El Auditor mantiene integridad frente a fallos **no triviales** de la batería predeclarada (detecta o bloquea). |
| **H-META-E003-00** | El Auditor protege principalmente la **forma** del protocolo; puede dar **PASS** a procesos epistemológicamente dañados si la estructura superficial es correcta. |

---

## 3. Batería de ataques (congelada)

| ID | Tipo | Descripción | Detección esperada si Auditor “completo” |
| -- | ---- | ----------- | ---------------------------------------- |
| **A1** | Estructural (baseline) | Reescritura post-resultado de predicción | **FAIL** (ya unitario) |
| **A2** | Estructural | Borrado de hipótesis MUERTA | **FAIL** (ya unitario) |
| **A3** | Cumplimiento formal | Cierre MUERTA sin death_reason | **FAIL** si se intenta; o estado inválido |
| **A4** | Escala estructural | Muchas fichas OPEN + una corrupción A1 oculta | **FAIL** al auditar el store |
| **A5** | Semántica / forma correcta | Registro `result_summary` engañoso; ficha y control formales OK | **PASS del Auditor actual** (punto ciego predeclarado) |
| **A6** | Métrica engañosa | Campaña reporta solo ECO sin coste de diversidad | **PASS del Auditor** (no exige métricas de cobertura) |
| **A7** | Cumplimiento formal + pregunta no respondida | Estados y controles OK; el “resultado” no habla de la predicción | **PASS del Auditor** (no hay chequeo semántico predicción↔resultado) |

**Clasificación de ataques:**

- **Estructurales (A1–A4):** el Auditor **debe** pillarlos → si falla, H-01 muere.  
- **Semánticos / de supuesto compartido (A5–A7):** se **espera** que el Auditor v0.1 dé PASS → evidencia para **H-00** (límites), no bug accidental.

---

## 4. Métricas

| ID | Definición |
| -- | ---------- |
| **DET_STRUCT** | % de A1–A4 detectados como FAIL |
| **PASS_SEM** | % de A5–A7 que reciben PASS (esperado alto para Auditor actual) |
| **FP_NOSABE** | ¿NO_SABEMOS legítimo se marca FAIL? (debe ser 0) |

---

## 5. Veredicto (congelado)

| Condición | Lectura |
| --------- | ------- |
| DET_STRUCT = 100 % y PASS_SEM ≥ 2/3 | **H-00 apoyada en límites semánticos**; H-01 **soportada solo en integridad documental** |
| DET_STRUCT &lt; 100 % | **H-01 debilitada/muerta** en estructurales |
| FP_NOSABE &gt; 0 | **H-01 debilitada** |

Salida: **mapa de áreas**, no “Auditor bueno/malo”.

---

## 6. Ejecución

```text
Runner: scripts/run_meta_e003.py
Una pasada de la batería A1–A7 (+ control NO_SABEMOS limpio)
```

---

## 7. Sello

| | |
| - | - |
| Congelado | **SÍ** |
| Prohibido | Rediseñar Auditor durante la corrida; reclamar “confianza total” |

---

# FIN — META-E003 PROTOCOL 1.0
