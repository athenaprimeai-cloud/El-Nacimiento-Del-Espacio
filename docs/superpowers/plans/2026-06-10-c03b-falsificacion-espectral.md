# C03-B Falsificacion Espectral Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Construir y ejecutar una auditoria aislada que intente falsificar la calibracion C03 mediante frecuencias incorrectas, ablacion, ventanas de escala, inversion del polo, persistencia fuera de muestra y controles max-T.

**Architecture:** Un modulo nuevo reutiliza solo las funciones publicas y los datos matematicos congelados de `c03_laplace_chi3.py`. Calcula una unica convolucion hasta `X=10^6`, deriva todas las ventanas desde sus momentos prefijos y escribe exclusivamente en un directorio nuevo. Las huellas SHA-256 de C00 y de los artefactos C03 se toman antes y despues de la ejecucion.

**Tech Stack:** Python 3.12, NumPy, `unittest`, CSV y JSON de la biblioteca estandar.

---

### Task 1: Nucleo de auditoria y controles deterministas

**Files:**
- Create: `athena_azr/c03b_stress.py`
- Test: `tests/test_c03b_stress.py`

- [ ] **Step 1: Write failing tests for wrong frequencies, ablation models, pole inversion, modular permutations, spectral statistics, and immutable-file hashing.**
- [ ] **Step 2: Run `python -m unittest tests.test_c03b_stress -v` and verify failures are caused by the missing module.**
- [ ] **Step 3: Implement the smallest public functions needed by those tests.**
- [ ] **Step 4: Run the focused suite and verify all new unit tests pass.**

### Task 2: Construccion integral del experimento

**Files:**
- Modify: `athena_azr/c03b_stress.py`
- Modify: `tests/test_c03b_stress.py`

- [ ] **Step 1: Write a failing integration test for the five windows, the 0/1/2/4/8 ablations, discovery-validation separation, 999-compatible max-T controls, and explicit no-novelty metadata.**
- [ ] **Step 2: Run the focused integration test and verify the expected failure.**
- [ ] **Step 3: Implement one-pass convolution, per-window audits, deterministic RNG, max-T FWER, and pass/fail diagnostics without changing C03.**
- [ ] **Step 4: Run the complete C03-B test module and verify it passes.**

### Task 3: Artefactos, ejecutor y documentacion

**Files:**
- Create: `scripts/run_c03b_stress.py`
- Create: `docs/experimentos/experimento-005c-c03b.md`
- Modify: `athena_azr/c03b_stress.py`
- Modify: `tests/test_c03b_stress.py`

- [ ] **Step 1: Write failing tests for independent CSV/JSON output, immutable hashes, and absence of C05/C35/C15 output.**
- [ ] **Step 2: Run the artifact tests and verify the expected failure.**
- [ ] **Step 3: Implement the writer and command-line runner, then document hypotheses, controls, thresholds, and limitations.**
- [ ] **Step 4: Run the focused tests and verify all pass.**

### Task 4: Ejecucion completa y verificacion

**Files:**
- Create: `artifacts/goldbach_cesaro/c03b_stress_tests/c03b_summary_X1e6.json`
- Create: `artifacts/goldbach_cesaro/c03b_stress_tests/c03b_ablation_X1e6.csv`
- Create: `artifacts/goldbach_cesaro/c03b_stress_tests/c03b_windows_X1e6.csv`
- Create: `artifacts/goldbach_cesaro/c03b_stress_tests/c03b_wrong_frequencies_X1e6.csv`
- Create: `artifacts/goldbach_cesaro/c03b_stress_tests/c03b_max_t_X1e6.csv`
- Create: `artifacts/goldbach_cesaro/c03b_stress_tests/c03b_immutability_X1e6.csv`

- [ ] **Step 1: Run the complete experiment with five windows, 800 logarithmic samples, and 999 modular permutations.**
- [ ] **Step 2: Verify post-run hashes equal pre-run hashes and inspect all reported metrics.**
- [ ] **Step 3: Run the entire project test suite.**
- [ ] **Step 4: Re-read the generated JSON and CSV files and report the actual verdict, including any failed falsification criterion.**

