# ATHENA

Athena es un programa de investigación matemática dentro de un laboratorio
metodológico. No es una IA genérica ni un motor de afirmaciones automáticas:
su trabajo es explorar mecanismos sin perder la capacidad de registrar
**no sabemos**, una hipótesis muerta o un bloqueo legítimo.

## Estado al 18 de julio de 2026

~~~text
Instrumento metodológico     operativo y validado
Discovery                    T-01, T-03, T-04, T-05 REFERENCE_COMPLETE
P*                           NONE
Intake                       EMPTY
Gate estructural             NOT CLOSED
T-06                         BLOCKED
H2 real / FLINT real / 006F  BLOCKED
~~~

La frase importante es:

> Infraestructura validada y evidencia reproducida no equivalen a una teoría
> descubierta.

## Empieza aquí

1. Lee [ATHENA_PROJECT_STATUS.md](ATHENA_PROJECT_STATUS.md).
2. Continúa con [ATHENA_PHASE_STATUS.md](ATHENA_PHASE_STATUS.md).
3. Lee [ATHENA_HANDOFF.md](ATHENA_HANDOFF.md) antes de editar, ejecutar o
   interpretar un carril.
4. Consulta el documento fuente del tema concreto.

## Carriles separados

| Carril | Situación | Documento de referencia |
| --- | --- | --- |
| Laboratorio / kernel | CORE y AUDITOR validan disciplina de proceso. | [LABORATORY.md](LABORATORY.md) |
| Discovery | La cartografía está completa hasta T-05; aún no hay candidato. | [ATHENA_MECHANISM_DISCOVERY_SYNTHESIS_v3.md](ATHENA_MECHANISM_DISCOVERY_SYNTHESIS_v3.md) |
| Gate estructural | Debe calibrarse con G-01…G-06. | [ATHENA_GATE_SELF_TEST_SPEC.md](ATHENA_GATE_SELF_TEST_SPEC.md) |
| H2 / L3 | Solo arquitectura inerte; ejecución real prohibida. | [01_CANONICAL_STATE.md](01_CANONICAL_STATE.md) |

## Qué no está autorizado

- Abrir T-06 o una campaña por inercia.
- Fabricar un mecanismo desde los observables E004–E007.
- Tratar una coincidencia o una réplica como teoría.
- Ejecutar H2, FLINT real, certificación de ceros o 006F.
- Cambiar un protocolo, umbral o predicción tras ver el resultado.

## Cómo continuar

Primero preserva y lee el estado. El siguiente trabajo intelectual permitido es
la autoprueba del Gate: demostrar que puede rechazar circularidad, acumulación
decorativa, identidad disfrazada y búsqueda retrospectiva, y que puede
reconocer dos certificados estructurales mínimos.

Para una fotografía completa de qué se incluyó en la instantánea local, consulta
[ATHENA_SNAPSHOT_MANIFEST.md](ATHENA_SNAPSHOT_MANIFEST.md).

---

*Athena no busca una simulación que produzca un patrón. Busca una arquitectura
que obligue una predicción antes de la simulación.*
