# ATHENA — ATTACK DESIGN (Fase 3)

**Capa:** diseño del **ataque** · cómo mueren las ideas · **no** agente crítico implementado · **no** código · **no** búsqueda activa  
**Depende de:**  
- Fase 0 — `ATHENA_PRINCIPIO_RECTOR.md`  
- Fase 1 — `ATHENA_INSTRUMENT_DESIGN.md`  
- Fase 2 — `ATHENA_EXPLORATION_DESIGN.md`  
**Programa:** B (Athena)  
**Programa A:** **no** se modifica  

---

## Lugar en el mapa

```text
FASE 0 — Brújula        ✅  qué proteger
FASE 1 — Instrumento    ✅  unidad de investigación
FASE 2 — Exploración    ✅  terreno · motor apagado
FASE 3 — Ataque         ✅  este documento · prueba de choque
FASE 4 — Control        ✅  ATHENA_CONTROL_DESIGN.md
FASE 5 — Registro       ✅  ATHENA_RECORD_DESIGN.md
```

### Cadena (correcta)

```text
Terreno
   ↓
Candidato
   ↓
Ataque          ⬅ aquí
   ↓
Control
   ↓
Registro
```

### Cadena (prohibida)

```text
Patrón
   ↓
Historia
```

### Condición heredada

> No hay hallazgo sin ficha, crítico y diseñador.

Athena no trata el descubrimiento como iluminación.  
Lo trata como **proceso de supervivencia**.

---

## Pregunta de Fase 3

**No es:**

> ¿Cómo construimos un agente que critique por criticar?

**Es:**

> ¿Qué debe intentar **destruir** una hipótesis **antes** de que Athena permita **invertir recursos** en ella?

Fase 3 diseña la **inmunidad del sistema contra su propio entusiasmo**.

Athena no se construye alrededor de la generación de inteligencia.  
Se construye alrededor de la **selección de conocimiento resistente**.

---

## 1. Misión del Crítico

### Objetivo

Encontrar el **punto débil** de un candidato o hipótesis **antes** del gasto serio de Control.

### No es la misión

| No | |
| -- | - |
| Buscar otra explicación “más bonita” | |
| Destruir todo por defecto | |
| Ganar una disputa retórica | |
| Proteger la intuición inicial | |
| Generar más patrones para diluir el ataque | |

### Sí es la misión

Buscar, de forma documentada:

| Blanco | Ejemplo de pregunta |
| ------ | ------------------- |
| **Errores** | ¿Hay fallo de definición, dominio o cálculo? |
| **Artefactos** | ¿El patrón es producto del método, truncación o borde? |
| **Condiciones de fallo** | ¿Dónde deja de aparecer? |
| **Supuestos ocultos** | ¿Qué se asumió sin declararlo en la ficha? |
| **Confusiones de variable** | ¿Se midió A y se atribuyó a B? |
| **Sobreclaim** | ¿La ficha afirma más que el dominio permite? |

### Traducción obligatoria

| Frase prohibida | Frase exigida |
| --------------- | ------------- |
| “No me convence” | “Falla si ocurre **W′** por razón **R**.” |
| “Es un artefacto obvio” | “Ataque de artefacto: control propuesto … predicción si es artefacto …” |
| “Hay que buscar otra teoría” | “Rival **ID** predice **Z′**; si **Z′** y no **Z**, muere la actual.” |

---

## 2. Tipos de ataque

Todo ataque se registra como objeto auditable (no como comentario de pasillo).

```text
Ataque:
  ID:
  Tipo:              (uno de la taxonomía abajo)
  Hipótesis/Candidato atacado:
  Supuesto que se pone en duda:
  Procedimiento de ataque:
  Resultado que debilitaría o mataría:
  Resultado que el ataque no logra (si falla el ataque):
  Estado del ataque:  propuesto | ejecutado | fallido | exitoso
```

### Taxonomía mínima

| Tipo | Pregunta | Si el ataque tiene éxito |
| ---- | -------- | ------------------------ |
| **Replicación** | ¿Aparece bajo las mismas condiciones declaradas? | No-reproducibilidad → debilita o mata |
| **Variación** | ¿Cambia al modificar parámetros **declarados irrelevantes**? | Dependencia espuria → debilita |
| **Simplificación** | ¿Existe explicación más simple con la misma predicción? | Coste explicativo / rival más parsimoniosa |
| **Artefacto** | ¿Es producto del método, borde, truncación, binning, seed? | Reclasificar como artefacto; no estructura |
| **Adversarial / rival** | ¿Una hipótesis rival explica igual o mejor? | Apoyo relativo se mueve; posible muerte de la favorita |
| **Dominio** | ¿Fuera del dominio de la ficha el claim se desmorona y la ficha lo ocultaba? | Sobreclaim; recorte o muerte |
| **Constructo** | ¿La métrica mide lo que la ficha dice medir? | Fallo de constructo; no se “arregla” cambiando la historia |

Se pueden añadir tipos **solo** con definición de muerte/ debilitamiento *a priori*.  
No se inventan tipos post-hoc para salvar o matar a conveniencia.

---

## 3. Regla de éxito del Crítico

El Crítico **también puede perder**.

### Éxito del Crítico

Encontró un punto débil **operativo** (ataque con procedimiento y resultado de muerte/ debilitamiento predeclarado) que:

- o bien **mata / debilita** la hipótesis tras Control,  
- o bien **obliga** a recortar dominio / no-afirmaciones de forma explícita.

### Fracaso del Crítico (no es vergüenza)

Tras un conjunto de ataques **predeclarados** (tipo, procedimiento, cuándo se detiene):

- no se encontró punto débil operativo, o  
- los ataques se ejecutaron y **fallaron** (la predicción de muerte no ocurrió).

### Efecto sobre la hipótesis (cuidado semántico)

| Situación | Efecto permitido | Efecto **prohibido** |
| --------- | ---------------- | -------------------- |
| Crítico falla (ataques fallidos) | Hipótesis **aumenta de resistencia** (relativa a esos ataques) | Hipótesis se vuelve **verdad** |
| Crítico acierta | Hipótesis **muere**, se **debilita**, o se **recorte** el dominio | “Casi muere pero la intuición la salva” |
| Ataques no se intentaron | **No** hay aumento de resistencia | Saltar a “hallazgo” |

**Resistencia ≠ verdad.**  
Resistencia = sobrevivió a ataques **documentados** en un marco fijo.

---

## 4. Prohibición central

> El Crítico **no** puede cambiar las reglas para ganar.

Debe atacar **dentro del mismo marco** que la ficha y el control propuestos.

| Prohibido | |
| --------- | - |
| Cambiar umbrales o métricas porque la favorita iba a morir | |
| Redefinir “qué predice” después de ver el ataque | |
| Inventar un tipo de ataque ad hoc solo para matar una rival incómoda | |
| Negarse a registrar un ataque exitoso contra la favorita | |
| Declarar victoria del Crítico sin procedimiento ejecutable | |

### Puente con E004.2 (Programa A) — lección, no fusión

La misma disciplina que aplicó E004.2 a H-E004-03:

- criterio **previo**,  
- derrota **registrada**,  
- **sin** reciclaje post-hoc,  

se convierte aquí en **arquitectura general** del ataque en Athena.

B no reescribe los resultados de A.  
B **hereda el principio**: las ideas pueden morir bajo reglas fijas.

---

## 5. Cuándo se permite invertir recursos (paso a Control)

Athena **no** invierte en Control serio hasta que:

| # | Condición |
| - | --------- |
| 1 | Existe ficha de hipótesis (Fase 1) |
| 2 | Existe al menos un **ataque propuesto** (tipo + procedimiento + forma de morir) |
| 3 | El Diseñador ha convertido al menos un ataque en **propuesta de control** (Fase 4) |
| 4 | El marco (métricas, dominio, predicciones) está **congelado** para ese control |
| 5 | No hay “ataques” que sean solo preferencia estética |

Si el entusiasmo pide gastar sin 1–5 → **bloqueo**.  
Eso es la inmunidad contra el propio entusiasmo.

---

## 6. Relación con funciones (Fase 1)

| Función | En Fase 3 |
| ------- | --------- |
| Explorador | Entrega candidato; **no** ataca ni cierra |
| **Crítico** | Propone y (más adelante) ejecuta ataques |
| Diseñador | Traduce ataque viable → control (Fase 4) |
| Auditor | Verifica que el Crítico no cambió reglas |
| Archivista | Guarda ataques exitosos y **fallidos** con el mismo peso |

---

## 7. Qué no se hace en este documento

- Implementar el agente Crítico  
- Ejecutar ataques sobre Goldbach u otros  
- Abrir Fase 4 con un control real  
- Tocar PEP-D / E004.2 / E005-A  
- Convertir “resistencia” en “demostración”  

---

## Puerta a Fase 4 (Control)

**Abierta en diseño:** `ATHENA_CONTROL_DESIGN.md`  
Marco congelado · comparación vs rival/nulo · ejecución reproducible · estado (no “ganó”) · prohibición de buscar el resultado deseado.

---

## Estado

```text
Brújula:     instalada
Instrumento: diseñado
Terreno:     definido
Ataque:      diseñado  (este doc)
Control:     diseñado  (ATHENA_CONTROL_DESIGN.md)
Registro:    diseñado
Motor:       apagado
```

---

# FIN — ATHENA ATTACK DESIGN (Fase 3)

*Diseñar cómo mueren las ideas.  
Selección de conocimiento resistente, no generación de entusiasmo.*
