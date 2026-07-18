# 006H02: L3 contour mathematical obligations review

```text
phase_id = 006H02
phase_name = L3_CONTOUR_MATHEMATICAL_OBLIGATIONS_REVIEW
phase_type = documentary_mathematical_contract
real_execution = false
backend_invoked = false
code_modified = false
network_used = false
dependencies_installed = false
H2_opened = false
006F_opened = false
novelty_claim = false
```

## 1. Alcance

006H02 congela las obligaciones matematicas necesarias para que una fase futura
pueda certificar el conteo completo de ceros no triviales de `L(s, chi_3)` hasta
`T=500` mediante principio del argumento validado con aritmetica de bolas.

Este documento no ejecuta contornos, no evalua `Lambda_3`, no aisla ceros, no
cuenta ceros, no modifica backend, no abre H2 y no autoriza 006F.

Fuentes contractuales:

| Fuente | Uso en 006H02 |
| --- | --- |
| `006H01` | Contrato H2/006F congelado y obligaciones L3 definidas no satisfechas. |
| `006H00` | Cuello de botella H2-R06/H2-R07/H2-R08. |
| `006B` | Protocolo de certificacion H2 y canal L3. |
| `006C` | Arquitectura del certificador L3 y principio del argumento. |

## 2. Definicion exacta del caracter chi_3

El caracter queda congelado como:

```text
modulus = 3
conductor = 3
character_type = primitive_real_nonprincipal
parity = odd
conrey_index = 2
chi_3(1) = 1
chi_3(2) = -1
chi_3(n) = 0 when 3 divides n
```

Forma equivalente:

```text
chi_3(n) =
  0   if n == 0 mod 3
  1   if n == 1 mod 3
 -1   if n == 2 mod 3
```

Propiedades documentales:

```text
chi_3(-1) = chi_3(2) = -1
parity_parameter_a = 1
principal = false
real = true
primitive = true
```

## 3. Funcion L y funcion completada

La funcion de Dirichlet objetivo es:

```text
L(s, chi_3) = sum_{n >= 1} chi_3(n) n^(-s)
```

en su region inicial de convergencia, con continuacion analitica estandar. La
forma de control documental heredada de 006C es:

```text
L(s, chi_3) =
3^(-s) * (HurwitzZeta(s, 1/3) - HurwitzZeta(s, 2/3)).
```

La funcion completada congelada es:

```text
Lambda_3(s) =
(3/pi)^((s + 1)/2) * Gamma((s + 1)/2) * L(s, chi_3).
```

Componentes:

| Componente | Valor |
| --- | --- |
| conductor | `q = 3` |
| parity parameter | `a = 1` |
| gamma factor | `Gamma((s + 1)/2)` |
| conductor power | `(3/pi)^((s + 1)/2)` |
| normalization | completed primitive Dirichlet L-function normalization |

### 3.1 Ecuacion funcional

Para un caracter primitivo, la forma estandar es:

```text
Lambda(s, chi) =
epsilon(chi) * Lambda(1 - s, conjugate(chi))

epsilon(chi) = i^(-a) * tau(chi) / sqrt(q)
```

Para `chi_3`:

```text
a = 1
q = 3
tau(chi_3) =
  chi_3(1) * exp(2*pi*i/3)
  + chi_3(2) * exp(4*pi*i/3)
= exp(2*pi*i/3) - exp(4*pi*i/3)
= i * sqrt(3)

epsilon(chi_3) = i^(-1) * (i * sqrt(3)) / sqrt(3) = 1
```

Como `chi_3` es real:

```text
conjugate(chi_3) = chi_3
Lambda_3(s) = Lambda_3(1 - s)
Lambda_3(conjugate(s)) = conjugate(Lambda_3(s))
```

### 3.2 Entera o meromorfa

Obligacion congelada:

```text
Lambda_3(s) is treated as an entire completed function
```

Justificacion documental:

1. `chi_3` es primitivo y no principal, por lo que `L(s, chi_3)` no tiene el
   polo de la funcion zeta principal.
2. Los polos de `Gamma((s + 1)/2)` ocurren en `s = -1, -3, -5, ...`.
3. Para un caracter impar, esos puntos son ceros triviales de `L(s, chi_3)` y
   cancelan los polos gamma en la funcion completada.
4. La fase futura debe conservar una referencia/proof package local que justifique
   la continuacion analitica, la ecuacion funcional y la cancelacion de polos.

006H02 congela esta obligacion matematica, pero no produce un certificado
backend de entereza.

## 4. Equivalencia con los ceros objetivo

Los ceros objetivo de H2-L3 son los ceros no triviales de:

```text
L(s, chi_3)
```

con:

```text
0 < Im(s) <= T
T in [143, 200, 300, 500]
```

Equivalencia congelada:

```text
zeros_of_Lambda_3_inside_contour =
nontrivial_zeros_of_L(s, chi_3)_inside_contour
```

bajo las condiciones:

1. El contorno queda dentro de una region sin polos de `Lambda_3`.
2. Los factores `(3/pi)^((s + 1)/2)` y `Gamma((s + 1)/2)` no introducen ceros.
3. Los ceros triviales de `L(s, chi_3)` quedan fuera de la region de conteo o
   son cancelados por la completacion.
4. No hay ceros sobre la frontera.
5. Las multiplicidades se preservan: si `L(s, chi_3)` tiene un cero de orden
   `m` en la region no trivial, `Lambda_3(s)` tiene el mismo orden `m`.

Separacion obligatoria:

| Objeto | Tratamiento |
| --- | --- |
| Ceros triviales | No son objetivo H2; quedan sobre enteros negativos impares y se tratan mediante la completacion y la eleccion del contorno. |
| Ceros no triviales | Deben ser contados con multiplicidad en el rectangulo critico superior. |
| Ceros en frontera | Prohiben certificacion hasta que la frontera sea demostrada libre de ceros o se cierre como bloqueada/inconclusa. |
| Factores gamma | No tienen ceros; sus polos cancelados no deben producir falsos ceros de `Lambda_3`. |
| Factor de conductor | Es no nulo; no modifica ceros ni multiplicidades. |

## 5. Region y contorno exactos

006H02 congela cuatro contornos independientes, uno por altura:

```text
T_set = [143, 200, 300, 500]
sigma_left = -1/2
sigma_right = 3/2
bottom_height = 0
top_height = T
orientation = positive_counterclockwise
```

Para cada `T`, el contorno rectangular cerrado `C_T` tiene vertices exactos:

```text
A_T = -1/2 + 0*i
B_T =  3/2 + 0*i
C_T =  3/2 + T*i
D_T = -1/2 + T*i
```

Segmentos orientados:

```text
S1_T: A_T -> B_T       bottom_horizontal
S2_T: B_T -> C_T       right_vertical
S3_T: C_T -> D_T       top_horizontal
S4_T: D_T -> A_T       left_vertical
```

Convencion de conteo:

```text
counted_region =
{ s : -1/2 < Re(s) < 3/2 and 0 < Im(s) < T }
```

Como la certificacion exige `boundary_zero_free = true`, no hay diferencia entre
`0 < Im(s) < T` y `0 < Im(s) <= T` para los ceros objetivo cuando el certificado
pasa.

### 5.1 Uso de T frente a T_star

006H02 congela la opcion primaria:

```text
boundary_mode = exact_T_boundary
T_star_mode = not_authorized_in_006H02
```

Si una futura fase no puede certificar que la frontera superior `Im(s)=T` esta
libre de ceros para una altura requerida, debe cerrar como:

```text
boundary_not_certified_zero_free
```

o como estado H2 compatible `H2_BLOCKED`, `H2_INCONCLUSIVE` o
`H2_FAIL_SCOPE_OR_SEMANTICS`. No puede cambiar adaptativamente a `T_star` dentro
de la misma autorizacion, salvo autorizacion separada explicita que modifique el
contrato de frontera.

### 5.2 Tratamiento de bordes

| Borde | Obligacion |
| --- | --- |
| `Im(s)=0` | Debe certificarse libre de ceros de `Lambda_3`; esto excluye ceros reales en el intervalo horizontal. |
| `Im(s)=T` | Debe certificarse libre de ceros para cada `T`. |
| `Re(s)=-1/2` | Debe certificarse libre de ceros; la linea queda a la izquierda de la franja critica no trivial. |
| `Re(s)=3/2` | Debe certificarse libre de ceros; la linea queda a la derecha de la franja critica no trivial. |
| `Re(s)=1/2` | Es interior, no borde; ceros sobre la linea critica se cuentan con multiplicidad. |

## 6. Contabilidad de simetria

El contorno congelado cuenta todo el rectangulo critico superior ampliado:

```text
-1/2 < Re(s) < 3/2
0 < Im(s) < T
```

No cuenta solo media region y no divide por simetria.

Reglas:

1. La simetria `s -> 1 - s` empareja ceros dentro de la misma region horizontal,
   pero no autoriza dividir el winding.
2. La simetria de conjugacion empareja ceros de altura positiva con ceros de
   altura negativa. El contorno superior solo cuenta la mitad positiva.
3. El numero objetivo H2-L3 para altura `T` es el winding entero de `Lambda_3`
   alrededor de `C_T`, con multiplicidad, siempre que no haya ceros en frontera.

Conversion congelada:

```text
N_L3(T) =
winding_number(Lambda_3(C_T), 0)
```

sin division adicional por pares funcionales o conjugados.

## 7. Principio del argumento

Identidad congelada:

```text
N_L3(T) =
(1 / (2*pi*i)) * integral_over_C_T Lambda_3'(s) / Lambda_3(s) ds
```

Forma equivalente por variacion de argumento:

```text
N_L3(T) =
Delta_arg_C_T(Lambda_3) / (2*pi)
```

Hipotesis necesarias:

| Hipotesis | Estado 006H02 |
| --- | --- |
| `Lambda_3` analitica dentro y sobre `C_T` | Defined; requires external theorem/proof package. |
| Ausencia de ceros en la frontera | Requires backend certificate. |
| Ausencia de polos, o contabilidad de polos | Defined as no poles for `Lambda_3`; requires theorem/proof package. |
| Imagen continua de la frontera | Follows from analyticity; requires backend representation. |
| Orientacion positiva | Frozen as counterclockwise. |
| Conteo con multiplicidad | Frozen by argument principle. |

Si se usara una funcion meromorfa alternativa `F`, el principio del argumento
contaria:

```text
zeros_inside - poles_inside
```

Por eso 006H02 congela `Lambda_3` entera como funcion primaria de conteo.

## 8. Estandar de frontera libre de ceros

Un certificado valido de:

```text
boundary_zero_free = true
```

debe demostrar para cada segmento `S_k,T`:

```text
0 notin Lambda_3(S_k,T)
```

No basta con muestrear puntos.

Campos minimos del certificado:

```text
segment_id
target_height
parameter_interval
subdivision_id
segment_box
lambda3_image_ball
zero_excluded
positive_separation_witness
working_precision_bits
subdivision_depth
backend_operation_trace
certificate_hash
```

Reglas de cobertura:

1. Cada segmento debe cubrirse por una union ordenada de intervalos cerrados
   de parametro.
2. La union debe cubrir completamente el segmento, sin huecos.
3. Las subdivisiones vecinas deben tocarse o solaparse solo en extremos.
4. Para cada caja, la imagen certificada por bolas debe excluir el origen.
5. La evidencia de separacion puede ser una cota inferior positiva de
   `abs(Lambda_3)` o una exclusion equivalente del disco que contiene cero.
6. Si una caja de imagen contiene o puede contener cero, se subdivide.
7. Si la subdivision alcanza el limite autorizado sin excluir cero, el resultado
   futuro es bloqueado o inconcluso, no certificado.

Condicion de terminacion:

```text
all_boundary_boxes_zero_excluded = true
and full_segment_coverage_verified = true
```

## 9. Imagen de segmentos y exclusion del origen

Objeto matematico primario:

```text
0 notin Lambda_3(segment_box)
```

006H02 congela la evaluacion directa de `Lambda_3` como estandar primario de
winding. Las alternativas quedan restringidas:

| Alternativa | Permitida solo si |
| --- | --- |
| Funcion reescalada equivalente | El factor de reescala es analitico y no nulo en la region, y su winding alrededor de cero es probado y sumado/cancelado explicitamente. |
| Logaritmo certificado | Existe una rama local certificada en cada subdivision y transiciones de rama auditables. |
| Incrementos de argumento locales | Cada incremento tiene una rama continua certificada y la imagen no cruza cero. |
| Cocientes entre extremos | El arco completo entre extremos queda certificado dentro de una region que no rodea ni cruza cero de forma ambigua. |

Prohibido:

```text
hidden_branch_choice = forbidden
point_sampling_as_zero_free_certificate = forbidden
floating_point_argument_tracking = forbidden
unproved_rescaling_winding_cancellation = forbidden
```

## 10. Encierro del incremento de argumento

Para una subdivision `j` de un segmento:

```text
delta_arg_j in [a_j, b_j]
```

debe estar certificado por bolas y por una rama local continua. El intervalo
puede obtenerse por una de estas rutas, siempre que quede documentada:

1. encierro sectorial de `Lambda_3(segment_box_j)` que excluye cero;
2. integral local certificada de `Lambda_3'/Lambda_3`;
3. logaritmo complejo con rama local certificada;
4. cociente certificado entre endpoints mas homotopia de imagen que excluye cero.

Suma intervalar:

```text
Delta_arg_total =
sum_j [a_j, b_j]
```

debe hacerse por aritmetica intervalar dirigida, sin redondeo decimal externo.

El winding intervalar se define como:

```text
W_T = Delta_arg_total / (2*pi)
```

La constante `pi` debe provenir del backend riguroso o de una bola certificada
que preserve inclusiones.

## 11. Criterio de entero unico

```text
unique_integer_count = true
```

solo si el intervalo cerrado `W_T = [w_low, w_high]` contiene exactamente un
entero.

Regla formal:

```text
integer_set(W_T) = { n in Z : w_low <= n <= w_high }
unique_integer_count = (cardinality(integer_set(W_T)) == 1)
```

Prohibido:

```text
round(midpoint(W_T)) = forbidden_as_certificate
nearest_integer_heuristic = forbidden
```

Casos de fallo:

| Caso | Resultado futuro |
| --- | --- |
| `W_T` contiene dos o mas enteros | `winding_interval_contains_multiple_integers` |
| `W_T` no contiene enteros | `argument_increment_not_certified` o semantic fail |
| `W_T` toca dos enteros | no es unico; bloquea certificacion |
| ancho demasiado grande para decidir | `argument_increment_not_certified` |
| suma intervalar pierde inclusion | `H2_FAIL_SCOPE_OR_SEMANTICS` |

## 12. Multiplicidades y clusters

El principio del argumento cuenta ceros con multiplicidad. La futura fase H2
debe comparar:

```text
global_count_with_multiplicity_from_winding
```

contra:

```text
sum_of_multiplicities_from_isolated_boxes
```

para cada altura.

Reglas:

| Situacion | Obligacion |
| --- | --- |
| Dos ceros muy cercanos | Deben aislarse individualmente o declararse `unresolved_cluster`. |
| Una caja contiene multiplicidad mayor que uno | Debe certificar multiplicidad exacta; si no, `multiplicity_unresolved`. |
| Conteo global supera numero de intervalos | Aceptable solo si multiplicidades explican la diferencia; si no, `count_mismatch`. |
| Conteo global supera suma de multiplicidades | `count_mismatch`; bloquea H2. |
| Cluster no resuelto | `unresolved_cluster`; bloquea H2. |
| Altura intermedia no coincide | `count_mismatch`; bloquea H2 para toda certificacion H2-L3. |

El campo `critical_line_certified` es independiente. Un cero fuera de la linea
critica seria contado por el contorno y no invalida por si mismo la completitud;
lo que invalida H2 es omitirlo, no encontrarlo fuera de la linea.

## 13. Alturas intermedias

006H02 congela:

```text
height_strategy = four_independent_contours
T_set = [143, 200, 300, 500]
```

Se ejecutarian, en una fase futura autorizada, cuatro certificados de winding:

```text
C_143
C_200
C_300
C_500
```

No se permite usar solo el contorno de `500` para inferir automaticamente los
conteos intermedios. La reutilizacion de segmentos es permitida solo como
optimizacion de artefactos si conserva independencia verificable:

1. el segmento reutilizado tiene el mismo objeto matematico;
2. su certificado hash se referencia sin alteracion;
3. cada altura mantiene su propio `unique_integer_count`;
4. cada altura mantiene su propio reporte de frontera libre de ceros;
5. ninguna altura intermedia depende de una resta heuristica de conteos.

## 14. No dependencia de RH o GRH

El metodo congelado no asume:

```text
RH = false
GRH = false
all_zeros_on_critical_line_assumed = false
zero_simplicity_assumed = false
```

Razon:

1. El principio del argumento cuenta todos los ceros dentro del contorno, no solo
   los ceros sobre `Re(s)=1/2`.
2. La comparacion con cajas aislantes debe incluir cualquier cero dentro de la
   region, con multiplicidad.
3. La simplicidad no se presupone; las multiplicidades se contabilizan.
4. `critical_line_certified` puede ser una propiedad adicional de un cero, pero
   no es condicion necesaria para el conteo completo.

## 15. Obligaciones semanticas Arb/Acb

Lista congelada de operaciones futuras y garantia requerida:

| Operacion | Garantia matematica requerida |
| --- | --- |
| Construccion de bolas reales y complejas | Inclusion rigurosa del punto/segmento objetivo y redondeo dirigido. |
| Subdivision de intervalos | Cobertura completa, sin huecos, con extremos exactos o certificados. |
| Potencia `(3/pi)^((s+1)/2)` | Evaluacion compleja con rama definida y envolvente correcta. |
| `Gamma((s+1)/2)` compleja | Bola de inclusion rigurosa, control de polos fuera de la region. |
| Evaluacion de `L(s, chi_3)` | Inclusion rigurosa para el caracter exacto congelado. |
| Forma Hurwitz de control | Evaluacion independiente opcional con inclusion rigurosa. |
| Multiplicacion de bolas | Inclusion del producto exacto. |
| Division de bolas | Permitida solo cuando el divisor excluye cero. |
| Exclusion de cero | Prueba de que `0` no pertenece a la bola o conjunto de imagen. |
| Valor absoluto o separacion | Cota inferior positiva certificada cuando se use. |
| Argumento complejo | Encierro de argumento con rama local continua certificada. |
| Logaritmo complejo | Rama local certificada, dominio sin cruce del origen. |
| Integral de `Lambda_3'/Lambda_3` | Inclusion rigurosa del integrando y de la integral, con divisor no cero. |
| Suma intervalar | Inclusion preservada bajo redondeo dirigido. |
| Division por `2*pi` | `pi` certificado y division intervalar inclusiva. |
| Hash y trazabilidad | Cada certificado referencia backend, precision, parametros y bytes finales. |

La evidencia 006E71/006E74 de `chi.l_function` permanece como smoke runtime
limitado y no satisface estas obligaciones semanticas generales.

## 16. Fallos matematicos posibles

Cada estado bloquea una futura certificacion H2-L3:

```text
boundary_not_certified_zero_free
segment_image_contains_or_may_contain_zero
argument_increment_not_certified
winding_interval_contains_multiple_integers
multiplicity_unresolved
count_mismatch
completed_function_equivalence_unproved
contour_accounting_ambiguous
lower_boundary_real_zero_unresolved
top_boundary_zero_unresolved
backend_semantics_insufficient
rescaling_winding_unproved
```

Mapeo minimo:

| Estado | Cierre futuro permitido |
| --- | --- |
| `boundary_not_certified_zero_free` | `H2_BLOCKED` or `H2_INCONCLUSIVE` |
| `segment_image_contains_or_may_contain_zero` | `H2_INCONCLUSIVE` |
| `argument_increment_not_certified` | `H2_INCONCLUSIVE` |
| `winding_interval_contains_multiple_integers` | `H2_INCONCLUSIVE` |
| `multiplicity_unresolved` | `H2_INCOMPLETE` |
| `count_mismatch` | `H2_INCOMPLETE` or `H2_FAIL_SCOPE_OR_SEMANTICS` |
| `completed_function_equivalence_unproved` | `H2_BLOCKED` |
| `contour_accounting_ambiguous` | `H2_BLOCKED` |

## 17. Teoremas, lemas y obligaciones pendientes

### PROVED_IN_006H02

```text
chi_3_definition_frozen
chi_3_parity_odd
Gauss_sum_for_chi_3 = i * sqrt(3)
root_number_epsilon_chi_3 = 1
contour_orientation_and_winding_sign_convention_frozen
unique_integer_count_rule_frozen
no_RH_or_GRH_dependency_in_contract
```

Estas son derivaciones documentales dentro de 006H02. No son certificados
runtime.

### DEFINED_BUT_NOT_PROVED

```text
boundary_zero_free_for_T_143_200_300_500
actual_L3_zero_counts
actual_L3_isolating_boxes
actual_multiplicities
actual_cluster_absence
actual_argument_increment_intervals
actual_backend_precision_sufficiency
```

### REQUIRES_EXTERNAL_THEOREM

```text
analytic_continuation_of_L(s, chi_3)
functional_equation_for_primitive_Dirichlet_L_functions
entireness_of_Lambda_3
trivial_zero_and_gamma_pole_accounting
nontrivial_zero_location_within_critical_strip
argument_principle_for_entire_functions
```

The future proof package must be local, cited, hashed and compatible with the
006H01 protocol hashes.

### REQUIRES_BACKEND_CERTIFICATE

```text
boundary_zero_free = true
segment_image_excludes_zero = true
ball_validated_subdivision = true
argument_increment_enclosures = true
total_winding_unique_integer = true
multiplicity_accounting = true
counts_match = true
```

### REQUIRES_REAL_EXECUTION

```text
l3_zeros_T500.csv
l3_isolation_report.json
l3_completeness_report.json
H2_ZERO_CERTIFICATION_MANIFEST.json
SHA256SUMS.txt
```

## 18. Canonical fields for future L3 completeness report

006H02 requires the future `l3_completeness_report.json` to include:

```text
function_id = L3
character_definition
completed_function_definition_hash
functional_equation_root_number
contour_family
height_strategy
height_set
boundary_mode
boundary_zero_free_certificates
segment_subdivision_certificates
argument_increment_intervals
winding_intervals_by_height
unique_integer_count_by_height
isolated_count_with_multiplicity_by_height
counts_match_by_height
unresolved_clusters
forbidden_assumptions
backend_semantic_operations
proof_package_hashes
status
```

## 19. Decision final 006H02

```text
L3_COMPLETED_FUNCTION_DEFINITION = FROZEN
L3_CONTOUR_DEFINITION = FROZEN
L3_ARGUMENT_PRINCIPLE_OBLIGATIONS = FROZEN
L3_BOUNDARY_CERTIFICATION_STANDARD = FROZEN
L3_WINDING_CERTIFICATION_STANDARD = FROZEN
L3_READY_FOR_CODE_PLAN = true
L3_READY_FOR_REAL_EXECUTION = false
```

Interpretacion:

```text
L3_READY_FOR_CODE_PLAN = true
```

significa que la proxima fase documental o de implementacion planificada puede
usar obligaciones matematicas congeladas para disenar codigo. No autoriza
modificar codigo en 006H02.

```text
L3_READY_FOR_REAL_EXECUTION = false
```

queda fijado porque aun faltan prueba/cita local hasheada, backend semantico,
certificados de frontera, certificados de subdivision, conteos reales, cajas
aislantes reales y autorizacion 006F separada.

## 20. Prohibiciones y cierre

```text
CODE_MODIFIED = false
FLINT_EXECUTED = false
ARB_EXECUTED = false
ACB_EXECUTED = false
CHI_L_FUNCTION_CALLED = false
LAMBDA_3_NUMERICALLY_EVALUATED = false
CONTOURS_EXECUTED = false
ZEROS_ISOLATED = false
ZEROS_COUNTED = false
ZERO_TABLES_GENERATED = false
H2_OPENED = false
006F_OPENED = false
NETWORK_USED = false
DEPENDENCIES_INSTALLED = false
NEXT_PHASE_AUTHORIZED = false
H2_PROOF_CLAIMED = false
RH_CLAIMED = false
GRH_CLAIMED = false
NOVELTY_CLAIMED = false
```

Resultado:

```text
006H02_RESULT =
006H02_L3_CONTOUR_MATHEMATICAL_OBLIGATIONS_FROZEN
```
