# ATHENA — CHALLENGE SELECTOR

**Estado legislativo:** **SOPORTADO CON LIMITACIONES** — ver `LEGISLATION_SELECTOR_v0_1.md`  
**Evidencia:** META-E001 (economía+integridad) · META-E002b (diversidad comprimida)  
**No es:** juez de verdad · Selector definitivo · LLM  

---

## Pregunta

> ¿Cuál intento **destruir primero**?

No:

> ¿Cuál es verdadera?

---

## Contrato

```text
Entrada:
  lista de candidatos / hipótesis OPEN (IDs)

Salida:
  orden de prioridad experimental
  grupos A / B / C
  razón por candidato

No decide:
  verdad, archivo terminal, interpretación matemática
```

| Puede | No puede |
| ----- | -------- |
| Ordenar presupuesto de ataque | Aceptar hipótesis como conocimiento |
| Clasificar alto/medio/redundante | Ejecutar controles |
| Exponer puntuaciones auditables | Saltar al registro como “hallazgo” |

---

## Función objetivo

**No:** encontrar la hipótesis correcta.  
**Sí:** maximizar **conocimiento esperado por unidad de experimento** (heurística transparente).

Un buen lab no es el que genera más ideas: es el que decide mejor **qué idea merece ser atacada primero**.

---

## Señales de puntuación (v0.1, deterministas)

| Señal | Idea |
| ----- | ---- |
| **Falsabilidad** | `dies_if` / `weakens_if` concretos (longitud, anclas numéricas, no vacíos) |
| **Novedad** | Baja solapamiento de tokens con otras fichas OPEN |
| **Redundancia** | Alta solapamiento → penaliza (grupo C) |
| **Coste** | Heurística simple (fichas más vagas / más largas = coste mayor) |
| **Completitud de ficha** | Campos presentes y no-ruido |

Puntuación combinada → rango → grupos:

| Grupo | Significado |
| ----- | ----------- |
| **A** | Alta falsabilidad + novedad relativa (atacar primero) |
| **B** | Valor medio |
| **C** | Redundantes / baja falsabilidad / ruido residual |

El Crítico trabaja sobre **A** (y luego B). No sobre los 1000 a la vez.

---

## Flujo

```text
Pregunta → Explorador → N candidatos
                ↓
            Selector
                ↓
         K prioritarios (A)
                ↓
            Crítico → Diseñador → Core → Auditor → Registro
```

---

## Éxito del Selector

**No:** “eligió la hipótesis correcta”.  
**Sí:** orden **auditable**, estable bajo re-ejecución, sin autoridad final; el kernel no se redefine.

---

## Riesgo: sesgo permanente · coste epistemológico

Si siempre favorece muy falsable / barato / novedoso, puede **excluir** hipótesis importantes pero difíciles.

META-E001 midió el **beneficio** (−85 % presupuesto).  
**META-E002b** debe estimar el **precio** (diversidad, cobertura, tipos relegados, sesgo a lo fácil, estabilidad de dominio).

El Selector **no** es componente definitivo: es **hipótesis permanente** — cada versión compite con la anterior bajo META-E.

Eso **no** invalida el Selector.  
Significa que sus heurísticas son **hipótesis metodológicas**, no verdades — y deben investigarse.

Cada puntuación expone algo como:

```text
Falsabilidad: 0.91
Coste: 0.18
Redundancia: 0.07
Prioridad final: A
Confianza del selector: 0.62
```

Meses después (retrospectiva):

- ¿las A sobrevivieron más?
- ¿las C escondían mejores descubrimientos?
- ¿las heurísticas estaban sesgadas?

`build_selector_retrospective_stub()` prepara esa auditoría.

**El Selector también debe poder equivocarse y ser auditado.**

---

## Recurso escaso

Al principio parecía: capacidad de generar hipótesis.  
Ahora: **experimentos**.

El Selector convierte ese hecho en una pieza explícita del lab.

---

## Código

```text
athena_core/selector.py
scripts/run_challenge_selector.py
tests/test_athena_selector.py
```

---

# FIN — CHALLENGE SELECTOR

*Prioriza el ataque. No declara verdad.  
Heurísticas = hipótesis metodológicas.*
