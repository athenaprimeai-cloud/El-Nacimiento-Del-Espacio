# META_EVIDENCE_MODEL — Constitución de evidencia del programa meta

**Qué es:** qué **tipos de evidencia** existen al **investigar el laboratorio**.  
**Qué no es:** cómo diseñar un experimento concreto (eso es cada META-E / protocolo).  
**Régimen:** el kernel no tiene privilegios; la brújula no es “evidencia meta”.  

---

## Propósito

Sin un modelo de evidencia, cada META-E elige métricas ad hoc y los resultados **no se acumulan**.

Con este modelo, un resultado se reporta como **perfil de evidencia**, no como “mejor/peor” monosilábico.

Ejemplo de cierre de campaña:

```text
META-E00x
E-M1: fuerte
E-M2: moderada
E-M3: insuficiente
E-M4: no evaluada
E-M5: no evaluada
```

---

## Tipos de evidencia

| Tipo | Pregunta | Ejemplos de métricas / observaciones |
| ---- | -------- | ------------------------------------ |
| **E-M1** | ¿El proceso **cumple sus propias reglas**? | Auditor detecta corrupción; POSTHOC=0; FT-CORE/auditor PASS; no reescritura post-resultado |
| **E-M2** | ¿**Reduce coste metodológico**? | Menos experimentos / presupuesto de ataque para un mismo conjunto de estados abiertos; budget_reduction |
| **E-M3** | ¿**Reduce errores** metodológicos? | Menos post-hoc, menos reinterpretaciones, menos cierres sin control, menos muertes sin razón |
| **E-M4** | ¿**Generaliza**? | Mismo régimen estable en Goldbach/E004, Collatz, secuencias aleatorias, otro dominio (sin reglas nuevas del kernel) |
| **E-M5** | ¿**Resiste modificaciones**? | Tras cambiar un componente (p.ej. heurística del Selector), integridad + economía no colapsan; o la regresión se detecta |

### Niveles de fuerza (por tipo, *a priori* en cada protocolo)

| Nivel | Significado |
| ----- | ----------- |
| **no evaluada** | El protocolo no midió este tipo |
| **insuficiente** | Datos insuficientes o umbral no alcanzado |
| **moderada** | Umbral predeclarado alcanzado en el diseño actual |
| **fuerte** | Umbral alto / multi-réplica / multi-condición predeclarado |
| **contraria** | Evidencia en contra de la hipótesis de mejora (también se registra) |

Los umbrales numéricos viven en el **protocolo de cada META-E**, no aquí.

---

## Regla: mejora local ≠ mejora del laboratorio

> **No toda mejora local es una mejora del laboratorio.**

| Ejemplo | Lectura |
| ------- | ------- |
| Selector reduce 40 % el presupuesto | Mejora **local** (E-M2 candidata) |
| …pero aumenta sesgo y deja escapar hipótesis importantes | Empeoramiento **global** (E-M3 / valor científico a largo plazo) |

Un informe META-E debe poder decir:

```text
E-M2: moderada (mejora local de coste)
E-M3: contraria o insuficiente (sesgo / errores)
→ no se adopta como mejora del laboratorio
```

El laboratorio **debe** distinguir ambas.

---

## Coste epistemológico de toda mejora (tercera dimensión)

Además de campañas de **dominio** (E00x) y de **laboratorio** (META-E), toda **mejora propuesta** arrastra un perfil medible:

> **Toda mejora propuesta debe tener un coste epistemológico medible.**

No basta el beneficio. Hay que estimar el **precio**.

| Beneficio (ej. META-E001) | Coste (preguntas medibles) |
| ------------------------- | -------------------------- |
| −85 % presupuesto | ¿% de candidatos potencialmente valiosos fuera? |
| +economía | ¿diversidad de hipótesis perdida? |
| +priorización | ¿tipos sistemáticamente relegados? |
| | ¿favor a fáciles de falsar vs profundas? |
| | ¿el sesgo es estable al cambiar de dominio? |

La decisión metodológica deja de ser binaria (“sirve / no sirve”) y pasa a un **perfil de intercambio** (beneficio × coste).

### Implicación para el Selector (y cualquier componente de legislación)

El Selector **no** es un componente definitivo.  
Es una **hipótesis permanente** (legislación): cada versión compite con la anterior bajo META-E.

Nunca “el Selector definitivo” — solo la mejor versión que ha **sobrevivido** hasta ahora.  
Eso evita convertir legislación en constitución.

### Pregunta dominante de la Era II (complemento)

| Era I | Era II (también) |
| ----- | ---------------- |
| ¿Qué deberíamos construir? | ¿Qué **perdemos** cuando **mejoramos** algo? |
| ¿Funciona? | ¿**Vale la pena**? (eficacia + coste) |

Incluso un éxito extraordinario debe demostrar que no compra la mejora a un **precio metodológico** demasiado alto.

---

## Tres ejes de toda mejora metodológica

No basta la ciencia experimental clásica (hipótesis → experimento → evidencia → decisión) si la decisión solo mira “¿funciona?”.

La **ingeniería científica** del lab pregunta también “¿vale la pena?”.

| Eje | Pregunta | Tipo de evidencia / artefacto |
| --- | -------- | ----------------------------- |
| **Eficacia** | ¿Produce la mejora prometida? | E-M1…E-M5 según el caso (p.ej. E-M2 economía) |
| **Coste epistemológico** | ¿Qué perdemos al adoptarla? | Cobertura, diversidad, sesgo, E-M3… |
| **Reversibilidad** | Si la retiramos, ¿recuperamos el comportamiento anterior **sin reinterpretar** la evidencia pasada? | Conservación + re-ejecución bajo reglas de la versión anterior |

### Reversibilidad (simétrica a la conservación)

Ya: *cambiar implementación no cambia la evidencia* (si conserva el régimen).

Ahora, simétrico para legislación:

> **Cambiar legislación no debe destruir la posibilidad de volver atrás**,  
> siempre que las campañas se **vuelvan a ejecutar** bajo las reglas de la versión correspondiente.

Las mejoras son **reversibles**: ninguna legislación deja cicatrices permanentes que impidan restaurar el régimen anterior (evidencia antigua se lee en su versión; nueva se re-ejecuta si hace falta).

Historial deseable a años vista:

| Legislación | Estado |
| ----------- | ------ |
| Selector v1 | retirada |
| Selector v2 | retirada |
| Selector v3 | vigente |

El repositorio explica **por qué** cada transición — no solo “la versión actual”.

---

## Cuatro preguntas antes de META-E (lectura, no capa nueva)

Toda propuesta de cambio metodológico debería poder responder:

1. **¿Qué mejora?** (eficacia)  
2. **¿Qué cuesta?** (coste epistemológico)  
3. **¿Qué evidencia lo demuestra?** (perfil E-M*)  
4. **¿Podemos volver atrás si la evidencia futura cambia?** (reversibilidad)

Si no puede → **todavía no** está lista para entrar en META-E.

No es una capa de diseño nueva: es la forma de **leer** cualquier cambio bajo el régimen ya decidido.

---

## Tres capas de trabajo (no confusiones)

| Capa | Pregunta | Produce |
| ---- | -------- | ------- |
| **Principio rector** | ¿Qué no negociamos? | Brújula (estable) |
| **Investigación del laboratorio** (META-E) | ¿Qué régimen **mejorar / no / no sabemos**? | Evidencia E-M1…E-M5 |
| **Ingeniería del laboratorio** | ¿Cómo **implementar** lo que META-E ya mostró que merece la pena? | Código, optimización, LLMs como herramientas |

La **ingeniería no demuestra** conocimiento metodológico.  
Solo **ejecuta** un régimen que la investigación meta ya legitimó (o mantiene el status quo).

Eso evita mezclar “refactoré el Selector” con “demostramos que el lab es mejor”.

---

## Regla epistemológica del código

> **El código nunca crea conocimiento; únicamente ejecuta un régimen de investigación.**

Consecuencias:

| Cambio | ¿Cambia el conocimiento automáticamente? |
| ------ | ---------------------------------------- |
| Python → Rust | **No** |
| LLM A → LLM B | **No** (si ejecuta el **mismo contrato**) |
| Algoritmo X → Y | **No**, salvo que el **régimen experimental** cambie y se evalúe |
| Paralelizar / UI | **No**, si no altera el significado de la evidencia |

Lo que cambia el conocimiento es el **régimen** que el código es capaz de ejecutar (y la evidencia que ese régimen produce).

Separación **ingeniería** / **epistemología**.

---

## Conservación epistemológica (propiedad operacional)

> **Una modificación solo es aceptable si aumenta las capacidades del laboratorio  
> sin alterar el significado de la evidencia ya obtenida.**

Es la “compatibilidad hacia atrás” del **conocimiento**, aplicada al método.

| Conserva evidencia | Rompe conservación |
| ------------------ | ------------------ |
| Python → Rust | Reinterpretar hipótesis ya evaluadas **sin** re-ejecutar |
| GPT → otro modelo **mismo contrato** | Redefinir estados (`MUERTA` significa otra cosa) |
| Paralelizar experimentos | Reescribir reglas de decisión y reaplicar a resultados antiguos |
| Mejorar interfaz | Cambiar umbrales y “releer” la historia |

Si se rompe la conservación → o se **repite** el experimento bajo el nuevo régimen, o el cambio es **inválido** como continuación de la evidencia previa.

---

## Dos tipos de cambio en el laboratorio

| Tipo | ¿Requiere nueva evidencia META-E / protocolo? | Ejemplos |
| ---- | --------------------------------------------- | -------- |
| **Cambio de implementación** | **No** necesariamente (si conserva el régimen y el significado de la evidencia) | Optimizar rendimiento; otro lenguaje; otro LLM con mismo contrato; paralelizar; UI |
| **Cambio metodológico** | **Sí** | Nueva heurística del Selector; nuevos estados del kernel; nuevas reglas de decisión; cambiar qué cuenta como control |

Eso evita que un refactor se trate como “nueva teoría metodológica”.

---

## Una mejora también debe poder morir

> **Ninguna optimización entra al kernel porque “parece mejor”.**  
> Entra porque supera el **mismo régimen** de investigación del laboratorio (perfil E-M*).

Extiende:

| Antes | Ahora |
| ----- | ----- |
| Una hipótesis puede morir | **Una mejora también debe poder morir** |

Cierra el punto ciego de incorporar “mejoras de ingeniería” sin el escrutinio de las hipótesis científicas — o, si son metodológicas, sin META-E.

---

## Criterio de confianza del proyecto

> **La confianza se desplaza desde las personas y las implementaciones  
> hacia el régimen experimental.**

No garantiza descubrimientos matemáticos.  
Establece base para evaluar **resultados** y el **proceso** que los produce.

---

## Cómo reporta un META-E

Todo informe de cierre META-E incluye:

```text
Perfil de evidencia:
  E-M1: …
  E-M2: …
  E-M3: …
  E-M4: …
  E-M5: …

Mejora local vs global: …
Adopción en kernel: sí / no / diferida (con razón)
NO_SABEMOS: si aplica
```

Sin perfil → el resultado **no es acumulativo**.

---

## Mapa a campañas

| Campaña | Tipos de evidencia que **debe** declarar (mínimo) |
| ------- | ------------------------------------------------- |
| META-E001 | E-M1, E-M2, E-M3 (E-M4/5 opcional) |
| META-E002 | E-M2 primario; E-M1 obligatorio; E-M3 vigilancia de sesgo |
| META-E003 | E-M1 primario (detección de corrupción) |
| META-E004 | E-M4 primario; E-M1 obligatorio |

---

## Relación con la jerarquía

| Capa | Régimen |
| ---- | ------- |
| Principio rector | No es “evidencia E-M*”; es condición de posibilidad |
| Kernel | Evaluado por E-M1…E-M5; **puede morir** por tipo de evidencia |
| Código | Ejecuta régimen; no crea conocimiento por sí solo |
| Programas de dominio | Evidencia de dominio (otro modelo); no sustituye E-M* |

---

# FIN — META EVIDENCE MODEL

*Qué cuenta como evidencia sobre el lab.  
Mejora local ≠ mejora global.  
El código ejecuta; no conoce.*
