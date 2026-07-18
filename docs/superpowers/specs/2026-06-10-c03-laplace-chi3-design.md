# Experimento 005B: Canal mixto C03

## Objetivo

Construir y ejecutar una calibración independiente del canal mixto

```text
r_03(n) = sum_{m=1}^{n-1} Lambda(m) Lambda(n-m) chi_3(n-m)
```

hasta `X=1_000_000`, usando el producto de series de Laplace `S_0(z) S_chi3(z)`. El experimento valida estructura conocida; no busca frecuencias nuevas.

## Carácter

El carácter primitivo real e impar módulo `3` queda definido por

```text
chi_3(n) =  0  si n = 0 mod 3
chi_3(n) =  1  si n = 1 mod 3
chi_3(n) = -1  si n = 2 mod 3
```

Los canales `C05`, `C35` y `C15` permanecen fuera de alcance.

## Observable

```text
C03_2(X) = 1/2 * sum_{n<=X} r_03(n) * (1 - n/X)^2
Z03(X) = C03_2(X) / X^(3/2)
```

No existe término `X^2/24`: `S_chi3` no tiene polo en `s=1`.

## Expansión Truncada Controlada

Sea

```text
c_chi = -(L'/L)(0, chi_3)
      = log(3) - 3 log(Gamma(1/3)/Gamma(2/3))
      = -0.9481988266726...
```

Para `k=2`, la contribución de polo de orden `X` es

```text
P03(X) = c_chi * X / Gamma(4) = c_chi * X / 6.
```

La expansión utilizada será

```text
C03_2(X) ~= P03(X)
             - sum_rhoL Gamma(rhoL)/Gamma(rhoL+4) X^(rhoL+1)
             + sum_rhoZ,rhoL Gamma(rhoZ)Gamma(rhoL)
               / Gamma(rhoZ+rhoL+3) X^(rhoZ+rhoL).
```

Bajo GRH:

- los términos lineales de `L(s, chi_3)` tienen orden `X^(3/2)` y amplitud constante en `Z03`;
- el polo y los dobles cruzados tienen orden `X` y decaen como `X^(-1/2)` en `Z03`;
- los términos lineales de ceros de zeta multiplicados por la constante de `S_chi3`, y los términos de ceros de `L` multiplicados por la constante de `S_0`, son de orden inferior y quedan reservados para la fórmula completa.

No se incluyen pares `L-L`: el generador es el producto mixto `S_0 S_chi3`, con un solo factor torcido.

## Modelos

- `M0_pole`: solo `P03(X)/X^(3/2)`.
- `M1_pole_lzeros`: `M0` más los ceros no triviales de `L(s, chi_3)` con amplitudes teóricas fijas.
- `M2_pole_lzeros_cross`: `M1` más pares cruzados zeta–`L`.

La auditoría libre de amplitud y fase utilizará exclusivamente el intervalo de descubrimiento y restará primero `M0` y, para evaluar los lineales, la contribución `M2-M1` conocida.

## Ceros De Control

La tabla local comienza con

```text
8.039737155681...
11.249206207773...
15.704619176722...
```

Cada valor se valida numéricamente mediante

```text
L(s, chi_3) = 3^(-s) * (zeta(s, 1/3) - zeta(s, 2/3)).
```

Los valores `4.5324` y `7.8096` se rechazan explícitamente porque no son ceros de este carácter.

## Separación Y Criterio

- Malla de `800` enteros próximos a uniformidad en `log X`.
- `65 %` para descubrimiento y `35 %` para validación.
- Convolución FFT contrastada con suma directa.
- Éxito principal: `RMSE(M1) < RMSE(M0)` en validación.
- Éxito completo truncado: `RMSE(M2) < RMSE(M1)` y recuperación de los primeros cinco coeficientes lineales con razón de amplitud en `[0.5, 2.0]` y error absoluto de fase menor o igual a `0.5` radianes.

Si la tabla de ceros o la fórmula truncada no bastan para superar estos criterios, el estado será `inconclusive_truncated_expansion`, no descubrimiento ni refutación.

## Archivos

- `athena_azr/c03_laplace_chi3.py`: carácter, función L de control, convolución, modelos y experimento.
- `scripts/run_c03_laplace.py`: ejecutor reproducible.
- `tests/test_c03_laplace_chi3.py`: pruebas matemáticas y de aislamiento.
- `docs/experimentos/experimento-005b-c03.md`: protocolo y resultados.
- `artifacts/c03_series_X1e6.csv`: serie muestreada.
- `artifacts/c03_summary_X1e6.json`: resumen y veredicto.

## Limitaciones

El modelo es una expansión truncada controlada. No incluye todavía todos los ceros triviales, residuos de polos negativos ni todos los términos auxiliares de la fórmula explícita completa. Ningún resultado se promoverá a evidencia de novedad.
