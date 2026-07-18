# Experimento 002: Espectro residual desingularizado

## Estado

```text
status: computationally_verified_on_interval
interval: [4, 10000]
even_inputs: 4999
counterexamples: 0
formal_proof: false
evidence_level: Identificación heurística de firma modular
```

## Objetivo

Separar la rueda modular visible en la Transformada de Goldbach del residuo más fino. El Experimento 001 detectó una línea dominante compatible con `f = 1/6`, atribuible a la modulación `N mod 6` inducida por el primo `3`. El Experimento 002 introduce el factor local:

```text
S(N) = product_{p | N, p > 2} (p - 1) / (p - 2)
```

y estudia:

```text
G(N) / (S(N) * N / log(N)^2)
```

## Canales generados

- `raw_counts`: conteo directo de particiones Goldbach `G(N)`.
- `smooth_residual`: `G(N)` menos tendencia suave por media móvil.
- `desingularized_ratio`: conteo normalizado por el factor local `S(N) * N / log(N)^2`.
- `random_control`: control aleatorio reproducible construido con semilla `1436`.

## Resultado principal

La línea `1/6` aparece con fuerza en el residuo suavizado:

```text
smooth_residual:
  f = 0.1666333267
  nearest = 1/6
  normalized_power = 1.0
```

Después de la desingularización, la misma línea cae:

```text
desingularized_ratio:
  f = 0.1666333267
  nearest = 1/6
  normalized_power = 0.0010000349
```

Esto respalda la lectura del Experimento 001: el pico dominante no era una nueva ley independiente, sino una firma modular esperable de los factores locales, especialmente del primo `3`.

## Interpretación

La desingularización eliminó casi toda la potencia relativa del pico `1/6`. El Albañil debe registrar esto como separación efectiva de la rueda modular primaria. Las señales que sobrevivan después de esta normalización son candidatas más interesantes para experimentos posteriores, siempre bajo clasificación de observación finita.

## Artefactos

- `artifacts/goldbach_desingularized/goldbach_002_channel_values_4_10000.csv`
- `artifacts/goldbach_desingularized/goldbach_002_peaks_4_10000.csv`
- `artifacts/goldbach_desingularized/goldbach_002_summary_4_10000.json`
- `artifacts/goldbach_desingularized/goldbach_002_raw_counts_spectrum_4_10000.csv`
- `artifacts/goldbach_desingularized/goldbach_002_smooth_residual_spectrum_4_10000.csv`
- `artifacts/goldbach_desingularized/goldbach_002_desingularized_ratio_spectrum_4_10000.csv`
- `artifacts/goldbach_desingularized/goldbach_002_random_control_spectrum_4_10000.csv`

## Próximo paso sugerido

Medir estabilidad por subventanas. Un pico posterior a la desingularización solo debe promoverse de observación a evidencia heurística si persiste al variar:

- ventana `[A, B]`;
- radio de tendencia suave;
- semilla del control aleatorio;
- límite superior `N`;
- forma exacta del normalizador.
