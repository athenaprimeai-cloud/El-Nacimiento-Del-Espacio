# PROJECT ERA — Dos cronologías

**Propósito:** leer la **historia** del proyecto, no añadir metodología.  
**No es:** constitución, legislación ni protocolo.  

---

## Idea central

```text
ERA I
Diseño del laboratorio
Estado: CERRADA

ERA II
Investigación del laboratorio
Estado: ACTIVA
```

Un lector futuro no necesita reconstruir toda la conversación de diseño para entender un META-E reciente: basta saber en qué **era** está el proyecto.

---

## Cronología 1 — Diseño (ERA I)

| | |
| - | - |
| **Naturaleza** | Finita |
| **Inicio** | Idea inicial / intuiciones |
| **Fin** | Congelamiento del kernel + constitución / legislación inicial |
| **Producto** | Principio rector, kernel, arquitectura, frontera IA, modelo de evidencia, freeze |
| **Pregunta dominante** | ¿Cómo **debería ser** el laboratorio? |
| **Estado** | **Cerrada** |

La imaginación **propone** y, en esta era, construye la identidad y el régimen.

---

## Cronología 2 — Científica (ERA II)

| | |
| - | - |
| **Naturaleza** | Abierta (sin final definido) |
| **Inicio** | Ahora (kernel congelado; META-E / campañas de dominio) |
| **Formada por** | E00x (dominio), META-E00x (lab), cambios de **legislación** respaldados por evidencia |
| **Pregunta dominante** | ¿Qué **evidencia** justifica cambiar el laboratorio? |
| **Estado** | **Activa** |

La imaginación sigue siendo valiosa: **solo propone**.  
La **evidencia decide**.

---

## Cierre de la Era I

> **El laboratorio ya no evoluciona por imaginación; evoluciona por evidencia.**

La Era I **no** termina porque el diseño sea perfecto.  
Termina porque el **diseño ha dejado de ser la herramienta adecuada para progresar**.

Si dentro de meses una parte del kernel resulta mala, eso **no reabre la Era I**.  
Significa que la **Era II** produjo evidencia suficiente para modificar la **legislación metodológica**. La arquitectura ya prevé ese mecanismo.

La imaginación sigue valiendo: **solo propone**. La evidencia **decide**.

---

## Mapa rápido para un lector nuevo

| Si buscas… | Lee… |
| ---------- | ---- |
| Identidad y eras | este documento + `LABORATORY.md` |
| Constitución | `CONSTITUTION_AND_LAW.md`, `ATHENA_PRINCIPIO_RECTOR.md` |
| Cómo se investiga el lab | `META_EXPERIMENTS.md`, `META_EVIDENCE_MODEL.md` |
| Un META-E concreto | `META-E00x/…` (no hace falta rehacer Era I) |
| Código del kernel | `athena_core/` (ingeniería, nivel 3) |

---

## Frontera que no depende del código

| Antes (Era I) | Ahora (Era II) |
| ------------- | -------------- |
| ¿Cómo debería ser el lab? | ¿Qué evidencia justifica **cambiarlo**? |
| ¿Qué construir? / ¿Funciona? | ¿Qué **perdemos** al mejorar? / ¿**Vale la pena**? (eficacia · coste · reversibilidad) |

### Lectura del repositorio (por nivel de pregunta)

| Nivel | Responde |
| ----- | -------- |
| Constitución | ¿Qué **identidad** debe conservar el lab? |
| Legislación metodológica | ¿Qué **reglas** usamos hoy y cómo pueden cambiar? |
| Ingeniería | ¿Cómo **ejecutamos** esas reglas? |
| META-E | ¿Debemos **cambiar** alguna regla? |
| E00x (dominio) | ¿Qué aprendimos del **fenómeno**? |

Cada nivel tiene una pregunta distinta. No mezclar debates.

### Señal de salud (no norma rígida)

> **La legislación debería crecer más lentamente que la evidencia que la justifica.**

Vigilar **inflación metodológica**: cada resultado no debe exigir una regla, un documento o un principio nuevo.

### Tres hitos que cierran la Era I

1. Separar **instrumento**, **evidencia** e **interpretación**.  
2. Aceptar que el **propio laboratorio es falsable**.  
3. **Congelar** el diseño y exigir evidencia para cualquier cambio metodológico.

A partir de aquí, la calidad no se mide por cuántas ideas nuevas aparecen, sino por cuántas **sobreviven** al mismo régimen que el lab exige a todo lo demás.

---

## Evolución de la pregunta dominante

| Etapa | Pregunta dominante |
| ----- | ------------------ |
| Inicio | ¿Cómo investigamos este **fenómeno**? |
| Diseño (Era I) | ¿Cómo debe ser un **laboratorio** para investigar con rigor? |
| Era II | ¿Qué **evidencia** justifica **cambiar** ese laboratorio? |

Ese desplazamiento de la pregunta es el verdadero cambio de fase.  
No depende del código, de los modelos ni de Goldbach.  
Depende de **dónde está la carga de la prueba**.

Cada documento del repositorio debería poder responder **por qué existe** y en **qué nivel de autoridad** está (`CONSTITUTION_AND_LAW.md`). Eso reduce el riesgo de un cementerio de archivos sin propósito.

---

## Criterio a 2–3 años (no “¿descubrió algo?”)

**Primero:**

> ¿Sigue cambiando por **evidencia** y no por **entusiasmo**?

Si la respuesta sigue siendo **sí**, la Era II habrá conservado la identidad del cierre de la Era I.

Un resultado matemático relevante (Athena u otro programa), si llega, tendrá un contexto metodológico más sólido: habrá surgido de un laboratorio que también aprendió a investigar **su propia forma de investigar**.

No garantiza descubrimientos.  
Establece un marco en el que, si aparecen, se evalúan con el mismo rigor que cualquier cambio en el propio laboratorio.

---

## Responsabilidad (frontera diseño / investigación)

| Era | Responsabilidad |
| --- | --------------- |
| **I** | De los **diseñadores**: decidir cómo debía funcionar el laboratorio |
| **II** | Del **régimen experimental**: decidir, con evidencia, qué merece permanecer y qué debe cambiar |

### Humildad metodológica (conservar en META-E y E00x)

No son estilo. Son mecanismo:

* «No sabemos.»  
* «Puede morir.»  
* «Bajo este control.»  
* «No generalizar.»  

Evitan confundir resultados **locales** con conclusiones **generales**.

Si esa forma de interpretar la evidencia se mantiene en 2–3 años —con o sin hallazgo matemático— el lab habrá conservado su identidad.

### Promesa del cierre de la Era I

No una promesa de descubrimientos.

> **A partir de ahora, el laboratorio deberá convencer a la evidencia antes que a sus propios diseñadores.**

Si la Era II cumple esa promesa, el cambio de fase no habrá sido solo documental: habrá pasado al **comportamiento** del proyecto.

### Cómo crece el lab en Era II

No por acumulación de capas.

Evalúa **trayectorias**, no solo resultados:

```text
Mejora:  propuesta → promete → paga un coste → se prueba → queda / se limita / muere
```

**Ejemplo:** Selector v0.1 — E001 economía + E002b diversidad → **soportado con limitaciones**  
(`LEGISLATION_SELECTOR_v0_1.md`).

**Registro fósil:** no solo “¿qué versión usamos?” sino “¿qué versiones **rechazamos** y **por qué**?”  
Excluidos del Selector = **memoria de diversidad**, no basura.

Una mejora del método compite contra costes, alternativas y retirada — no es inevitable por ser la actual.

---

# FIN — PROJECT ERA

*Era I cerrada · Era II activa.  
La imaginación propone. La evidencia decide.  
Convencer a la evidencia, no a los diseñadores.*
