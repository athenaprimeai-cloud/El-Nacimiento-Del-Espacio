# META-E001 — Informe de cierre

**Protocolo:** v1.0 **CONGELADO**  
**Ejecución:** `scripts/run_meta_e001.py` · N_rep=10 · N_cand=100  
**Fuente:** `resultados/classification.json`  
**Era:** II — investigar el laboratorio (intentar falsar el pipeline)

---

## 0. Cumplimiento

| Requisito | Estado |
| --------- | ------ |
| Protocolo congelado antes de corrida | ✅ v1.0 |
| 10 seeds | ✅ 0..9 |
| 100 candidatos / seed | ✅ |
| MONOLITO vs PIPELINE_SEPARADO | ✅ (sin Selector vs + Selector) |
| Sin re-ejecutar para “buscar A” | ✅ una pasada |
| Perfil E-M* | ✅ abajo |

---

## 1. Pregunta

> ¿Un pipeline separado produce realmente mejores indicadores metodológicos que un monolito de presupuesto (todo OPEN = ataque)?

**No se buscó confirmar el kernel.** Se intentó, con las reglas predeclaradas, que **H-META-E001-00** ganara.

---

## 2. Resultados agregados

| Métrica | Valor |
| ------- | ----- |
| Reducción media de presupuesto M2 vs M1 | **0.85** (85 %) |
| Reducción mínima (peor seed) | **0.85** |
| Réplicas con reducción ≥ 50 % | **10 / 10** |
| POSTHOC limpio en todas | **sí** |
| budget M1 (típico) | 20 |
| budget M2 (típico) | 3 |

Todas las seeds: M1 budget=20, M2 budget=3, posthoc_clean=true.

---

## 3. Veredicto de hipótesis (protocolo §5)

| ID | Estado |
| -- | ------ |
| **H-META-E001-01** | **SOPORTADA_BAJO_CONTROL** (solo en el eje E-M2 + E-M1 de este diseño) |
| **H-META-E001-00** | **MUERTA** (no sostiene “no hay mejora de economía con integridad” bajo umbral 50 % × 10/10) |

**Código de veredicto:** `H-META-E001-01_WINS_E-M2`

---

## 4. Perfil de evidencia (`META_EVIDENCE_MODEL.md`)

| Tipo | Nivel | Lectura |
| ---- | ----- | ------- |
| **E-M1** | **fuerte** | Integridad PASS y POSTHOC=0 en 10/10 réplicas |
| **E-M2** | **fuerte** | Reducción de presupuesto ≥ 50 % en 10/10 (media 85 %) |
| **E-M3** | **insuficiente** | No hay Crítico/eliminación de hipótesis “incorrectas”; solo proxy POSTHOC |
| **E-M4** | **no evaluada** | Solo dominio toy sintético |
| **E-M5** | **no evaluada** | No se modificó el kernel |

### Mejora local vs global

- **Local (E-M2):** sí — menos unidades de ataque planificadas.  
- **Global (calidad científica a largo plazo / sesgo del Selector):** **no demostrado**.  
- Por tanto: **no** se interpreta como “el laboratorio es científicamente superior en general”.

---

## 5. Límites de alcance (obligatorios)

1. **MONOLITO** = sin Selector; **Core + Auditor siguen presentes** en ambos brazos. No es un proceso sin disciplina de registro.  
2. Explorador **sintético**, no LLM ni dominio Goldbach.  
3. “Presupuesto de ataque” es **proxy** (¿cuántas OPEN se atacarían primero?), no campañas experimentales de dominio reales.  
4. H-META-E001-01 **no** se eleva a verdad del kernel; es apoyo **bajo este control**.

---

## 6. Lecturas permitidas y prohibidas

### Lo que **realmente** mostró META-E001

> En **este** entorno experimental, un pipeline con **selección previa** redujo el presupuesto experimental (20 → 3) **sin** romper la integridad metodológica definida por Core y Auditor.

Eso justifica E-M1 fuerte · E-M2 fuerte · E-M3 abierto · E-M4/E-M5 sin evidencia.

### Permitido

- Observación experimental (no filosofía): separar exploración y priorización **parece** reducir coste experimental sin romper la disciplina del protocolo **bajo este control**.  
- H-META-E001-00 no sobrevive al umbral de economía predeclarado.  
- El lab puede medirse a sí mismo al estilo E004.2 (H, rival, congelado, archivo, límites).

### Prohibido (todavía)

- “El laboratorio investiga **mejor**.”  
- “El Selector mejora la **ciencia**.”  
- “El pipeline completo (M4) está validado.”  
- “El Selector no tiene sesgo.”  
- Mejoró una métrica → mejoró el laboratorio (local ≠ global).

---

## 7. ¿Debemos cambiar el kernel?

**No** por este resultado como mandato de expansión.

- E-M2 sugiere que **mantener** el Selector como legislación actual tiene apoyo económico **bajo este control**.  
- E-M3 insuficiente y sesgo abierto: **no** coronar el Selector.  
- Constitución intacta. Legislación del Selector: **sin cambio** (sigue siendo hipótesis metodológica con evidencia E-M2 parcial-fuerte en un proxy).

Si en el futuro E-M3/E-M4 contrarios → el Selector **puede morir**.

---

## 8. Residual / siguiente META-E natural

| Residual | Ruta |
| -------- | ---- |
| Sesgo del Selector (A baratas vs difíciles) | META-E002 ampliación / retrospectiva |
| Monolito sin Core | Nuevo protocolo si se mide |
| E-M3 real (errores de juicio) | Requiere Crítico — solo si META-E lo exige |
| E-M4 cross-domain | META-E004 |

---

## 9. Cumplimiento de la Era II

| Promesa | |
| ------- | - |
| Convencer a la evidencia, no a los diseñadores | Se intentó falsar; H-00 no ganó en E-M2 |
| Perfil E-M*, no eslogan | ✅ |
| Mejora local ≠ global | ✅ declarado |
| Kernel puede morir | H-00 murió; H-01 no es el kernel entero |

---

# FIN — META-E001 REPORT

*E-M1 fuerte · E-M2 fuerte (proxy de presupuesto) · E-M3 insuficiente.  
No se reabrió la Era I. No se amplió la arquitectura.*
