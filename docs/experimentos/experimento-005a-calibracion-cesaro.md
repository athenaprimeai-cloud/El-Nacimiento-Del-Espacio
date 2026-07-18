# Experimento 005A: Calibración Cesàro C2

## Objetivo

Comprobar si el laboratorio puede reconstruir, en una escala finita, la contribución conocida de los ceros de `zeta(s)` al promedio Cesàro de orden 2 de la convolución ponderada de Goldbach.

El experimento calibra un canal conocido. No busca una frecuencia nueva.

## Definición

```text
r_G(n) = sum_{m=1}^{n-1} Lambda(m) Lambda(n-m)

C2(X) = 1/2 * sum_{n<=X} r_G(n) * (1 - n/X)^2

Z1(X) = (C2(X) - X^2/24) / X^(3/2)
```

La auditoría posterior a la primera ejecución detectó que el modelo había omitido el término explícito de orden `X` señalado por Brüdern, Kaczorowski y Perelli:

```text
-2 * (zeta'/zeta)(0) * X / Gamma(k+2)
```

Como `(zeta'/zeta)(0) = log(2*pi)` y `k=2`, el término es:

```text
-log(2*pi) * X / 3
```

Después de normalizar por `X^(3/2)`, aporta `-log(2*pi)/(3*sqrt(X))`. El coeficiente teórico `-0.6126256888...` coincide con el `-0.613382...` recuperado de forma ciega en el intervalo de descubrimiento.

Los modelos corregidos son:

- `M0_pole_correction`: término de polo conocido;
- `M1_pole_linear`: `M0` más contribuciones lineales de ceros;
- `M2_pole_linear_double`: `M1` más la suma doble truncada.

El exponente de la suma doble permanece `X^(rho1+rho2)`. La propuesta de sustituirlo por `X^(rho1+rho2+1)` confundía el kernel normalizado `(1-n/X)^k` con el observable no normalizado `(N-n)^k`.

## Parámetros Ejecutados

| Parámetro | Valor |
| --- | ---: |
| Rango | `1000 <= X <= 1000000` |
| Muestras próximas a malla logarítmica | `800` |
| Fracción de descubrimiento | `0.65` |
| Alturas de truncamiento | `50`, `100`, `143` |
| Ceros positivos disponibles | `49` hasta `143.111845...` |

Los ceros proceden de las tablas de Andrew Odlyzko. El programa rechaza alturas superiores a la tabla local en vez de extrapolarlas.

## Validaciones Numéricas

- La convolución FFT fue comparada con sumas directas en puntos seleccionados.
- Error absoluto máximo observado: `3.725290298461914e-09`.
- La identidad acumulada de `C2` coincide con su definición directa en pruebas pequeñas.
- Las 12 pruebas específicas y las 27 pruebas de la suite completa pasan.

## Resultados Fuera De Muestra

| Altura | Modelo | RMSE de validación |
| ---: | --- | ---: |
| `50` | `M0_pole_correction` | `6.980854185627089e-05` |
| `50` | `M1_pole_linear` | `6.649922370701005e-07` |
| `50` | `M2_pole_linear_double` | `6.523382709308774e-07` |
| `100` | `M1_pole_linear` | `1.415537e-07` |
| `100` | `M2_pole_linear_double` | `8.626044e-08` |
| `143` | `M1_pole_linear` | `1.255742e-07` |
| `143` | `M2_pole_linear_double` | `5.757272858089859e-08` |

Para `T=143`, los ceros lineales reducen el RMSE de `M0` en aproximadamente `99.82 %`. La suma doble reduce después el RMSE de `M1` en aproximadamente `54.15 %`.

## Auditoría De Amplitud Y Fase

La estimación secundaria usa únicamente el intervalo de descubrimiento y resta primero el término de polo conocido. Para `T=50`:

- mediana de `amplitud estimada / amplitud teórica`: `1.0719`;
- mediana del error absoluto de fase: `0.3116` radianes;
- primer cero: razón de amplitud `0.9734` y error de fase `-0.0368` radianes.

Los primeros cinco ceros satisfacen simultáneamente el intervalo de amplitud `[0.5, 2.0]` y el límite de fase absoluta `0.5` radianes fijados antes de recalcular el veredicto.

## Veredicto

```text
estado = passed
calibracion_superada = true
canal_base_C00 = calibrado
```

La primera clasificación `inconcluso_por_escala_finita` se debía a una fórmula truncada que omitía el término de polo de orden `X`. No fue causada por el exponente doble ni por una ventana incapaz de resolver el primer cero: el intervalo logarítmico contiene aproximadamente `15.54` ciclos de ese cero.

El resultado valida el instrumento contra estructura conocida. No constituye evidencia de una frecuencia nueva ni una demostración relacionada con Goldbach.

## Próximo Paso Autorizado

El canal base `C00` supera la puerta de calibración. El siguiente paso puede abrir un único canal torcido de control, comenzando por `q=3`, manteniendo:

1. término principal y términos de polo explícitos;
2. separación descubrimiento/validación;
3. amplitudes teóricas fijas en la comparación principal;
4. auditoría secundaria de amplitud y fase;
5. prohibición de etiquetar como novedad cualquier contribución ya explicada por ceros o factores locales conocidos.

## Artefactos

- `artifacts/goldbach_cesaro/goldbach_005a_samples_1000_1000000.csv`
- `artifacts/goldbach_cesaro/goldbach_005a_metrics_1000_1000000.csv`
- `artifacts/goldbach_cesaro/goldbach_005a_convolution_checks_1000_1000000.csv`
- `artifacts/goldbach_cesaro/goldbach_005a_coefficient_audits_1000_1000000.csv`
- `artifacts/goldbach_cesaro/goldbach_005a_summary_1000_1000000.json`

## Referencias

- Languasco y Zaccagnini, `A Cesàro Average of Goldbach numbers`, arXiv:1206.0251.
- Brüdern, Kaczorowski y Perelli, `Explicit formulae for averages of Goldbach representations`, arXiv:1712.00737.
- Cantarini, `Some identities involving the Cesàro average of Goldbach numbers`, arXiv:1711.08610.
- Andrew Odlyzko, `Tables of zeros of the Riemann zeta function`.
