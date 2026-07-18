# ATHENA — PRINCIPIO RECTOR

**Lugar en el mapa:** **Nivel 1** — arriba de todo · filtro de entrada  
**Ver también:** `LABORATORY.md` (kernel = lab; Athena = programa sobre el kernel)  
**Programa PEP-D (dinámica discreta):** separado  
**Estado:** brújula · estable aunque cambien kernel y programas  

La brújula **no es una tecnología**. Es un **criterio**.  
El **laboratorio** es el **kernel metodológico**.  
**Athena** es un **programa de investigación** (hoy: estructuras aritméticas / banco Goldbach) que **corre sobre** el kernel — no es el nombre del laboratorio.

---

## Principio rector

```text
ATHENA — PRINCIPIO RECTOR

Usar un laboratorio computacional riguroso para investigar
estructuras matemáticas profundas, separando señal de ruido,
sin permitir que las intuiciones iniciales controlen los resultados.
```

**Todo lo demás pasa por ese filtro** — agentes, modelos, simulaciones, arquitecturas, visualizaciones, hipótesis.

### Test de admisión (cualquier capacidad nueva)

> ¿Esta capacidad aumenta la capacidad de responder preguntas matemáticas profundas **con rigor**?

Si la respuesta es **no** → **distracción**. No se construye.

---

## Qué no es el objetivo

| No es | |
| ----- | - |
| Crear una IA “interesante” | |
| Crear un sistema autónomo por la autonomía | |
| Generar miles de teorías y elegir la más bonita | |
| Encontrar la estructura a toda costa | |

### Núcleo (principio de diseño)

> **Athena no existe para encontrar estructuras.**  
> **Existe para construir instrumentos capaces de distinguir estructuras reales de ilusiones producidas por el propio método.**

La herramienta cambia. **La brújula no.**

**No es** especificación técnica ni hoja de ruta de implementación.  
**Es** capa superior: criterio de orientación que permanece aunque cambien modelos, agentes, algoritmos o experimentos.

### Filtro ante un agente que “encuentra” diez mil patrones

La pregunta **no** es:

> ¿Qué descubrió la IA?

La pregunta **es**:

> ¿Qué **sobrevivió** después de que el sistema intentó **destruirlo**?

Ese es el puente entre investigación clásica y sistemas de IA más autónomos.

---

## Preguntas guía (dominio Athena)

### 1. Estructura vs apariencia

> ¿Existe una estructura no trivial detrás de un fenómeno matemático observado?

Ejemplos de terreno (no lista cerrada):

- error de Goldbach  
- distribuciones residuales  
- patrones espectrales  
- relaciones entre transformaciones  

**Regla:**

```text
Patrón observado
≠
estructura matemática confirmada
```

El patrón es una **señal candidata**. No una conclusión.

---

### 2. Señal real vs artefacto

Toda observación debe pasar por una separación:

```text
Observación
    |
    ├── estructura potencial
    |
    ├── efecto de borde
    |
    ├── truncación
    |
    ├── elección del método
    |
    └── ruido
```

El trabajo de Athena **no** es enamorarse del primer patrón.  
Es **intentar destruirlo**.

---

### 3. Intuición inicial bajo control

La intuición puede generar **preguntas**.  
No puede decidir **resultados**.

```text
Intuición
   ↓
Hipótesis candidata
   ↓
Control independiente
   ↓
Supervivencia o muerte
```

**Nunca:**

```text
Intuición
   ↓
Interpretación final
```

---

## Propiedad principal (no negociable)

> Una hipótesis **puede morir**.

El sistema no se diseña para encontrar respuestas.  
Se diseña para **eliminar respuestas falsas más rápido** sin bajar el criterio de muerte.

Eso es lo que E004.2 (Programa A) demostró como disciplina de laboratorio y lo que Athena (Programa B) debe **conservar** si alguna vez usa agentes u otras herramientas.

---

## Agentes (futuro — solo si pasan el filtro)

Un agente que **solo busca patrones** es peligroso.

Un sistema Athena necesitaría equilibrios:

```text
Explorar
   +
Atacar
   +
Controlar
   +
Registrar
```

### Dirección mala

```text
Crear 20 agentes IA
↓
Generan miles de teorías
↓
Elegimos la más bonita
```

### Dirección buena

```text
Pregunta matemática
        ↓
Agentes generan explicaciones rivales
        ↓
Agentes diseñan controles
        ↓
Agentes intentan destruir resultados
        ↓
Experimentos reproducibles
        ↓
Registro permanente
        ↓
Solo sobreviven las ideas resistentes
```

### Pregunta de diseño (antes de construir agentes)

> ¿Cómo convertir Athena en investigación asistida por agentes **sin** perder su propiedad principal: que una hipótesis pueda morir?

No se está construyendo una IA autónoma.  
Se está intentando construir un **instrumento científico** que pueda usar IA para explorar más territorio **sin soltar la brújula**.

---

## Relación con Programa A (PEP-D)

| | Programa A · PEP-D | Programa B · Athena |
| - | ------------------ | ------------------- |
| Objeto | Dinámica discreta / protocolos / instrumento Alpha | Estructuras matemáticas profundas (p.ej. Goldbach, residuos, espectros) |
| Lección transferible | Hipótesis pueden morir; restricción ≠ explicación | Misma disciplina sobre otro dominio |
| Mezcla | **Prohibida** en la misma campaña | |

PEP-D no es “investigación sobre primos”. Athena no reescribe el motor Alpha para “ganar” Goldbach.

---

## Uso de este documento

1. Léelo **antes** de proponer agentes, arquitecturas o campañas Athena.  
2. Si una propuesta no pasa el principio rector ni el test de admisión → **no se hace**.  
3. No se modifica este principio “para acomodar” una herramienta nueva.  
4. La herramienta se adapta al principio, o se descarta.

---

## Estado (asentado)

```text
Nivel 1 Brújula  ✅  este documento (estable)
Nivel 2 Kernel   ✅  el laboratorio (dominio-agnóstico)
Nivel 3 Athena   =   un programa sobre el kernel (no el lab)
Meta             →   investiga el kernel (M1–M4)
Ver: LABORATORY.md
```

La herramienta y los programas pueden cambiar. **La brújula permanece.**  
La arquitectura del kernel es **falsable**.

---

# FIN — PRINCIPIO RECTOR

*Brújula antes del laboratorio.  
Laboratorio antes de los programas.  
Athena es un programa, no el laboratorio.*
