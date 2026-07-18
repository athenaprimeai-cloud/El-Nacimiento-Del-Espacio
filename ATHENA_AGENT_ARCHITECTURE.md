# ATHENA — AGENT ARCHITECTURE (diseño mínimo)

**Capa:** arquitectura de **componentes** · **no** implementación · **no** motor encendido · **no** agentes desplegados  
**Entrada obligatoria:**  
- Brújula — `ATHENA_PRINCIPIO_RECTOR.md`  
- Método 0–5 — Instrument / Exploration / Attack / Control / Record  
- Frontera — `ATHENA_AUTOMATION_BOUNDARY.md`  
**Programa:** B (Athena)  
**Programa A:** **no** se modifica  

---

## Idea central

> La arquitectura futura **no** parte de las capacidades de la IA.  
> Parte de las **restricciones que protegen el método**.

```text
Objetivo → Método → Límites → Automatización
```

**No:**

```text
Modelo potente → buscar dónde usarlo
```

---

## Pregunta de este documento

> ¿Qué **componentes mínimos** permiten recorrer el ciclo Athena **sin** que **ningún** componente pueda convertirse en **juez absoluto** del conocimiento?

### Salida

Diseño mínimo de roles/componentes **compatibles con el método**.  
No una mente que gobierne el laboratorio.  
Un laboratorio donde **ninguna mente individual** pueda gobernarlo sola.

---

## Estado de partida

```text
ATHENA

Brújula                      ✅ instalada
Método 0–5                   ✅ diseñado
Frontera de automatización   ✅ definida
Arquitectura de agentes      ⬅ este documento (diseño)
Motor                        apagado
Agentes                      no creados
```

---

## 1. Ciclo que la arquitectura debe servir

```text
                 PREGUNTA
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

Ningún componente puede **saltar** fases ni **cerrar** el ciclo en solitario.

---

## 2. Componentes mínimos (herencia de Fase 1)

```text
Explorador
↓
propone candidatos

Crítico
↓
intenta destruirlos

Diseñador
↓
convierte ataques en controles

Auditor
↓
vigila reglas

Archivista
↓
conserva memoria
```

| Componente | Aporta | **No** puede |
| ---------- | ------ | ------------ |
| **Explorador** | Candidatos (X/Y/Z/W) | Declarar hallazgo ni verdad |
| **Crítico** | Ataques, puntos débiles | Falsedad definitiva sin control |
| **Diseñador** | Controles con marco congelable | Ejecutar y reinterpretar a gusto |
| **Auditor** | Detección de post-hoc y saltos de fase | Reescribir la historia a favor de nadie |
| **Archivista** | Memoria (éxitos + muertes + límites) | Coronar por antigüedad |

### Condición arquitectónica

**Ninguno tiene autoridad final.**

```text
No:  Explorador encontró patrón → verdad
No:  Crítico rechazó algo → falso definitivo

Sí:  Cada función aporta presión distinta.
     El conocimiento emerge del ciclo completo.
```

---

## 3. Defensas obligatorias (heredadas)

| Defensa | Origen | En arquitectura |
| ------- | ------ | --------------- |
| Hipótesis puede morir | Brújula / E004.2 | Ningún rol la protege de la ficha |
| No hallazgo sin ficha + crítico + diseñador | Instrumento | Explorador bloqueado sin formato |
| Resistencia ≠ verdad | Ataque | Crítico puede “perder” sin coronar |
| Resultado no modifica protocolo | Control | Diseñador/ejecutor no retunean |
| Memoria ≠ autoridad | Registro | Archivista no es trono |
| Amplía territorio, no mueve brújula | Frontera | Ningún agente reescribe Fase 0 |

---

## 4. La memoria no es un trono

El registro responde:

> ¿Qué **ocurrió** y qué **aprendimos**?

**No:**

> ¿Qué **debemos creer**?

| Registro permite | Registro **no** permite |
| ---------------- | ----------------------- |
| Trazar ciclos previos | “Está archivado → es cierto” |
| Evitar reabrir caminos muertos sin nuevo ID | Blindar una hipótesis “reforzada” |
| Memoria negativa visible | Borrar derrotas |

---

## 5. Interfaces entre componentes (mínimo)

```text
Explorador  →  Candidato(ID, X, Y, Z, W)
Crítico     →  Ataque(ID, tipo, procedimiento, forma de morir)
Diseñador   →  ControlDraft(marco congelable, brazos, umbrales)
[Autorización de ejecución — humano o política de frontera]
Ejecución   →  Resultado(datos + versión instrumento)
Auditor     →  Cumplimiento(sí/no + violaciones)
Archivista  →  Registro(existencia, hipótesis, decisión≠dato, memoria negativa)
```

Sin interfaz tipada (aunque sea en papel) → el componente **no** está listo para implementar.

---

## 6. Quién no existe en esta arquitectura

| No existe | Motivo |
| --------- | ------ |
| Oráculo de significado | Viola frontera |
| Agente único “Athena” que hace todo | Se corona a sí mismo |
| Juez final de verdad | El ciclo es el juez distribuido |
| Borrador de memoria negativa | Amnesia selectiva |
| Puente silencioso A↔B que reinterpreta E004.x como primos | Separación de programas |

---

## 7. Principio arquitectónico (distribución de autoridad)

```text
Ningún componente produce conocimiento final.
El ciclo completo produce evaluación.
```

```text
Explorador  ≠  descubridor
Crítico     ≠  juez final
Diseñador   ≠  confirmador
Auditor     ≠  intérprete
Archivista  ≠  autoridad
```

Cada pieza tiene una **función** y una **limitación**.  
El conocimiento no es el output de un rol; es el **resultado del ciclo**.

---

## 8. Criterio de encendido

```text
ENCENDIDO SOLO SI:

✓ interfaces claras
✓ ningún módulo puede cerrar verdad solo
✓ hipótesis muertas quedan registradas
✓ auditoría puede detener un ciclo
✓ brújula no puede ser modificada por resultados
```

El último punto es crítico:

> Un sistema que puede cambiar su **objetivo** mientras explora no está investigando: está persiguiendo una **recompensa móvil**.

Si falta cualquier ✓ → la máquina **no** se enciende.

---

## 9. Qué no se hace en este documento

- Código, prompts de producción, orquestadores  
- Elegir modelo LLM o framework multi-agente  
- Ejecutar exploración Goldbach “para probar”  
- Sustituir el método por “capacidades del modelo de turno”  

---

## 10. Próxima etapa (si se abre) — ingeniería, no “hacer agentes”

```text
OBJETIVO → MÉTODO → LÍMITES → AUTOMATIZACIÓN → ARQUITECTURA
                                                      ↓
                                          [ implementación futura ]
```

Etapa de ingeniería (diseño):

| Documento | Estado |
| --------- | ------ |
| `ATHENA_INTERFACE_CONTRACTS.md` | ✅ fronteras por rol |
| `ATHENA_FAILURE_TESTS.md` | ✅ suite de fallo correcto |

**Solo después:** implementación mínima → primer ciclo real.

### Umbral antes de encender

**No:** ¿Puede una IA investigar?

**Sí:** ¿Puede el sistema investigar **sin** perder la capacidad de decir **no sabemos** — y **pasar** las failure tests?

Sin eso → máquina apagada.

---

## Estado consolidado

```text
ATHENA

Brújula                      ✅
Método 0–5                   ✅
Frontera de automatización   ✅
Arquitectura conceptual      ✅  (este doc)
Implementación               ❌  no iniciada
Motor                        apagado
Agentes                      no creados
```

Mapa listo. Reglas listas. Arquitectura de **autoridad distribuida** lista.  
Máquina apagada hasta que merezca el umbral “no sabemos”.

---

# FIN — ATHENA AGENT ARCHITECTURE

*Ningún componente produce conocimiento final.  
El ciclo completo produce evaluación.  
El motor espera al umbral: poder decir «no sabemos».*
