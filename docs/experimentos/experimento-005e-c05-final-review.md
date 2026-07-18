# Experimento 005E-R: revisión final y cuarentena de C05

## 1. Decisión

```text
C05_RETROSPECTIVE_APPROVAL = rejected_for_now
C05_WITHDRAWAL = authorized_as_official_candidate_only
DELETE_FILES = false
KEEP_QUARANTINE_ARCHIVE = true
C05_FINAL_REVIEW = required
```

C05 queda retirado del linaje oficial sin borrar ni revertir archivos. La
implementación y sus resultados se conservan como archivo exploratorio
provisional. Ningún resultado C05 puede justificar C35, C15 o una afirmación de
novedad.

### Distinción de conteos

```text
manifest_c05_quarantine = 17 archivos
protected_files_in_archived_run = 26 archivos
```

Los 17 son archivos pertenecientes al paquete C05 inventariado en cuarentena,
incluidos fuentes, documentación, artefactos y cachés generadas. Los 26 son un
conjunto diferente: archivos externos de C00, C03 y C03-B cuyos hashes fueron
vigilados durante la corrida histórica para comprobar que C05 no los modificó.
Los conteos miden universos distintos y no deben sumarse ni compararse como si
fueran el mismo inventario.

## 2. Motivo metodológico

El Experimento 005D exigía seis condiciones conjuntas antes de descongelar C05.
La implementación se ejecutó antes de sellar el protocolo final y antes de
resolver todas esas condiciones. En particular, los falsificadores y el diseño
confirmatorio definitivo no quedaron fijados antes de observar los resultados.

Esta contaminación es temporal y metodológica. No demuestra que las fórmulas o
los números sean falsos; impide tratarlos como evidencia confirmatoria oficial.

## 3. Auditoría de la implementación contra 005D

| Elemento | Implementación observada | Estado de revisión |
| --- | --- | --- |
| Carácter `chi_5` | `(1,-1,-1,1)` y cero en múltiplos de 5 | Coincide con 005D |
| Constante `b0` | `-0.022024657838726918...` fijada en código | Coincide numéricamente; el código no repite las tres verificaciones independientes |
| Fondo M0 | `(H3-b0-log X)/(6 sqrt(X))` en el observable normalizado | Signo y factor `1/6` coinciden con 005D |
| Primer cero | `6.648453344727717` | Residuo directo pequeño; falta certificación externa de la tabla completa |
| M1 | Coeficiente `-1/[rho(rho+1)(rho+2)(rho+3)]` | Coincide con la truncación declarada |
| M2 | Cruces zeta-`L5` | Coincide con `S0*S_chi5`; no incluye pares `L5-L5` |
| Inmutabilidad | 26 archivos protegidos sin cambios en la corrida archivada | Superada para esa ejecución |
| Fórmula explícita completa | Declarada falsa | Correcto |
| Inventario auxiliar | No hay inventario completo de polos, ceros triviales y bordes | Pendiente |
| Protocolo previo | Finalizado después de observar resultados C05 | No cumple 005D |

## 4. Partes rescatables

Se conservan como trabajo técnico útil:

1. La derivación local de 005D para `L(0,chi_5)=0`, `b0` y el término `X log X`.
2. La implementación del carácter, la convolución aditiva y los modelos M0/M1/M2.
3. Las pruebas unitarias de identidades locales, FFT, Cesàro e inmutabilidad.
4. Los CSV y JSON existentes como evidencia exploratoria reproducible.
5. Las métricas observadas, siempre rotuladas como provisionales y no oficiales.

No se rescatan como evidencia confirmatoria:

1. La antigua declaración `calibration_passed = true`.
2. El uso de los resultados para abrir C35 o C15.
3. La presentación de los umbrales observados como protocolo preregistrado.
4. Cualquier afirmación de novedad, GRH o Goldbach.

## 5. Condiciones pendientes

Antes de autorizar un rerun limpio deben cerrarse estas condiciones:

1. Revisión independiente del signo y del factor `1/6` de M0.
2. Evidencia independiente para la identidad funcional de `b0` y sus tres rutas
   de verificación: Hurwitz, ecuación funcional y Cauchy.
3. Tabla de ceros de `L(s,chi_5)` certificada o auditada contra una fuente
   independiente, con procedencia y precisión registradas.
4. Inventario explícito de residuos auxiliares, ceros triviales, colas y términos
   de borde incluidos o excluidos.
5. Protocolo estadístico que preserve tendencia, heterocedasticidad y dependencia
   en los controles nulos; no se aceptan permutaciones cuya intercambiabilidad no
   esté justificada.
6. Hashes previos de C00, C03 y C03-B, más una salida nueva y separada.

## 6. Protocolo propuesto para el rerun limpio

El protocolo deberá existir como JSON antes de ejecutar y contener, al menos:

```text
experiment_id = G5B-005E-R
status = sealed_before_rerun
approved = true
approved_by = <identidad registrada>
sealed_at = <fecha y hora>
protocol_sha256 = <hash del protocolo inmutable>
```

El ejecutor C05 queda bloqueado si falta ese archivo o si no contiene todos los
campos anteriores.

Parámetros que deberán fijarse antes del rerun:

```text
rango X = [1000, 1000000]
muestras logarítmicas = 800
descubrimiento / validación = 65 / 35
alturas L5 = [50, 100, 143]
altura zeta = 143
modelos = [M0_local, M1_local_lzeros, M2_local_lzeros_cross]
salida = artifacts/goldbach_cesaro/c05_rerun_clean/
```

Falsificadores preregistrados:

1. Frecuencias incorrectas `6.0206` y `9.810574`, más controles aleatorios.
2. Ablación de `0, 1, 2, 4, 8` ceros correctos.
3. Ventanas con techo `10000, 30000, 100000, 300000, 1000000`.
4. Inversión artificial del signo del fondo M0.
5. Persistencia fuera de muestra de amplitud y fase.
6. Auditoría residual separada con corrección global y nulidad justificable.

Criterios confirmatorios mínimos:

```text
RMSE(M1) < RMSE(M0)
RMSE(M2) < RMSE(M1)
amplitud del primer cero en [0.9, 1.1]
error absoluto de fase <= 0.1 rad
ablación monotónica
frecuencias falsas rechazadas
archivos protegidos sin cambios
```

Los umbrales no podrán modificarse después del sello. El rerun no se ejecutará
como parte de esta revisión.

## 7. Estado final de la revisión

```text
experiment_id = G5B-005E-R
review_status = quarantine_established
C05_IMPLEMENTATION = provisional_quarantined
C05_CALIBRATION = numerically_passed_but_not_finally_approved
C05_OFFICIAL_STATUS = not_accepted
C05_FINAL_REVIEW = pending_clean_rerun
C05_RERUN = blocked_until_sealed_protocol
C05_DOWNSTREAM_USE = forbidden
C35 = frozen
C15 = frozen
DELETE_FILES = false
NOVELTY_CLAIM = false
```

## Referencias

1. NIST DLMF, [§25.15, funciones L de Dirichlet](https://dlmf.nist.gov/25.15).
2. NIST DLMF, [§25.11, zeta de Hurwitz](https://dlmf.nist.gov/25.11).
3. M. Cantarini, A. Gambini y A. Zaccagnini,
   [Cesàro averages for Goldbach representations with summands in arithmetic
   progressions](https://arxiv.org/abs/1911.07220), arXiv:1911.07220.
