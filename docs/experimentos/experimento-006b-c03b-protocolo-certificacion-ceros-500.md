# Experimento 006B: protocolo de certificacion de ceros hasta altura 500

## 1. Alcance y estado

```text
experiment_id = G5B-006B
target = H2_zero_certification_to_height_500
status = authorized_protocol_only
scope = theoretical_certification_protocol
implementation = not_authorized
execution = not_authorized
artifacts = none
zero_tables = not_generated
tests = none
rerun = false
novelty_claim = false
005F = frozen
006A = accepted_derivation_only
H3_Cesaro_boundary_correction = identically_zero
C03B_residual_audit = pending
C05 = provisional_quarantined
C05_RERUN = forbidden
C35 = frozen
C15 = frozen
```

Este protocolo no autoriza calculo, codigo ni generacion de tablas. Una
certificacion H2 valida requerira una autorizacion posterior separada para
implementacion y una autorizacion posterior separada para ejecucion.

Queda expresamente prohibido durante 006B:

1. crear o modificar modulos, ejecutores o pruebas;
2. calcular, refinar o exportar ceros;
3. generar CSV, JSON, manifiestos o reportes numericos;
4. recalcular metricas de C03-B;
5. modificar 005F, 006A o los artefactos historicos;
6. tocar C05 o su cuarentena;
7. abrir C35 o C15;
8. usar aproximaciones de ceros como si fueran certificados de completitud.

## 2. Estado heredado y motivacion

005F preregistro H2 como la hipotesis de que la deriva residual de C03-B puede
provenir de truncar las colas de ceros no triviales de `zeta(s)` y
`L(s,chi_3)`. Las alturas futuras quedaron congeladas en:

```text
T = [143, 200, 300, 500].
```

006A resolvio H3 de forma exacta:

```text
H3_Cesaro_boundary_correction = identically_zero.
```

Por tanto, antes de solicitar una implementacion de 005F, el siguiente bloqueo
es producir tablas H2 que no solo aproximen ceros, sino que acrediten que todos
los ceros relevantes hasta `T=500` fueron encontrados.

## 3. Regla central de certificacion

```text
Certificacion H2
= aislamiento riguroso de cada cero
+ conteo completo hasta T=500.
```

Ambas condiciones son necesarias y ninguna sustituye a la otra:

1. **Aislamiento individual:** cada fila debe contener un intervalo riguroso que
   encierre un unico cero, con multiplicidad declarada o acotada.
2. **Completitud global:** un conteo certificado debe demostrar que la suma de
   multiplicidades de los intervalos coincide con el numero total de ceros en
   la region declarada hasta `T=500`.

Advertencia obligatoria:

```text
Evaluar zeta(1/2+i*gamma) o L(1/2+i*gamma,chi_3) cerca de cero NO certifica
completitud.
```

Un residuo numerico pequeno solo verifica proximidad a un cero candidato. No
descarta ceros omitidos, pares muy proximos, multiplicidades no resueltas ni
errores de ordenacion.

## 4. Funciones y regiones que deberan certificarse

### 4.1 Canal zeta

La certificacion futura debera cubrir los ceros no triviales de `zeta(s)` con:

```text
0 < Im(s) <= 500.
```

El reporte debera declarar si el conteo se realiza en toda la franja critica o
si usa un teorema o algoritmo riguroso que identifica el conteo total con los
ceros aislados sobre la recta critica. No se asumira RH como reemplazo de ese
paso.

### 4.2 Canal L3

Sea `chi_3` el caracter primitivo real impar modulo 3:

```text
chi_3(n) = 0,  si 3 divide n
chi_3(n) = 1,  si n = 1 mod 3
chi_3(n) = -1, si n = 2 mod 3.
```

La certificacion futura debera cubrir los ceros no triviales de
`L(s,chi_3)` con:

```text
0 < Im(s) <= 500.
```

La simetria de la ecuacion funcional puede reducir trabajo, pero no sustituye
el conteo completo en la region declarada. Tampoco se asumira GRH para concluir
que todos los ceros contados estan sobre `Re(s)=1/2`.

## 5. Convenciones de frontera y multiplicidad

Para evitar ambiguedades en `T=500`, la futura certificacion debera usar uno de
estos cierres, elegido antes de ejecutar:

1. demostrar rigurosamente que no existe un cero con `Im(s)=500` y contar
   `0 < Im(s) <= 500`; o
2. elegir un numero racional o diadico certificado `T_star >= 500`, libre de
   ceros en la frontera, contar hasta `T_star` y filtrar mediante intervalos
   rigurosos los ceros con altura a lo sumo 500.

Cada cero se contara con multiplicidad. Si el metodo solo certifica un numero
de ceros dentro de una caja, pero no unicidad, la caja debera subdividirse hasta
obtener aislamiento individual o marcarse como `unresolved_cluster`. Una tabla
con `unresolved_cluster` no satisface H2.

## 6. Ruta permitida para zeta

La ruta primaria recomendada es FLINT/Arb, o una herramienta equivalente con
aritmetica de bolas e intervalos rigurosos.

La documentacion de FLINT incluye para `zeta`:

1. aislamiento de un cero de Hardy `Z` en un intervalo que no contiene otro;
2. refinamiento riguroso del intervalo aislante;
3. generacion de ceros consecutivos;
4. conteo de ceros `N(T)` con multiplicidades;
5. metodos basados en las ideas de Turing para cerrar la completitud.

Una futura implementacion podra usar esas funciones siempre que registre la
version exacta de FLINT, precision, parametros y salida intervalar. El nombre de
una rutina no basta: el reporte debera mostrar que el conteo global y la lista
aislada coinciden en la misma convencion de frontera.

La ruta Platt de FLINT no es necesaria para alturas tan bajas y sus funciones
documentadas esperan indices mucho mayores. No se usara por costumbre si la
ruta directa de aislamiento y Turing ya cubre `T<=500`.

## 7. Ruta permitida para L(s,chi_3)

FLINT permite evaluar rigurosamente funciones `L` de Dirichlet y la funcion de
Hardy asociada a caracteres primitivos. Sin embargo, la documentacion citada no
ofrece para un caracter general la misma interfaz completa de aislamiento y
conteo que ofrece especificamente para `zeta`.

Por ello, la futura certificacion de L3 debera implementar y documentar uno de
estos cierres rigurosos:

### Ruta L3-A: principio del argumento

1. definir una funcion completada entera cuya cantidad de ceros equivalga a la
   buscada;
2. fijar un rectangulo con frontera certificada libre de ceros;
3. evaluar con aritmetica de bolas el cambio total de argumento en toda la
   frontera;
4. subdividir adaptativamente cada segmento hasta certificar que la imagen no
   cruza el origen y que el incremento de argumento queda encerrado;
5. obtener un entero unico para el numero total de ceros, con multiplicidad;
6. compararlo con la suma de los intervalos aislantes individuales.

### Ruta L3-B: metodo de Turing riguroso o equivalente

1. construir la funcion real de Hardy asociada a `chi_3`;
2. aislar cambios de signo y posibles ceros de multiplicidad par mediante
   evaluaciones y derivadas rigurosas;
3. aplicar una cota Turing valida para esta funcion `L` y este conductor;
4. demostrar que el numero de ceros detectados coincide con el conteo total;
5. documentar todas las constantes y cotas usadas.

Una mezcla de ambas rutas es admisible. Una exploracion por cambios de signo
sin un teorema de completitud no es admisible, porque puede omitir ceros de
multiplicidad par o ceros fuera de la recta critica.

## 8. Requisitos de aislamiento individual

Cada intervalo futuro debera ser producido con aritmetica certificada y cumplir:

```text
lower < gamma < upper
upper - lower <= 1e-20
intervals_pairwise_disjoint = true
ordering_certified = true
unique_zero_in_interval = true
```

El ancho `1e-20` es el minimo documental para H2; la implementacion podra usar
mayor precision. No se aceptaran decimales sin radio de error.

Para cada fila se deberan registrar al menos:

```text
index
function_id
conductor
character_id
parity
lower_bound
upper_bound
midpoint_display_only
radius
multiplicity
isolation_method
working_precision_bits
certificate_reference
```

`midpoint_display_only` no tendra valor probatorio. Los campos probatorios son
los extremos intervalares y el certificado que demuestra unicidad.

## 9. Requisitos de completitud

Para cada funcion y cada altura congelada `143, 200, 300, 500`, el futuro
reporte debera incluir:

```text
T_requested
T_counting_boundary
boundary_zero_free = true
certified_total_count
isolated_count_with_multiplicity
counts_match = true
counting_method
counting_precision_bits
counting_parameters
proof_or_bound_references
```

La condicion de aceptacion es:

```text
certified_total_count
= isolated_count_with_multiplicity
```

simultaneamente para ambas funciones y las cuatro alturas. Si una sola altura
no cierra, H2 conserva el estado `not_auditable` y no se autoriza sustituirla
por interpolacion o por una tabla externa.

## 10. Fuentes externas y contraste cruzado

### 10.1 Odlyzko

Las tablas de Odlyzko se usaran solamente como contraste independiente para
los ceros de `zeta`. Podran detectar errores de orden, transcripcion o escala,
pero no reemplazan los intervalos generados y el conteo certificado del futuro
proceso H2.

### 10.2 LMFDB

LMFDB se usara solamente como contraste externo para la identidad del caracter,
conductor, paridad y ceros publicados de `L(s,chi_3)`. Una coincidencia decimal
con LMFDB no constituye el sello final de completitud de Athena.

### 10.3 Regla de desacuerdo

Si una referencia externa no intersecta el intervalo certificado correspondiente
o presenta un conteo distinto, la ejecucion futura debera detenerse con:

```text
cross_reference_status = disagreement
H2_certification_status = failed_pending_review
```

No se corregira automaticamente ninguna tabla para hacerla coincidir.

## 11. Reproducibilidad y procedencia

Antes de una futura ejecucion se deberan congelar:

1. sistema operativo y arquitectura;
2. version exacta y origen de FLINT/Arb o herramienta equivalente;
3. hash SHA-256 de binarios, bibliotecas y codigo autorizado;
4. precision de trabajo y regla de incremento adaptativo;
5. parametros de aislamiento, subdivisiones y conteo;
6. definicion exacta del caracter `chi_3` y su identificador;
7. convencion de frontera y tratamiento de multiplicidades;
8. formato canonico de serializacion;
9. fuentes externas, fecha de consulta y hashes de las copias usadas.

No se aceptara una certificacion que dependa de estado remoto mutable sin una
copia local hasheada de los datos usados como contraste.

## 12. Salidas futuras previstas

Una autorizacion posterior podra proponer, sin reutilizar directorios
historicos, las siguientes salidas:

```text
artifacts/goldbach_cesaro/c03b_h2_zero_certification/
    zeta_zeros_T500.csv
    l3_zeros_T500.csv
    zeta_isolation_report.json
    l3_isolation_report.json
    zeta_completeness_report.json
    l3_completeness_report.json
    H2_ZERO_CERTIFICATION_MANIFEST.json
```

El manifiesto debera incluir SHA-256, tamano, tipo de contenido y relacion entre
cada tabla y su reporte. Estos nombres son un contrato de diseno, no una
autorizacion para crear archivos.

## 13. Formato canonico futuro

Las tablas CSV deberan usar UTF-8, salto de linea LF, encabezado fijo y numeros
intervalares en notacion decimal sin separador de miles. Los JSON deberan usar
UTF-8, claves ordenadas y serializacion canonica definida antes de ejecutar.

Los hashes se calcularan sobre bytes exactos despues de cerrar los archivos.
Toda regeneracion, incluso numericamente equivalente, producira una nueva
version del paquete y requerira nuevo manifiesto.

## 14. Criterios de aceptacion de H2

H2 podra marcarse `certified_for_future_005F_use` solo si se cumplen todos los
criterios:

1. cada cero hasta altura 500 tiene un intervalo aislante riguroso;
2. no existen intervalos superpuestos ni grupos sin resolver;
3. el conteo completo coincide con la suma de multiplicidades;
4. la igualdad de conteos se verifica en `T=143,200,300,500`;
5. las fronteras de conteo estan certificadas libres de ceros;
6. ambas funciones pasan los controles internos;
7. Odlyzko y LMFDB se usan como contraste y todo desacuerdo esta resuelto;
8. todos los archivos, herramientas y parametros tienen procedencia y hash;
9. una revision humana acepta literalmente los reportes y el manifiesto;
10. no se modifican C00, C03, C03-B, C05 ni sus artefactos.

Si falla cualquier condicion:

```text
H2_zero_certification = incomplete_or_failed
005F_implementation_unlock = false
statistical_verdict = inconclusive
```

## 15. Fallos que deben detener una futura ejecucion

La ejecucion futura debera detenerse sin producir un paquete aceptable si:

1. una evaluacion intervalar contiene cero en un tramo de frontera no resuelto;
2. el cambio de argumento no encierra un unico entero;
3. el conteo total y los intervalos aislados no coinciden;
4. una raiz no puede separarse de otra con la precision maxima preregistrada;
5. aparece una multiplicidad no resuelta;
6. la frontera superior contiene o puede contener un cero;
7. cambia una dependencia, precision o parametro despues de observar resultados;
8. se intenta completar una ausencia copiando un decimal externo.

El estado obligatorio sera `inconclusive`, no una certificacion parcial
presentada como completa.

## 16. Separacion de autorizaciones futuras

El avance desde 006B requiere tres decisiones humanas distintas:

```text
fase 1: aprobar y congelar este protocolo documental
fase 2: autorizar por separado la implementacion del certificador
fase 3: revisar la implementacion y autorizar por separado su ejecucion
```

La autorizacion de fase 2 no implica fase 3. La ejecucion de pruebas tecnicas
que calculen ceros o conteos tambien pertenece a fase 3, aunque se denominen
"tests".

## 17. Relacion con 005F

006B solo prepara la precondicion documental de H2. No evalua si la cola de
ceros explica la deriva residual y no autoriza recalcular `R0`, `R1`, `R2` o
ninguna metrica.

Despues de una certificacion H2 futura y aceptada, todavia quedaran pendientes:

```text
H1 = pending
H2 = certified_tables_required_then_diagnostic_execution
H3 = theoretically_resolved_as_zero
H4 = pending_admissible_null_model
```

C05 continuara bloqueado hasta que la auditoria residual y el modelo nulo
cumplan sus propias condiciones. H2 no desbloquea automaticamente C05.

## 18. Estado final

```text
experiment_id = G5B-006B
target = H2_zero_certification_to_height_500
status = authorized_protocol_only
certification_rule = individual_isolation_plus_complete_count
implementation = not_authorized
execution = not_authorized
artifacts = none
zero_tables = not_generated
tests = none
rerun = false
novelty_claim = false
005F = frozen
006A = accepted_derivation_only
H2 = protocol_defined_not_executed
C03B_residual_audit = pending
C05 = provisional_quarantined
C05_RERUN = forbidden
C35 = frozen
C15 = frozen
```

## Referencias

1. FLINT, [acb_dirichlet.h: Dirichlet L-functions, Riemann zeta and related
   functions](https://flintlib.org/doc/acb_dirichlet.html), para aritmetica de
   bolas, funciones de Hardy, aislamiento, refinamiento y conteo de ceros de
   `zeta`, incluida la ruta de Turing documentada.
2. Andrew Odlyzko, [Tables of zeros of the Riemann zeta
   function](https://www-users.cse.umn.edu/~odlyzko/zeta_tables/), usada solo
   como referencia cruzada externa.
3. LMFDB, [Dirichlet L-function 3.2](https://www.lmfdb.org/L/Character/Dirichlet/3/2/),
   usada solo como referencia cruzada externa para `L(s,chi_3)`.
4. Experimento 005F congelado,
   `docs/experimentos/experimento-005f-c03b-auditoria-residual.md`.
5. Experimento 006A aceptado,
   `docs/experimentos/experimento-006a-c03b-derivacion-borde-cesaro.md`.
