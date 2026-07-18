# META-E002b — Pregunta (pre-protocolo)

**Estado:** pregunta fijada · **no** protocolo · **no** ejecución · **no** Selector v2  
**Objeto:** Selector v0.1 como **hipótesis sobre el instrumento**  
**Régimen:** el de E004.2 (destruir la mejora aparente), no “mejorar el Selector”  

---

## Pregunta central

> ¿La reducción de coste del Selector viene de **eliminar ruido** o de **eliminar diversidad**?  
> (¿Qué tipo de **compresión** está haciendo?)

Externamente idéntico:

```text
20 ataques → 3 ataques
```

| A) Compresión de ruido | B) Compresión de diversidad |
| ---------------------- | --------------------------- |
| Menos pruebas inútiles | Menos caminos explorados |
| Cobertura conservada | Pérdida de posibilidades |
| | Ceguera elegante |

Superficie idéntica · estructura interna opuesta.

---

## Modelo de error del filtro

```text
Selector
  incluye  → acierto | falso positivo  (cuesta presupuesto)
  excluye  → acierto | falso negativo  (puede matar una línea a destiempo)
```

El **falso negativo** es el más peligroso para el lab.

### Dos salidas del Selector (zona crítica = la segunda)

```text
Candidatos iniciales → Selector
        ├── Conservados (evaluados)     ← la mayoría de sistemas solo mira aquí
        └── Excluidos   (no evaluados)  ← META-E002b estudia esto
```

### Fallo silencioso

| Visible | Silencioso |
| ------- | ---------- |
| FP: eligió una mala hipótesis | FN: **nunca** dejó evaluar una que debía llegar |

El segundo **desaparece del registro** salvo que el experimento mire la **zona excluida**.

### Pregunta experimental profunda

> ¿La frontera del Selector separa **ruido de señal**, o separa **lo conocido de lo desconocido**?

Un filtro puede ser excelente con patrones familiares y fallar justo donde empieza la exploración real.

### Tensión economía / cobertura

Objetivo conceptual: \(\text{economía} + \text{cobertura}\).  
Aumentar una suele reducir la otra.  
**No** maximizar la reducción: 99 % puede ser peor que 50 % si destruye diversidad necesaria.

### Control oculto (diseño de campaña, cuando se congele)

```text
Explorador genera 100
Selector ve todos → prioriza 20
Una muestra de los 80 excluidos se evalúa después (el Selector no “sabe” el control)
Comparación: ¿qué características tienen los que el filtro tiende a perder?
```

No para que los excluidos “ganen”.  
Para que el lab vea sus **puntos ciegos**.

### Lectura fuerte del resultado

**No:** “El Selector acertó X veces” ni solo “presupuesto ahorrado = 85 %”.  
**Sí:** perfil — economía · cobertura · pérdidas · dependencia · reversibilidad · mapa de validez.

Un buen filtro no solo filtra “bien”: **revela el precio de su eficiencia**.

---

## Simetría con E004.2

| E004.2 | META-E002b |
| ------ | ---------- |
| ¿La estructura aparente sobrevive al intentar **destruirla**? | ¿La mejora aparente sobrevive al buscar **qué la destruye**? |
| Objeto: hipótesis matemática | Objeto: hipótesis sobre el **instrumento** |

Misma brújula. Distinto objeto.

---

## Salida deseada (ficha, no medalla)

```text
Selector v0.1
  Beneficio observado:     …
  Coste epistemológico:    …
  Tipos de candidatos afectados: …
  Casos donde falló:       …
  Casos donde ayudó:       …
  Reversibilidad:          …
  Mapa de validez:
    Aceptado:      …
    Limitado:      …
    No recomendado: …
  Estado: ACEPTADO_BAJO_LIMITES | RECHAZADO | NO_SABEMOS
```

En la puerta:

> Si el Selector tiene razón demasiado rápido, ¿qué está dejando de ver?

---

## Siguiente

Protocolo congelado (cuando se abra) → ejecución → evidencia → decisión.  
**No** construir Selector v2 antes.

---

# FIN — META-E002b PREGUNTA
