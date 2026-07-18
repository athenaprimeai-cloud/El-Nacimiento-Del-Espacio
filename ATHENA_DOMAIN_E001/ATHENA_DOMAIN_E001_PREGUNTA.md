# ATHENA DOMAIN-E001 — Pregunta (primera campaña de dominio post-kernel)

**Estado:** pregunta + protocolo **ejecutados** · ver `ATHENA_DOMAIN_E001_REPORT.md` (H-01 MUERTA)  
**Programa:** Athena (nivel 3) sobre kernel medido  
**No es:** META-E · Selector v2 · “hemos encontrado la estructura de los primos”  

---

## Contexto

La pregunta **grande** del programa Athena sigue viva:

> ¿Existe una arquitectura matemática donde los primos no son una lista misteriosa,  
> sino una **consecuencia necesaria** de una estructura más profunda?

DOMAIN-E001 **no** cierra esa pregunta.  
Es el **primer peldaño** de vuelta a la montaña: una subpregunta **falsable** y acotada.

---

## Pregunta de DOMAIN-E001 (propuesta)

> Bajo un protocolo congelado de **residuos / transformada / control aleatorio**  
> (familia ya usada en el historial Athena de artefactos),  
> ¿un pico o regularidad observada en datos de Goldbach/primos  
> **sobrevive** a controles de (a) barajado, (b) modelo nulo, (c) cambio de ventana,  
> o se comporta como **artefacto** de la representación?

En una línea:

> **¿Esta señal concreta es estructura del objeto o de la transformación?**

---

## Hipótesis (borrador)

| ID | Enunciado |
| -- | --------- |
| **H-ATH-D001-01** | La señal predeclarada **resiste** los controles nulos del protocolo (apoyo relativo a estructura del objeto **bajo este control**). |
| **H-ATH-D001-00** | La señal **colapsa** bajo nulos/barajado/ventana (compatible con artefacto / ruido / método). |

Ambas son éxitos del lab.  
“Pared pintada” es un resultado **válido** y valioso.

---

## Uso del kernel

| Pieza | Rol |
| ----- | --- |
| Core | Ficha, predicción, muerte, estados |
| Auditor | Forma del protocolo (recordar E003: no confiar semántica ciega) |
| Selector | **No** como juez único en exploración abierta; si se usa, con control de excluidos |
| Registro | Archivar también MUERTA y NO_SABEMOS |

---

## Qué no es esta campaña

- Demostrar la distribución de primos  
- Nueva fórmula generadora “profunda” por defecto  
- Más META-E salvo que se toque el instrumento  

---

## Siguiente

Congelar `ATHENA_DOMAIN_E001_PROTOCOL.md` con:

- señal concreta a atacar (elige un artefacto/resultado ya en el repo o uno nuevo acotado),  
- controles nulos exactos,  
- umbrales,  
- seeds,  
- perfil de no-afirmaciones.

Luego: ejecución → informe.

---

# FIN — DOMAIN-E001 PREGUNTA

*Volver a la montaña. Golpear la puerta.  
Si es pared pintada, el lab también gana.*
