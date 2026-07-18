# META-E002b — Protocolo experimental **CONGELADO**

**Clase:** investigación del **instrumento** (Selector v0.1)  
**Régimen:** E004.2 / META-E001 (hipótesis, rival, congelado, muerte, perfil)  
**Versión:** **1.0 CONGELADO**  
**Fecha:** 2026-07-17  
**No es:** Selector v2 · “mejorar el Selector” · medalla binaria  

---

## 1. Pregunta

> ¿La reducción de coste del Selector viene de **eliminar ruido** o de **eliminar diversidad**?  
> ¿Qué tipo de **compresión** hace?  
> *Si el Selector tiene razón demasiado rápido, ¿qué está dejando de ver?*

---

## 2. Hipótesis

| ID | Enunciado |
| -- | --------- |
| **H-META-E002b-01** | El Selector reduce coste **principalmente** eliminando **ruido** (cobertura de clases “valiosas latentes” se conserva en gran medida). |
| **H-META-E002b-00** (rival) | El Selector reduce coste **eliminando diversidad** (clases valiosas latentes se concentran en la zona excluida). |

Ambas pueden ganar. Preferible un **mapa de validez** a un binario simple.

---

## 3. Variable / diseño

```text
100 candidatos (Explorador sintético, seed s)
        → Selector v0.1
        → grupo A (priorizados) | excluidos (B+C + no-A)

Control oculto:
  muestra aleatoria de excluidos se etiqueta con clases latentes
  (invisibles al Selector) y se compara con los priorizados
```

| Brazo | Definición |
| ----- | ---------- |
| **Conservados** | grupo A del Selector |
| **Excluidos** | OPEN no en A |
| **Latentes** (solo meta) | `noise` · `common_ok` · `rare_valuable` asignadas en generación |

El Selector **no** ve las etiquetas latentes.

---

## 4. Métricas (no solo % de presupuesto)

| ID | Métrica | Eje |
| -- | ------- | --- |
| **ECO** | reducción budget M2/M1 (referencia E001; se re-mide) | Eficacia E-M2 |
| **COV_RARE** | fracción de `rare_valuable` que caen en A vs en excluidos | Coste / cobertura |
| **DIV_DROP** | 1 − (clusters en A / clusters en todos OPEN) | Diversidad |
| **FN_RATE** | rare_valuable en excluidos / rare_valuable totales | Falso negativo de valor |
| **REV** | ¿registro conserva IDs de excluidos y scores del Selector? (sí/no booleano) | Reversibilidad |

---

## 5. Predicciones y muerte

### H-META-E002b-01 (ruido)

- FN_RATE **&lt; 0.40** y COV_RARE en A **≥ 0.50** de los rare_valuable, en media de réplicas.  
- DIV_DROP **&lt; 0.50**.

### H-META-E002b-00 (diversidad)

- FN_RATE **≥ 0.50** o COV_RARE en A **&lt; 0.35**, o DIV_DROP **≥ 0.55**.

### NO_SABEMOS

- Entre umbrales o discordancia entre métricas sin patrón *a priori*.

### Umbrales de muerte de 01

Si en ≥ **7/10** seeds se cumple el patrón de 00 → **01 DEBILITADA o MUERTA** según severidad (FN_RATE ≥ 0.60 en media → MUERTA de 01).

---

## 6. Ejecución congelada

```text
N_rep = 10 (seeds 0..9)
N_cand = 100
Runner: scripts/run_meta_e002b.py
Salida: META-E002b/resultados/classification.json + REPORT
```

---

## 7. Perfil de evidencia exigido

```text
E-M1: integridad del registro / control oculto documentado
E-M2: economía (re-medida)
E-M3: sesgo / FN de valor (primario de esta campaña)
E-M4: no evaluada (un generador sintético)
E-M5: no evaluada
```

**Local ≠ global.** Mapa de validez, no “el lab es mejor”.

---

## 8. Sello

| Campo | Valor |
| ----- | ----- |
| Congelado | **SÍ** |
| Ejecución | **autorizada** |
| Prohibido | Selector v2; redefinir umbrales post-datos |

---

# FIN — META-E002b PROTOCOL 1.0
