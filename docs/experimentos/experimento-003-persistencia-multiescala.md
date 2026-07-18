# Experimento 003: Persistencia multiescala y nulidad controlada del residuo Goldbach

## Objetivo

Evaluar si los picos que sobreviven a la desingularización local persisten al deformar el laboratorio. Un pico solo puede promoverse si aparece en varias ventanas, mantiene frecuencia estable y supera controles aleatorios reproducibles.

## Ventanas iniciales

```text
[4, 2500]
[4, 5000]
[4, 7500]
[4, 10000]
[1000, 4000]
[3000, 6000]
[5000, 8000]
[7000, 10000]
```

## Controles

Semillas iniciales:

```text
1436, 2718, 3141, 5772, 16180
```

El control implementado en esta fase permuta el canal real seleccionado con semilla reproducible. Esto conserva distribución de valores, pero destruye orden temporal. Controles más duros, como fases Fourier aleatorizadas y surrogates con tendencia/factor modular preservados, quedan como extensión posterior.

## Métricas por candidato

```text
candidate_frequency
nearest_rational
windows_detected
coverage
mean_frequency
frequency_std
mean_power_fraction
control_percentile
normalizers_survived
classification
```

## Clasificación

- `evidencia_heuristica_multiescala`: cobertura alta, estabilidad dentro de resolución media y percentil de control alto.
- `observacion_persistente`: aparece en varias ventanas y supera controles de forma moderada.
- `observacion_local`: insuficiente persistencia o ventaja sobre controles.

## Regla de honestidad

Este experimento no prueba Goldbach ni Riemann. Su función es filtrar picos que podrían merecer análisis posterior.
