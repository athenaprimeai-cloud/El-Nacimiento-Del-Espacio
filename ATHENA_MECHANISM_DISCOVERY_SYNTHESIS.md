# ATHENA — Síntesis de Mechanism Discovery (Phase III)

**Estado:** **SYNTHESIS** · MD-068  
**Fecha:** 2026-07-18  
**No es:** nuevo generador · Intake · P\* · explicación de S-004…S-006  

---

## Conclusión hasta ahora

> **La generación ciega de mecanismos produce matemática real,  
> pero la matemática real no produce automáticamente  
> una hipótesis sobre Athena.**

Eso es exactamente lo que Phase III debía comprobar.

```text
T-01  REFERENCE_COMPLETE  P*=NONE  INTAKE=NOT_ELIGIBLE
T-03  REFERENCE_COMPLETE  P*=NONE  INTAKE=NOT_ELIGIBLE
```

---

## 1. Clases ya exploradas

| ID | Clase dinámica | Naturaleza de la generación | Estado |
| -- | -------------- | --------------------------- | ------ |
| **T-01** | Ocupación + exclusión local + birth | **Estocástica** (init + births cada paso) | REFERENCE_COMPLETE |
| **T-03** | Autómata elemental Wolfram \(r=1\) | **Determinista** (init aleatorio → trayectoria única) | REFERENCE_COMPLETE |

### Diferencia real (no cosmética)

```text
T-01:  estado → regla + azar continuo → estado siguiente
T-03:  estado inicial → regla fija f → trayectoria única
```

| Eje | T-01 | T-03 |
| --- | ---- | ---- |
| Azar en la transición | sí (\(p_{\mathrm{birth}}\)) | no |
| Forma de la regla | umbral de conteo \(\theta\) | tabla booleana / código \(W\) |
| Consecuencias típicas | empaquetamiento **solo si** \(p_{\mathrm{birth}}=0\) | cono de luz; aditividad GF(2) en 90/150 |
| Extinción global trivial | solo N1 (saturación de vecinos) | \(W=0\) en un paso |

**Prohibido en el futuro:** reabrir T-01/T-03 con “otra pintura”  
(otro \(\theta\), otra lista \(W\)) y llamarlo **nueva clase**.

---

## 2. Tipos de consecuencias necesarias producidas

### Por familia

| Familia | NECESSARY (cartografía) | ¿Trivial para P\*? |
| ------- | ----------------------- | ------------------ |
| T-01 | N1–N3 locales; **N4** densidad↓ si \(p_b=0\); **N5** packing si \(p_b=0,\theta=1\); **N7** birth rompe packing | N1–N3 sí; N4–N5 no triviales **en el mundo T-01**, no como P\* Athena |
| T-03 | N1–N3; **N4** quiescencia \(f(000)=0\); **N5** cono de luz; **N7** superposición XOR | N1/N4/N6 triviales; N3/N5/N7 estructura de clase CA |

### Taxonomía de **tipos** de consecuencia (meta-nivel)

| Tipo | Ejemplo | ¿Emergió? |
| ---- | ------- | --------- |
| **Local-branch** | “si ns≥θ entonces muere” | sí (T-01 N1–N3) |
| **Parametric fixed-point** | “si \(p_b=0\) densidad no crece” | sí (T-01 N4) |
| **Parametric packing / hard geometry** | gap ≥ r+1 bajo \(\theta=1,p_b=0\) | sí (T-01 N5) |
| **Global null rule** | W=0 ⇒ cero | sí (T-03 N1) |
| **Light-cone / causality** | dependencia en bola de radio T | sí (T-03 N5) |
| **Algebraic linearity** | XOR / GF(2) | sí (T-03 N3/N7) |
| **Anti-theorem (boundary of necessity)** | birth síncrono rompe packing | sí (T-01 N7) |
| **Necessary bridge to Athena S-00x** | “luego S-004…” | **NO** |
| **Sellable P\* (future measurement)** | apuesta peligrosa pre-datos | **NO** |

---

## 3. Tipos de P\* que **no** han emergido

Registro explícito (para no reescribir la historia):

| Tipo de P\* ausente | Significado |
| ------------------- | ----------- |
| P\*-A | Predicción sobre **primos / Goldbach / \(M_2\)** bajo protocolo Athena |
| P\*-B | Predicción sobre **rueda W=30 / Cramér** sin contrabando |
| P\*-C | Predicción de **orden \(S(1)>S(2)>S(6)>S(30)\)** desde un ℳ ciego |
| P\*-D | Predicción de **estabilidad bajo cambio de N** (estilo E007) desde ℳ |
| P\*-E | Cualquier apuesta **cuantitativa sellable** que no sea tautología de la regla |

**Hecho Phase III:** dos vehículos ciegos → **cero** P\* de Intake.

Eso **no** es fracaso del generador: es información sobre la distancia entre  
“matemática del mecanismo” y “hipótesis sobre el historial Athena”.

---

## 4. Clases de la taxonomía **aún sin explorar**

| ID | Familia (taxonomía) | Región del espacio | ¿Por qué aportaría diversidad? |
| -- | ------------------- | ------------------ | ------------------------------ |
| **T-02** | Hard-core / min dist \(d\) | Geometría de exclusión **global** (no birth síncrono) | Distinto de T-01 (sin \(p_b\)) y de T-03 (sin tabla \(f\)) |
| **T-04** | Renovación / gaps paramétricos | Proceso de **puntos en la recta** por ley de gaps | Genera conjuntos sin dinámica de vecindad binaria |
| **T-05** | Embedding + umbral | Geometría en \(\mathbb{R}^d\) / distancia | Aristas/ocupación por **métrica embebida**, no CA ni exclusión 1D pura |
| **T-06** | Memoria finita | Estado interno \(s_t\) | Dinámica **no Markov de orden 0** en la config sola |
| **T-07** | Capacidad local (cupos) | Conteo en ventanas con capacidad | Distinto de umbral de muerte T-01 |
| **T-08** | Contacto / infección 1D | Propagación epidémica | Frente de onda / umbral epidemiológico |

### Regiones ya “cubiertas” (no re-explorar como “nueva clase”)

| Región | Cubierta por |
| ------ | ------------ |
| Markov local estocástico en la línea con conteo | T-01 |
| CA binario determinista radio 1 | T-03 |
| Variantes de lista \(W\) o de \((r,\theta,p_b)\) | **ola 2 del mismo ID**, no nueva familia |

---

## 5. Restricciones que debe cumplir una **nueva** familia

Para aportar **diversidad real** (no estacionamiento de vehículos):

### R-DIV-1 — Distinta naturaleza de generación

Debe diferir de T-01 **y** T-03 en al menos un eje estructural:

| Eje | T-01 | T-03 | Nueva familia debe… |
| --- | ---- | ---- | ------------------- |
| Estocasticidad de transición | sí | no | no copiar el mismo patrón sin cambio de objeto |
| Objeto de regla | conteo de vecinos | tabla en \(\{0,1\}^{2r+1}\) | otro tipo de regla (gaps, embedding, estado interno, …) |
| Espacio de estado | config binaria 1D | config binaria 1D | **preferible** salir de “solo bits en la línea”, o justificar por qué la misma base aporta eje nuevo (p.ej. T-02 hard-core **global** sin birth) |

### R-DIV-2 — Declaración anti-pintura

El documento de spec debe incluir una tabla:

```text
Por qué NO es T-01:
Por qué NO es T-03:
```

Si no se puede llenar con honestidad → **no abrir**.

### R-DIV-3 — Ceguera

Igual que T-01/T-03: no leer SURVIVORS, E00x, ni raw/analysis de familias previas  
**salvo** las restricciones de diversidad de **este** documento y MD-035.

### R-DIV-4 — Un solo vehículo a la vez

No abrir T-04 y T-05 en paralelo.  
Tras síntesis: **una** clase nueva, spec cerrada, luego código.

### R-DIV-5 — Criterio de éxito de Phase III para esa familia

Igual pipeline: raw → propiedades → necessary layer →  
`REFERENCE_COMPLETE` **o** P\* → Intake.  
**Sin** obligación de P\*.

### R-DIV-6 — Uso de TR-01… y TR-03-…

Las restricciones de cartografía de T-01/T-03 sirven para:

- **no** redescubrir “packing under no birth” y llamarlo nuevo;  
- **no** redescubrir “W=0 dies” y llamarlo nuevo;  

**No** sirven para ajustar la regla de la nueva familia a “parecerse a los primos”.

---

## 6. Mapa de cobertura (visual)

```text
                    determinista
                         │
            T-03 ●       │
           (CA 1D)       │
                         │
   ──────────────────────┼──────────────────────  config binaria 1D
                         │
            T-01 ●       │
         (excl+birth)    │
                         │
                    estocástico

        [ hueco: hard-core global T-02 ]
        [ hueco: proceso de gaps T-04 ]
        [ hueco: embedding T-05 ]
        [ hueco: memoria / infección T-06/T-08 ]
```

La siguiente familia debe **ocupar un hueco**, no densificar el cuadrante ya marcado.

---

## 7. Decisión de síntesis (congelada aquí)

| Acción | ¿Ahora? |
| ------ | ------- |
| Otro generador arbitrario | **no** |
| Documento de síntesis | **este** |
| Elegir **una** clase nueva (T-02/T-04/T-05/…) | **después** de este doc, en MD dedicado |
| Intake / E008 | **no** |

### Pregunta operativa de aquí en adelante

**No:**

> ¿Qué mecanismo probamos?

**Sí:**

> **¿Qué región del espacio de mecanismos todavía no hemos cartografiado?**

---

## 8. Candidatos a “única clase nueva” (solo ranking de cobertura, no apertura)

| Prioridad de cobertura | ID | Motivo breve |
| ---------------------- | -- | ------------ |
| 1 | **T-04** | Sale del mundo “bits + vecindad”: genera el **conjunto** por ley de gaps |
| 2 | **T-02** | Geometría de exclusión **sin** birth síncrono (eje distinto a T-01) |
| 3 | **T-05** | Sale de la línea embebida en 1D puro |
| 4 | T-06 / T-08 | Memoria / frentes — más complejos; después |

**Ninguno se abre en este MD.** La elección es el **siguiente** acto consciente, no acumulación.

---

## Historial

| Fecha | Evento |
| ----- | ------ |
| 2026-07-18 | Síntesis post T-01 + T-03; cobertura y R-DIV-1…6 |

---

# FIN — MECHANISM DISCOVERY SYNTHESIS

*Dos puntos firmes en la carretera.  
El siguiente ladrillo aumenta cobertura, no el estacionamiento.*
