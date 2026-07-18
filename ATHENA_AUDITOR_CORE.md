# ATHENA — AUDITOR CORE (PASO 2)

**Estado:** autorizado · implementación mínima  
**No es:** juez científico · IA · descubrimiento  
**Es:** vigilancia de que el laboratorio no rompa sus reglas  

> El auditor no dice: «esta hipótesis es verdadera».  
> Dice: «este proceso incumplió la regla X».

**Pregunta del paso:**

> ¿Puede una máquina revisar que el propio laboratorio no haya roto sus reglas?

---

## Contrato

```text
ENTRA:
- ficha de hipótesis
- historial de decisiones / audit log
- resultados
- protocolo usado (implícito en el núcleo)

REVISA:
- cambios post-resultado
- ausencia de controles al cerrar
- estados inválidos
- pérdida de registros (intento de borrado)
- conclusiones superiores a la evidencia (p.ej. SOPORTADA sin control)

SALE:
- PASS
- WARN
- FAIL
  + lista de hallazgos
```

**NO ENTRA:** interpretación matemática · verdad de la hipótesis · generación de candidatos.

---

## Relación con PASO 1

| Núcleo | Auditor |
| ------ | ------- |
| Impone disciplina al **escribir** | Revisa disciplina al **leer** el registro |
| Rechaza operaciones ilegales en caliente | Detecta inconsistencias residuales y violaiones de política |
| Guardián de la escritura | Guardián de la lectura / cierre de ciclo |

Ambos: **puertas**, no reyes.

---

## Código

```text
athena_core/auditor.py
tests/test_athena_auditor_core.py
```

---

# FIN — AUDITOR CORE

*Guardián de puertas. No rey del laboratorio.*
