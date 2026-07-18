# META-E003 — Pregunta (pre-protocolo)

**Estado:** pregunta prioritaria post-E004 · **no** protocolo · **no** ejecución  
**Objeto:** el **Auditor** (guardián del proceso)  
**Prioridad:** #1 por jerarquía de dependencia (si el Auditor falla, se erosiona la confianza en E001–E004 y en E00x futuros)  

---

## Lectura previa (cerrada)

```text
Selector v0.1
  E001  → economía
  E002b → coste de diversidad
  E004  → el coste reaparece en otros dominios sintéticos
  → herramienta con régimen de aplicación (no bueno/malo)
```

---

## Pregunta

**No:** “¿El Auditor funciona?”

**Sí:**

> ¿Existe un tipo de fallo metodológico que puede **atravesar** el sistema  
> porque el Auditor **comparte los mismos supuestos** que debería vigilar?

El enemigo no es solo una puerta rota.  
Es una puerta **perfectamente cerrada en la pared equivocada**.

---

## Qué ya se demostró (unitario)

| | |
| - | - |
| Violaciones conocidas | detección / bloqueo (FT-CORE, casos A/B/C) |
| Escenario | relativamente **limpio** |

---

## Qué falta (prueba difícil)

```text
corrupción compleja / a escala
        ↓
¿sigue viendo la grieta?
```

Ejemplos de ataque (borrador de diseño):

| Tipo | Idea |
| ---- | ---- |
| Cumplimiento formal vacío | Registro completo, interpretación sesgada |
| Pérdida de información con forma correcta | Estados válidos, significado empobrecido |
| Métrica “válida” mala | El Auditor acepta porque el formato es correcto |
| Optimización para pasar auditoría | Protocolo cosmético que satisface reglas y esconde el fallo |
| Escala | Muchas decisiones/registros; grieta rara |

---

## Hipótesis (borrador)

| ID | Enunciado |
| -- | --------- |
| **H-META-E003-01** | El Auditor detecta (o bloquea) una clase predeclarada de corrupciones complejas/a escala con tasa ≥ umbral. |
| **H-META-E003-00** | Existe al menos una clase predeclarada de fallo que **pasa** al Auditor compartiendo sus supuestos (falso negativo de vigilancia). |

Si 00 gana: victoria del régimen — el guardián también merece ser vigilado / rediseñado (legislación, no constitución).

---

## Relación con la cadena de confianza

```text
Auditor
   ↓
confianza en E001, E002b, E004, futuros E00x
   ↓
investigación de dominio
```

---

## No hacer todavía

- Rediseñar el Auditor “porque sí”  
- Confundir tests unitarios con E003 cerrado  
- Selector v2  

**Siguiente:** protocolo congelado → batería de corrupciones complejas → perfil → decisión.

---

# FIN — META-E003 PREGUNTA

*¿Los ojos del lab tienen manchas en el lente?*
