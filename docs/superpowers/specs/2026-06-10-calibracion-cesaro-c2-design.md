# Calibración Cesàro C2 del Experimento 005A

## Objetivo

Construir un instrumento numérico reproducible que compare el promedio Cesàro de orden 2 de la convolución de von Mangoldt con la fórmula explícita conocida para Goldbach. Esta fase calibra el laboratorio; no busca una frecuencia nueva ni estudia todavía caracteres de Dirichlet.

## Observable

Para

```text
r_G(n) = sum_{m=1}^{n-1} Lambda(m) Lambda(n-m),
```

se calculará

```text
C2(X) = 1/2 * sum_{n<=X} r_G(n) * (1 - n/X)^2.
```

La fórmula truncada corregida de referencia para `k=2` es

```text
C2(X) = X^2/24
        - log(2*pi) X/3
        - 2 sum_rho Gamma(rho)/Gamma(rho+4) X^(rho+1)
        + sum_rho1,rho2 Gamma(rho1)Gamma(rho2)
          / Gamma(rho1+rho2+3) X^(rho1+rho2)
        + terminos explicitos de orden inferior.
```

Bajo RH se analizará

```text
Z1(X) = (C2(X) - X^2/24) / X^(3/2).
```

## Arquitectura

- `athena_azr/cesaro_calibration.py`: von Mangoldt, convolución aditiva, acumuladores de `C2`, malla logarítmica, modelos lineal y doble, y métricas.
- `scripts/run_goldbach_cesaro_calibration.py`: ejecución reproducible, selección de límites y escritura de artefactos.
- `tests/test_cesaro_calibration.py`: pruebas pequeñas y exactas para cada transformación.
- `docs/experimentos/experimento-005a-calibracion-cesaro.md`: protocolo, parámetros y resultados observados.

## Flujo De Datos

1. Generar `Lambda(n)` hasta `X_max` mediante una criba de potencias primas.
2. Obtener `r_G` por convolución FFT conservando sus valores reales. Como `Lambda` contiene logaritmos, `r_G` no es entero; solo se anularán residuos numéricos de magnitud despreciable.
3. Contrastar posiciones seleccionadas con una suma directa exacta.
4. Construir acumuladores `S_j(X) = sum_{n<=X} n^j r_G(n)` para `j=0,1,2`.
5. Evaluar

```text
C2(X) = 1/2 * (S0 - 2*S1/X + S2/X^2)
```

en enteros próximos a una malla uniforme en `log X`.
6. Comparar tres modelos: corrección de polo (`M0`), polo más ceros lineales (`M1`) y polo más términos lineales y dobles (`M2`).
7. Reportar error fuera de muestra, coherencia de amplitud y fase, y estabilidad al aumentar la altura de truncamiento.

## Decisiones De Alcance

- El primer recorrido completo usa `X_max=1_000_000`.
- No se usará FFT sobre la malla logarítmica ni interpolación espectral.
- No se usarán `max-T`, controles aleatorios ni umbrales de descubrimiento en esta calibración determinista.
- Las amplitudes teóricas se mantienen fijas en la comparación principal. Un ajuste libre se reservará como auditoría secundaria.
- Los canales `C03`, `C05`, `C35` y `C15` quedan fuera de alcance.

## Criterios De Validez

El instrumento debe:

- reproducir exactamente casos pequeños de `Lambda`, `r_G` y `C2`;
- hacer coincidir la convolución FFT con la suma directa en puntos de control;
- mostrar mejora fuera de muestra de `M0` a `M1` cuando el rango permita resolver los términos lineales;
- mantener estables los resultados al aumentar el conjunto de ceros;
- registrar por separado el error teórico, el error de truncamiento y el error numérico.

Una discrepancia no se etiquetará como fenómeno nuevo hasta descartar normalización, truncamiento, ceros incompletos, términos auxiliares y precisión numérica.
