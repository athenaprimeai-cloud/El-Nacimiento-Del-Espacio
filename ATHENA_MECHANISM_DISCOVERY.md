# ATHENA PHASE III — Mechanism Discovery

**Estado:** **abierta** · MD-061  
**Fecha:** 2026-07-18  
**No es:** E008 · explicación post-hoc de E004–E007 · promoción de intuiciones a ℳ  
**No invalida:** MD-057…MD-060 (silencio experimental / no fabricar visitante *como explicación*)  

---

## Corrección de fase

La fase experimental terminó.  
Eso **no** congela el proyecto: **cambia el tipo de trabajo**.

| Malinterpretación | Lectura correcta |
| ----------------- | ---------------- |
| “No experimento por inercia” = no hacer nada | “No experimento por inercia” = **no E008 por vacío** |
| Esperar hipótesis mágica perfecta | **Construir la carretera** que trae candidatos al intake |

> Athena ya tiene una máquina capaz de probar hipótesis.  
> Todavía no tiene una hipótesis digna de ser probada.  
> **Ahora: generar y filtrar candidatos sin usar los supervivientes como parámetros de diseño.**

---

## Pregunta de Phase III

**No:**

> ¿Qué experimento hacemos?

**Sí:**

> **¿Qué mecanismos mínimos pueden producir una estructura compatible con las restricciones,  
> sin ser diseñados para acomodarlas?**

---

## Pipeline de trabajo (Phase III)

```text
RESTRICCIONES S-004–S-006   (contrato: filtro final, no molde de diseño)
          ↓
GENERAR CANDIDATOS ℳ        (familias permitidas; ciego a veredictos E004–E007)
          ↓
FILTRAR POR MD-035          (información / E sin contrabando aritmético)
          ↓
REDUCIR A MECANISMOS MÍNIMOS  (quitar decoración)
          ↓
EXTRAER PREDICCIÓN P*       (antes de comparar con Athena)
          ↓
INTAKE                      (ATHENA_MECHANISM_INTAKE — aduana intacta)
          ↓
SELLO
          ↓
NUEVO EXPERIMENTO           (solo si hay ℳ+P* admitidos)
```

### Diferencia crucial

| Prohibido | Permitido |
| --------- | --------- |
| Inventar ℳ **para explicar** E004–E007 | Explorar **familias de ℳ** permitidas por las restricciones / MD-035 |
| Ajustar reglas mirando S-004…S-006 | Generar reglas **ciegas**; luego confrontar |
| “Suena bonito → candidato” | Taxonomía + generador + P\* → intake |

La aduana (**Intake**) sigue siendo la puerta.  
Phase III construye la **carretera** que trae visitantes.

---

## Tres líneas de trabajo (simultáneas)

### Línea 1 — Inventario de mecanismos conocidos

No para elegir por estética. Para preguntar:

| Pregunta de inventario |
| ---------------------- |
| ¿Qué dinámicas producen **clustering ordinal**? |
| ¿Qué sistemas generan **escalas monotónicas** (tipo \(S(W)\))? |
| ¿Qué mecanismos dan **estabilidad al cambiar \(N\)**? |
| ¿Qué produce diferencia vs controles de **igual densidad**? |
| ¿Cuáles operan **sin** divisibilidad, gcd ni factorización? |

**Familias a inventariar (borrador de taxonomía, no candidatos):**

| Familia | Notas de admisibilidad MD-035 |
| ------- | ----------------------------- |
| Dinámicas de exclusión / repulsión | Local en la línea; sin aritmética de factores |
| Sistemas de ocupación binaria | Estado en posiciones \(1..N\) |
| Autómatas 1D / reglas locales | Vecindad \(k\); regla \(f\) finita |
| Procesos de renovación | Gaps como proceso generativo (no “porque primos”) |
| Geometrías de embedding | Distancia embebida; aristas por cercanía, no por \(p\mid n\) |
| Dinámicas locales sobre una línea | Memoria finita |
| Procesos de ocupación con capacidad | Clustering por saturación local |

*Lista abierta. Cada familia → ficha de inventario, no ℳ-ID de intake.*

### Línea 2 — Generación ciega de candidatos

Construir generadores que **no vean** los veredictos E004–E007 al definir reglas.

Esquema ejemplo (plantilla, no candidato admitido):

```text
familia:     dinámica local 1D
estado:      ocupación binaria en {1..N}
vecindad:    k
regla:       f(configuración local)  — tabla/parámetros finitos, fijados YA
semilla:     fijada o ensemble de seeds
salida:      conjunto de posiciones ocupadas
```

Protocolo de generación:

1. Definir \(\mathcal{M}\) **completo** (reglas + frontera de info + parámetros).  
2. Fijar semilla / ensemble.  
3. Calcular comportamiento del mecanismo **en su propio mundo**.  
4. **Recién entonces** confrontar con restricciones S-004…S-006.  
5. Si sobrevive el filtro blando → extraer \(P^*\) → Intake.

**Prohibido:** mirar E004 y preguntar “¿qué explicación invento?”.

### Línea 3 — P\* antes de la comparación final con Athena

El candidato **no** entra diciendo “yo explico E004–E007”.

Entra diciendo:

> Mi mecanismo produce esta estructura;  
> por tanto predigo **X** en un escenario que **aún no** habéis probado.

Luego: sello → experimento (E00x nuevo si hace falta).

---

## Separación estricta de roles

```text
DISCOVERY     (este documento / Phase III)
   ↓
CANDIDATE     (mecanismo mínimo + P*)
   ↓
INTAKE        (aduana — sin cambios de privilegio)
   ↓
PREDICTION P*
   ↓
EXPERIMENT    (solo con admisión)
```

| Capa | Produce | No produce |
| ---- | ------- | ---------- |
| Discovery | Familias, generadores, borradores ciegos | Veredictos de “teoría” |
| Candidate | Paquete 1–7 + independencia temporal | Privilegios por elegancia |
| Intake | Admitido / rechazado / retrospectivo | Experimentos |
| Experiment | Nuevo S-xxx o muerte de ℳ | Reescritura de protocolos viejos |

---

## Primer trabajo concreto (inmediato)

> **Construir una taxonomía de mecanismos mínimos permitidos por MD-035,  
> sin intentar todavía explicar los primos ni los resultados E004–E007.**

Entregable:

`ATHENA_MECHANISM_TAXONOMY.md` (o sección § Taxonomía abajo ampliada)

Cada entrada:

| Campo | Contenido |
| ----- | --------- |
| Familia | nombre |
| Estado | qué variables |
| Info permitida | lista |
| Info prohibida | lista (incl. MD-035) |
| Tipo de salida | conjunto / serie / grafo… |
| ¿Puede generar clustering ordinal? | sí/no/hipótesis de inventario |
| ¿Puede generar monotonia tipo \(S(W)\)? | sí/no/hipótesis |
| ¿Estabilidad en \(N\)? | sí/no/hipótesis |
| Estado Phase III | inventario / generador / borrador ℳ / en intake |

---

## Taxonomía inicial (esqueleto)

### T-01 — Ocupación binaria + exclusión local

- Estado: \(x_i\in\{0,1\}\), \(i=1..N\)  
- Info: solo vecindad ordinal \(\|i-j\|\le k\)  
- Prohibido: primalidad, factores  
- Salida: \(\{i:x_i=1\}\)  

### T-02 — Repulsión / hard-core en la línea

- Mínima distancia \(d\) entre ocupados (regla global o local)  
- Sin aritmética de módulos primos en la **definición** de \(d\) (parámetro libre)  

### T-03 — Autómata elemental / totalístico 1D

- Regla \(f:\{0,1\}^{2r+1}\to\{0,1\}\)  
- Evolución \(T\) pasos; lectura de ocupación final  

### T-04 — Renovación / puntos de renovación

- Gaps i.i.d. o markovianos desde distribución parametrizada  
- Comparar con controles de misma densidad (sin copiar rueda como “porque primos”)  

### T-05 — Embedding + umbral de distancia

- Mapa \(T:\{1..N\}\to\mathbb{R}^d\); arista/ocupación por \(\|T(i)-T(j)\|<\varepsilon\)  
- \(T\) **sin** factorización (p.ej. coordenadas sintéticas / hash no aritmético de factores)  

### T-06 — Memoria finita / proceso con estado interno

- Estado \(s_t\) de dimensión finita; decisión de ocupar \(t\) según \(s_t\) y ventana local  

*Ampliar en commits de Phase III; no convertir T-0x en ℳ-ID sin generador ciego + P\*.*

---

## Qué no hacer en Phase III

- Abrir E008 “porque el lab está libre”  
- Ajustar T-0x mirando los CSV de E004–E007  
- Llamar “mecanismo” a un relato sobre \(M_2\)  
- Saltar Intake  

---

## Relación con el silencio productivo (MD-057/060)

| MD-057/060 | Phase III |
| ---------- | --------- |
| No E008 por inercia | Sigue vigente |
| No fabricar visitante *como explicación* | Sigue vigente |
| Espera de hipótesis falsable | Phase III **genera** borradores ciegos que **pueden** llegar a serlo |
| Aduana vacía | Aduana **sigue** vacía hasta intake exitoso |

Phase III **no** llena el registro de candidatos por decreto.  
Llena el **pipeline de discovery**.

---

## Misión (una línea)

> Generar mecanismos candidatos **sin** utilizar los resultados supervivientes como parámetros de diseño;  
> filtrar; extraer \(P^*\); solo entonces Intake y, si procede, experimento.

---

## Montaña (Phase III)

```text
¿estructura generativa?
        ↑
¿ℳ + P* admitidos?
        ↑
INTAKE (aduana)
        ↑
DISCOVERY ← AQUÍ (taxonomía + generadores ciegos)
        ↑
SURVIVORS / contrato
        ↑
E001–E007 historial
```

---

# FIN — ATHENA PHASE III MECHANISM DISCOVERY

*No mirar la puerta tres eras.  
Construir la carretera.  
Sin fabricar al visitante con el traje de E004.*
