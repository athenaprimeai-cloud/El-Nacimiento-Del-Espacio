# ATHENA — AUTOMATION BOUNDARY

**Capa:** criterio de **qué automatizar** · **después** del ciclo de diseño 0–5 · **no** implementación  
**Depende de:** Fases 0–5 (método completo en papel)  
**Programa:** B (Athena)  
**Programa A:** **no** se modifica  

---

## Estado del método

```text
ATHENA — CICLO DE DISEÑO

FASE 0 — Brújula        ✅  define dirección
FASE 1 — Instrumento    ✅  define unidad de investigación
FASE 2 — Exploración    ✅  define terreno
FASE 3 — Ataque         ✅  define resistencia
FASE 4 — Control        ✅  define ejecución interpretable
FASE 5 — Registro       ✅  define memoria permanente

Motor: apagado
Agentes: no creados
Implementación: pendiente
```

```text
                 BRÚJULA
                    ↓
              INSTRUMENTO
                    ↓
              EXPLORACIÓN
                    ↓
                 ATAQUE
                    ↓
                CONTROL
                    ↓
               REGISTRO
                    ↺
              nueva pregunta
```

El **registro no es el final** del ciclo: es lo que permite **continuidad sin repetir errores**.

```text
Conocimiento acumulado
=
éxitos registrados
+
fracasos registrados
+
límites conocidos
```

Un sistema que solo conserva victorias aprende una versión **deformada** del mundo.

---

## Pregunta de ingeniería (correcta)

**No:**

> ¿Cómo hacemos una IA autónoma?  
> ¿Qué puede hacer una IA?

**Sí:**

> ¿**Dónde** aumenta la capacidad de investigación la automatización y **dónde** empieza a **deformar** el proceso científico?  
> ¿Qué parte del ciclo se **delega** sin destruir la capacidad de **fallar correctamente**?

### Separación fundamental

```text
IA puede aumentar:
- velocidad
- cobertura
- comparación
- memoria
- detección de candidatos

IA no decide:
- qué significa una estructura
- qué evidencia "vale más"
- cuándo una hipótesis es verdadera
```

### Regla de diseño (frontera)

> **La automatización puede ampliar el territorio explorado, pero no puede mover la brújula.**

### Orden (inverso al habitual)

```text
Habitual (riesgo):  modelo → capacidades → buscar usos
Athena:             objetivo → método → límites → automatización
```

Eso evita un motor potente **sin** dirección.  
Athena tiene **teoría de límites antes de capacidades**.

---

## Principio de prioridad

Automatizar primero lo **más seguro y útil**, no lo “más inteligente”.

| Prioridad | Criterio |
| --------- | -------- |
| Alta | Amplía capacidad · **no** decide significado · auditable · reversible |
| Baja / prohibida sin freno | Decide estructura · mueve umbrales · reescribe hipótesis · elige evidencia post-hoc |

---

## 1. Alta automatización posible (candidata a primera implementación)

Estas tareas **amplían** capacidad **sin decidir demasiado**.

### Registro

| Tarea | Por qué es segura |
| ----- | ----------------- |
| Crear fichas (plantillas ID) | Estructura, no veredicto |
| Guardar versiones de instrumento | Trazabilidad |
| Comparar resultados bajo mismo marco | Cálculo, no significado |
| Mantener trazabilidad (enlaces padre/hijo) | Memoria, no autoridad |

### Auditoría

| Tarea | Por qué es segura |
| ----- | ----------------- |
| Detectar cambios post-hoc en protocolo/métricas | Protege Fase 4 |
| Verificar cumplimiento de campos obligatorios | Checklist |
| Alertar si falta ataque antes de control | Bloqueo de Fase 3 |

### Exploración inicial (acotada)

| Tarea | Por qué es acotada |
| ----- | ------------------ |
| Generar **candidatos** en formato X/Y/Z/W | Salida de Fase 2, no hallazgo |
| Buscar regularidades **sin** declarar estructura | Señal candidata |
| Enumerar confusiones posibles para el Crítico | Alimenta ataque |

**Tope:** la salida de exploración automatizada es **candidato**, nunca “descubrimiento” ni estado de hipótesis cerrado.

---

## 2. Automatización peligrosa (freno metodológico)

| Acción | Riesgo |
| ------ | ------ |
| Declarar **significado matemático** | Salto estructura/apariencia |
| Decidir que una anomalía **es** estructura | Sobreclaim |
| **Modificar** hipótesis después del resultado | Inmunidad post-hoc |
| **Elegir** qué evidencia importa tras ver datos | Negociación con el dato |
| Cerrar estado “reforzada/muerta” sin control congelado | Salto de fases |
| Borrar o ocultar memoria negativa | Amnesia selectiva |
| Mezclar resultados de instrumento v1 y v2 sin marcar | Falsa continuidad |

Ahí debe existir **freno humano o de protocolo** hasta que el diseño demuestre lo contrario.

---

## 3. Primera forma deseable (no mente autónoma)

La primera versión de Athena con IA **no** debe parecer una mente autónoma.  
Debe parecer un **laboratorio con asistentes especializados**:

```text
IA (Explorador):
"Encontré 37 candidatos."

IA (Crítico):
"35 tienen explicación por borde o método."

IA (Diseñador):
"Estos 2 tienen controles posibles."

Humano:
"¿Ejecutamos?"

Sistema (Archivista):
"Registro creado."
```

| Principio | |
| --------- | - |
| La inteligencia está en el **circuito** | No en un agente individual |
| Explorar + atacar + controlar + registrar | Equilibrio de la brújula |
| El humano (u otro freno) autoriza gasto de Control serio | Hasta que la automatización de Control esté acotada |

---

## 4. Orden de implementación sugerido (cuando se active)

```text
1. Registro + plantillas + trazabilidad
2. Auditoría de cumplimiento de protocolo
3. Explorador de candidatos (formato estricto)
4. Crítico asistido (ataques propuestos, no veredictos finales)
5. Diseñador de controles (borradores)
6. Solo después: automatización parcial de ejecución
7. Nunca primero: "oráculo de significado"
```

Cada paso debe pasar el filtro:

> ¿Puede el sistema seguir **equivocándose** y **registrar** la derrota?

Si la automatización **impide** la muerte de hipótesis → **no** se implementa.

---

## 5. Qué no se hace todavía

- Implementar agentes  
- Encender motor de exploración masiva  
- Declarar que Athena “ya es autónoma”  
- Tocar PEP-D desde B  
- Sustituir Fase 0–5 por un framework de agentes genérico  
- Empezar arquitectura desde “lo que el modelo actual puede hacer”  

---

## Arquitectura de agentes (diseño)

```text
ATHENA_AGENT_ARCHITECTURE.md  ✅  diseño mínimo
Pregunta: componentes sin juez absoluto / sin auto-coronación
Nace de: brújula + método + esta frontera
Estado: diseño · no implementación · motor apagado
```

---

## Estado canónico

```text
ATHENA

Brújula:                    ✅ instalada
Método Fase 0–5:            ✅ diseñado
Frontera de automatización: ✅ definida
Motor:                      apagado
Agentes:                    no creados
```

```text
Mapa: listo
Reglas: listas
Frontera: definida
Máquina: todavía apagada
```

Ahora sí existe un **lugar desde donde construir**.  
Sin prisa por encender el motor.

---

# FIN — ATHENA AUTOMATION BOUNDARY

*La automatización amplía territorio. No mueve la brújula.*
