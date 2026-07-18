# Constitución, legislación e ingeniería

**Propósito:** proteger las reglas ya existentes clasificando **autoridad**, no añadir una constitución paralela de contenido.  
**Diseño del kernel:** congelado (`KERNEL_FREEZE.md`) hasta evidencia META-E.  

---

## Tres niveles de autoridad

```text
CONSTITUCIÓN
    ↓
Legislación metodológica
    ↓
Ingeniería
```

| Nivel | Función | Cambio |
| ----- | ------- | ------ |
| **Constitución** | Protege la **identidad** del laboratorio | Acontecimiento **excepcional** |
| **Legislación metodológica** | Reglas del régimen investigable | Solo con **evidencia META-E** (pueden morir) |
| **Ingeniería** | Implementa un régimen | Conservación epistemológica; **no** define el lab |

Ante un cambio propuesto, la **primera** pregunta es:

> **¿Qué nivel está intentando modificar?**

El procedimiento sigue de esa respuesta — no de “¿es buena idea?”.

---

## Nivel 1 — Constitución (extremadamente estable)

Sin esto, el laboratorio **deja de ser** ese laboratorio.

| Documento / pieza | Rol |
| ----------------- | --- |
| `ATHENA_PRINCIPIO_RECTOR.md` | Brújula |
| `LABORATORY.md` | Identidad: brújula / kernel / programas |
| `01_CANONICAL_STATE.md` | **Solo** la parte constitucional de identidad y fase (no el ledger de fases runtime 006H*) |
| `KERNEL_FREEZE.md` | Carga de la prueba: no cambiar kernel sin evidencia |
| `META_EVIDENCE_MODEL.md` | Régimen de qué cuenta como evidencia meta (E-M*) + conservación epistemológica + código no crea conocimiento |

**Procedimiento de cambio:** excepcional, explícito, decision log MD-*, no “mejora incremental”.

---

## Nivel 2 — Legislación metodológica (falsable)

Vive lo que puede **evolucionar o morir** vía META-E.

| Ejemplos |
| -------- |
| Heurísticas del Selector |
| Estados del kernel (si se redefinen) |
| Contratos de componentes (si cambian el régimen) |
| Protocolos META-E (META-E001, …) |
| Pipeline (qué capas existen y cómo se acoplan) |
| `ATHENA_CHALLENGE_SELECTOR.md`, `ATHENA_EXPLORER.md`, contratos de ataque/control cuando definen régimen |
| Decisiones MD-* que no son constitucionales |

**Procedimiento de cambio:** hipótesis META-E → perfil E-M* → adopción o rechazo.  
**Nunca** por “parece mejor”.

---

## Nivel 3 — Ingeniería (no define el laboratorio)

| Ejemplos |
| -------- |
| Código Python (`athena_core/`) |
| CLI, tests, scripts |
| Rust u otro stack |
| LLMs |
| UI, paralelización, optimización de rendimiento |
| Formato de archivos **si** no altera el significado de la evidencia |

**Procedimiento de cambio:** conservación epistemológica.  
Si el cambio **altera** el significado de la evidencia → es **metodológico** (nivel 2), no ingeniería.

---

## Tabla de enrutamiento

| Propuesta | Nivel | Acción |
| --------- | ----- | ------ |
| Cambiar la brújula | 1 Constitución | **No** (casi nunca) |
| Nueva heurística del Selector | 2 Legislación | META-E |
| Python → Rust, mismo régimen | 3 Ingeniería | Conservación |
| Redefinir `MUERTA` | 2 (o 1 si rompe identidad) | META-E / excepcional |
| Añadir componente “porque es cool” | ¿? | Filtro: ¿hipótesis metodológica? Si no → fuera |
| Optimizar CLI | 3 | Ingeniería |

---

## Señal de evolución madura

Ver también `PROJECT_ERA.md`: **Era I (diseño) cerrada · Era II (investigación) activa**.

El siguiente avance importante **no** es otro documento de diseño.

Es que un documento de **legislación metodológica** cambie porque un **META-E** produjo evidencia suficiente, mientras la **constitución** permanece intacta.

> El laboratorio ya no evoluciona por imaginación; evoluciona por evidencia.

**Señal de salud:** la legislación crece **más lento** que la evidencia que la justifica  
(evitar inflación metodológica: no una regla nueva por cada resultado).

---

## Relación con la jerarquía de muerte

| Capa | Puede morir |
| ---- | ----------- |
| Constitución (brújula + identidad mínima) | Solo en crisis de identidad (excepcional) |
| Legislación metodológica | **Sí** (META-E) |
| Ingeniería | Se reemplaza sin drama si conserva el régimen |
| Hipótesis de dominio / meta | **Sí** |

---

# FIN — CONSTITUTION AND LAW

*La ingeniería implementa.  
La legislación experimenta.  
La constitución protege la identidad.*
