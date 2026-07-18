# Experimento 005F: protocolo de auditoría residual C03-B

## 1. Estado y prohibiciones

```text
experiment_id = G5B-005F
target = C03B_residual_audit
status = preregistered_protocol_only
implementation = not_authorized
execution = not_authorized
artifacts = none
tests = none
novelty_claim = false
C05 = provisional_quarantined
C05_PREEXECUTION_AUDIT = blocked_on_residual_null_model
C05_RERUN = forbidden
C35 = frozen
C15 = frozen
```

Este protocolo no autoriza implementación ni ejecución. Cualquier código,
corrida o artefacto derivado requerirá una autorización posterior explícita,
emitida después de revisar y congelar este documento.

Queda expresamente prohibido durante esta fase:

1. crear o modificar módulos Python, ejecutores o pruebas;
2. recalcular métricas de C03-B;
3. escribir CSV, JSON u otros artefactos experimentales;
4. modificar los artefactos o el código histórico de C03-B;
5. tocar la cuarentena o el protocolo sellado de C05;
6. usar este documento para abrir C35 o C15;
7. interpretar una estructura residual como novedad matemática.

## 2. Motivación y estado heredado

El Experimento 005C superó los controles estructurales de ablación, frecuencias
incorrectas, signo del polo y persistencia de amplitud/fase. No superó el
criterio de blancura residual. Su test max-T histórico informó un máximo en
`omega = 2.15`, inferior a la resolución de Rayleigh `2.6048624785` del segmento
de validación. El residuo mostró además una correlación aproximada de `-0.79`
con `log X`.

Las permutaciones dentro de clases módulo 3 destruyeron esa deriva suave. Por
ello, su `p_FWER = 0.001` histórico no se acepta como p-valor calibrado para una
frecuencia nueva: el supuesto de intercambiabilidad no quedó justificado.

El estado heredado permanece:

```text
controles_estructurales = superados
robustness_passed = false
C03B_residual_audit = open
residual_class = unresolved_low_frequency_drift
novelty_status = not_established
```

## 3. Principio de triangulación

La futura auditoría seguirá este orden obligatorio:

```text
componente mecanicista H1
-> componente mecanicista H2
-> componente mecanicista H3
-> diagnóstico del residuo combinado
-> admisibilidad de modelos nulos H4
-> inferencia estadística, solo si H4 es admisible
```

No se permitirá seleccionar retrospectivamente el subconjunto de correcciones
que produzca el mejor resultado. Se informarán el residuo histórico, cada
hipótesis por separado y la secuencia acumulativa completa `H1 -> H2 -> H3`.

La inferencia primaria se realizará sobre el residuo acumulativo completo. Si
H2 no dispone de ceros certificados o H3 no dispone de una derivación congelada
antes de la futura ejecución, el veredicto estadístico será `inconclusive`.

## 4. Observable y particiones congeladas

La futura implementación deberá reconstruir el mismo observable normalizado de
C03-B:

```text
Z03(X) = C03_2(X) / X^(3/2)

R0(X) = Z03(X)
      - M0_pole(X)
      - M1_L3_zeros(X; T=143)
      - M2_zeta_L3_cross(X; T_zeta=143, T_L3=143).
```

No se reutilizará el p-valor histórico como evidencia. Los valores históricos
solo sirven para justificar este protocolo.

Parámetros congelados para una futura solicitud de ejecución:

```text
X_min = 1000
window_maxima = [10000, 30000, 100000, 300000, 1000000]
primary_windows = [100000, 300000, 1000000]
log_samples_per_window = 800
discovery_fraction = 0.65
validation_fraction = 0.35
frequency_scan = [0.5, 143.0]
frequency_step = 0.05
spectral_window = Hann
max_T_controls_per_configuration = 999
random_seed = 20260612
```

Cada ventana conservará su propia división cronológica descubrimiento/validación.
Ningún coeficiente estimado en validación podrá volver al modelo.

## 5. Métricas permitidas

Sea `u = log X` y sea `P_R(omega)` la potencia espectral normalizada con la
misma ventana Hann utilizada en 005C. Para cada segmento de validación:

```text
delta_R = 2*pi / (max(u) - min(u))

E_low(R)  = sum P_R(omega), 0.5 <= omega < delta_R
E_high(R) = sum P_R(omega), delta_R <= omega <= 143
```

Las métricas permitidas son:

1. RMSE y MAE fuera de muestra;
2. `E_low` y `E_high`;
3. coeficientes mecanicistas y su estabilidad entre ventanas;
4. autocorrelación de retardos `1..32` en el orden logarítmico observado;
5. tendencia lineal respecto de `u`;
6. varianza local en ocho intervalos de igual anchura en `u`;
7. media, varianza y cuantiles `0.10`, `0.50`, `0.90` por clase `X mod 3`;
8. máximo espectral global y su frecuencia;
9. p-valor max-T empírico con corrección global.

No se agregarán métricas después de observar una futura corrida. Cualquier
métrica adicional requerirá una nueva versión preregistrada de 005F.

## 6. H1: términos auxiliares omitidos

### 6.1 Base congelada

H1 utilizará exclusivamente la base normalizada:

```text
f1(X) = X^(-1/2)
f2(X) = X^(-1/2) log X
f3(X) = X^(-1)
f4(X) = X^(-1) log X
f5(X) = X^(-3/2)
```

No se permitirán potencias, logaritmos, quiebres o suavizadores adicionales.
Los cinco coeficientes se estimarán conjuntamente por mínimos cuadrados solo en
descubrimiento y se evaluarán sin reajuste en validación.

### 6.2 Predicción cuantitativa

Si la deriva procede de residuos auxiliares de polo o ceros triviales, la base
debe explicar una porción estable y decreciente de baja frecuencia. H1 recibe
`diagnostic_support` únicamente si, en cada una de las tres ventanas primarias:

1. reduce el RMSE de validación al menos `10 %` respecto de `R0`;
2. reduce `E_low` al menos `50 %`;
3. no aumenta `E_high` más de `5 %`;
4. al menos un coeficiente es distinto de cero a dos errores estándar en las
   tres ventanas;
5. todo coeficiente activo conserva signo y difiere como máximo `30 %` de su
   mediana entre ventanas.

Si falla una condición, H1 se clasificará `not_supported_at_current_scale`. No
se retirarán términos para mejorar el ajuste después de observar los datos.

## 7. H2: cola de ceros no triviales

### 7.1 Alturas congeladas

```text
T_L3 = [143, 200, 300, 500]
T_zeta = [143, 200, 300, 500]
```

Todos los ceros adicionales deberán estar certificados antes de cualquier
ejecución futura. La fuente, precisión, cantidad y hash de ambas tablas deberán
figurar en una autorización posterior. No se ajustarán frecuencias ni amplitudes:
se usarán exclusivamente los coeficientes teóricos de la expansión truncada.

### 7.2 Predicción cuantitativa

Si la deriva es una envolvente producida por truncar la cola, al elevar
simultáneamente las alturas debe observarse una convergencia ordenada. H2 recibe
`diagnostic_support` únicamente si:

1. el RMSE de validación no aumenta en la secuencia `143 -> 200 -> 300 -> 500`;
2. la altura 500 mejora el RMSE al menos `10 %` frente a la altura 143 en cada
   ventana primaria;
3. la altura 500 reduce `E_low` al menos `50 %` frente a la altura 143;
4. `E_high` no aumenta más de `5 %`;
5. la norma de cada contribución incremental conserva su orden de magnitud y
   varía como máximo `30 %` entre las tres ventanas primarias.

Una tabla no certificada, una frecuencia ajustada o una mejora no monótona
implican `H2_status = not_supported_or_not_auditable`.

## 8. H3: términos de borde Cesàro

H3 no podrá medirse hasta que exista una derivación analítica independiente de
la diferencia entre:

```text
kernel Cesàro discreto usado por el laboratorio
vs.
inversión continua Mellin/Laplace usada por la fórmula truncada.
```

La derivación deberá fijar antes de la ejecución:

1. forma funcional exacta de cada corrección;
2. signo;
3. exponente en `X` y posibles potencias de `log X`;
4. coeficiente teórico o regla no ajustable para obtenerlo;
5. orden del resto uniforme en las ventanas declaradas.

No se aceptará una base empírica denominada posteriormente “borde”.

H3 recibe `diagnostic_support` únicamente si la corrección congelada:

1. mejora el RMSE de validación al menos `10 %` en cada ventana primaria;
2. reduce `E_low` al menos `50 %`;
3. no aumenta `E_high` más de `5 %`;
4. presenta la potencia, signo y razón de amplitud predichos, con desviación
   máxima de `30 %` entre teoría y observación en cada ventana;
5. decrece con `X` según el orden uniforme derivado.

Sin derivación previa, el estado obligatorio será `H3_status = not_auditable`.

## 9. H4: modelos nulos dependientes y heterocedásticos

### 9.1 Preprocesamiento común

H4 se aplicará al residuo acumulativo `R123` después de H1, H2 y H3, sin
selección retrospectiva.

En descubrimiento se estimará un modelo de tendencia y escala deliberadamente
limitado:

```text
media:  alpha_0 + alpha_1*u + efectos fijos de X mod 3
log escala: beta_0 + beta_1*u + efectos fijos de X mod 3
```

No se permitirán splines, polinomios de grado superior, puntos de quiebre ni
selección automática. Las innovaciones estandarizadas se generarán bajo cada
nulo y luego se reconstruirán usando la tendencia, escala y clase modular
congeladas desde descubrimiento.

### 9.2 Familias preregistradas

**N1. Wild bootstrap dependiente**

Multiplicadores gaussianos con covarianza Bartlett y longitudes:

```text
ell = [8, 16, 32, 64]
```

**N2. Bootstrap circular por bloques**

Remuestreo circular de innovaciones estandarizadas con longitudes:

```text
ell = [8, 16, 32, 64]
```

**N3. Sustitutos de fase**

Aleatorización de fases de las innovaciones estandarizadas, preservando módulo
de Fourier, componente DC, frecuencia de Nyquist y simetría conjugada. Después
se restituirán tendencia, escala y efectos módulo 3.

Cada configuración producirá `999` controles usando la semilla base declarada
y una derivación determinista por familia y longitud.

### 9.3 Admisibilidad obligatoria

Un modelo nulo no podrá producir p-valores hasta pasar todas estas pruebas en
las tres ventanas primarias:

**Tendencia**

- la pendiente observada respecto de `u` cae dentro del intervalo central de
  `90 %` de controles;
- la pendiente mediana simulada difiere como máximo `15 %` de la observada.

**Varianza local**

- se usan ocho intervalos fijos de igual anchura en `u`;
- la varianza observada cae en el intervalo central de `90 %` en al menos siete
  de ocho intervalos;
- el error relativo mediano de las varianzas simuladas no supera `15 %`.

**Dependencia**

- la autocorrelación observada cae dentro del intervalo central de `90 %` en al
  menos 29 de los 32 retardos;
- la máxima diferencia absoluta entre ACF observada y ACF mediana no supera
  `0.10`.

**Energía de baja frecuencia**

- `E_low` observada cae dentro del intervalo central de `90 %`;
- la razón `mediana(E_low_control) / E_low_observada` pertenece a `[0.8,1.25]`.

**Distribución módulo 3**

- para cada clase `0,1,2`, la media, varianza y cuantiles `0.10`, `0.50`, `0.90`
  observados caen dentro de sus intervalos centrales de `90 %`.

Cada longitud de N1 y N2 constituye una configuración distinta. Solo las
configuraciones que pasan todos los criterios se denominan `admissible_null`.
Ningún umbral podrá ajustarse después de observar los controles.

### 9.4 Ausencia o insuficiencia de nulos

```text
si configuraciones_admisibles = 0:
    null_model_status = no_admissible_null
    statistical_verdict = inconclusive

si familias_admisibles < 2:
    null_model_status = insufficient_null_diversity
    statistical_verdict = inconclusive
```

No se forzarán p-valores cuando el modelo nulo sea inadecuado.

## 10. Filtro estadístico de estructura remanente

Solo si al menos dos familias diferentes contienen configuraciones admisibles
se calculará max-T en la banda preregistrada `0.5 <= omega <= 143`, con paso
`0.05` y corrección por el máximo global de cada control.

Una estructura remanente atraviesa el filtro únicamente si:

1. obtiene `p_FWER <= 0.05` bajo todas las configuraciones admisibles;
2. su frecuencia supera `delta_R` en cada ventana primaria;
3. existe una frecuencia común `omega_star` tal que el máximo de cada ventana
   cae dentro de `omega_star +/- delta_R/2`;
4. mantiene el mismo signo de fase proyectada en las tres ventanas;
5. no coincide, dentro de una resolución de Rayleigh, con una frecuencia ya
   incluida por H1-H3 o con un cero conocido incorporado al modelo.

Incluso si cumple todo:

```text
classification = unexplained_residual
novelty_claim = false
proof_status = none
```

Un resultado que no supere Rayleigh seguirá siendo
`unresolved_low_frequency_drift`, aunque su p-valor numérico sea pequeño.

## 11. Árbol de decisión final

```text
si H2 no tiene tablas certificadas:
    verdict = inconclusive

si H3 no tiene derivación congelada:
    verdict = inconclusive

si null_model_status en [no_admissible_null, insufficient_null_diversity]:
    verdict = inconclusive

si existe estructura que pasa todos los nulos admisibles y Rayleigh:
    verdict = unexplained_residual
    novelty_claim = false

en otro caso:
    verdict = residual_explained_or_not_detected_at_current_scale
    novelty_claim = false
```

El soporte de H1, H2 o H3 es diagnóstico, no una demostración de una fórmula
explícita completa.

## 12. Archivos que deberán protegerse en una fase futura

Antes de cualquier implementación autorizada deberán calcularse y congelarse
hashes SHA-256 de:

1. código, pruebas, ejecutor, documento y seis artefactos históricos de C03-B;
2. artefactos base C00 y C03 usados para reconstruir el observable;
3. `docs/experimentos/experimento-005d-c05-derivacion.md`;
4. `docs/experimentos/experimento-005e-c05-final-review.md`;
5. todo el directorio de cuarentena `artifacts/goldbach_cesaro/c05_controlled/`;
6. `artifacts/goldbach_cesaro/c05_rerun_clean/C05_SEALED_PROTOCOL.json`;
7. este documento 005F ya revisado y congelado.

La futura auditoría escribirá, si es autorizada, en un directorio nuevo. Nunca
reutilizará `c03b_stress_tests`, `c05_controlled` ni `c05_rerun_clean`.

## 13. Diseño de una implementación futura

Una solicitud posterior podrá proponer componentes separados para:

1. reconstrucción inmutable de `R0`;
2. evaluación fuera de muestra de H1;
3. carga certificada y evaluación de H2;
4. evaluación de la corrección H3 previamente derivada;
5. estandarización fija de tendencia y escala;
6. generación y validación de N1, N2 y N3;
7. max-T bajo configuraciones admisibles;
8. escritor de artefactos aislado e inventario de hashes.

Esta enumeración no constituye autorización para crear esos componentes.

## 14. Condiciones para solicitar autorización posterior

Solo podrá pedirse autorización de implementación cuando existan conjuntamente:

1. revisión humana explícita y congelamiento de 005F;
2. tablas de ceros de zeta y `L(s,chi_3)` hasta altura 500 certificadas;
3. derivación completa y revisada de H3;
4. lista exacta de archivos protegidos y sus hashes;
5. especificación de formatos de salida en un directorio nuevo;
6. confirmación escrita de que C05, C35 y C15 permanecen bloqueados;
7. autorización explícita distinta para código;
8. autorización explícita posterior y distinta para ejecución.

## 15. Estado final

```text
experiment_id = G5B-005F
target = C03B_residual_audit
method = mechanistic_then_multi_null_triangulation
status = preregistered_protocol_only
implementation = not_authorized
execution = not_authorized
new_artifacts = none
new_tests = none
rerun = false
novelty_claim = false
C03B_residual_audit = protocol_defined_not_executed
C05 = provisional_quarantined
C05_PREEXECUTION_AUDIT = blocked_on_residual_null_model
C05_RERUN = forbidden
C35 = frozen
C15 = frozen
```

## Referencias

1. Experimento 005C, `docs/experimentos/experimento-005c-c03b.md`.
2. Experimento 005D,
   `docs/experimentos/experimento-005d-c05-derivacion.md`.
3. Experimento 005E-R,
   `docs/experimentos/experimento-005e-c05-final-review.md`.
4. Y. Rho y X. Shao,
   [Bootstrap-Assisted Unit Root Testing With Piecewise Locally Stationary
   Errors](https://arxiv.org/abs/1802.05333), para bootstrap dependiente en un
   marco no estacionario/localmente estacionario.
5. J. B. Hill y K. Motegi,
   [A Max-Correlation White Noise Test for Weakly Dependent Time
   Series](https://arxiv.org/abs/1602.04107), para inferencia bootstrap sobre
   residuos débilmente dependientes y máximos globales.
6. D. Prichard y J. Theiler,
   [Generating surrogate data for time series with several simultaneously
   measured variables](https://arxiv.org/abs/comp-gas/9405002), para el uso y
   las limitaciones de sustitutos con fases aleatorizadas.
