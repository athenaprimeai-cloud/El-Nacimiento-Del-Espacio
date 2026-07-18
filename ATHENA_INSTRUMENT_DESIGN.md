# ATHENA — INSTRUMENT DESIGN (Fase 1)

**Capa:** diseño del instrumento · **no** código · **no** agentes implementados · **no** hoja de ruta de producto  
**Depende de:** `ATHENA_PRINCIPIO_RECTOR.md` (Fase 0 — brújula)  
**Programa:** B (Athena)  
**Programa A (PEP-D):** **no** se modifica desde este documento  

---

## Mapa de fases

```text
FASE 0 — Brújula
✅ ATHENA_PRINCIPIO_RECTOR.md
    Define qué vale y qué no vale.

FASE 1 — Instrumento
⬅ este documento
    Capacidades mínimas del laboratorio.

FASE 2 — Exploración
✅ ATHENA_EXPLORATION_DESIGN.md  (terreno; motor apagado)

FASE 3 — Ataque
✅ ATHENA_ATTACK_DESIGN.md

FASE 4 — Control
✅ ATHENA_CONTROL_DESIGN.md

FASE 5 — Registro
✅ ATHENA_RECORD_DESIGN.md
```

Secuencia canónica (brújula):

```text
Brújula → Instrumento → Exploración → Ataque → Control → Registro
```

Primero la dirección. Después la máquina.  
**Ahora:** diseñar el instrumento, **no** saltar a agentes.

---

## Pregunta de Fase 1

**No es:**

> ¿Qué agente construimos?

**Es:**

> ¿Qué **capacidades mínimas** necesita Athena para investigar **mejor que un humano solo**, manteniendo la capacidad de **equivocarse** (y de que una hipótesis **muera**)?

Si una capacidad no mejora la investigación rigurosa ni preserva la muerte de hipótesis → **no** entra al instrumento.

Filtro (Fase 0):

> ¿Aumenta la capacidad de responder preguntas matemáticas profundas **con rigor**?

---

## 1. Unidad mínima de investigación

Athena **no** trabaja con “ideas sueltas”.  
Trabaja con **objetos auditables** en una cadena.

```text
Pregunta matemática
        ↓
Hipótesis candidatas
        ↓
Predicciones observables
        ↓
Experimentos / controles
        ↓
Resultado
        ↓
Estado de hipótesis
        ↓
(Registro permanente)
```

| Objeto | Requisitos mínimos |
| ------ | ------------------ |
| **Pregunta** | Una línea; dominio acotado; no es conclusión |
| **Hipótesis** | Ficha (§2); predecible; matable |
| **Predicción** | Observable *a priori*; comparable a datos |
| **Experimento / control** | Variable(s) declaradas; criterio de cierre |
| **Resultado** | Reproducible; sin reinterpretación post-hoc del umbral |
| **Estado** | Apoyada / debilitada / muerta / abierta / residual — explícito |

**Prohibido:** pasar de intuición a “hallazgo” sin objetos intermedios auditables.

---

## 2. Anatomía de una hipótesis

Cada hipótesis tiene una **ficha**. Sin ficha no es hipótesis del instrumento.

```text
ID:
Origen:                    (intuición / residual / campaña previa / agente)
Qué explica:
Qué predice:               (observable, *a priori*)
Qué la podría matar:       (resultado sorprendente / incompatibilidad)
Qué controles requiere:
Estado:                    (abierta | apoyo relativo | debilitada | muerta | residual)
Dominio:                   (condiciones bajo las que se afirma)
No-afirmaciones:           (qué NO reclama)
```

### Traducción obligatoria

| Frase prohibida | Frase exigida |
| --------------- | ------------- |
| “Encontré algo interesante” | “Propongo **X**. Moriría si ocurre **Y**.” |
| “La IA descubrió un patrón” | “Candidato **ID**. Controles: … Supervivencia si… Muerte si…” |
| “Encaja con la intuición” | “Predicción predeclarada: … Resultado: … Estado: …” |

La intuición puede **generar** la ficha.  
No puede **rellenar** el estado final.

---

## 3. Roles futuros de IA (funciones, no agentes)

Aún **no** se implementan agentes.  
Se definen **funciones** que cualquier implementación futura debe poder cubrir (humano, script o modelo).

| Función | Rol | No es |
| ------- | --- | ----- |
| **Explorador** | Genera candidatos (preguntas, hipótesis, patrones) | Juez final |
| **Crítico** | Busca contradicciones, confusiones, sobreclaims | Generador de más patrones sin freno |
| **Diseñador** | Propone pruebas y controles (qué mataría a quién) | Ejecutor opaco |
| **Auditor** | Revisa sesgos, umbrales post-hoc, fugas de Programa A/B | Autor de la historia favorita |
| **Archivista** | Conserva memoria: fichas, resultados, estados, no-afirmaciones | Borrador de derrotas |

Equilibrio obligatorio (de la brújula):

```text
Explorar + Atacar + Controlar + Registrar
```

Un sistema con solo Explorador es **peligroso** (colonia sin brújula).

---

## 4. Regla de supervivencia

La unidad que **sobrevive** no es la idea más elegante ni la más generada.

Es la idea que:

1. **Explica** (un hecho o patrón en dominio declarado),  
2. **Predice** (observable *a priori*),  
3. **Resiste ataques** (crítico + controles + intentos de destrucción),  
4. **No necesita cambiar reglas** del instrumento ni del protocolo para seguir viva.

| Sobrevive | Muere / se debilita |
| --------- | ------------------- |
| Predicción predeclarada se cumple bajo control | Ocurre lo que “la podría matar” |
| Alternativas rivales fallan o se restringen | Solo se salva reinterpretando umbrales |
| Dominio y no-afirmaciones se mantienen | Requiere reescribir la ficha post-hoc para “ganar” |

**Criterio ante IA:**

```text
No:  ¿Qué descubrió?
Sí:  ¿Qué sobrevivió después de intentar destruirlo?
```

---

## 5. Separación Programa A / Programa B

```text
Programa A (PEP-D):
  experimentos específicos, motor/protocolos concretos,
  evidencia de campaña, SPEC de A.

Programa B (Athena):
  filosofía del laboratorio, diseño de instrumentos,
  arquitectura de investigación asistida, brújula.
```

| Regla | |
| ----- | - |
| B **no** modifica resultados de A | Un diseño de instrumento no reescribe E004.2 |
| A **no** se reinterpreta como “prueba Athena” de primos/Goldbach | Dominios distintos |
| Lecciones de método (hipótesis pueden morir, restricción ≠ explicación) | **Sí** pueden transferirse A → B como disciplina |
| Agentes de B no “corrigen” campañas de A in-place | Solo proponen nuevas preguntas / controles en su dominio |

---

## Capacidades mínimas del instrumento (checklist Fase 1)

Athena, como instrumento, debe poder:

| # | Capacidad | Estado diseño |
| - | --------- | ------------- |
| 1 | Representar la unidad mínima (§1) de punta a punta | Definida aquí |
| 2 | Exigir ficha de hipótesis (§2) antes de “resultado” | Definida aquí |
| 3 | Asignar las cinco funciones (§3) sin colapsarlas en un solo rol | Definida aquí |
| 4 | Aplicar regla de supervivencia (§4) de forma explícita | Definida aquí |
| 5 | Mantener muro A/B (§5) | Definida aquí |
| 6 | Registrar derrotas con el mismo peso que victorias | Exigida; detalle en Fase 5 |
| 7 | Admitir residual / no-decisión sin narrativa | Exigida (brújula) |

**Aún no:** implementación de explorador/crítico/… como procesos, UI, ni LLMs.

---

## Qué no se hace en Fase 1

- Implementar agentes  
- Elegir modelos o frameworks  
- Abrir E005-A o tocar PEP-D / SPEC de A  
- Convertir este documento en “roadmap de features” de producto  
- Generar hipótesis Goldbach “para probar el instrumento” sin ficha ni control  

---

## Puerta a Fase 2 (Exploración)

**Abierta en diseño:** `ATHENA_EXPLORATION_DESIGN.md`  
Contrato: sin ficha + crítico + diseñador **no** hay hallazgo.  
Terreno definido; **motor de exploración apagado** hasta campaña autorizada.

---

## Pregunta diferida (correcta, más adelante)

> ¿Qué agente implementamos?

Solo después de que este diseño diga **qué objeto procesa**, **cómo muere una hipótesis** y **quién ataca**.  
Si se invierte el orden: mucho movimiento, poca navegación.

---

# FIN — ATHENA INSTRUMENT DESIGN (Fase 1)

*Convierte la brújula en el diseño del instrumento.  
Sin máquina todavía. Sin colonia sin brújula.*
