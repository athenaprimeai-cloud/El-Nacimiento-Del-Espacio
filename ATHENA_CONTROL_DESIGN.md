# ATHENA — CONTROL DESIGN (Fase 4)

**Capa:** diseño del **control** · cómo se ejecuta la prueba de forma interpretable · **no** código · **no** ejecución de campañas · **no** agentes  
**Depende de:**  
- Fase 0 — `ATHENA_PRINCIPIO_RECTOR.md`  
- Fase 1 — `ATHENA_INSTRUMENT_DESIGN.md`  
- Fase 2 — `ATHENA_EXPLORATION_DESIGN.md`  
- Fase 3 — `ATHENA_ATTACK_DESIGN.md`  
**Programa:** B (Athena)  
**Programa A:** **no** se modifica  

---

## Lugar en el mapa

```text
FASE 0 — Brújula        ✅  qué se busca proteger
FASE 1 — Instrumento    ✅  qué cuenta como investigación
FASE 2 — Exploración    ✅  dónde puede buscar
FASE 3 — Ataque         ✅  cómo intenta morir una hipótesis
FASE 4 — Control        ⬅  este documento · procedimiento ejecutable
FASE 5 — Registro       ✅ ATHENA_RECORD_DESIGN.md
Motor: apagado
```

### Cadena

```text
Brújula → Instrumento → Exploración → Ataque → Control → Registro
```

### Pregunta de Fase 4

**No es:**

> ¿Cómo conseguimos un resultado favorable?

**Es:**

> ¿Cómo se ejecuta una prueba de forma que el **resultado sea interpretable** y **no** una negociación después de ver los datos?

Paso de:

> “Intentamos destruirla”

a:

> “Sabemos **qué ocurrió** cuando la pusimos a prueba.”

---

## Frases heredadas (no se diluyen aquí)

| Fuente | Principio |
| ------ | --------- |
| Fase 3 | El Crítico no existe para tener razón; existe para encontrar el punto donde la hipótesis deja de sostenerse |
| E004.2 → arquitectura | Una hipótesis fuerte no es una hipótesis **protegida**; es una que **sobrevivió intentos legítimos de destrucción** |
| Fase 1 | No hay hallazgo sin ficha, crítico y diseñador |

---

## 1. Marco congelado

**Antes** de correr, y **sin** modificar tras ver datos:

| Elemento | Estado pre-ejecución |
| -------- | -------------------- |
| Pregunta | Definida (una línea) |
| Hipótesis | Ficha registrada (Fase 1) |
| Predicciones | Escritas *a priori* (incluida forma de morir) |
| Métricas | Fijadas (primarias vs secundarias si aplica) |
| Condiciones de fallo / éxito | Establecidas |
| Ataques que motiva el control | Referenciados (Fase 3) |
| Alternativa / nulo / rival | Declarada (§2) |

### Regla central

```text
Resultado no modifica protocolo.
Protocolo determina cómo interpretar resultado.
```

| Prohibido post-datos | |
| -------------------- | - |
| Cambiar umbrales | |
| Cambiar la pregunta “para que quepa el plot” | |
| Promover un secundario a primario porque salió “interesante” | |
| Redefinir “casi éxito” | |

Si el marco debe cambiar → **nuevo ID de control**, no reescritura del que ya corrió.

---

## 2. Diseño del control

Toda prueba necesita **comparación**.  
Una sola rama “hipótesis + datos + historia” **no** es control.

### Incorrecto

```text
Hipótesis → datos → interpretación
```

### Correcto

```text
Hipótesis
   vs
Alternativa / nulo / rival
   ↓
Control (marco congelado)
   ↓
Diferencia observable (métricas predeclaradas)
   ↓
Estado de hipótesis (§4)
```

### Elementos mínimos del diseño

| Campo | Contenido |
| ----- | --------- |
| **Brazo A** | Condición bajo la hipótesis (o implementación de la predicción) |
| **Brazo B** | Nulo, rival, o control negativo |
| **Variable única** (o malla predeclarada) | Qué cambia; qué queda congelado |
| **Observable** | Qué se mide |
| **Umbrales de medición** | Cuándo dos ejecuciones se consideran distintas / iguales |
| **Umbrales de decisión** | Cómo la diferencia se traduce en estado (§4) |
| **Ataque que cierra** | Qué tipo de ataque de Fase 3 se está operativizando |

Lección transferible de PEP-D (sin fusionar programas): separar **medición** y **decisión** evita reescribir la física del dato porque cambió la filosofía del veredicto.

---

## 3. Ejecución reproducible

La memoria **no** debe depender del agente (humano o IA) que ejecutó.

### Registro mínimo de ejecución

| Campo | |
| ----- | - |
| ID del control | |
| Versión del instrumento / código / commit | |
| Parámetros completos | |
| Datos de entrada (hash o referencia inmutable) | |
| Semillas (si existen) | |
| Entorno (OS, dependencias relevantes, fechas) | |
| Tiempo de ejecución | |
| Salida completa (artefactos primarios) | |
| Incidencias | |
| Quién/qué ejecutó (humano, script, rol) | **no** es fuente de verdad; solo traza |

### Reglas

- Misma entrada + mismo instrumento + mismos parámetros → resultado **comparable**.  
- Si no se puede reproducir, el control **no** eleva el estado de la hipótesis (como máximo: “indeterminado / fallo de instrumento”).  
- El Archivista (Fase 5) recibe este paquete **entero**, no un resumen narrativo.

---

## 4. Resultado y estado

El resultado **no** dice:

> “Ganó la hipótesis.”

Dice un **estado** bajo el control ejecutado:

```text
Estado (bajo control X):

- reforzada bajo control X
- debilitada bajo control Y
- indeterminada
- requiere nuevo ataque
- muerta (si la forma de morir predeclarada ocurrió)
- residual / no-decisión (si el diseño no separó)
```

| Estado | Significado permitido |
| ------ | --------------------- |
| **Reforzada** | Predicciones se cumplieron **y** el rival/nulo no explica igual bajo este control |
| **Debilitada** | Ocurrió debilitamiento predeclarado; no se “salva” con nueva historia |
| **Muerta** | Ocurrió la forma de morir **W** de la ficha |
| **Indeterminada** | Ejecución incompleta, fallo REF/instrumento, o datos insuficientes |
| **Requiere nuevo ataque** | El control no tocó el punto débil; no es victoria |
| **Residual / no-decisión** | Ambas (o ninguna) historias siguen vivas; no forzar ganador |

### Semántica dura

| | |
| - | - |
| Reforzada ≠ verdad universal | Solo bajo control X y dominio de la ficha |
| Muerta ≠ “nunca más se reformula” | Se puede abrir **nueva** hipótesis con **nuevo** ID |
| Indeterminada ≠ “casi reforzada” | No se promociona por entusiasmo |

---

## 5. Prohibición principal

> El control **no** puede convertirse en una búsqueda hasta obtener un resultado deseado.

### Incorrecto

```text
Probamos 100 variantes.
Elegimos la que funciona.
```

### Correcto

```text
Definimos antes qué cuenta como evidencia.
Ejecutamos.
Aceptamos el resultado.
```

| Variante del error | Nombre |
| ------------------ | ------ |
| Re-correr hasta que salga A | p-hacking / outcome shopping |
| Ampliar malla post-hoc solo donde “se ve el efecto” | cherry-picking |
| Descartar seeds incómodas sin regla previa | sesgo de selección |
| Cambiar rival después de ver datos | redefinición post-hoc |

Si se necesita otra variante → **nuevo control** con marco congelado **antes** de esa corrida.

---

## 6. Relación Ataque → Control

| Fase 3 | Fase 4 |
| ------ | ------ |
| Ataque **propuesto** (punto débil) | Control que **operativiza** ese ataque |
| “Moriría si W” | Umbral y brazo que miden W |
| Crítico puede perder | Resultado: reforzada / debilitada / … sin coronar verdad |

Sin ataque documentado → **no** hay Control serio (bloqueo de Fase 3 §5).  
Sin marco congelado → **no** hay interpretación válida.

---

## 7. Qué no se hace en este documento

- Ejecutar controles Athena reales  
- Implementar runners o agentes  
- Definir umbrales numéricos de un fenómeno concreto (Goldbach, etc.)  
- Tocar PEP-D / E004.2  
- Abrir Fase 5 más allá del puntero  

Los umbrales de un fenómeno viven en el **protocolo de esa campaña**, no en este diseño genérico.

---

## Puerta a Fase 5 (Registro)

**Abierta en diseño:** `ATHENA_RECORD_DESIGN.md`  
Existencia · hipótesis (vivas y muertas) · datos vs decisiones · versiones · memoria negativa · memoria ≠ autoridad.

---

## Estado

```text
Brújula:     instalada
Instrumento: diseñado
Terreno:     definido
Ataque:      diseñado
Control:     diseñado  (este doc)
Registro:    diseñado  (ATHENA_RECORD_DESIGN.md)
Motor:       apagado
```

Ciclo de diseño **completo**. Implementación / agentes: solo con la pregunta de automatización post-Fase 5.

---

# FIN — ATHENA CONTROL DESIGN (Fase 4)

*De “intentamos destruirla” a “sabemos qué ocurrió en la prueba”.  
Sin negociación post-datos.*
