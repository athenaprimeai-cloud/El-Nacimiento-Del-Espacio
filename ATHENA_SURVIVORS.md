# ATHENA — Supervivientes (restricciones empíricas)

**Estado:** documento transversal · **fase de acumulación de evidencia**  
**Fecha de apertura:** 2026-07-18  
**No es:** hipótesis · teoría · interpretación · operador · montaña narrativa  

**Regla de uso:**  
Cualquier modelo futuro \(\mathcal{M}\) se evalúa por **cuántas de estas restricciones satisface** sin violar MD-035 ni las decisiones congeladas del log — no por elegancia.

**Carga de la prueba (invertida):**  
\(\mathcal{M}\) debe encajar en la lista. La lista no se reescribe para encajar en \(\mathcal{M}\).

---

## Restricciones

### S-001

**E001 no sobrevivió.**

- Campaña: DOMAIN-E001  
- Objeto de prueba: pico espectral \(\sim 1/6\) en residual Goldbach (media)  
- Resultado: H-01 **MUERTA** bajo nulos prerregistrados  
- Código: no extremidad vs controles  

### S-002

**E002 no sobrevivió.**

- Campaña: DOMAIN-E002  
- Objeto de prueba: conservación de entropía espectral bajo familia \(\mathcal{R}\)  
- Resultado: **DESAPARECE** (no diferencial vs nulos)  
- Código: `H00_NO_DIFFERENTIAL_CONSERVATION`  

### S-003

**E003 no sobrevivió.**

- Campaña: DOMAIN-E003  
- Objeto de prueba: resistencia de identidad (\(\Delta_{\mathrm{real}}\) vs \(\Delta_{\mathrm{nulo}}\)) bajo ventanas rectangulares y \(D_{1/2}\)  
- Resultado: **DESAPARECE**  
- Código: `H00_NO_DIFFERENTIAL_IDENTITY_RESISTANCE`  
- Nota: FASE 2 borde no abierta (no había sombra que auditar)  

### S-004

**E004 persistió frente a controles (nulo uniforme equicardinal).**

- Campaña: DOMAIN-E004  
- Objeto de prueba: \(M_2\) Laplaciano inducido, grafo ordinal, vs C1 uniforme / C2 / C3  
- Resultado protocolar histórico: PERSISTE vs C1 uniforme  
- **Addendum revisor:** H-00 global **no** muerta con nulo uniforme solo; Cramér es el asesino legítimo de densidad local (→ E005)  
- Restricción operativa: existe firma de \(M_2\) ordinal **distinta** de un conjunto equicardinal uniforme bajo el protocolo E004  

### S-005

**E005 persistió frente a Cramér; E006 persistió frente a rueda 30.**

- **E005:** PERSISTE / `H01_MATERIAL_BEYOND_CRAMER` (sello #1)  
  - Addendum: Cramér es hombre de paja conocido; no implica material “nuevo”  
- **E006:** PERSISTE / `H01_MATERIAL_BEYOND_WHEEL_30` (sello #2)  
  - Curva \(S(W)\) monótona en \(W\in\{1,2,6,30\}\) en \(N=10^5\)  
- Restricción operativa conjunta: la firma **no** se disuelve bajo Cramér ni bajo Cramér-rueda \(W=30\) en los protocolos sellados  

### S-006

**E007 reprodujo clasificación y orden.**

- Campaña: DOMAIN-E007 (réplica, no descubrimiento)  
- Único cambio: \(N=5\cdot 10^4\) (vs \(N=10^5\) en E006)  
- Resultado: **REPRODUCIDA**  
  - class_W30 = PERSISTE  
  - orden \(S(1)>S(2)>S(6)>S(30)\)  
- **No** se reprodujeron (ni se exigieron): valores de \(M_2\), amplitudes de \(S(W)\), ley funcional de la curva  
- Regla: E007 **no** reescribe E006  

---

## Lo que la familia **no** es

Esta lista **no** afirma:

- geometría generativa de primos  
- Hilbert–Pólya  
- conexión con ceros de \(\zeta\)  
- que \(M_2\) sea “la” variable correcta  
- ontología de “material”  

Describe únicamente: **familia reproducida de observables** bajo protocolos prerregistrados.

---

## Tres preguntas obligatorias a cualquier modelo mínimo \(\mathcal{M}\)

Antes de aceptar \(\mathcal{M}\), debe responder **simultáneamente**:

| # | Pregunta | Restricciones que toca |
| - | -------- | ---------------------- |
| **(1)** | ¿Por qué aparece E004? | S-004 |
| **(2)** | ¿Por qué E006 no desaparece bajo rueda 30? | S-005 |
| **(3)** | ¿Por qué la réplica E007 conserva el orden \(S(1)>S(2)>S(6)>S(30)\)? | S-006 |

Si no explica las tres a la vez, \(\mathcal{M}\) **no** ha ganado el derecho a existir en Athena.

Además: no puede violar **S-001…S-003** reinventando como “señal” lo ya matado sin nuevo ID y nuevo control.

---

## Disciplina de fase

| Fase anterior | Fase actual |
| ------------- | ----------- |
| Exploración / linterna | **Acumulación de evidencia** |
| Peligro dominante: falso positivo | Peligro dominante: **modelo demasiado grande** |
| Pregunta: ¿hay señal? | Pregunta: ¿mecanismo mínimo compatible con **todos** los supervivientes? |

**No** abrir E008 experimental por defecto.  
Primero: confrontar propuestas de modelo con esta lista.

---

## Montaña (vocabulario operativo)

```text
¿Operador oculto?
        ↑
¿Geometría generativa?
        ↑
¿Mecanismo mínimo?          ← debe satisfacer S-004, S-005, S-006 (+ no resucitar S-001..003)
        ↑
Familia reproducida de observables
        │
        ├── S-001 E001 muerto
        ├── S-002 E002 muerto
        ├── S-003 E003 muerto
        ├── S-004 E004 persistió (uniforme)
        ├── S-005 E005/E006 persistió (Cramér / rueda 30)
        └── S-006 E007 reprodujo clasificación y orden
```

---

## Historial de ediciones

| Fecha | Cambio |
| ----- | ------ |
| 2026-07-18 | Apertura: S-001…S-006 desde E001–E007 |

*Añadir nuevas filas S-xxx solo con campaña ID y veredicto protocolar — no con narrativa.*

---

# FIN — ATHENA_SURVIVORS

*No hipótesis.  
Restricciones.  
La elegancia no puntúa.*
