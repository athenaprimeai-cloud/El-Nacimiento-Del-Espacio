# ATHENA — Taxonomía de mecanismos mínimos (Phase III)

**Estado:** borrador de inventario · **no** lista de candidatos de intake  
**Fecha:** 2026-07-18  
**Ancla:** MD-061 · `ATHENA_MECHANISM_DISCOVERY.md`  
**Regla:** **no** diseñar entradas mirando veredictos E004–E007  

---

## Propósito

Clasificar **familias** de mecanismos compatibles con MD-035  
(sin divisibilidad / gcd / factores en la geometría o en \(E\)),  
**sin** pretender explicar los primos ni acomodar S-004…S-006.

Cada fila es material de **discovery**, no ℳ-ID.

---

## Preguntas de inventario (para cada familia)

1. ¿Puede producir **clustering ordinal**?  
2. ¿Puede producir **escalas monotónicas** (análogo de \(S(W)\))?  
3. ¿Puede ser **estable al cambiar \(N\)**?  
4. ¿Puede diferir de controles de **igual densidad**?  
5. ¿Opera sin contrabando aritmético?

Respuestas: `sí` / `no` / `?` (hipótesis de inventario, no resultado experimental).

---

## Tabla maestra

| ID | Familia | Estado | Info OK | Info NO | Salida | Clust. | Mono. \(S\) | Estab. \(N\) | ≠ dens. | Phase |
| -- | ------- | ------ | ------- | ------- | ------ | ------ | ----------- | ------------ | ------- | ----- |
| T-01 | Ocupación binaria + exclusión local | \(x_i\in\{0,1\}\) | vecindad \(\|i-j\|\le k\) | primos, factores | conjunto ocupado | — | — | — | — | **REFERENCE_COMPLETE** (`discovery/T01_STATUS.md`) |
| T-03 | Autómata 1D / Wolfram \(r=1\) | config binaria | vecindad \(2r+1\), tabla \(f\) | T-01 raw, Athena, factores | ocupación tras \(T\) | — | — | — | — | **REFERENCE_COMPLETE** (`discovery/T03_STATUS.md`) |
| T-02 | Hard-core / repulsión en la línea | min dist \(d\) entre 1s | posiciones, \(d\) | \(p\mid n\), gcd en \(E\) | conjunto | ? | ? | ? | ? | inventario |

| T-04 | Renovación / gaps paramétricos | puntos en \(\mathbb{N}\) | ley de gaps (params) | “porque primo” | conjunto | ? | ? | ? | ? | inventario |
| T-05 | Embedding + umbral | \(T:i\mapsto\mathbb{R}^d\) | \(T(i)\), \(\varepsilon\) | \(T\) vía factores | ocupación/aristas | ? | ? | ? | ? | inventario |
| T-06 | Memoria finita | estado \(s_t\) finito | \(s_t\), ventana | primalidad | ocupación | ? | ? | ? | ? | inventario |
| T-07 | Exclusión por capacidad local | cupo en ventanas | conteos locales | factorización | conjunto | ? | ? | ? | ? | inventario |
| T-08 | Proceso de contacto / infección 1D | estados salud/ocup. | vecinos | aritmética | conjunto | ? | ? | ? | ? | inventario |

*Ampliar filas en commits Phase III. No promover a Intake sin generador ciego + P\*.*

---

## Fichas breves

### T-01 — Ocupación + exclusión local

```text
estado:   x[1..N] ∈ {0,1}
update:   x_i depende solo de x en |j-i|≤k
params:  k, f (tabla o fórmula finita), init
salida:  { i : x_i = 1 }
MD-035:  E del grafo de Athena no se redefine con gcd; esto es el ℳ generador del conjunto
```

### T-02 — Hard-core

```text
regla:   no dos ocupados a distancia < d
params:  d, o densidad + muestreo condicional
nota:    d es parámetro libre, no primorial ni “mod primos” disfrazado
```

### T-03 — Autómata

```text
regla:   f : {0,1}^{2r+1} → {0,1}
tiempo:  T pasos desde semilla
salida:  soporte de 1s
```

### T-04 — Renovación

```text
gaps:    ~ distribución parametrizada (exp, log-normal truncada, …)
nota:    comparar vs controles misma densidad es legítimo en discovery;
         no copiar rueda W=30 como definición de ℳ “porque E006”
```

### T-05 — Embedding

```text
T:       mapa sintético (p.ej. coords de proceso / ruido fijo / curva)
arista:  ||T(i)-T(j)|| < ε  →  solo si el ℳ define grafo propio
prohibido: T(i) = (i mod p, …) con p primo como “geometría profunda” sin declarar
```

### T-06 — Memoria finita

```text
s_{t+1} = g(s_t, ventana local)
ocupar t según s_t
```

---

## Criterio de promoción (Discovery → Candidate)

Una entrada T-0x **no** es candidato hasta:

1. Generador ciego especificado e implementable  
2. Ensemble de comportamiento documentado **sin** mirar CSV Athena  
3. Filtro blando vs S-004…S-006 (sí/no/parcial) **después**  
4. \(P^*\) peligrosa extraída  
5. Paquete Intake 1–7  

---

## Historial

| Fecha | Cambio |
| ----- | ------ |
| 2026-07-18 | Apertura T-01…T-08 esqueleto |

---

# FIN — TAXONOMY

*Inventario, no museo de explicaciones.*
