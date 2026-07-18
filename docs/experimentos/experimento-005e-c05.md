# Experimento 005E: canal mixto C05

> **CUARENTENA METODOLÓGICA:** esta corrida se ejecutó antes de sellar el
> protocolo confirmatorio final. Sus datos se preservan como evidencia
> exploratoria, pero C05 no pertenece al linaje oficial y no puede justificar
> C35, C15 ni afirmaciones nuevas.

## Objetivo

Evaluar la expansión truncada controlada del canal

```text
r_05(n) = sum Lambda(m) Lambda(n-m) chi_5(n-m)
```

con la contribución local derivada en el Experimento 005D:

```text
M0_05(X) = X/6 * (H3 - b0 - log X).
```

## Modelos predeclarados

- `M0_local`: fondo local con `X log X`.
- `M1_local_lzeros`: M0 más ceros lineales de `L(s,chi_5)`.
- `M2_local_lzeros_cross`: M1 más cruces zeta-`L_5`.

El generador es `S_0 S_chi5`; no se incluyen pares `L_5`-`L_5`.

## Criterios

La corrida provisional evaluó, fuera de muestra:

1. `RMSE(M1) < RMSE(M0)`;
2. `RMSE(M2) < RMSE(M1)`;
3. razón de amplitud del primer cero en `[0.9,1.1]`;
4. error absoluto de fase del primer cero no mayor que `0.1` radianes;
5. inmutabilidad de C00, C03 y C03-B.

El resultado seguirá marcado como `controlled_truncation`, sin fórmula explícita
completa y sin afirmación de novedad.

## Parámetros ejecutados

| Parámetro | Valor |
| --- | ---: |
| Rango | `1000 <= X <= 1000000` |
| Muestras logarítmicas | `800` |
| Descubrimiento / validación | `65 % / 35 %` |
| Alturas de `L_5` | `50`, `100`, `143` |
| Ceros de `L_5` bajo altura 143 | `85` |
| Ceros de zeta bajo altura 143 | `49` |

## Resultados fuera de muestra

| Altura | Modelo | RMSE |
| ---: | --- | ---: |
| `50` | `M0_local` | `6.038552803358335e-04` |
| `50` | `M1_local_lzeros` | `5.473609043397165e-07` |
| `50` | `M2_local_lzeros_cross` | `4.797578457343575e-07` |
| `100` | `M1_local_lzeros` | `2.850278429100215e-07` |
| `100` | `M2_local_lzeros_cross` | `1.3407110445103656e-07` |
| `143` | `M1_local_lzeros` | `2.804768036978571e-07` |
| `143` | `M2_local_lzeros_cross` | `1.2596052747994743e-07` |

En el corte final, M1 reduce el RMSE de M0 en `99.9536 %`. Los cruces
zeta-`L_5` reducen después el RMSE de M1 en `55.09 %`. M2 queda en
`0.02086 %` del RMSE de M0.

## Primer cero

Para

```text
gamma_5,1 = 6.648453344727717,
```

el ajuste efectuado únicamente en descubrimiento recupera:

```text
razón de amplitud = 0.9992089893414787
error de fase     = -0.014388805355039835 rad
```

Ambas métricas satisfacen los umbrales numéricos usados por la corrida. Esto no
equivale a una aprobación confirmatoria, porque el protocolo final no quedó
sellado antes de observar estos resultados.

## Integridad

- error máximo FFT frente a controles directos: `1.8977175386680756e-10`;
- archivos protegidos: `26`;
- archivos protegidos modificados: `0`.

## Veredicto

```text
channel = C05
numerical_calibration_passed = true
calibration_passed = false
implementation_status = provisional_quarantined
official_status = not_accepted
retrospective_approval = rejected_for_now
final_review = pending
eligible_for_downstream_use = false
expansion_status = controlled_truncation
explicit_formula_complete = false
novelty_claim = false
stress_audit = not_run
C35 = frozen
C15 = frozen
```

Los números son compatibles con la estructura truncada elegida hasta `X=10^6`,
pero no constituyen una calibración oficial. No demuestran GRH, Goldbach ni una
fórmula nueva. C05 todavía no ha pasado una fase de falsificación análoga a
C03-B ni un rerun limpio con protocolo previamente sellado.

## Artefactos

- `artifacts/goldbach_cesaro/c05_controlled/c05_series_X1e6.csv`
- `artifacts/goldbach_cesaro/c05_controlled/c05_metrics_X1e6.csv`
- `artifacts/goldbach_cesaro/c05_controlled/c05_coefficient_audits_X1e6.csv`
- `artifacts/goldbach_cesaro/c05_controlled/c05_convolution_checks_X1e6.csv`
- `artifacts/goldbach_cesaro/c05_controlled/c05_immutability_X1e6.csv`
- `artifacts/goldbach_cesaro/c05_controlled/c05_summary_X1e6.json`
