# Experimento 005B: Torsión Mixta C03

## Objetivo

Calibrar el canal mixto

```text
r_03(n) = sum_{m=1}^{n-1} Lambda(m) Lambda(n-m) chi_3(n-m)
```

mediante el producto aditivo de series de Laplace `S_0(z)S_chi3(z)`. El experimento es un control de estructura conocida y no una búsqueda de novedad.

## Definición

```text
C03_2(X) = 1/2 * sum_{n<=X} r_03(n) * (1 - n/X)^2
Z03(X) = C03_2(X) / X^(3/2)
```

El carácter utilizado es el primitivo real e impar módulo `3`:

```text
chi_3(n) = 0, 1, -1 para n mod 3 = 0, 1, 2.
```

## Modelo Truncado

La constante fija es

```text
(L'/L)(0, chi_3)
  = -log(3) + 3 log(Gamma(1/3)/Gamma(2/3))
  = 0.9481988266726209...
```

Por tanto, la contribución de polo en `C03_2` es negativa:

```text
P03(X) = -(L'/L)(0, chi_3) * X / 6.
```

Los modelos comparados son:

- `M0_pole`: corrección de polo;
- `M1_pole_lzeros`: `M0` más ceros de `L(s,chi_3)`;
- `M2_pole_lzeros_cross`: `M1` más pares cruzados zeta–`L`.

No hay pares `L-L`, porque el generador contiene un solo factor `S_chi3`.

## Ceros Y Controles

La tabla local contiene `74` ceros positivos hasta `143.638477...`, evaluados con

```text
L(s,chi_3) = 3^(-s) * (zeta(s,1/3) - zeta(s,2/3)).
```

El primer cero es `8.039737155681468`. Las frecuencias `4.5324` y `7.8096` fueron probadas y rechazadas para este carácter.

## Parámetros

| Parámetro | Valor |
| --- | ---: |
| Rango | `1000 <= X <= 1000000` |
| Muestras | `800` |
| Descubrimiento / validación | `65 % / 35 %` |
| Alturas chi3 | `50`, `100`, `143` |
| Altura zeta | `143` |
| Ceros chi3 usados en el modelo final | `73` |
| Ceros zeta usados | `49` |

## Resultados Fuera De Muestra

| Modelo final, altura `143` | RMSE |
| --- | ---: |
| `M0_pole` | `3.0686971884808526e-04` |
| `M1_pole_lzeros` | `2.2241860234504135e-07` |
| `M2_pole_lzeros_cross` | `1.0618132908362876e-07` |

`M1` reduce el RMSE de `M0` en `99.9275 %`. Los dobles cruzados reducen después el RMSE de `M1` en `52.2606 %`.

El error máximo de la convolución FFT frente a controles directos fue `3.4924596548080444e-10`.

## Amplitud Y Fase

Para los primeros cinco ceros, evaluados mediante ajuste libre solo en descubrimiento después de retirar el polo y los dobles conocidos:

- mediana de la razón de amplitud: `1.0133`;
- mediana del error absoluto de fase: `0.0733` radianes;
- primer cero: razón `0.9981`, error de fase `0.0129` radianes.

Los cinco satisfacen el intervalo de amplitud `[0.5,2.0]` y el límite de fase `0.5` radianes.

El ajuste libre simultáneo de los `73` ceros altos es inestable. Esta observación no afecta la comparación principal, que mantiene coeficientes teóricos fijos, pero limita la afirmación de recuperación individual a los primeros cinco.

## Veredicto

```text
canal = C03
estado = passed
calibracion_superada = true
expansion = controlled_truncation
formula_explicita_completa = false
afirmacion_de_novedad = false
```

El canal `C03` reproduce la jerarquía prevista y recupera los primeros ceros de `L(s,chi_3)` con amplitud y fase correctas. Esto valida la expansión truncada utilizada; no prueba que todos los términos auxiliares de la fórmula completa sean despreciables.

Los canales `C05`, `C35` y `C15` permanecen congelados.

## Artefactos

- `artifacts/c03_series_X1e6.csv`
- `artifacts/c03_metrics_X1e6.csv`
- `artifacts/c03_convolution_checks_X1e6.csv`
- `artifacts/c03_coefficient_audits_X1e6.csv`
- `artifacts/c03_summary_X1e6.json`

## Referencias

- DLMF, sección 25.15, funciones `L` de Dirichlet.
- LMFDB, carácter primitivo `3/2`.
- Cantarini, Gambini y Zaccagnini, `Cesàro averages for Goldbach representations with summands in arithmetic progressions`, arXiv:1911.07220.
- Arb, `acb_dirichlet.h`.
