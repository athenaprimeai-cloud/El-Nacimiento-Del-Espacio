# ATHENA — EXPLORATION DESIGN (Fase 2)

**Capa:** diseño del **espacio de exploración** · **no** búsqueda matemática activa · **no** generación de hipótesis de campaña · **no** código · **no** agentes  
**Depende de:**  
- Fase 0 — `ATHENA_PRINCIPIO_RECTOR.md`  
- Fase 1 — `ATHENA_INSTRUMENT_DESIGN.md`  
**Programa:** B (Athena)  
**Programa A (PEP-D):** **no** se modifica  

---

## Transición de fases

```text
FASE 0 — Dirección
¿Qué buscamos proteger?
        ↓
FASE 1 — Instrumento
¿Qué debe existir para investigar sin perder rigor?
        ↓
FASE 2 — Exploración  ⬅ este documento
¿Qué territorio puede recorrer el sistema y con qué restricciones?
        ↓
FASE 3 — Ataque     ✅ ATHENA_ATTACK_DESIGN.md
FASE 4 — Control    ✅ ATHENA_CONTROL_DESIGN.md
FASE 5 — Registro   ✅ ATHENA_RECORD_DESIGN.md
```

### Condición heredada de Fase 1 (no negociable)

> **No existe “hallazgo” sin ficha, crítico y diseñador.**

Eso evita el fallo clásico de sistemas generativos: **volumen ≠ conocimiento**.

### Pregunta de Fase 2

**No es:**

> ¿Qué hipótesis generamos?  
> ¿Qué patrón encontramos?

**Es:**

> ¿Qué **clase de territorio** matemático puede explorar Athena y qué **restricciones** debe tener para que la exploración produzca **candidatos auditables**?

Primero el **terreno** donde Athena caminará.  
Después el laboratorio hace preguntas.  
**Motor de exploración todavía apagado.**

---

## 1. Entrada

Athena recibe **objetos matemáticos definidos**, no narrativas sueltas.

### Clases de entrada admitidas (catálogo de terreno)

| Clase | Ejemplos (orientativos) |
| ----- | ----------------------- |
| Secuencias numéricas | conteos, particiones, series residuales |
| Residuos / errores | error de Goldbach, restos tras modelo suave |
| Transformaciones | operadores, convoluciones, desingularizaciones |
| Espectros / transformadas | FFT, Laplace, representaciones espectrales |
| Distribuciones | histogramas, medidas empíricas, densidades |
| Grafos / estructuras discretas | si están definidos formalmente |
| Objetos con ficha formal | definición + dominio + parámetros de cálculo |

### Requisitos de cualquier entrada

| Requisito | |
| --------- | - |
| **Definición** | Qué es el objeto (fórmula, procedimiento o referencia) |
| **Dominio** | Rango, malla, truncación, precisión |
| **Procedencia** | Origen de datos o generador reproducible |
| **Parámetros fijos** | Todo lo que no se declara variable experimental |
| **No-afirmación** | La entrada **no** es ya “estructura profunda” |

### Entradas no válidas

- “Algo interesante que vi en un plot” sin objeto definido  
- Conclusiones previas disfrazadas de datos  
- Mezcla opaca Programa A / B (p.ej. reutilizar un outcome de PEP-D como “prueba Goldbach”)  
- Datos sin procedimiento de reproducción  

---

## 2. Operaciones permitidas y prohibidas

### Permitidas (exploración)

| Operación | Propósito |
| --------- | --------- |
| Buscar regularidades | Candidatos, no conclusiones |
| Comparar modelos / transformaciones | Diferencias controlables |
| Generar transformaciones de un objeto de entrada | Ampliar terreno con traza |
| Construir predicciones observables | Preparar ficha de hipótesis |
| Registrar confusiones y artefactos sospechosos | Alimentar al Crítico |
| Proponer rivales explícitas | Material para Ataque |

### Prohibidas (siempre)

| Prohibición | Motivo |
| ----------- | ------ |
| Cambiar métricas porque un resultado no gusta | Retuning post-hoc |
| Redefinir una hipótesis después del resultado | Inmunidad artificial |
| Declarar significado profundo sin control | Salto estructura/apariencia |
| Omitir ficha y pasar a “hallazgo” | Viola Fase 1 |
| Saltar Crítico y Diseñador | Volumen ≠ conocimiento |
| Reescribir umbrales de un control ya ejecutado | Destruye auditabilidad |
| Mezclar victoria de exploración con muerte de rival no intentada | Sesgo de supervivencia |

### Regla de disciplina

La exploración **amplía el conjunto de candidatos**.  
**No** cierra el estado de una hipótesis.  
Cerrar estado = Ataque + Control + Registro (Fases 3–5).

---

## 3. Salida válida

### No es salida válida

> “Encontré un patrón.”  
> “La IA descubrió algo.”  
> “Encaja con la intuición.”

### Sí es salida válida: **Candidato auditable**

```text
Candidato:
  ID:
  Descripción de X:

Evidencia:
  Y:  (qué se observó; dominio; parámetros; reproducibilidad)

Predicción:
  Z:  (qué debería observarse *a priori* si el candidato es serio)

Forma de morir:
  W:  (qué resultado lo invalidaría o debilitaría)

Origen:
  (explorador humano / función / residual / …)

Estado del candidato:
  provisorio — NO es hipótesis cerrada ni hallazgo
```

### Puente a ficha de hipótesis (Fase 1 §2)

Un candidato **puede** promoverse a **hipótesis** solo si se completa la ficha:

```text
ID, Origen, Qué explica, Qué predice, Qué la podría matar,
Qué controles requiere, Estado, Dominio, No-afirmaciones
```

Sin esa promoción formal, el candidato **permanece** en la bandeja de exploración.  
No entra a “investigación” ni a registro de hallazgo.

---

## 4. Criterio de paso a ataque (Fase 3)

Ninguna observación pasa directamente a “investigación concluida”.

```text
Exploración
    ↓
Candidato auditable (§3)
    ↓
¿Ficha de hipótesis completa?  ──no──→  permanece en exploración
    ↓ sí
Crítico intenta destruirlo          (Fase 3)
    ↓
Diseñador propone prueba            (Fase 3/4)
    ↓
Control                             (Fase 4)
    ↓
Registro                            (Fase 5)
```

### Condiciones para salir de Fase 2 hacia Ataque

| Condición | |
| --------- | - |
| Existe al menos un **candidato** en formato §3 | |
| Existe **ficha de hipótesis** (Fase 1) | |
| El Crítico ha dejado por escrito al menos un **ataque** o confusión posible | |
| El Diseñador ha propuesto al menos un **control** con forma de morir **W** operativa | |
| No se ha cambiado la métrica ni la hipótesis post-hoc | |

Si falta cualquiera → **no** hay paso a Ataque.  
Seguir explorando o archivar el candidato como **no promovido**.

---

## Territorio vs campaña

| | Exploración (Fase 2) | Campaña experimental |
| - | -------------------- | -------------------- |
| Objetivo | Generar candidatos auditables | Restringir o matar hipótesis |
| Salida | Candidato / ficha provisional | Estado de hipótesis + registro |
| Motor | **Apagado** en este documento de diseño | Protocolo + ejecución |
| Riesgo | Volumen de patrones | Sobreclaim / inmunidad |

Este documento **diseña el terreno**.  
**No** autoriza una campaña Athena concreta (Goldbach, espectro, etc.).

---

## Relación con Programa A

| | |
| - | - |
| Lecciones de método (muerte de hipótesis, restricción ≠ explicación) | Transferibles |
| Resultados E004.x como “prueba” de estructura aritmética profunda | **Prohibidos** |
| Reutilizar protocolos de A dentro de B | Solo con dominio y no-afirmaciones explícitos |

---

## Qué no se hace en Fase 2 (este documento)

- Ejecutar búsquedas o pipelines  
- Implementar Explorador/Crítico como agentes  
- Generar listas de hipótesis Goldbach “para llenar el terreno”  
- Abrir Fase 3 sin candidatos con ficha  
- Tocar PEP-D, SPEC de A, o E005-A  

---

## Puerta a Fase 3 (Ataque)

**Abierta en diseño:** `ATHENA_ATTACK_DESIGN.md`  
Contrato: misión del Crítico, taxonomía de ataques, resistencia ≠ verdad, prohibición de cambiar reglas.  
Ningún candidato llega a Control sin ataque documentado.

---

## Estado

```text
Brújula:     instalada   (Fase 0)
Instrumento: diseñado    (Fase 1)
Exploración: terreno diseñado (Fase 2 · este doc)
Motor:       todavía apagado
Agentes:     no implementados
```

Eso es exactamente donde debe estar:  
**primero el laboratorio y el terreno; después las preguntas del laboratorio.**

---

# FIN — ATHENA EXPLORATION DESIGN (Fase 2)

*Terreno para caminar. No todavía la marcha.*
