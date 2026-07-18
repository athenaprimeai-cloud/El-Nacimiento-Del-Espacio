# Experimento 006A: derivación del borde Cesàro para C03-B

## 1. Alcance y estado

```text
experiment_id = G5B-006A
target = H3_Cesaro_boundary_terms
status = derivation_only
scope = theoretical_derivation_only
implementation = not_authorized
execution = not_authorized
artifacts = none
tests = none
rerun = false
novelty_claim = false
005F = frozen
C03B_residual_audit = pending
C05 = provisional_quarantined
C05_RERUN = forbidden
C35 = frozen
C15 = frozen
```

Este documento no autoriza código, ejecutores, pruebas, corridas ni artefactos.
No recalcula C03-B y no utiliza sus resultados observados para elegir una forma
funcional.

Queda prohibido:

1. crear o modificar módulos Python;
2. crear ejecutores o pruebas;
3. generar CSV, JSON u otros artefactos experimentales;
4. modificar C03-B o sus resultados históricos;
5. tocar la cuarentena o el protocolo sellado de C05;
6. abrir C35 o C15;
7. declarar apoyo diagnóstico de H3;
8. reinterpretar la deriva residual como novedad matemática.

## 2. Pregunta matemática

005F definió H3 como la posible diferencia entre:

```text
el promedio Cesàro discreto calculado por el laboratorio
```

y

```text
el kernel continuo de inversión Laplace usado por la fórmula truncada.
```

006A determina si esa diferencia genera una corrección adicional con forma,
signo, potencia, logaritmos y coeficiente propios.

El resultado será más fuerte que una estimación asintótica: para el kernel de
orden 2 utilizado en C03-B, ambas expresiones son idénticas. No existe un término
de borde discreto-continuo separado.

## 3. Observable discreto exacto

Sea

```text
a_n = r_03(n)
    = sum_{m=1}^{n-1} Lambda(m) Lambda(n-m) chi_3(n-m).
```

El código del laboratorio calcula, para `X` entero positivo,

```text
C03_2(X)
 = (1/2) sum_{1 <= n <= X} a_n (1 - n/X)^2
 = (1/(2 X^2)) sum_{1 <= n <= X} a_n (X-n)^2.
```

El término `n=X` es exactamente cero. Por ello puede escribirse también

```text
C03_2(X)
 = (1/(2 X^2)) sum_{n >= 1} a_n (X-n)_+^2,

(y)_+ = max(y,0).
```

La implementación por momentos prefijos,

```text
(1/2) [S0(X) - 2 S1(X)/X + S2(X)/X^2],
```

es una reorganización algebraica exacta de la misma suma. No introduce una
cuadratura continua ni una fórmula de Euler-Maclaurin.

## 4. Generador de Laplace

Definamos

```text
F_03(z) = sum_{n >= 1} a_n exp(-n z),     Re(z) > 0.
```

Por la convolución aditiva,

```text
F_03(z) = S_0(z) S_chi3(z),

S_0(z)    = sum_{m >= 1} Lambda(m) exp(-m z),
S_chi3(z) = sum_{m >= 1} chi_3(m) Lambda(m) exp(-m z).
```

Esta identidad conserva exactamente la condición `m+(n-m)=n`. No convierte la
convolución aditiva en un producto de series de Dirichlet.

## 5. Inversión exacta del kernel

Para `c>0`, `k>-1` y `y` real, la inversión de Laplace proporciona

```text
(1/(2 pi i)) integral_(c-i infinity)^(c+i infinity)
    exp(y z) z^(-k-1) dz

 = y^k / Gamma(k+1),   si y>0,
 = 0,                  si y<0.
```

En `y=0` puede aparecer una convención de semisuma para kernels discontinuos,
pero aquí `k=2` y `y^2/Gamma(3)=0`; la elección no altera el resultado.

Tomando `k=2` y `y=X-n`,

```text
(X-n)_+^2 / 2
 = (1/(2 pi i)) integral_(c-i infinity)^(c+i infinity)
     exp((X-n)z) z^(-3) dz.
```

Sustituyendo en la suma y usando convergencia absoluta para `Re(z)=c>0`,

```text
C03_2(X)
 = X^(-2) (1/(2 pi i)) integral_(c-i infinity)^(c+i infinity)
     exp(Xz) F_03(z) z^(-3) dz

 = X^(-2) (1/(2 pi i)) integral_(c-i infinity)^(c+i infinity)
     exp(Xz) S_0(z) S_chi3(z) z^(-3) dz.
```

Esta es una identidad exacta para el observable del laboratorio. Coincide con
la fórmula general de promedios Cesàro

```text
sum_{n <= X} a_n (X-n)^k / Gamma(k+1)
```

representada mediante `F(z) exp(Xz) z^(-k-1)`.

## 6. Resultado de H3

Definamos formalmente la corrección de borde puro:

```text
B_Cesaro(X)
 = C03_2_discreto(X)
 - X^(-2) LaplaceInverse[F_03(z) z^(-3)](X).
```

Por la identidad anterior,

```text
B_Cesaro(X) = 0
```

para todo `X` entero positivo para el cual el observable esté definido.

Por tanto:

| Propiedad solicitada por 005F | Resultado derivado |
| --- | --- |
| Forma funcional | `B_Cesaro(X)=0` |
| Signo | nulo |
| Potencia de `X` | no aplica; todos los coeficientes son cero |
| Potencias de `log X` | ausentes |
| Coeficiente teórico | `0`, no ajustable |
| Resto uniforme | exactamente `0` |

En particular, no existe una familia adicional

```text
c X^(-alpha) (log X)^j
```

que pueda atribuirse a la diferencia entre el kernel discreto y la inversión
Laplace completa.

## 7. Qué no cubre esta identidad

El resultado `B_Cesaro=0` no afirma que el modelo espectral truncado sea
completo. La igualdad usa el generador exacto `F_03`. Cuando el laboratorio lo
reemplaza por un subconjunto de polos y ceros, la diferencia resultante pertenece
al contenido analítico omitido de los generadores, no al borde Cesàro.

Quedan fuera de H3:

1. términos locales de polos y ceros triviales en `S_0` o `S_chi3`;
2. integrales de contorno restantes después de desplazar la línea de Mellin;
3. colas de ceros no triviales truncadas por altura;
4. términos por caracteres inducidos o factores locales omitidos;
5. error de redondeo de la FFT o de acumulación en coma flotante;
6. efectos del muestreo logarítmico usado para analizar distintos valores de
   `X`.

Los puntos 1, 2 y 4 pertenecen a H1 o a una ampliación teórica explícita de H1.
El punto 3 pertenece a H2. Los puntos 5 y 6 son auditorías numéricas o de diseño
de muestreo, no correcciones del kernel Cesàro.

## 8. Distinción entre identidad y fórmula truncada

La descomposición utilizada en la literatura tiene la forma esquemática

```text
S(z;chi)
 = delta(chi)/z
 - sum_rho Gamma(rho) z^(-rho)
 + Q(z;chi)
 + R(z;chi).
```

Para un carácter impar, el término local `Q` es una constante relacionada con
`L'/L(0,chi)`. El término `R` procede de la integral restante sobre una línea
desplazada. Al multiplicar dos generadores e invertir el kernel exacto, todas
esas piezas producen contribuciones al promedio Cesàro. Omitir alguna de ellas
puede dejar una deriva lenta.

Pero esa deriva satisface

```text
deriva por truncamiento = LaplaceInverse[contenido analítico omitido],
```

no

```text
deriva por truncamiento = error discreto-continuo del peso Cesàro.
```

Esta distinción impide usar una base empírica de baja frecuencia y llamarla
retrospectivamente “corrección de borde”.

## 9. Extremos y posibles ambigüedades

### 9.1 Extremo superior

En `n=X`, el peso `(1-n/X)^2/2` se anula exactamente. No hay término de mitad de
salto ni corrección `1/2 a_X`.

### 9.2 Extremo inferior

El generador comienza en `n=1`; en la convolución de Goldbach, `a_0=a_1=0`.
No existe un término inferior omitido por la inversión.

### 9.3 Valores enteros de X

El laboratorio evalúa `X` enteros. La cuadrícula logarítmica solo elige qué
enteros observar; no modifica el valor exacto del promedio en cada entero.

### 9.4 Factor de normalización

El factor `1/2` del código es `1/Gamma(3)`. La división posterior por `X^2`
convierte `(X-n)^2/2` en `(1-n/X)^2/2`. No queda un factor de borde pendiente.

## 10. Consecuencia para el protocolo 005F

006A satisface la exigencia de derivar H3 antes de medirlo, pero la derivación
produce la hipótesis nula exacta:

```text
H3_Cesaro_boundary_correction = identically_zero
H3_free_parameters = 0
H3_measurement = not_applicable
H3_diagnostic_support = not_applicable
```

En una futura implementación autorizada de 005F:

```text
R123(X) = R12(X)
```

porque no se añadirá ningún regresor H3. Los criterios históricos de mejora de
RMSE, reducción de energía y estabilidad de coeficientes no se aplican a una
corrección derivada como cero.

Si una futura auditoría desea estudiar errores de FFT, redondeo, truncamiento de
contorno o selección de cuadrícula, deberá preregistrarlos con otro nombre y otra
hipótesis. No podrán reintroducirse como H3.

## 11. Orden uniforme del resto

Para la diferencia estricta definida por H3,

```text
sup_{X >= 1, X entero} |B_Cesaro(X)| = 0.
```

Así, para cualquier `A>0`, también es cierto formalmente que

```text
B_Cesaro(X) = O(X^(-A)),
```

pero la declaración informativa correcta es la identidad exacta `B_Cesaro=0`,
no una cota asintótica.

No se formula aquí una cota para el resto analítico `R(z;chi)` de los
generadores. Esa es una tarea distinta y permanece abierta dentro de H1/H2.

## 12. Estado heredado y bloqueos

La conclusión de 006A no cierra por sí sola la auditoría residual:

```text
005F = frozen
H1 = pending
H2 = pending_certified_zero_tables
H3 = theoretically_resolved_as_zero
H4 = pending_admissible_null_model
C03B_residual_audit = pending
C05_PREEXECUTION_AUDIT = blocked_on_residual_null_model
C05_RERUN = forbidden
C35 = frozen
C15 = frozen
```

No se autoriza retirar, modificar ni recalibrar ningún resultado existente.

## 13. Estado final

```text
experiment_id = G5B-006A
target = H3_Cesaro_boundary_terms
status = derivation_only
derivation_result = exact_zero_boundary_correction
functional_form = zero
sign = zero
power_of_X = none
log_X_terms = none
theoretical_coefficient = 0
uniform_remainder = 0
implementation = not_authorized
execution = not_authorized
artifacts = none
tests = none
rerun = false
diagnostic_support = not_claimed
novelty_claim = false
C03B_residual_audit = pending
C05 = provisional_quarantined
C05_RERUN = forbidden
C35 = frozen
C15 = frozen
```

## Referencias

1. M. Cantarini, A. Gambini y A. Zaccagnini,
   [Cesàro averages for Goldbach representations with summands in arithmetic
   progressions](https://arxiv.org/abs/1911.07220), especialmente la identidad
   de generación e inversión Cesàro en las ecuaciones (1) y (7), y la
   descomposición del generador en (8), (9) y (19).
2. NIST Digital Library of Mathematical Functions,
   [§1.14(iii), transformada de Laplace](https://dlmf.nist.gov/1.14#iii), para
   definiciones e inversión de Laplace.
3. Código histórico leído, sin modificar:
   `athena_azr/cesaro_calibration.py`, funciones `cesaro_c2_direct`,
   `cesaro_prefix_moments` y `cesaro_c2_from_prefix`.
4. Código histórico leído, sin modificar:
   `athena_azr/c03_laplace_chi3.py`, generador mixto y envoltorios Cesàro.
5. Experimento 005F congelado:
   `docs/experimentos/experimento-005f-c03b-auditoria-residual.md`.
