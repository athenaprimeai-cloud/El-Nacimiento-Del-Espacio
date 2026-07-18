# META-E004 — Protocolo experimental **CONGELADO**

**Clase:** investigación del instrumento (generalización del Selector)  
**Versión:** **1.0 CONGELADO**  
**Fecha:** 2026-07-17  
**No es:** Selector v2 · repetir E002b · buscar fallos a la fuerza  

---

## 1. Pregunta

> ¿La relación **economía ↔ diversidad** es una propiedad del **mecanismo de selección**  
> o una propiedad del **generador de candidatos** con el que se midió en META-E002b?

No: “¿El Selector pierde diversidad?” (ya hay respuesta **limitada** en E002b).  
Sí: **¿ese precio existe fuera de ese entorno?**

---

## 2. Objeto congelado

```text
Selector v0.1  (sin cambios de código/heurísticas)
+ nuevos dominios de generación de candidatos
+ mismo régimen Core + Auditor + métricas de zona excluida
```

Si se cambia el Selector, **ya no** se mide generalización.

---

## 3. Hipótesis

| ID | Enunciado |
| -- | --------- |
| **H-META-E004-01** | El coste de diversidad de E002b **aparece** en otros dominios (patrón transversal del filtrado). |
| **H-META-E004-00** | El coste era **específico** del generador sintético E002b; en otros dominios la cobertura se mantiene o el patrón se debilita. |

Ambas son victorias del régimen.

---

## 4. Dominios (tres familias)

| ID | Familia | Generador | Rol |
| -- | ------- | --------- | --- |
| **D-A** | Estructuras matemáticas | `math_struct` | Cercano a Athena |
| **D-B** | Ingeniería / optimización | `engineering` | Fuera de matemática pura |
| **D-C** | Exploración creativa controlada | `creative` | Presión a diversidad (sin copiar E002b rare) |

**Anti-trampa:** no diseñar dominios “sabiendo” que habrá el mismo fallo.  
Cada generador tiene su propia estructura de latentes y formulaciones.

Baseline de referencia (no re-ejecuta E002b como dominio de esta campaña): resultados archivados de META-E002b.

---

## 5. Métricas (por dominio y seed)

| ID | Métrica |
| -- | ------- |
| **ECO** | 1 − \|A\|/\|OPEN\| |
| **DIV_DROP** | 1 − clusters(A)/clusters(OPEN) |
| **FN_RATE** | latentes “high_value” en excluidos / total high_value en OPEN |
| **COV_HV** | high_value en A / total high_value |
| **REV** | IDs de excluidos y ranking conservados |

`high_value` = etiqueta latente **por dominio** (invisible al Selector).

---

## 6. Criterios de lectura (congelados)

Por dominio, patrón **diversidad** si:

- DIV_DROP ≥ 0.55 **o** FN_RATE ≥ 0.50 **o** COV_HV &lt; 0.35  

Patrón **ruido/cobertura OK** si:

- FN_RATE &lt; 0.40 **y** COV_HV ≥ 0.50 **y** DIV_DROP &lt; 0.50  

### Veredicto global

| Condición | Lectura |
| --------- | ------- |
| ≥ 2/3 dominios con patrón diversidad (media de seeds) | Apoyo a **H-01** (transversal) |
| ≥ 2/3 dominios con patrón cobertura OK | Apoyo a **H-00** (contextual E002b) |
| Mezcla 1–1–1 o umbrales intermedios | **NO_SABEMOS** / mapa mixto |

Salida principal: **tabla por dominio** (economía / diversidad / estado), no una medalla única.

---

## 7. Ejecución

```text
N_rep = 5 seeds por dominio
N_cand = 100
Dominios = D-A, D-B, D-C
Runner: scripts/run_meta_e004.py
```

---

## 8. Perfil E-M*

| Tipo | Rol en esta campaña |
| ---- | ------------------- |
| E-M1 | integridad / reversibilidad |
| E-M2 | economía por dominio |
| E-M3 | diversidad / FN (primario) |
| E-M4 | **primario** — generalización |
| E-M5 | no evaluada |

---

## 9. Sello

| | |
| - | - |
| Congelado | **SÍ** |
| Selector | **v0.1 sin tocar** |
| Prohibido | Rediseñar generadores post-datos; Selector v2 |

---

# FIN — META-E004 PROTOCOL 1.0
