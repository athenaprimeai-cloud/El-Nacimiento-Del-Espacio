# Experimento 004: Descomposición de deriva y rueda prima

## Objetivo

Retirar del residuo Goldbach tres estructuras explicables antes de buscar candidatos nuevos:

```text
R0(N) = G(N) / (S(N) * N / log(N)^2)
R1(N) = R0(N) - mean(R0)
R2(N) = R0(N) - (a + b log N)
R3(N) = R2(N) - Pi_M R2(N)
```

`Pi_M` proyecta sobre una base modular conocida construida con:

```text
cos(2 pi k N / q), sin(2 pi k N / q)
q in {3, 5, 7, 11, 13}
k = 1..floor(q/2)
```

## Hipótesis de trabajo

Si los picos principales son residuos de rueda prima pequeña, la energía de `1/6`, `1/10`, `1/5`, `1/14` y armónicos relacionados debe caer después de `R3`.

## Estadística global

Cada pico se compara contra el máximo global no-cero de controles permutados:

```text
p_global = (1 + #{M_b >= P_real}) / (1 + B)
```

Esto evita premiar un pico por haber sido seleccionado después de mirar todo el espectro.

## Interpretación permitida

Este experimento no prueba Goldbach. Tampoco prueba ausencia de estructura nueva. Solo separa:

- deriva casi DC;
- tendencia log-lineal;
- ruedas modulares pequeñas;
- residuo ortogonal restante.

Lo que sobreviva en `R3` será candidato a análisis posterior.

## Corrida inicial

```text
interval: [4, 10000]
modular_primes: [3, 5, 7, 11, 13]
control_seeds: [1436, 2718, 3141, 5772, 16180]
formal_proof: false
```

Energía espectral por etapa:

| Etapa | Energía total | Lectura principal |
| --- | ---: | --- |
| `R0_desingularized` | `1126477.8733590953` | La componente casi-DC retiene `0.99175559` de la energía. |
| `R1_mean_centered` | `9466.6067522850` | Retirar la media elimina casi toda la niebla inicial. |
| `R2_log_detrended` | `9314.8303698238` | El ajuste `a + b log N` aporta una reducción menor frente a la media. |
| `R3_modular_orthogonal` | `7012.8318902791` | La proyección modular reduce energía, pero no deja un residuo vacío. |

Picos principales:

```text
R0:
  0/1 fraction = 0.9917555901
  1/6 fraction = 0.0009917902

R2:
  1/6 fraction = 0.11994097
  1/10 fraction = 0.01929018
  1/5 fraction = 0.00837642

R3:
  1/30 fraction = 0.01059850
  1/6 fraction = 0.00993357
  2/15 fraction = 0.00863409
```

La extracción confirma que el pico `1/6` no desaparece por completo, pero cae desde `0.11994097` en `R2` a `0.00993357` en `R3`. Esto respalda la lectura de residuo modular conocido más que una novedad aritmética establecida.

Con cinco semillas de control, el mejor límite empírico posible para `p_global` es:

```text
1 / (1 + 5) = 0.1666667
```

Por tanto, ningún resultado de esta corrida puede reclamar significancia más fuerte que ese límite. La próxima versión debe ampliar controles si se quiere estimar `p_global` con mayor resolución.
