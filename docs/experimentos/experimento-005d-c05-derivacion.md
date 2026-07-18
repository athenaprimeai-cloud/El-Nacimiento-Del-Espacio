# Experimento 005D: derivación local del canal C05

> **Estado posterior, 11 de junio de 2026:** la implementación C05 llegó a
> ejecutarse antes de cerrar el protocolo final exigido por este documento.
> La derivación local permanece aceptada, pero el código y sus resultados se
> conservan como `provisional_quarantined`; no existe aprobación retrospectiva.

## 1. Alcance y estado heredado

Este documento deriva la contribución local asociada a `s=0` para el canal
mixto

```text
r_05(n) = sum_{m=1}^{n-1} Lambda(m) Lambda(n-m) chi_5(n-m)
```

con promedio Cesàro de orden 2

```text
C05_2(X) = 1/2 * sum_{n<=X} r_05(n) * (1 - n/X)^2.
```

No implementa C05, no presenta una fórmula explícita completa y no formula una
afirmación de novedad.

El estado heredado de C03-B es:

```text
controles estructurales = superados
robustness_passed = false
auditoría residual = abierta
```

La descripción precisa es: C03 sobrevivió a los controles estructurales, pero
dejó una estructura remanente de baja frecuencia pendiente de auditoría. En el
segmento de validación `[89627, 1000000]`, la extensión logarítmica es
`2.4120986651` y la resolución de Rayleigh es `2.6048624785`. El máximo observado
en `omega = 2.15` no constituye una frecuencia resuelta. Además, el residuo tiene
correlación aproximada `-0.79` con `log X`; las permutaciones destruyen esa deriva
y no satisfacen una hipótesis limpia de intercambiabilidad.

## 2. El carácter cuadrático módulo 5

Se usa el carácter primitivo real

```text
chi_5(n) =  0  si 5 divide n
             1  si n = 1 o 4 (mod 5)
            -1  si n = 2 o 3 (mod 5).
```

Es cuadrático, par y de orden 2. En particular,

```text
chi_5(-1) = 1,
chi_5^2 = chi_0.
```

Por la representación finita de una función `L` de Dirichlet mediante zetas de
Hurwitz,

```text
L(s, chi_5) = 5^(-s) A(s),

A(s) = zeta(s,1/5) - zeta(s,2/5)
     - zeta(s,3/5) + zeta(s,4/5).
```

Como `zeta(0,a) = 1/2-a`, se obtiene `A(0)=0` y, por tanto,

```text
L(0, chi_5) = 0.
```

Este cero trivial es simple. En consecuencia, `L'/L` no posee un valor finito
en el origen.

## 3. Expansión local en el origen

Escribamos

```text
L(s,chi_5) = a_1 s + a_2 s^2 + O(s^3),
```

donde

```text
a_1 = L'(0,chi_5),
a_2 = L''(0,chi_5)/2.
```

Entonces

```text
L'/L(s,chi_5) = 1/s + b_0 + O(s),

b_0 = a_2/a_1
    = L''(0,chi_5) / (2 L'(0,chi_5)).
```

El generador aditivo torcido se representa formalmente por

```text
S_chi5(z)
  = sum_{n>=1} chi_5(n) Lambda(n) exp(-nz)
  = (1/(2 pi i)) integral Gamma(s) (-L'/L)(s,chi_5) z^(-s) ds.
```

Alrededor de `s=0`,

```text
-L'/L(s,chi_5) = -1/s - b_0 + O(s),
Gamma(s)        =  1/s - gamma + O(s),
z^(-s)          =  1 - s log z + O(s^2).
```

El producto tiene parte singular

```text
-1/s^2 + (log z + gamma - b_0)/s.
```

Por tanto, la contribución del origen a `S_chi5(z)` es

```text
log z + gamma - b_0.
```

Este es el mecanismo que distingue C05 de C03. Para el carácter impar
`chi_3`, `L(0,chi_3)` no se anula y no aparece este doble polo.

## 4. Derivación de `L'(0,chi_5)` por zeta de Hurwitz

Como `A(0)=0`, al derivar `5^(-s)A(s)` se obtiene directamente

```text
L'(0,chi_5) = A'(0).
```

Usando

```text
zeta'(0,a) = log Gamma(a) - (1/2) log(2 pi),
```

los términos `log(2 pi)` se cancelan y queda

```text
L'(0,chi_5)
 = log [Gamma(1/5) Gamma(4/5)
        / (Gamma(2/5) Gamma(3/5))].
```

La identidad de reflexión de Gamma da

```text
Gamma(1/5) Gamma(4/5) = pi / sin(pi/5),
Gamma(2/5) Gamma(3/5) = pi / sin(2pi/5).
```

Así,

```text
L'(0,chi_5)
 = log [sin(2pi/5)/sin(pi/5)]
 = log [2 cos(pi/5)]
 = log phi,

phi = (1 + sqrt(5))/2.
```

Numéricamente,

```text
L'(0,chi_5)
 = 0.4812118250596034474977589134243601475...
```

La misma representación proporciona una expresión directa para la segunda
derivada. Si `A''(0)` denota la combinación con los mismos signos de
`zeta''(0,a)`, entonces

```text
L''(0,chi_5) = A''(0) - 2 log(5) A'(0),

b_0 = A''(0)/(2 log phi) - log 5.
```

Esta identidad es la ruta simbólica de Hurwitz para `b_0`; no requiere evaluar
`L'/L - 1/s` cerca del polo.

## 5. Verificación mediante la ecuación funcional

Para el carácter primitivo, par y real de conductor 5, la función completada es

```text
Lambda(s,chi_5)
 = (5/pi)^(s/2) Gamma(s/2) L(s,chi_5),
```

y satisface la simetría funcional `Lambda(s,chi_5)=Lambda(1-s,chi_5)`.

Su derivada logarítmica es

```text
F(s) = (1/2) log(5/pi)
     + (1/2) psi(s/2)
     + L'/L(s,chi_5),
```

con `F(s)=-F(1-s)`. Al usar

```text
psi(s/2) = -2/s - gamma + O(s),
psi(1/2) = -gamma - 2 log 2,
```

y comparar `s=0` con `s=1`, se obtiene

```text
b_0 = gamma + log(2 pi/5) - L'/L(1,chi_5).
```

La evaluación independiente en `s=1` produjo

```text
L(1,chi_5)
 = 0.4304089409640040388894332329506042550...,

L'(1,chi_5)
 = 0.3562406470307614988646845863712747858...,

L'/L(1,chi_5)
 = 0.8276794767155048879910469896773795881...,
```

y, por tanto,

```text
b_0
 = -0.02202465783872691842463476000992951686...
```

## 6. Control numérico por coeficientes de Cauchy

La verificación numérica no resta `1/s` de `L'/L`. En su lugar recupera los
coeficientes de Taylor de `L` mediante la fórmula de Cauchy discretizada:

```text
a_k(r,N)
 = (1/(N r^k)) sum_{j=0}^{N-1}
   L(r exp(2 pi i j/N),chi_5) exp(-2 pi i k j/N).
```

Se utilizaron:

```text
precisión decimal = 60 dígitos
N del contorno    = 64
radios            = 0.20, 0.10, 0.05
Hurwitz            = Euler-Maclaurin con 32 términos y 10 correcciones
```

Los tres radios dieron, en los dígitos mostrados,

```text
a_1 =  0.4812118250596034474977589134243601475...
a_2 = -0.0105985257948870816288912820069450020...

a_2/a_1
    = -0.0220246578387269184246347600098998675...
```

La evaluación por ecuación funcional y la evaluación de Cauchy difieren en
aproximadamente `3e-32`. Esta coincidencia verifica mucho más de los 15 dígitos
exigidos, sin incorporar código C05 al proyecto.

## 7. Inversión Cesàro y origen de `H_3`

El otro generador del canal satisface, en su contribución principal,

```text
S_0(z) = 1/z + términos de menor orden o espectrales.
```

El kernel utilizado por el laboratorio cumple

```text
C05_2(X)
 = X^(-2) (1/(2 pi i)) integral
   S_0(z) S_chi5(z) exp(Xz) z^(-3) dz.
```

La contribución conjunta de `S_0(z)=1/z` y del origen de `S_chi5` contiene

```text
z^(-4) [log z + gamma - b_0].
```

Para `a>0`,

```text
Laplace^(-1)[z^(-a)]
 = X^(a-1)/Gamma(a),

Laplace^(-1)[z^(-a) log z]
 = X^(a-1)/Gamma(a) [psi(a) - log X].
```

Como

```text
psi(4) = H_3 - gamma,
H_3 = 1 + 1/2 + 1/3 = 11/6,
```

la constante de Euler se cancela exactamente. Después de dividir por `X^2`,
la contribución local queda

```text
M0_05(X)
 = X/6 [H_3 - b_0 - log X]
 = X/6 [11/6 - b_0 - log X].
```

Numéricamente,

```text
H_3 - b_0
 = 1.8553579911720602517579680933432332002...,

M0_05(X)
 = X/6 [1.8553579911720602518... - log X].
```

El `11/6` procede del valor exacto `psi(4)+gamma=H_3`; no es un resto de una
aproximación de Stirling.

## 8. Normalización y jerarquía de potencias

La normalización propuesta continúa siendo

```text
Z05(X) = C05_2(X) / X^(3/2).
```

Bajo GRH, un cero no trivial `rho=1/2+i gamma` de `L(s,chi_5)` contribuye

```text
-Gamma(rho)/Gamma(rho+4) * X^(rho+1)
 = -X^(rho+1) / [rho(rho+1)(rho+2)(rho+3)].
```

Por tanto:

| Componente | Orden antes de normalizar | Orden en `Z05` |
| --- | ---: | ---: |
| Fondo local `M0_05` | `X log X` | `X^(-1/2) log X` |
| Ceros lineales de `L_5` | `X^(3/2)` bajo GRH | `O(1)` |
| Cruces zeta-`L_5` | `X` bajo GRH | `X^(-1/2)` |

Así, `X log X` domina a un término simple `X`, pero es asintóticamente menor
que `X^(3/2)`. Los ceros lineales siguen siendo la señal dominante tras la
normalización elegida.

## 9. Estructura espectral permitida

El generador mixto es

```text
S_0(z) S_chi5(z),
```

no `S_chi5(z)^2`. Por ello, el esquema truncado permitido es:

```text
M0 = contribución local de s=0, incluido X log X;
M1 = M0 + ceros lineales de L(s,chi_5);
M2 = M1 + cruces entre ceros de zeta y ceros de L(s,chi_5).
```

No aparecen pares `L_5`-`L_5` en este canal mixto. Tales pares pertenecerían a
un observable con dos factores torcidos.

## 10. Relación con la auditoría residual C03-B

La deriva observada en C03-B no puede atribuirse al mecanismo `X log X` de C05:
`chi_3` es impar y `L(0,chi_3)` no se anula. La semejanza visual entre una deriva
lenta y un término omitido no constituye una derivación.

Las hipótesis abiertas para C03-B son:

1. residuos auxiliares de polos o ceros triviales omitidos por la expansión
   truncada;
2. cola de ceros no triviales, capaz de producir una envolvente lenta en una
   ventana finita;
3. términos de borde del promedio Cesàro;
4. nulidad estadística inadecuada, porque la permutación modular destruye la
   dependencia suave con `log X`.

Cada hipótesis requiere una predicción cuantitativa separada. Hasta entonces,
el estado permanece `auditoría residual abierta` y
`novelty_status = not_established`.

## 11. Condiciones para descongelar C05

C05 no debe implementarse hasta satisfacer conjuntamente:

1. revisión independiente de los signos y del factor `1/6` en `M0_05`;
2. revisión independiente de la identidad funcional para `b_0`;
3. tabla certificada de ceros de `L(s,chi_5)` y verificación del primero;
4. inventario explícito de residuos auxiliares y ceros triviales que serán
   incluidos o declarados fuera de la truncación;
5. protocolo de descubrimiento/validación y falsificadores fijados antes de
   observar los resultados C05;
6. garantía de inmutabilidad para C00, C03 y C03-B.

## 12. Estado final

```text
experiment_id = G5B-005D
channel = C05
status = derivation_only
local_s0_derivation = completed_and_cross_checked
explicit_formula_complete = false
implementation = provisional_quarantined
artifacts = quarantined_exploratory_archive
tests = archival_validation_only
retrospective_approval = rejected_for_now
final_review = pending
eligible_for_downstream_use = false
novelty_claim = false
C03B_residual_audit = open
```

## Referencias

1. NIST DLMF, [§25.15, funciones L de Dirichlet](https://dlmf.nist.gov/25.15),
   en particular 25.15.3 para la representación por zeta de Hurwitz, 25.15.5
   para la ecuación funcional y 25.15.7 para los ceros triviales.
2. NIST DLMF, [§25.11, zeta de Hurwitz](https://dlmf.nist.gov/25.11), en
   particular 25.11.18 para `zeta'(0,a)`.
3. M. Cantarini, A. Gambini y A. Zaccagnini,
   [Cesàro averages for Goldbach representations with summands in arithmetic
   progressions](https://arxiv.org/abs/1911.07220), arXiv:1911.07220.
