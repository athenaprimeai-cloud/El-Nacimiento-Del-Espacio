# Calibración Cesàro C2 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implementar y ejecutar la calibración determinista `C2` del canal Goldbach no torcido hasta `X=1_000_000`.

**Architecture:** Un módulo matemático independiente construirá `Lambda`, la convolución aditiva y los acumuladores Cesàro. Un ejecutor producirá CSV y JSON con validaciones pequeñas, métricas por altura de ceros y comparación fuera de muestra de los modelos `M0`, `M1` y `M2`.

**Tech Stack:** Python 3.11+, `numpy`, biblioteca numérica disponible para ceros y gamma compleja, `unittest`.

---

### Task 1: Primitivas aritméticas

**Files:**
- Create: `tests/test_cesaro_calibration.py`
- Create: `athena_azr/cesaro_calibration.py`

- [x] Escribir pruebas para `von_mangoldt_values`, convolución directa y convolución FFT.
- [x] Ejecutar las pruebas y confirmar que fallan por símbolos ausentes.
- [x] Implementar las funciones mínimas.
- [x] Confirmar igualdad exacta en casos pequeños y coincidencia FFT/directa.

### Task 2: Promedio Cesàro

**Files:**
- Modify: `tests/test_cesaro_calibration.py`
- Modify: `athena_azr/cesaro_calibration.py`

- [x] Escribir una prueba que compare acumuladores y definición directa de `C2`.
- [x] Confirmar el fallo esperado.
- [x] Implementar acumuladores `S0`, `S1`, `S2` y evaluación estable de `C2`.
- [x] Ejecutar las pruebas específicas y la suite completa.

### Task 3: Modelo explícito truncado

**Files:**
- Modify: `tests/test_cesaro_calibration.py`
- Modify: `athena_azr/cesaro_calibration.py`

- [x] Probar el coeficiente lineal `-2/[rho(rho+1)(rho+2)(rho+3)]`.
- [x] Probar conjugación y realidad numérica del modelo lineal.
- [x] Probar la gamma compleja y la realidad numérica del modelo doble con conjuntos conjugados.
- [x] Implementar carga verificable de ceros, modelos `M0`, `M1`, `M2` y métricas.

### Task 4: Ejecutor y artefactos

**Files:**
- Create: `scripts/run_goldbach_cesaro_calibration.py`
- Modify: `tests/test_cesaro_calibration.py`
- Create: `docs/experimentos/experimento-005a-calibracion-cesaro.md`

- [x] Probar estructura del resumen y separación descubrimiento/validación.
- [x] Implementar argumentos `--max-x`, `--min-x`, `--log-samples`, `--zero-heights` y `--output-dir`.
- [x] Escribir valores muestreados, métricas por modelo, controles de convolución y metadatos.
- [x] Documentar parámetros, limitaciones y criterio de interpretación.

### Task 5: Ejecución completa y verificación

**Files:**
- Generate: `artifacts/goldbach_cesaro/*`
- Modify: `docs/experimentos/experimento-005a-calibracion-cesaro.md`

- [x] Ejecutar primero un recorrido pequeño y corregir únicamente fallos reproducidos por pruebas.
- [x] Ejecutar `X_max=1_000_000`.
- [x] Ejecutar toda la suite de pruebas.
- [x] Revisar artefactos para valores no finitos, errores de redondeo y contradicciones entre resumen y CSV.
- [x] Registrar resultados sin promoverlos por encima de calibración numérica.

## Self-Review

- La especificación cubre observable, normalización, convolución, modelos, muestreo y validación.
- No se incluyen canales torcidos ni estadística de descubrimiento.
- Cada función nueva se introduce después de una prueba que debe fallar primero.
- El repositorio actual no contiene metadatos Git; por ello el plan no exige commits durante esta ejecución.
