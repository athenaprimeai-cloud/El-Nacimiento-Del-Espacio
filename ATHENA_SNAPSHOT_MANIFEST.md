# ATHENA — Manifiesto de instantánea de conservación

**Fecha:** 2026-07-18
**Propósito:** describir el alcance de la primera instantánea versionada del
estado local de Athena. Preservar no equivale a validar científicamente.

## Incluido

- Código de protocolo, auditoría, exploración y certificación inerte:
  athena_core/ y athena_azr/.
- Pruebas y scripts: tests/ y scripts/.
- Documentación de raíz, docs/, META-E*/ y ATHENA_DOMAIN_E005/.
- Resultados y registros pequeños que describen el estado del kernel y sus
  validaciones: todo data/.
- artifacts/: manifiestos, hashes, ledgers y salidas experimentales referidas
  por la documentación. Se conservan como evidencia histórica, no como
  autorización para repetir o extender experimentos.
- El ledger actualizado de E006 ya presente en el árbol de trabajo.

## Excluido deliberadamente

| Ruta o clase | Razón |
| --- | --- |
| .venv/, .venv-*/, venv/, venv-*/ | Entornos locales recreables. |
| __pycache__/ y .pytest_cache/ | Cachés recreables. |
| .kiro/ | Estado local de herramienta, no evidencia del proyecto. |

## Garantías de la operación

- No se ejecutan T-06, H2 real, FLINT real, 006F ni un experimento nuevo.
- No se borran, mueven ni reinterpretan artefactos excluidos.
- Incluir un resultado conserva su procedencia; no lo transforma en teoría,
  P* ni autorización.
- La instantánea se verifica con el estado de Git y pruebas locales antes de
  cerrarse.

## Continuidad

Después de esta instantánea, el punto de entrada es README.md. La navegación
continúa en ATHENA_PROJECT_STATUS.md y ATHENA_HANDOFF.md.

---

*Preservar antes de reorganizar. Separar evidencia, código y caché antes de
interpretar progreso.*
