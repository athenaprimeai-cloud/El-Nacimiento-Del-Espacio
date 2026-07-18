# META-E004 — Informe de cierre

**Protocolo:** v1.0 **CONGELADO**  
**Selector:** **v0.1 sin modificar**  
**Ejecución:** `scripts/run_meta_e004.py` · 3 dominios × 5 seeds × 100 candidatos  
**Fuente:** `resultados/classification.json`  

---

## 1. Pregunta

> ¿La relación economía ↔ diversidad es del **mecanismo de selección** o del **generador E002b**?

No se repitió E002b. No se buscó “otro fallo a la fuerza”.  
Se cambió de **terreno** manteniendo las **reglas**.

---

## 2. Tabla por dominio

| Dominio | Economía | Diversidad | mean ECO | mean DIV_DROP | mean FN | Estado |
| ------- | -------- | ---------- | -------- | ------------- | ------- | ------ |
| **math_struct** | + | − | 0.84 | 0.83 | 0.69 | diversidad_comprimida |
| **engineering** | + | − | 0.84 | 0.84 | 1.00 | diversidad_comprimida |
| **creative** | + | − | 0.84 | 0.83 | 0.20 | diversidad_comprimida |

En los tres: economía alta y **DIV_DROP ≈ 0.83–0.84**.  
FN de `high_value` varía (1.0 en engineering, 0.2 en creative) pero el patrón de **concentración en A** es transversal.

---

## 3. Veredicto

| ID | Estado |
| -- | ------ |
| **H-META-E004-01** (coste transversal) | **SOPORTADA_BAJO_CONTROL** |
| **H-META-E004-00** (solo generador E002b) | **DEBILITADA** |

**Código:** `H01_TRANSVERSAL_DIVERSITY_COST`

Lectura: bajo este diseño multi-dominio sintético, el precio de diversidad **no** se ve como artefacto exclusivo de E002b.  
Aparece de nuevo al cambiar formulaciones y familias de candidatos.

---

## 4. Perfil de evidencia

| Tipo | Nivel |
| ---- | ----- |
| E-M1 | fuerte |
| E-M2 | fuerte (economía en todos los dominios) |
| E-M3 | coste de diversidad reaparece (ver tabla) |
| **E-M4** | **apoyo a generalización del patrón** (no a “especificidad E002b”) |
| E-M5 | no evaluada |

### Local ≠ global

No prueba ceguera en Goldbach real.  
Prueba: **tres generadores distintos** + mismo Selector → mismo tipo de compresión.

---

## 5. Mapa de validez actualizado (Selector v0.1)

| | |
| - | - |
| **Excelente para** | eliminar redundancia / recortar presupuesto |
| **Peligroso para** | explorar territorios desconocidos / diversidad de caminos |
| **Estado legislativo** | **soportado con limitaciones** (reafirmado y **endurecido** en alcance) |

---

## 6. Lecturas permitidas / prohibidas

### Permitido

- E002b no se ve como sobreajuste puro al generador original.  
- La legislación del Selector debe mantener controles (excluidos, límites de dominio).  
- H-00 (solo contexto E002b) queda debilitada **bajo este control**.

### Prohibido

- “El Selector está roto en todo el universo.”  
- Selector v2 sin diseño justificado por este perfil.  
- Reescribir E001 (la economía sigue siendo real).  
- Tratar dominios sintéticos como Athena matemática real.

---

## 7. Decisión de legislación

| Acción | |
| ------ | - |
| ¿Cambiar Selector v0.1 código? | **No** (objeto congelado de la campaña) |
| ¿Actualizar límites documentados? | **Sí** — generalización del riesgo de diversidad |
| ¿Constitución? | Intacta |

Ver `LEGISLATION_SELECTOR_v0_1.md` (actualización post-E004).

---

## 8. Victoria del régimen

No se protegió E002b por orgullo ni se destruyó el Selector por pánico.

> El coste de diversidad **no** se limitó al entorno artificial original (bajo estos tres dominios).  
> La legislación se endurece en **alcance de uso**, no se inventa una pieza nueva.

---

# FIN — META-E004 REPORT

*Mismo Selector. Otros terrenos. Misma compresión.  
Mapa, no corona.*
