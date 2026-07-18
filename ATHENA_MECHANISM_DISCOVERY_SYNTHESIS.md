# ATHENA — Síntesis de Mechanism Discovery (Phase III)

**Estado:** **SYNTHESIS v2** · MD-068 · MD-071  
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
T-04  REFERENCE_COMPLETE  P*=NONE  INTAKE=NOT_ELIGIBLE
```

### Propiedad sana de la carretera

```text
nueva clase
   ↓
nueva matemática
   ≠
nueva explicación
```

> **La diversidad de mecanismos puede crecer  
> sin que Athena tenga todavía un candidato.**

Eso no es estancamiento: es el **mapa aprendiendo a distinguir terreno**.

---

## 1. Clases ya exploradas (mapa, no colección)

| ID | Representación | Interacción | Dinámica | Estado |
| -- | -------------- | ----------- | -------- | ------ |
| **T-01** | campo binario 1D | vecindad / exclusión por conteo | estocástica (birth continuo) | REFERENCE_COMPLETE |
| **T-03** | campo binario 1D | tabla local \(f\) / Wolfram | determinista (solo init aleatorio) | REFERENCE_COMPLETE |
| **T-04** | **proceso de puntos** | **ninguna local** (gaps i.i.d.) | **renovación** (un barrido) | REFERENCE_COMPLETE |

```text
T-01 → campo binario + interacción local + azar dinámico
T-03 → campo binario + regla determinista + evolución CA
T-04 → proceso de puntos + gaps i.i.d. + renovación
```

### Ejes estructurales (los tres que importan)

| Eje | T-01 | T-03 | T-04 |
| --- | ---- | ---- | ---- |
| **Representación** | campo \(x\in\{0,1\}^N\) | campo \(x\in\{0,1\}^N\) | conjunto \(S\) por renovación |
| **Interacción** | local (vecindad) | local (tabla) | **ausente** (i.i.d.) |
| **Dinámica** | síncrona estocástica | síncrona determinista | **no-CA** (gaps) |

### Matemática típica (sin P\*)

| ID | NECESSARY no trivial (en su mundo) |
| -- | ---------------------------------- |
| T-01 | packing solo si \(p_b=0,\theta=1\); densidad no crece si \(p_b=0\) |
| T-03 | cono de luz; aditividad GF(2) en 90/150; W=0 aniquila |
| T-04 | densidad asintótica \(=q\); \(\mathbb{E}[G]=1/q\); sin campo local |

**Prohibido:** reabrir T-01/T-03/T-04 con “otra pintura” y llamarlo nueva clase.

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

## 4. Cobertura v2 — qué hueco **aportaría** (no “T-05 porque toca”)

### Ya cubierto

| Región | ID |
| ------ | -- |
| Campo binario + estocástico local (conteo) | T-01 |
| Campo binario + CA determinista \(r=1\) | T-03 |
| Proceso de puntos + gaps i.i.d. | T-04 |
| Variantes de params de lo anterior | ola 2 del **mismo** ID, no nueva familia |

### Segundo eje de decisión (post T-04)

> **¿Qué hueco aportaría una nueva representación  
> o una nueva relación estructural  
> que no esté cubierta por T-01, T-03 ni T-04?**

No basta con “el siguiente nombre de la lista”.

### Huecos que **sí** cambiarían el mapa

| ID | Familia | ¿Nueva representación? | ¿Nueva relación estructural? | Notas de diversidad |
| -- | ------- | ---------------------- | ---------------------------- | ------------------- |
| **T-05** | Embedding + umbral | **sí** (\(\mathbb{R}^d\) / distancia) | cercanía métrica, no gap i.i.d. ni CA | Sale de la recta “plana” |
| **T-02** | Hard-core min dist \(d\) | no (sigue siendo conjunto en \(\mathbb{N}\)) | **sí**: exclusión **global** sin birth ni campo evolutivo | Cercano a packing de T-01 N5 pero **sin** dinámica de birth; vigilar R-DIV vs T-04 |
| **T-06** | Memoria finita | estado \(s_t\) extra | **sí**: no Markov-0 en la config sola | Representación ampliada |
| **T-08** | Contacto / infección | campo o marcas | **sí**: frente / umbral epidémico | Dinámica de contagio ≠ exclusión T-01 |
| **T-07** | Capacidad local | campo + cupos | parcial (variante de conteo) | Riesgo de “T-01 con cupo” — exige tabla anti-pintura fuerte |

### Huecos **débiles** (no abrir sin justificación fuerte)

| Tentación | Por qué no |
| --------- | ---------- |
| Otra geométrica / otra \(q\) | T-04 ola 2 |
| Otros \(W\) Wolfram | T-03 ola 2 |
| T-01 con \(p_b=0\) fijo | caso de T-01 N4–N5, no nueva clase |
| “T-04 con gaps markovianos” | ola 2 de T-04 o T-04b con R-DIV explícito |

### Ranking de cobertura (orientativo, **sin apertura automática**)

1. **T-05** — nueva representación (embedding)  
2. **T-06** o **T-08** — nueva relación (memoria / contagio)  
3. **T-02** — solo si se argumenta distancia real a T-04 (conjunto) y a T-01 (packing)  
4. **T-07** — último (riesgo de pintura)

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
REPRESENTACIÓN
  campo binario 1D          proceso de puntos           embedding / memoria
  ─────────────────         ────────────────          ──────────────────
  T-01 ● estocástico        T-04 ● renovación i.i.d.  [ ] T-05
  T-03 ● determinista CA    [ ] T-02 hard-core?       [ ] T-06 / T-08
                            (conjunto, sin campo)

INTERACCIÓN
  local conteo/tabla        ninguna (i.i.d.)          métrica / contagio / cupo
  T-01 · T-03               T-04                      T-05 · T-08 · T-07?
```

La siguiente familia debe **ocupar un hueco de representación o de relación estructural**,  
no densificar un cuadrante ya marcado.

---

## 7. Decisión de síntesis v2

| Acción | ¿Ahora? |
| ------ | ------- |
| T-05 “porque toca” | **no** |
| Otro generador por acumulación | **no** |
| Actualizar mapa de cobertura | **este doc (v2)** |
| Elegir **una** clase en un hueco real | acto **posterior** consciente (MD dedicado) |
| Intake / E008 | **no** |

### Pregunta operativa

**No:**

> ¿Qué mecanismo probamos?

**Sí:**

> **¿Qué hueco de representación o de relación estructural  
> aún no está en el mapa T-01 · T-03 · T-04?**

### Resultado acumulado

```text
3 clases · 2 representaciones · 3 dinámicas
0 candidatos · 0 P*
```

La diversidad creció. Athena **sigue sin candidato**.  
Eso es progreso del **mapa**, no estancamiento del laboratorio.

---

## Historial

| Fecha | Evento |
| ----- | ------ |
| 2026-07-18 | Síntesis v1 post T-01 + T-03 |
| 2026-07-18 | Síntesis v2 post T-04; segundo eje de huecos; anti T-05-por-tocar |

---

# FIN — MECHANISM DISCOVERY SYNTHESIS

*Tres puntos firmes.  
El mapa distingue terreno.  
El siguiente ladrillo debe cambiar el mapa, no el conteo de vehículos.*
