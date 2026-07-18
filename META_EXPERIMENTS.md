# META-E — Investigar el laboratorio (no ampliarlo)

**Fase del proyecto:** **investigación del laboratorio** (no invención de arquitectura)  
**Objeto:** el **kernel**, como objeto experimental de pleno derecho  
**Régimen:** el **mismo** que E004.2 (pregunta, H, rival, protocolo, métricas, muerte, residual, decision log)  
**No:** formato especial “porque es meta” · no “validar” en sentido confirmatorio  

---

## Jerarquía (simetría instrumento / objeto)

> **Todo en el laboratorio puede morir, excepto el principio rector.**

| Capa | Régimen |
| ---- | ------- |
| Principio rector | Estable |
| Kernel | **Falsable** — sin privilegio por haber sido diseñado primero |
| Programas (Athena, …) | Falsables |
| Hipótesis | Falsables |

**Regla corta:**

> El kernel **nunca** obtiene privilegios epistemológicos por haber sido diseñado primero.

Si META-E demuestra que una parte empeora la investigación → **sale**.

**Lenguaje:** no “validar el lab” → **investigar el lab**  
Finales admisibles: mejora · no mejora · **no sabemos**.  
Derrota del kernel = **éxito del régimen** si el protocolo se respetó.

### Modelo de evidencia (obligatorio)

`META_EVIDENCE_MODEL.md` — tipos **E-M1…E-M5**.  
Todo META-E reporta un **perfil de evidencia**, no un eslogan.

| Tipo | Pregunta breve |
| ---- | -------------- |
| E-M1 | ¿Cumple sus reglas? |
| E-M2 | ¿Reduce coste metodológico? |
| E-M3 | ¿Reduce errores? |
| E-M4 | ¿Generaliza? |
| E-M5 | ¿Resiste modificaciones? |

**Mejora local ≠ mejora del laboratorio.**

### Tres capas de trabajo

| | |
| - | - |
| Principio rector | Brújula |
| Investigación del lab (META-E) | Produce evidencia E-M* |
| Ingeniería del lab | Implementa lo que META-E legitimó; **no** crea conocimiento por sí sola |

> **El código nunca crea conocimiento; únicamente ejecuta un régimen de investigación.**

---

## Cambio de fase

| Hasta ahora | A partir de ahora |
| ----------- | ----------------- |
| Invención de arquitectura | **Investigar** el laboratorio |
| ¿Qué pieza falta? | ¿El kernel mejora / no / no sabemos? |
| Ampliar | **Protocolos META-E** como E004.x |

Dos objetos científicos **separados**: (1) fenómeno de dominio, (2) el laboratorio.

---

## Modularidad epistemológica (ya ganada)

| Capa | Se puede cambiar… |
| ---- | ----------------- |
| Principio rector | …casi nunca (brújula) |
| Kernel | …con evidencia meta (falsable) |
| Programas (Athena, …) | …sin tocar el kernel |

Separados: un cambio en uno no rompe los otros.

---

## Advertencia (filtro de nuevas piezas)

Ante una “buena idea” de componente:

**No:** ¿Es una buena idea?  
**Sí:** ¿Qué **hipótesis metodológica** intenta poner a prueba?

Si no responde → **no** pertenece al kernel (como mucho, al programa de dominio o a un experimento).

---

## Familia de experimentos META-E

Mismo espíritu que E004.x en PEP-D: **una pregunta por campaña**, protocolo, métricas de **proceso**.

### META-E001 — Separación de funciones

| | |
| - | - |
| **Pregunta** | ¿La separación de funciones reduce errores metodológicos / mejora economía con integridad? |
| **Protocolo** | `META-E001/META_E001_PROTOCOL.md` **0.1-DRAFT** (mismo rigor E004.2) |
| **Estado** | **CERRADO** — `META_E001_REPORT.md` · E-M2 fuerte bajo este control; E-M3 insuficiente |
| **Decision log** | MD-013 |

### META-E002 — Economía del Selector (parcialmente absorbida)

| | |
| - | - |
| **Pregunta** | ¿El Selector mejora la economía experimental? |
| **Estado** | Evidencia **E-M2 fuerte** bajo META-E001 (mismo eje); no reabrir como duplicado |
| **Límite** | No mide calidad científica ni sesgo |

### META-E002b — Atacar la selección, no mejorarla (**siguiente**)

| | |
| - | - |
| **Objeto** | Hipótesis **sobre el instrumento** (Selector v0.1), no un fenómeno de dominio |
| **Régimen** | Mismo que E004.2: *¿esta mejora aparente sobrevive cuando intento encontrar qué la destruye?* |
| **Pregunta central** | ¿La reducción de coste viene de **eliminar ruido** o de **eliminar diversidad**? |
| **No preguntar** | “¿El Selector es bueno?” / máquina de aciertos |
| **Modelo de error** | Falso positivo (incluir de más → cuesta presupuesto) · **falso negativo** (excluir de más → puede matar una línea antes de defenderse; **más peligroso**) |
| **Trampa numérica** | 20→3 puede ser Mundo A (ruido fuera, misma cobertura) o Mundo B (raros fuera, ceguera); el número es igual, el significado opuesto |
| **Salida preferida** | **Mapa de validez**, no solo aceptado/rechazado (dónde sirve / limitado / no recomendado) |
| **No es** | Selector v2 · coronar · “el lab ve más claro” sin medir “ve menos” |
| **Estado** | **CERRADO** — `META_E002b_REPORT.md` · H-00 diversidad · legislación actualizada |

**Legislación:** `LEGISLATION_SELECTOR_v0_1.md` — **soportado con limitaciones** (no muerto, no general).

### META-E003 — Valor del Auditor

| | |
| - | - |
| **Pregunta** | ¿El Auditor detecta corrupción que un humano (o el Core solo) pasaría por alto? |
| **Diseño** | Inyectar corrupciones (post-hoc, borrado de muerta) con/sin auditor |
| **Métricas** | Tasa de detección FAIL, falsos positivos sobre NO_SABEMOS |
| **Estado** | Tests de auditor (casos A/B/C) = **evidencia unitaria**; falta campaña formal vs “humano ciego” |
| **Artefacto** | `tests/test_athena_auditor_core.py` |

### META-E004 — Generalización del Selector (**prioridad #1**)

| | |
| - | - |
| **Pregunta** | ¿La ceguera de diversidad es **general** o artefacto del generador E002b? |
| **Poder** | Reinterpreta E002b: sobreajuste vs propiedad estructural del filtrado |
| **Pregunta doc** | `META-E004/META_E004_PREGUNTA.md` |
| **Estado** | **CERRADO** — `META_E004_REPORT.md` · H-01 transversal · H-00 debilitada |
| **No es** | Selector v2 |

### META-E003 — El guardián vigilado (**prioridad #1 ahora**)

| | |
| - | - |
| **Pregunta** | ¿Hay fallos que atraviesan el Auditor porque **comparten sus supuestos**? (puerta en la pared equivocada) |
| **También** | Escala: ¿sigue viendo grietas cuando hay muchas decisiones? |
| **No** | “¿Funciona el Auditor?” (unitario ya sí) |
| **Pregunta doc** | `META-E003/META_E003_PREGUNTA.md` |
| **Estado** | **CERRADO** — `META_E003_REPORT.md` · forma fuerte · semántica limitada |

### META-E004-kernel (legado / opcional)

Estabilidad del **kernel** (API/estados) cross-domain — distinta de E004-Selector; no confundir.

### META-E005 (futuro) — Valor emergente M3/M4

| | |
| - | - |
| **Pregunta** | ¿Crítico + pipeline completo superan M2 en robustez? |
| **Requisito** | Implementar Crítico/Diseñador **solo** si esta hipótesis metodológica lo exige |
| **Estado** | No abrir hasta tener resultados de E001–E004 o necesidad clara |

---

## Qué no se hace en esta fase

- Nuevos roles en el kernel “porque suenan bien”  
- LLM por defecto  
- Ampliar arquitectura sin META-E que lo justifique  
- Confundir éxito meta con descubrimiento matemático  

---

## Logro ya comprobable (sin Goldbach correcto)

El proyecto puede **evaluar su propia forma de investigar** sin depender de que una hipótesis matemática concreta sea verdadera.

Ese **desacoplamiento** es la mejor protección contra el sesgo que se quería evitar desde el primer día:  
que el deseo de tener razón modifique el instrumento con el que se averigua si se tiene razón.

---

## Estado

```text
Invención de arquitectura     →  pausa deliberada
Validación del laboratorio    →  programa activo (META-E)
META-E002                     →  evidencia inicial (Selector)
META-E001, E003, E004         →  abiertos / a formalizar
```

---

# FIN — META EXPERIMENTS

*Medir el lab. No ampliarlo por impulso.  
La disciplina experimental empieza en casa.*
