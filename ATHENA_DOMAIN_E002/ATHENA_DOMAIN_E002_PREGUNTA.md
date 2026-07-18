# ATHENA DOMAIN-E002 — Pregunta (simetría candidata mínima)

**Estado:** pregunta de dominio · **no** protocolo · **no** ejecución  
**Después de:** DOMAIN-E001 (pico ~1/6 residual media → **MUERTA** vs nulos)  
**No es:** operador de Riemann · demostración · “hemos encontrado la variedad”  

---

## Deuda conceptual (explícita)

La arquitectura actual de Athena **no asume** todavía una simetría global generativa.

Hasta ahora el flujo ha sido:

```text
objeto observado → transformación → señal candidata → nulos
```

La pregunta tipo Riemann empuja hacia:

```text
principio generador → espacio/operador → restricciones → primos/ceros como consecuencia
```

La **flecha superior** (principio → espacio) **aún no está construida**.  
DOMAIN-E002 no la inventa: busca una **pista mínima** (conservación) que justifique o mate la búsqueda de ese espacio.

---

## Tres principios globales (implícitos, no axiomas)

| # | Principio | Idea | Estado en Athena |
| - | -------- | ---- | ---------------- |
| 1 | **Invarianza bajo representación** | Si es real, no debería depender en exceso de cómo se mira (ventana, escala, base, espectro) | E001: la firma 1/6 en residual media **no** tuvo invarianza / extremidad frente a nulos |
| 2 | **Conservación de información** | ¿Hay una cantidad que una transformación “correcta” no debe destruir? (diversidad, entropía, energía espectral, …) | Eco del Selector: menos exploración → posible pérdida estructural |
| 3 | **Dualidad discreto-continuo** | Primos y ceros (u otros duales) como idiomas del mismo objeto | Aspiracional; no formalizado |

---

## Pregunta de DOMAIN-E002

**No:**

> ¿Cuál es el operador oculto?

**Sí:**

> **¿Existe alguna cantidad global aproximadamente conservada al cambiar la representación del sistema primo / Goldbach residual?**

Formalmente (candidato):

\[
|P(X)-P(T(X))| < \varepsilon
\]

para una familia predeclarada de transformaciones \(T\) “equivalentes” y una propiedad \(P\).

Si esa conservación **no** aparece → la búsqueda del espacio generador empieza desde una **ilusión** (o hay que cambiar \(P\)/\(T\) con **nuevo ID**).  
Si aparece → pista de simetría; **no** teorema.

### Lectura riemanniana (laboratorio, no literatura)

E001: *¿este pico es real o sombra?*  
E002: *si hay estructura real, **qué permanece** cuando cambiamos la luz con la que la miramos?*

Ahí empieza la búsqueda de una “geometría” subyacente **como hipótesis atacable**, no como mito.

---

## Candidatos a \(P\) (a elegir en el protocolo; no todos a la vez)

| \(P\) | Notas |
| ----- | ----- |
| Distribución de gaps (resumen) | |
| Densidad local en ventanas | |
| Energía espectral (total / bandas) | |
| Entropía de histograma de residuos | |
| Correlaciones de largo alcance | |
| Estructura modular (firma en residuos mod m) | |

Una campaña = **un** \(P\) + **una** familia de \(T\) + nulos.

---

## Hipótesis (borrador)

| ID | Enunciado |
| -- | --------- |
| **H-ATH-D002-01** | Existe \(P\) predeclarada que permanece estable bajo la familia \(T\) y **no** bajo nulos que rompen la estructura del objeto. |
| **H-ATH-D002-00** | Ninguna \(P\) de la lista predeclarada muestra conservación diferencial vs nulos (compatible con no-simetría en este régimen, o \(P\)/`T` mal elegidos). |

---

## Uso del lab

Ficha Core · nulos · muerte · NO_SABEMOS.  
Selector **no** como juez de exploración abierta.  
Auditor de **forma**; semántica a cargo del protocolo y del informe (E003).

---

## Montaña

```text
¿estructura fundamental → primos?
        ↑
DOMAIN-E001: una sombra (1/6, residual media) no resistió
DOMAIN-E002: ¿hay algo que se conserve al cambiar la luz?
```

---

## Siguiente

Congelar protocolo eligiendo **un** \(P\) y **una** familia \(T\) + \(\varepsilon\) + nulos.  
Ejecutar. Archivar. Sin operador todavía.

---

# FIN — DOMAIN-E002 PREGUNTA

*No el operador. La simetría mínima.  
Si no se conserva nada, no hay variedad que proyectar.*
