# ATHENA — PHASE 6 GATE (transición)

**Capa:** transición diseño → implementación · **no** Fase 6 completa · **no** agentes · **no** “cerebro Athena”  
**Riesgo que evita:** catedral de planos sin primera piedra  
**Riesgo que también evita:** máquina antes de demostrar control  
**Programa:** B (Athena)  

---

## Pregunta de este documento

> ¿Qué **evidencia mínima** demostraría que Athena puede **implementarse** sin perder la capacidad de decir **«no sabemos»**?

Aquí se deja de solo diseñar la nave.  
Se define el **primer tornillo** y cómo saber si sujeta.

---

## Estado de partida

```text
Diseño (NIVEL 1–3)     ✅  terminado
FASE 6 completa        ⏳  no abierta
Implementación         ❌  no iniciada
Motor                  apagado
Agentes                no creados
```

La pregunta correcta **ya no** es “¿hacemos agentes?” ni “¿encendemos todo?”.

Es:

> ¿Cuál es la **pieza mínima** que demuestra que el método puede **vivir en una máquina** sin perder sus propiedades?

---

## Qué es este Gate (y qué no)

| Es | No es |
| -- | ----- |
| Transición **FASE 6-GATE** | Implementación completa de Athena |
| Criterio de evidencia mínima | Enjambre de agentes |
| Autorización a construir el **núcleo de protocolo** si se acepta | Explorador IA / auto-mejora |
| Prueba de **fidelidad del ciclo** | Demostración de inteligencia |

```text
FASE 6-GATE
(no implementación todavía de agentes ni lab completo)

Objetivo:
demostrar que el ciclo Athena puede representarse y auditarse.
```

---

## Regla de transición (heredada)

```text
Posible ≠ Permitido
Permitido = verificable + compatible con la brújula
```

No se enciende una capacidad porque sea posible.  
Se enciende porque existe un modo de saber si **ayuda** o **deforma**.

---

## Evidencia mínima exigida (criterio de PASS del Gate)

El Gate se considera **superado** solo si existe (o se ha construido y demostrado) un sistema **mínimo** que:

| # | Evidencia |
| - | --------- |
| 1 | Representa **Pregunta → Ficha/Hipótesis → Predicción → Forma de morir → Control → Estado → Registro** |
| 2 | Puede emitir y **conservar** estado **«no sabemos» / indeterminada** como salida de primera clase |
| 3 | Puede registrar **hipótesis muerta** con razón y **no** borrarla |
| 4 | **Rechaza** o marca violación si se intenta cambiar predicción/umbrales post-resultado |
| 5 | **No** requiere modelo de IA para existir |
| 6 | Pasa un subconjunto crítico de failure tests (al menos FT-01, FT-02, FT-03, FT-04, FT-08 en forma ejecutable o checklist forzada) |

Si falta cualquiera → Gate **no** PASS · no se sube a agentes ni a exploración masiva.

### Primera victoria (misma de siempre)

**No:** “Athena descubrió algo.”  
**Sí:** “Esta hipótesis **murió correctamente** y quedó **archivada**.”  
(o: “El ciclo cerró en **no sabemos** y quedó archivado.”)

Si Athena no puede hacer eso con una hipótesis **pequeña**, no podrá con Goldbach, Riemann u otro problema grande.

---

## Primer paso tras PASS del Gate: ATHENA_CORE_PROTOCOL

**No IA. No agentes. No descubrimiento.**

Solo:

```text
Pregunta
   ↓
Crear hipótesis
   ↓
Definir predicción
   ↓
Registrar posible muerte
   ↓
Registrar control
   ↓
Cerrar estado
```

Probar únicamente:

> ¿La disciplina Athena puede existir como **estructura ejecutable**?

### Ejemplo de entrada (el sistema no opina)

```text
Hipótesis:   H-001
Pregunta:    ¿Existe una diferencia medible entre A y B?
Predicción:  Si H es cierta, ocurre X.
Muerte:      Si ocurre Y, H pierde soporte.
```

El núcleo **obliga** a que el proceso exista.  
No genera la matemática.

---

## Ruta de construcción (orden fijo)

```text
PASO 0   Gate de Fase 6          ⬅ este documento
              ↓
PASO 1   Núcleo de protocolo     (ATHENA_CORE_PROTOCOL · sin modelos)
              ↓
PASO 2   Auditor automático      (violaciones de protocolo, no matemáticas)
              ↓
PASO 3   Generador de candidatos (IA opcional, salida solo candidatos)
              ↓
PASO 4   Crítico IA              (ataques, no veredictos finales)
              ↓
PASO 5   Ciclo experimental real
```

**No** se salta a PASO 3–5 sin PASO 1–2.  
**No** se encienden agentes ni auto-mejora en el primer encendido.

### Auditor automático (PASO 2) — alcance

Busca **violaciones**, no verdades:

```text
¿Se cambió la hipótesis después del resultado?
¿Falta una predicción previa?
¿Existe un control?
¿Se borró una hipótesis muerta?
```

Encaja con la frontera de automatización: seguro y útil, sin decidir significado.

### Explorador IA (PASO 3+) — condición

La IA **no** es la investigadora.  
Es una **herramienta dentro del laboratorio** que ya tiene núcleo + auditor.

---

## Decisiones de este Gate

| Decisión | Valor |
| -------- | ----- |
| ¿Abrir Fase 6 completa ahora? | **No** |
| ¿Abrir FASE 6-GATE? | **Sí** (este doc) |
| ¿Implementar agentes ahora? | **No** |
| ¿Siguiente construcción permitida si se avanza? | Solo **núcleo de protocolo** (PASO 1) |
| ¿PASO 1 autorizado? | **Sí** — `ATHENA_CORE_PROTOCOL.md` + `athena_core/` |
| ¿Criterio de éxito del núcleo? | FT-CORE-01/02/03 PASS; muerte/no sé archivables |

---

## Qué haría “colocar la primera piedra” (cuando se autorice código)

1. Repositorio o módulo mínimo (p.ej. fichas JSON/YAML + CLI o script).  
2. Comandos: crear pregunta, crear hipótesis, registrar control, cerrar estado.  
3. Tests automatizados que implementen FT-01…04 y FT-08 en el núcleo.  
4. Un ciclo de juguete (A vs B sintético) que termine en `muerta` o `no_sabemos`.  
5. **Stop.** Revisar. No añadir IA todavía.

Eso es el tornillo.  
No la nave.

---

## Relación con documentos previos

| Documento | Rol |
| --------- | --- |
| `ATHENA_IMPLEMENTATION_GATE.md` | Criterio de existencia / razón para encender |
| **Este** `ATHENA_PHASE6_GATE.md` | Transición + evidencia mínima + ruta PASO 0–5 |
| (futuro) Core protocol | Estructura ejecutable sin IA |
| Failure tests | Qué debe PASS el núcleo |

---

## Estado

```text
PASO 1 ATHENA_CORE_PROTOCOL   ✅  FT-CORE PASS
PASO 2 ATHENA_AUDITOR_CORE    ✅  Casos A/B/C PASS
PASO 3+ IA                    ❌
Motor científico              apagado
```

Núcleo impone disciplina. Auditor la **vigila** sin ser juez científico.

---

# FIN — ATHENA PHASE 6 GATE

*Evidencia mínima: el ciclo vive en máquina y aún puede decir no sabemos.  
Primera piedra: protocolo, no IA.*
