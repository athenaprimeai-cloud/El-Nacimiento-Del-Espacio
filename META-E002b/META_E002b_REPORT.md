# META-E002b — Informe de cierre

**Protocolo:** v1.0 **CONGELADO**  
**Ejecución:** `scripts/run_meta_e002b.py` · N_rep=10 · N_cand=100  
**Fuente:** `resultados/classification.json`  
**Objeto:** Selector v0.1 (hipótesis sobre el **instrumento**)  
**No es:** Selector v2 · “el lab investiga mejor”  

---

## 0. Pregunta

> ¿La reducción de coste viene de eliminar **ruido** o **diversidad**?  
> *Si el Selector tiene razón demasiado rápido, ¿qué está dejando de ver?*

Zona crítica: la **columna de excluidos** (no los priorizados).

---

## 1. Diseño (cumplimiento)

| Elemento | Estado |
| -------- | ------ |
| H-META-E002b-01 (compresión de ruido) | predeclarada |
| H-META-E002b-00 (compresión de diversidad) | rival |
| Latentes invisibles al Selector | `noise` / `common_ok` / `rare_valuable` |
| Control oculto | métricas sobre excluidos vs A |
| 10 seeds | ✅ |

---

## 2. Resultados agregados (10/10 seeds)

| Métrica | Media |
| ------- | ----- |
| Economía (reducción budget) | **0.85** (20→3) |
| DIV_DROP (1 − clusters_A/clusters_all) | **0.85** |
| FN_RATE (rare en excluidos / rare total)* | **0.17** media (0.85 cuando hay rare; 0 cuando no hay rare en el seed) |
| COV_RARE en A* | **0.03** media |
| Reversibilidad (IDs/scores intactos) | **sí** en 10/10 |
| Seeds con patrón diversidad (00) | **10/10** |
| Seeds con patrón ruido (01) | **0/10** |

\*En este generador, `rare_valuable` solo aparece en algunos seeds; cuando aparece, **FN≈0.85** (casi todos fuera de A). En seeds sin rare, el patrón 00 se activa por **DIV_DROP=0.85**.

---

## 3. Veredicto

| ID | Estado |
| -- | ------ |
| **H-META-E002b-01** (ruido) | **DEBILITADA** |
| **H-META-E002b-00** (diversidad) | **SOPORTADA_BAJO_CONTROL** |

**Código:** `H00_DIVERSITY_COMPRESSION_MODERATE`

Lectura: la economía del −85 % **no** se lee como “solo ruido fuera”. Bajo este generador, el Selector **comprime el espacio** (pocos clusters en A) y, cuando hay rare, los **excluye en masa**.

---

## 4. Perfil de evidencia

| Tipo | Nivel | Nota |
| ---- | ----- | ---- |
| **E-M1** | **fuerte** | Reversibilidad / registro intacto |
| **E-M2** | **fuerte** | Economía re-confirmada (como E001) |
| **E-M3** | **contraria** (bajo este control) | Coste de ceguera / pérdida de diversidad en A |
| **E-M4** | no evaluada | Un solo generador sintético |
| **E-M5** | no evaluada | |

### Local ≠ global

- **Local (E-M2):** sigue valiendo la economía.  
- **Global (E-M3 aquí):** el precio es compresión de diversidad — **no** adoptar como “Selector mejora la ciencia”.

---

## 5. Mapa de validez (salida, no medalla)

| | |
| - | - |
| **Aceptado** | Solo si se acepta pérdida fuerte de diversidad de OPEN |
| **Limitado** | Exploración inicial con alta redundancia; **requiere** control oculto / muestreo de excluidos |
| **No recomendado** | Búsqueda abierta de estructuras raras o baja frecuencia; dominios donde la diversidad de caminos es el activo |

---

## 6. ¿Qué había en los 80?

| Observación | |
| ----------- | - |
| OPEN típicos | 20; A = 3; excluidos = 17 |
| Clusters | ~20 → ~3 en A (**DIV_DROP 0.85**) |
| rare_valuable (cuando existen) | ~85 % en zona excluida |
| common_ok | dominan A cuando no hay rare |

El cementerio de excluidos **no** es solo basura incompleta (eso ya lo filtró el Core): son OPEN con ficha completa que el Selector **no prioriza**.

---

## 7. Lecturas permitidas / prohibidas

### Permitido

- Bajo este protocolo y generador, el Selector compra economía **pagando diversidad**.  
- H-01 (solo ruido) no se sostiene; H-00 gana apoyo **relativo**.  
- E001 (E-M2) y E002b (E-M3 de coste) **juntos** dan un perfil de intercambio, no una corona.

### Prohibido

- “El Selector es malo y se elimina ya” sin política de límites (el mapa dice **limitado** / no recomendado en dominios exploratorios).  
- “El lab es ciego siempre” (ámbito sintético).  
- Selector v2 por entusiasmo.  
- Reescribir META-E001 (la economía sigue siendo real).

---

## 8. Decisión de legislación

| Acción | |
| ------ | - |
| ¿Eliminar Selector del kernel? | **No automáticamente** — mapa de validez primero |
| ¿Selector v2? | **No** hasta diseño justificado por este coste |
| ¿Uso por defecto en exploración abierta? | **No recomendado** bajo este control |
| ¿Conservar v0.1 como hipótesis con límites? | **Sí** — documentado; puede morir con más E-M4 |

---

## 9. Cumplimiento Era II

| | |
| - | - |
| Hipótesis + rival | ✅ |
| Protocolo congelado | ✅ |
| Zona excluida medida | ✅ |
| Ficha de supervivencia (no medalla) | ✅ |
| Local ≠ global | ✅ |

---

# FIN — META-E002b REPORT

*Economía fuerte · diversidad comprimida.  
El filtro reveló el precio de su eficiencia.*
