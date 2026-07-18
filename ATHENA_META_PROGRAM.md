# ATHENA — PROGRAMA META (investigación metodológica)

**Estado:** abierto en diseño · harness mínimo de métricas  
**No es:** autoedición del código por IA · reescritura de la brújula  
**Es:** Athena como **objeto experimental** — ¿el conjunto supera a las partes?  

---

## Cambio de nivel

Ya no: “¿qué componente falta?”  
Sino: **¿el conjunto es mejor que la suma de las partes?**

### Propiedad emergente (hipótesis de diseño)

> **Ningún componente puede producir conocimiento por sí solo,  
> pero el sistema completo sí puede producir evaluaciones más robustas  
> que cualquiera de sus componentes aislados.**

Si esa frase se demuestra → colección de módulos pasa a ser **laboratorio**.  
Si se falsea → la arquitectura debe poder cambiar **sin** abandonar la brújula.

---

## Capas (ver `LABORATORY.md`)

| Capa | Rol |
| ---- | --- |
| Principio rector | Brújula |
| **Kernel** | El **laboratorio** (agnóstico) |
| Programa Athena | Un programa de dominio sobre el kernel |
| **Programa meta** | Estudia el **kernel**, no Goldbach |

| | Programa de dominio (p.ej. Athena) | Programa meta |
| - | ----------------------------------- | ------------- |
| Objeto | Matemáticas / estructuras | El **kernel / laboratorio** |
| Pregunta típica | ¿Hay estructura no trivial en…? | ¿Esta modificación **mejora** la calidad metodológica? |
| Kernel | Lo **usa** | Lo **mide** |

**Brújula:** estable.  
**Arquitectura:** falsable.  
Principios permanentes ≠ diseño revisable.

La pregunta central del proyecto:

> ¿Cómo diseñar un laboratorio donde cada componente tenga poder para **aportar** conocimiento, pero no para **imponerlo**?

Eso es una **hipótesis de diseño**. También debe poder **morir**.

---

## Recurso escaso (recordatorio)

Experimentos, no hipótesis.  
El Selector ya codifica esa economía; el Programa meta mide si la codificación **funciona**.

---

## Campaña metodológica: modos M1–M4

Misma **pregunta de dominio** (puede ser toy o real).  
Cuatro modos de trabajo:

| Modo | Componentes |
| ---- | ----------- |
| **M1** | Solo Explorador |
| **M2** | Explorador + Selector |
| **M3** | Explorador + Selector + Crítico |
| **M4** | Pipeline completo (… + Diseñador + Core disciplina + Auditor + Registro) |

Hoy implementables de verdad: **M1, M2** (+ disciplina Core/Auditor siempre bajo el registro).  
M3/M4: cuando exista Crítico/Diseñador; hasta entonces se miden con stubs o se marcan N/A.

### Métricas de **proceso** (no Goldbach)

| Métrica | Idea |
| ------- | ---- |
| **HUE** | Hipótesis útiles por experimento (proxy: fichas completas / ataques ejecutados) |
| **ELIM** | % hipótesis eliminadas/debilitadas **correctamente** (con control + razón) |
| **POSTHOC** | Tasa de revisiones post-hoc (ideal: **0**; auditor FAIL count) |
| **REG_STAB** | Estabilidad del registro (muertes no borradas, IDs estables) |
| **COST_K** | Coste por conocimiento retenido (experimentos / (soportadas + muertas informativas + NO_SABEMOS honestos)) |
| **BUDGET** | En M2+: fracción del presupuesto gastada en grupo A vs C |

### Criterio de valor emergente

Si M2 (o M4 cuando exista) **supera sistemáticamente** a M1 en ELIM/POSTHOC/COST_K **sin** subir POSTHOC:

→ evidencia de que la arquitectura añade **valor metodológico**, no solo complejidad.

Si no:

→ hipótesis de diseño debilitada; rediseñar separación de funciones **sin** tocar la brújula.

---

## Selector como hipótesis metodológica

Las heurísticas del Selector (falsable/barato/novedoso) pueden sesgar contra lo difícil-e-importante.  
El Programa meta **debe** medir retrospectivamente:

- ¿las A sobrevivieron más?
- ¿las C escondían valor?
- ¿hay sesgo permanente?

---

## Código

```text
athena_core/meta_eval.py
scripts/run_meta_modes.py
tests/test_athena_meta_eval.py
data/athena_meta/META_MODES_REPORT.json
```

## Resultado inicial M1 vs M2 (N=100, sintético)

| | M1 solo Explorador | M2 + Selector |
| - | ------------------ | ------------- |
| OPEN aceptados | 20 | 20 |
| Rechazo core | 80 | 80 |
| Budget (ataques planeados) | 20 | **3** (grupo A) |
| Post-hoc / auditor | PASS | PASS |
| Reducción de presupuesto | — | **~85%** |

**Interpretación permitida:** M2 mejora la **economía experimental** sin romper integridad.  
**No permitido:** “M2 descubre más matemáticas” (no medido).  
**Abierto:** sesgo del Selector; M3/M4 cuando exista Crítico.

---

# FIN — META PROGRAM

*El lab se investiga a sí mismo.  
Brújula fija. Arquitectura falsable.*
