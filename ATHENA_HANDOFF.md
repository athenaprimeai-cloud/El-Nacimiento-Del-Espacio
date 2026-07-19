# ATHENA — Handoff canónico

**Fecha:** 2026-07-18
**Propósito:** permitir continuidad sin reconstruir el proyecto desde
conversaciones, nombres de carpetas o resultados aislados.
**Autoridad:** este documento orienta; nunca autoriza una ejecución por sí solo.
Cuando haya conflicto, prevalece el documento fuente más reciente dentro de su
propio carril.

## Regla canónica de continuidad

~~~text
ATHENA_HANDOFF.md
  → verificar ba33893
  → identificar carril
  → leer la autoridad documental correspondiente
  → aplicar el Gate correspondiente
  → solo entonces actuar
~~~

**Punto de restauración canónico:** **ba33893515dc9c3129c44ac1da5214c444a557b4**
(ba33893).

**Réplica remota verificable:** la rama **main** de
https://github.com/athenaprimeai-cloud/El-Nacimiento-Del-Espacio contiene ese
commit en su historia. Athena ya no depende exclusivamente de esta máquina para
restaurar ese estado. Esta réplica conserva historia y evidencia; no valida
resultados científicos ni concede autorizaciones de ejecución.

## Orden de lectura de contexto

~~~text
ATHENA_HANDOFF
  → verificar ba33893
  → identificar carril
  → ATHENA_PROJECT_STATUS
  → ATHENA_PHASE_STATUS
  → documento fuente específico
~~~

## Qué es Athena

Athena es el primer programa científico de un laboratorio metodológico. El
objetivo no es convertir una señal numérica en una teoría ni “hacer una IA que
resuelva Goldbach”. El objetivo es investigar mecanismos bajo un régimen que
preserve controles, errores y la salida **NO_SABEMOS**.

La Era I de diseño del laboratorio está cerrada. La Era II está activa: la
evidencia decide qué permanece o cambia.

## Estado de los tres carriles

| Carril | Estado | No inferir |
| --- | --- | --- |
| Kernel | CORE, AUDITOR y validación del kernel funcionan bajo sus contratos. | Que existe una teoría matemática. |
| Discovery | T-01, T-03, T-04 y T-05 son REFERENCE_COMPLETE; P* es NONE; Intake está vacío. | Que una nueva simulación o T-06 esté justificada. |
| H2/L3 | 006H18 es la referencia de gobernanza; 006H16 es fake-only. | Que H2 esté certificada o que FLINT real esté permitido. |

E004–E007 dejaron restricciones supervivientes bajo protocolos sellados. Un
mecanismo futuro tendría que explicar S-004, S-005 y S-006 sin romper las
prohibiciones; todavía no existe ese mecanismo.

## El cuello de botella

El bloqueo principal no es capacidad de cómputo. Es el Gate estructural:

~~~text
¿Puede el Gate distinguir una restricción genuina
de una reformulación tautológica?
~~~

La secuencia de calibración es:

~~~text
R0
  → M4/M5 del Memory Axis Gate
  → R5
  → R4
~~~

R4 protege la autoprueba desde su diseño; no se deja para después de mirar sus
resultados.

## No hacer

- No fabricar un candidato a partir de E004–E007, espectros o gráficos.
- No reutilizar evidencia de descubrimiento como validación confirmatoria.
- No ajustar parámetros, métricas, escalas o umbrales tras ver resultados.
- No abrir T-06 sin R-DIV + M1–M5 de Discovery congelados.
- No ejecutar H2 real, FLINT real, 006F ni generar tablas de ceros.
- No usar una prueba sintética como certificación matemática.

## Siguiente trabajo permitido

1. Mantener esta instantánea, su réplica remota y la navegación canónica.
2. Congelar cada prueba G-01…G-06 contra su expectativa.
3. Ejecutar, evaluar y registrar cada resultado sin usar datos de Athena ni
   ejecutar un experimento de dominio.
4. Corregir el criterio ante una discrepancia y volver a congelarlo antes de
   reevaluar.

~~~text
self-test implementado ≠ self-test aprobado ≠ Gate aprobado
~~~

Un PASS de la autoprueba solo significaría que el Gate es apto para evaluar un
futuro candidato. No crea P*, no resuelve R1–R3 y no desbloquea T-06, que
permanece bloqueado.

## Fuentes por pregunta

| Pregunta | Fuente |
| --- | --- |
| ¿Qué es el laboratorio? | LABORATORY.md y PROJECT_ERA.md |
| ¿Qué restricciones debe explicar un mecanismo? | ATHENA_SURVIVORS.md |
| ¿Cómo entra un candidato? | ATHENA_MECHANISM_INTAKE.md |
| ¿Por qué T-06 está bloqueado? | ATHENA_MECHANISM_DISCOVERY_SYNTHESIS_v3.md |
| ¿Qué debe pasar el Gate? | ATHENA_GATE_SELF_TEST_SPEC.md |
| ¿Qué está permitido en H2/L3? | 01_CANONICAL_STATE.md |

**Deuda abierta H2/L3:** stale_006E8_documented_inventory.

---

*Primero identificar el carril y su autoridad. Después trabajar. Nunca usar
progreso de infraestructura como sustituto de una teoría.*
