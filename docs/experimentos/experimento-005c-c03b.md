# Experimento 005C: C03-B

## Objetivo

Intentar falsificar la calibracion controlada del canal C03. El experimento no
busca una frecuencia nueva ni constituye una demostracion de Goldbach o GRH.

## Controles

1. Sustitucion del primer cero correcto por 4.5324, 7.8096 y frecuencias
   aleatorias deterministas.
2. Ablacion con 0, 1, 2, 4 y 8 ceros de `L(s, chi_3)`.
3. Ventanas con techo 10000, 30000, 100000, 300000 y 1000000.
4. Inversion artificial del signo de la correccion de polo.
5. Estimacion en descubrimiento y evaluacion en validacion de amplitud y fase.
6. Correccion max-T con 999 permutaciones dentro de clases modulo 3.
7. Comparacion SHA-256 de todos los artefactos congelados C00/C03 y de cualquier
   artefacto futuro C05/C35/C15 presente antes de la ejecucion.

## Criterios declarados

- El RMSE M2 de validacion debe disminuir estrictamente al agregar ceros.
- El primer cero correcto debe superar fuera de muestra a todos los controles
  de frecuencia falsa.
- Invertir el polo debe aumentar el RMSE de validacion en cada ventana.
- En las tres ventanas mayores, la razon de amplitud debe quedar en `[0.9, 1.1]`
  y el error absoluto de fase por debajo de `0.1` radianes.
- El residuo final no debe superar el maximo global de los controles al nivel
  `0.05` para considerarse compatible con ausencia de estructura remanente.
- Todos los archivos protegidos deben conservar exactamente su SHA-256.

Un criterio fallido se registra como tal. No se reinterpreta automaticamente
como novedad matematica: primero exige una auditoria teorica independiente.

## Salidas

Los CSV y el resumen JSON se escriben exclusivamente en
`artifacts/goldbach_cesaro/c03b_stress_tests/`.
