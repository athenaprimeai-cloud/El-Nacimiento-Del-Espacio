# Vuelta al dominio Athena

**Estado:** decisión de Era II · el laboratorio se **usa**, no solo se investiga  
**No es:** abandono del meta-programa · promesa de descubrimiento  
**Es:** atacar de nuevo la pregunta original **con** el kernel medido  

---

## Qué problema se resolvía primero

**No** (solo):

> ¿Otra fórmula para generar primos?

Eso ya existe en muchas formas (cribas, generadores parciales, distribución, análisis, etc.).

**Sí** (pregunta grande, abierta):

> ¿Existe una estructura más profunda de la cual los **números primos** emergen como consecuencia natural?  
> ¿Por qué tienen **exactamente** la distribución que tienen?  
> ¿Hay una representación donde esa estructura sea **inevitable**, no un patrón pintado?

Gran parte de las **herramientas** es conocida. La **pregunta profunda** no tiene respuesta aceptada.  
El peligro clásico: enamorarse de un patrón que es (2) artefacto de la transformación, (3) ruido, o (4) elección de representación — no (1) estructura del objeto.

El kernel existe para **golpear la puerta** antes de creer que hay habitación detrás.

---

## Por qué hubo tanta precaución (y cuándo basta)

| Riesgo | Respuesta del proyecto |
| ------ | ---------------------- |
| Patrón bonito ≠ estructura | Controles, rivales, muerte, no generalizar |
| Instrumento que se engaña | META-E sobre Selector, Auditor, economía/diversidad |

**Riesgo contrario ahora real:**

> Volverse tan cuidadoso que **nunca se ataca la montaña**  
> (telescopio apuntando a otro telescopio).

La Era I construyó el equipo.  
La Era II lo probó.  
La montaña sigue siendo:

```text
                PRIMOS
        ¿emergen de una estructura?
```

---

## Respuesta a la pregunta de fondo

| | |
| - | - |
| ¿Todo esto porque ya hay matemática nueva? | **No** |
| ¿Por qué entonces? | Porque el problema no era solo una fórmula: era una forma de investigar **que no se engañe a sí misma** |
| ¿Hay que volver a la matemática? | **Sí** — o el lab solo estudia labs |
| ¿Con miedo? | No: con un sistema que permite **equivocarse dejando huellas** |

---

## Cómo se vuelve (diferencia enorme)

### Antes

```text
Busquemos estructura en los primos
→ algo bonito
→ esperamos que sea real
```

### Ahora

```text
Pregunta matemática
→ hipótesis explícita (ficha)
→ predicción
→ ataques
→ control
→ resultado (incl. NO_SABEMOS / MUERTA)
→ registro
```

El lab **no** evita investigar por miedo.  
Existe **para** poder volver a equivocarse de forma que deje rastro:

- “Parecía una puerta. La golpeamos. Era una pared pintada.”  
- “Resistió los golpes. Vale la pena mirar detrás.”

---

## Qué no se pierde al volver

| Pieza | Uso en dominio |
| ----- | -------------- |
| Core | Fichas, estados, muerte |
| Auditor | Forma del protocolo (no semántica total — E003) |
| Selector | Solo con **límites** (E002b/E004); no juez en exploración abierta |
| Excluidos | Memoria de diversidad si se prioriza |
| META-E | Sigue disponible si el **instrumento** se toca |

---

## Campañas de dominio

| ID | Pregunta | Estado |
| -- | -------- | ------ |
| **DOMAIN-E001** | ¿Firma ~1/6 residual **media** es extrema vs nulos? | **CERRADO** — H-01 **MUERTA** (pared pintada bajo ese control) |
| **DOMAIN-E002** | ¿Entropía espectral se conserva bajo \(\mathcal{R}\) de forma diferencial vs nulos? | **CERRADO** — **DESAPARECE** (H-01 MUERTA) |

Ver `ATHENA_DOMAIN_E002/ATHENA_DOMAIN_E002_PREGUNTA.md`.

No se asume aún simetría global generativa.  
La flecha “principio → espacio → primos” **no** está construida; E002 busca una **pista de conservación** o la mata.

---

# FIN — DOMAIN RETURN

*Equipo medido. Montaña intacta.  
No más telescopio al telescopio por defecto.*
