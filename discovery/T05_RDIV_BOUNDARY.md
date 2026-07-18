# T-05 — Frontera R-DIV (antes de la regla)

**Estado:** **BOUNDARY CONGELADA** · MD-072  
**Fecha:** 2026-07-18  
**Siguiente:** `ATHENA_T05_REFERENCE_GENERATOR.md` solo si esta frontera se sostiene  

---

## Por qué T-05 (y no “el siguiente número”)

Hasta ahora:

```text
T-01 / T-03 → x : ℕ → {0,1}     (campo sobre la recta)
T-04         → S ⊂ ℕ             (puntos por gaps en la recta)
```

T-05 debe abandonar la **geometría lineal como soporte primario**:

```text
T-05 → puntos embebidos en ℝᵈ
            ↓
      distancia métrica
            ↓
      regla de selección
            ↓
         conjunto S (etiquetas)
```

Pregunta de la spec:

> **¿Qué sucede cuando la relación fundamental deja de ser  
> “quién está al lado de quién” y pasa a ser  
> “a qué distancia se encuentran”?**

---

## T-05 **no puede ser**

| Prohibición | Motivo |
| ----------- | ------ |
| T-01 con coordenadas reales añadidas | Decoración: la dinámica seguiría siendo vecindad ordinal |
| T-04 con una distancia cosmética | Gaps en \(\mathbb{N}\) disfrazados de \(\|\cdot\|\) |
| Proyección de enteros que conserve la estructura ordinal | Misma geometría de línea embebida (p.ej. \(i\mapsto (i,0)\)) |
| Métrica diseñada para reproducir geometría Athena / supervivientes | Post-hoc / contrabando (P2, espíritu intake) |
| Embedding generado desde propiedades de E004–E007 | Diseñar para el contrato = retrospectiva |
| “T-03 en un grafo geométrico” sin regla generativa propia | Pintura de CA sobre aristas métricas sin cambiar el objeto |

### Frase de control

> Si T-05 se puede describir honestamente como  
> “T-01/T-03/T-04 **con** coordenadas / distancia / proyección…”,  
> **no es T-05**.

---

## T-05 **debe** cambiar realmente

| Eje | T-01 / T-03 / T-04 | **T-05** |
| --- | ----------------- | -------- |
| Soporte | recta discreta \(\mathbb{N}\) | **espacio métrico** \(\mathbb{R}^d\) (caja acotada) |
| Relación primaria | vecindad / \(f\) / gaps en \(\mathbb{N}\) | **distancia euclídea** (u otra métrica fija en spec) |
| Objeto | ocupación o puntos ordenados en la línea | **configuración geométrica** \(\{X_i\}\subset\mathbb{R}^d\) |
| Selección | regla sobre \(\mathbb{N}\) | **umbral / interacción métrica** sobre \(\|X_i-X_j\|\) |
| Información | ordinal / local en la línea | **geométrica** (posiciones + distancia) |
| Generatividad | — | la geometría es **generativa**, no decorativa |

### Generativa vs decorativa

| Decorativa (rechazo) | Generativa (admisible) |
| -------------------- | ---------------------- |
| Asignar coords a \(\{1..N\}\) y seguir usando \(|i-j|\) | Muestrear puntos en \(\mathbb{R}^d\); la **única** relación de selección es métrica |
| Embedding monótono de la línea | PPP / Unif en caja; sin orden de \(\mathbb{N}\) en la regla |
| Distancia monótona con \(|i-j|\) | \(\|X_i-X_j\|\) independiente del índice ordinal (salvo etiquetas) |

---

## Declaración anti-pintura (obligatoria)

| | |
| - | - |
| **Por qué NO es T-01** | No hay campo \(x_i\) en \(\mathbb{N}\); no hay \(\theta\) ni birth en vecindad ordinal |
| **Por qué NO es T-03** | No hay tabla \(f\) ni pasos de CA sobre una cadena |
| **Por qué NO es T-04** | No hay gaps i.i.d. sobre la recta; la estructura nace de **posiciones en \(\mathbb{R}^d\)** y un umbral métrico |

---

## Ceguera

No leer: T-01/T-03/T-04 raw o analysis, SURVIVORS, E00x, classification.  
Solo: Phase III, MD-035, esta frontera, spec T-05.

---

## Criterio de “representación realmente nueva”

| Check | ¿OK? |
| ----- | ---- |
| Eliminar las coordenadas hace **imposible** aplicar la regla de selección | debe ser **sí** |
| Reemplazar \(\|X_i-X_j\|\) por \(|i-j|\) produce **otra** familia (no la misma) | debe ser **sí** |
| La ley de los \(X_i\) no codifica la estructura de primos/Athena | debe ser **sí** |

Si algún check falla → **cerrar T-05** sin generador.

**Decisión de frontera (MD-072):** los tres checks se cumplen con el diseño de spec 1.0 (PPP/Unif + hard-core métrico).  
→ **SÍ** a spec 1.0. Generador en paso siguiente, no en este ladrillo de frontera.

---

## Si T-05 no produce candidato

No es tiempo perdido:

> Una tercera representación (métrica genuina) que tampoco basta por sí sola  
> **reduce el espacio de mecanismos posibles**.

Eso mantiene la carretera limpia.

---

# FIN — T-05 R-DIV BOUNDARY
