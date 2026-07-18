# META-E001 — Protocolo experimental (investigación del laboratorio)

**Clase:** investigación **metodológica** (objeto = kernel / separación de funciones)  
**No es:** campaña de dominio (Goldbach, etc.) · ampliación de arquitectura  
**Régimen:** el **mismo** que E004.2 — no un formato “especial por ser meta”  
**Versión:** **1.0 CONGELADO**  
**Estado:** **CONGELADO** · ejecución autorizada (Era II — medir, no diseñar)  
**Fecha de congelación:** 2026-07-17  
**Programa:** Meta (sobre el kernel) · ver `LABORATORY.md`, `META_EXPERIMENTS.md`  
**R0:** auto-sello de sesión (Nivel 1) — no revisor académico externo  

---

## Regla de jerarquía (proyecto)

> **Todo en el laboratorio puede morir, excepto el principio rector.**

| Capa | Régimen |
| ---- | ------- |
| Principio rector | **Estable** |
| Kernel metodológico | **Falsable** |
| Programas científicos | **Falsables** |
| Hipótesis concretas | **Falsables** |

### Privilegio prohibido

> **El kernel nunca obtiene privilegios epistemológicos por haber sido diseñado primero.**

Si META-E demuestra que una parte del kernel **empeora** la investigación, esa parte **sale**. Sin excepciones.

---

## 0. Lenguaje

**No:** “validar el laboratorio” (suena a buscar confirmación).  
**Sí:** **investigar el laboratorio** — admite: mejora / no mejora / **no sabemos**.

Una derrota de la separación de funciones sería un **éxito del régimen experimental**: el instrumento también puede ser falsado.

---

## 1. Pregunta

> ¿La **separación de funciones** (pipeline: Explorador → Selector → … → Core → Auditor) **reduce errores metodológicos** frente a un proceso **menos estructurado** (exploración monolítica / sin priorización / sin auditoría)?

---

## 2. Hipótesis

| ID | Enunciado |
| -- | --------- |
| **H-META-E001-01** | Bajo la misma pregunta de dominio (toy o real) y presupuesto comparable, el pipeline con separación de funciones produce **menos errores metodológicos** y/o **mejor economía experimental con integridad** que un proceso monolítico. |
| **H-META-E001-00** (rival) | La separación de funciones **no** mejora (o empeora) esos indicadores frente al monolito; la complejidad es cosmética. |

Ambas son informativas. **H-META-E001-00 puede ganar.**

---

## 3. Variable única (conceptual)

```text
modo_de_trabajo ∈ { MONOLITO, PIPELINE_SEPARADO }
```

| Nivel | Definición operativa (v0.1) |
| ----- | --------------------------- |
| **MONOLITO** | Explorador solo; presupuesto de “ataque” = todos los OPEN; sin Selector; sin capa de priorización |
| **PIPELINE_SEPARADO** | Explorador + Selector (grupo A = presupuesto de ataque); Core + Auditor activos en ambos (el registro siempre existe) |

**Nota de honestidad:** “monolito total” sin Core sería otro diseño; aquí el monolito es **sin economía de ataque**.  
Extensiones futuras (sin Core, sin Auditor) = **nuevo ID** de protocolo si se miden.

**Congelado entre brazos:** pregunta de dominio, N candidatos del explorador, generador sintético, umbrales del auditor, seeds del generador si aplica.

---

## 4. Métricas y tipos de evidencia (ver `META_EVIDENCE_MODEL.md`)

| ID | Métrica | Tipo de evidencia |
| -- | ------- | ----------------- |
| **POSTHOC** | Violaciones FAIL del auditor | **E-M1**, **E-M3** |
| **BUDGET** | Unidades de presupuesto de ataque (|OPEN| vs \|A\|) | **E-M2** |
| **INTEGRITY** | auditor verdict PASS | **E-M1** |
| **REJECT** | % rechazo por ficha incompleta | Secundaria (ruido) |
| **ELIM** | Terminales correctos (futuro con Crítico) | **E-M3** |

**Perfil de evidencia exigido en el informe de cierre** (no un solo “mejor/peor”):

```text
E-M1: …
E-M2: …
E-M3: …
E-M4: no evaluada (salvo extensión)
E-M5: no evaluada
Mejora local vs global: …
```

**Regla:** mejora local de BUDGET (E-M2) **sin** E-M1 limpio o con E-M3 contraria → **no** se adopta como mejora del laboratorio.

---

## 5. Predicciones y muerte

### Bajo H-META-E001-01

- PIPELINE_SEPARADO: **BUDGET** estrictamente menor que MONOLITO con **INTEGRITY=PASS** y **POSTHOC=0** en ambos.  
- No aumento de POSTHOC al añadir Selector.

### Muerte / debilitamiento de H-META-E001-01

| | |
| - | - |
| **Debilita** | BUDGET similar y POSTHOC igual — sin ganancia clara |
| **Mata** | PIPELINE_SEPARADO con **más** POSTHOC o INTEGRITY FAIL, o BUDGET no menor de forma predeclarada |
| **NO_SABEMOS** | Efectos mixtos / tamaño de efecto bajo umbral sin patrón *a priori* |

### Muerte de H-META-E001-00 (rival)

- PIPELINE reduce BUDGET ≥ **50%** (umbral *a priori* v0.1) con POSTHOC=0 e INTEGRITY PASS en ≥ **N_rep** réplicas.

---

## 6. Protocolo de ejecución (congelado)

```text
Réplicas: N_rep = 10 (seeds 0..9)
Candidatos por réplica: N_cand = 100
Dominio: toy sintético (misma pregunta base)
Runner: scripts/run_meta_e001.py
```

**Cierre:** tras N_rep + classification.json + informe con perfil E-M*.

**Sin** re-ejecutar hasta “encontrar” superioridad del pipeline.

---

## 7. Residual

Si el pipeline reduce presupuesto pero **empeora** alguna métrica no primaria no predeclarada → residual / nuevo META-E, no redefinir umbrales post-hoc.

---

## 8. Decision Log (entrada de campaña)

| Campo | Contenido |
| ----- | --------- |
| **Motivo** | Investigar el lab: separación de funciones vs monolito de presupuesto |
| **No es** | Validar buscando confirmación; proteger el kernel por antigüedad |
| **Reversión** | Si H-META-E001-00 gana → documentar y **retirar o simplificar** piezas que no aporten |

---

## 9. Evidencia previa (no sustituye este protocolo)

M1 vs M2 en una corrida: budget 20→3 (~85%), auditor PASS.  
Eso es **preliminar**, no cierre de META-E001 (falta multi-seed, umbrales congelados, R0).

---

## 10. Sello

| Campo | Valor |
| ----- | ----- |
| Versión | **1.0 CONGELADO** |
| Congelado | **SÍ** |
| Ejecución autorizada | **SÍ** |
| Declaración | No alterar umbrales §5–§6 ni brazos sin nuevo ID |

---

# FIN — META-E001 PROTOCOL 1.0 CONGELADO

*Investigar el laboratorio. Intentar falsar el pipeline.  
El kernel puede morir. La brújula no.*
