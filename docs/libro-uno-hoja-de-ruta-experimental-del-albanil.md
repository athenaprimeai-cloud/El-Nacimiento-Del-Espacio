# Libro Uno: Hoja de Ruta Experimental del Albañil

Especificación operativa para convertir el lenguaje CED+RAP del Libro Cero en simulaciones, mediciones y reportes reproducibles.

## Propósito

El Libro Uno define protocolos que un agente puede ejecutar. Su objetivo no es declarar resueltas las conjeturas de Goldbach o Riemann, sino producir evidencia organizada, falsable y comparable entre ciclos.

## Contrato de honestidad

Cada experimento debe declarar uno de estos niveles:

| Nivel | Significado |
| --- | --- |
| Observación | Resultado computacional directo en una ventana finita. |
| Evidencia heurística | Patrón estable observado en muchas ventanas, sin prueba general. |
| Modelo formal parcial | Definición operatoria que explica una familia de observaciones bajo supuestos explícitos. |
| Candidato a prueba | Argumento estructurado que podría transformarse en demostración formal, todavía con brechas declaradas. |

Ningún resultado experimental puede llamarse demostración sin una prueba independiente de la ventana computada.

---

## Modelo de datos común

### NumberRecord

Registro mínimo para cada número natural explorado:

```json
{
  "n": 10,
  "ced_state": "I",
  "factorization": [[2, 1], [5, 1]],
  "rap_potential": 7,
  "rap_integrity": 2,
  "rap_loss": 3,
  "is_prime": false
}
```

### GoldbachPartition

Registro para cada partición `p + q = N`:

```json
{
  "N": 20,
  "p": 3,
  "q": 17,
  "p_is_prime": true,
  "q_is_prime": true,
  "epsilon": 14,
  "center_distance": 7,
  "ced_pair": ["D", "D"],
  "ced_result": "I",
  "pair_rap_integrity": 2,
  "merged_rap_loss": 11,
  "exclusion_pass": true
}
```

### ExperimentResult

Todo experimento debe producir un resumen con:

```json
{
  "experiment_id": "G1",
  "window": {"min": 4, "max": 1000000},
  "parameters": {},
  "evidence_level": "Observación",
  "metrics": {},
  "artifacts": [],
  "interpretation": "",
  "falsifiers": []
}
```

---

## Línea 1: Goldbach-CED/RAP

### G1: Censo exacto de particiones Goldbach

**Nivel inicial:** Observación.

**Pregunta:** Para cada par `N > 2`, ¿cuántas particiones `p + q = N` existen con `p` y `q` primos?

**Entrada**

- `M`: límite superior par.
- Tabla de primalidad hasta `M`.
- Registros RAP para `2..M`.

**Procedimiento**

1. Generar todos los pares `p <= q` tales que `p + q = N`.
2. Aplicar Exclusión `X_prime`: conservar solo pares donde `Omega(p) = Omega(q) = 1`.
3. Registrar `g(N)`, número de particiones sobrevivientes.
4. Registrar el par más central, definido por menor `abs(p - N/2)`.

**Métricas**

- `g(N)`: número de representaciones.
- `epsilon_min(N)`: menor distancia `abs(p - q)` entre pares primos.
- `centrality(N) = 1 / (1 + epsilon_min(N))`.
- `rap_merge_loss(N, p, q) = Psi(p) + Psi(q) - Psi(N)`.

**Criterio de fallo**

Si algún par `N` en la ventana tiene `g(N) = 0`, el experimento debe detenerse y emitir un reporte de contraejemplo computacional.

**Salida esperada**

Una tabla ordenada por `N` con particiones, métricas CED/RAP y estado de exclusión.

### G2: Simetría alrededor de N/2

**Nivel inicial:** Evidencia heurística.

**Pregunta:** ¿Las particiones primas tienden a formar puentes simétricos alrededor del centro `N/2`?

**Procedimiento**

1. Para cada `N`, mapear cada partición prima como distancia `d = abs(p - N/2)`.
2. Construir el espectro de distancias `D_N`.
3. Comparar `D_N` contra todas las particiones enteras de `N`.
4. Medir concentración cerca del centro.

**Métricas**

- distancia media;
- distancia mínima;
- varianza de distancias;
- proporción de pares en el tercio central;
- persistencia de pares centrales al crecer `N`.

**Interpretación permitida**

Una concentración central puede sugerir resonancia estructural. No prueba Goldbach.

### G3: Interferencia CED/RAP y medición de kappa

**Nivel inicial:** Modelo formal parcial.

**Pregunta:** ¿Cambiar el orden entre estabilidad CED y orden RAP altera el conjunto de candidatos?

**Entrada**

- Ventana `W = {N pares: A <= N <= B}`.
- Porcentaje de recorte RAP `r`.
- Regla de ordenamiento RAP, por ejemplo menor pérdida `L`.

**Procedimiento**

1. Construir `P_N = {(a, b): a <= b, a + b = N}`.
2. Calcular `R1(N) = E(O_r(P_N))`.
3. Calcular `R2(N) = O_r(E(P_N))`.
4. Medir `d(R1, R2)` por diferencia simétrica normalizada.
5. Promediar sobre la ventana para obtener `kappa_W`.

**Métricas**

- `kappa_N`;
- `kappa_W`;
- sensibilidad ante `r`;
- sensibilidad ante cambios de ventana;
- pares excluidos por cada ruta.

**Criterio de calidad**

`kappa_W` solo puede tratarse como candidato a invariante si se mantiene estable bajo varias ventanas y reglas `r`.

### G4: Transformada de Goldbach

**Nivel inicial:** Evidencia heurística.

**Pregunta:** ¿La serie `g(N)` contiene periodicidades o interferencias detectables por análisis espectral?

**Procedimiento**

1. Construir la serie `g(4), g(6), ..., g(M)`.
2. Normalizar por una tendencia suave local.
3. Aplicar ventana de Hann para reducir fuga espectral.
4. Ejecutar FFT sobre el residuo.
5. Registrar picos dominantes y estabilidad por subventanas.

**Métricas**

- frecuencias dominantes;
- potencia relativa de picos;
- estabilidad de picos entre ventanas;
- correlación con patrones modulares.

**Control**

El reporte debe comparar contra una serie permutada con la misma media local para evitar confundir ruido con estructura.

---

## Línea 2: Riemann-Firma Espectral

### R1: Residuo de conteo primo

**Nivel inicial:** Observación.

**Pregunta:** ¿Cómo oscila `pi(x)` frente a `Li_2(x)` y frente a `x / log(x)`?

**Procedimiento**

1. Calcular `pi(x)` mediante criba para puntos de muestreo.
2. Calcular `Li_2(x) = integral_2^x dt / log(t)`.
3. Calcular `x / log(x)` como tendencia de primer orden.
4. Registrar dos residuos separados:
   - `R_li(x) = pi(x) - Li_2(x)`;
   - `R_pnt(x) = pi(x) - x/log(x)`.

**Regla obligatoria**

Los reportes deben nombrar explícitamente qué tendencia usan. `Li_2(x)` y `x/log(x)` no son intercambiables.

### R2: Función de Chebyshev psi

**Nivel inicial:** Observación.

**Pregunta:** ¿Las oscilaciones de `psi(x)` muestran una firma más limpia que `pi(x)`?

**Procedimiento**

1. Calcular `psi(x) = sum_{p^k <= x} log(p)`.
2. Medir residuo `psi(x) - x`.
3. Comparar amplitud y frecuencia de oscilaciones con `R_li(x)`.

**Métricas**

- máximo residuo absoluto por ventana;
- cambios de signo;
- frecuencia dominante del residuo;
- correlación con ventanas de alta o baja densidad prima.

### R3: Espaciado de ceros y comparación GUE

**Nivel inicial:** Evidencia heurística.

**Pregunta:** ¿El espaciado normalizado de ceros no triviales se aproxima al patrón GUE?

**Entrada**

- Lista verificada de ceros `1/2 + i gamma_n`.

**Procedimiento**

1. Ordenar alturas `gamma_n`.
2. Calcular brechas `delta_n = gamma_{n+1} - gamma_n`.
3. Normalizar por densidad local.
4. Comparar histograma de brechas con:

```text
P_GUE(s) = (32 / pi^2) * s^2 * exp(-4s^2 / pi)
```

5. Medir divergencia entre histograma empírico y curva GUE.

**Control**

Comparar también contra secuencia aleatoria de Poisson para confirmar que la repulsión de niveles no aparece por accidente.

### R4: Correlación cruzada entre primos y ceros

**Nivel inicial:** Modelo formal parcial.

**Pregunta:** ¿Los residuos de conteo primo y la señal construida desde ceros zeta comparten estructura medible?

**Procedimiento**

1. Construir una señal de residuo primo sobre una malla logarítmica.
2. Construir una señal espectral usando un número finito de ceros.
3. Normalizar ambas señales.
4. Medir correlación cruzada por desplazamiento.
5. Repetir con subconjuntos de ceros para estimar estabilidad.

**Advertencia**

Una correlación fuerte no prueba Riemann. Solo indica que el modelo espectral captura parte de la oscilación observada.

---

## Línea 3: Puente cuántico-operatorio

### Q1: Implementación de operadores observables

**Nivel inicial:** Modelo formal parcial.

**Operadores mínimos**

```text
E(n) = n mod 2
O(n) = (Psi(n), Omega(n), L(n))
EPS(a, b) = abs(a - b)
X(S, regla) = subconjunto de S que cumple regla
```

**Requisito**

Cada operador debe declarar:

- dominio;
- codominio;
- si conserva cardinalidad;
- si es filtro, proyección, ranking o transformación;
- si puede componer con otros operadores.

### Q2: Ablación de Exclusión

**Nivel inicial:** Evidencia heurística.

**Pregunta:** ¿Qué estructura desaparece cuando se elimina `X_prime`?

**Procedimiento**

1. Ejecutar G1 con Exclusión prima.
2. Ejecutar G1 sin Exclusión prima.
3. Ejecutar G1 con Exclusión por baja pérdida RAP.
4. Comparar espectros de distancia, `g(N)` y residuos.

**Interpretación permitida**

Si la estructura se degrada sin `X_prime`, la primalidad actúa como filtro estabilizador. No prueba que sea necesario en sentido lógico universal.

### Q3: Estabilidad de kappa por escala

**Nivel inicial:** Modelo formal parcial.

**Pregunta:** ¿`kappa_W` converge, oscila o se dispersa al aumentar la ventana?

**Procedimiento**

1. Medir `kappa_W` en ventanas crecientes.
2. Repetir con varios valores de `r`.
3. Repetir con reglas RAP alternativas.
4. Graficar trayectoria de `kappa_W`.

**Criterios**

- Si converge: candidato a constante experimental.
- Si oscila: posible firma modular o espectral.
- Si se dispersa: el conmutador no está bien definido para esa regla.

### Q4: Dualidad CED

**Nivel inicial:** Observación.

**Pregunta:** ¿Qué cambia cuando se aplica el Dual CED antes o después de RAP?

**Procedimiento**

1. Definir Dual como `Dual(I) = D` y `Dual(D) = I`.
2. Aplicar Dual a estados individuales y a particiones.
3. Comparar diagnósticos RAP antes y después del cambio.
4. Registrar casos donde la interpretación de estabilidad cambie sin cambiar la factorización.

**Uso esperado**

Este experimento sirve para separar estado CED de estructura RAP, evitando que el agente los confunda.

---

## Orden de ejecución recomendado

### Fase 1: Base exacta

- Implementar criba de primos.
- Implementar factorización.
- Implementar `NumberRecord`.
- Verificar CED y RAP contra ejemplos pequeños del Libro Cero.

### Fase 2: Goldbach operativo

- Ejecutar G1 hasta una ventana pequeña.
- Validar que no haya contraejemplos computacionales en esa ventana.
- Ejecutar G2 y G3.
- Registrar sensibilidad de `kappa_W`.

### Fase 3: Señales espectrales

- Ejecutar G4 sobre `g(N)`.
- Ejecutar R1 y R2.
- Separar residuos `Li_2` y `x/log(x)`.

### Fase 4: Zeta y GUE

- Importar o generar ceros zeta verificados.
- Ejecutar R3.
- Ejecutar R4 solo después de validar la normalización.

### Fase 5: Ciclo del agente

- El agente propone una hipótesis.
- El agente la clasifica por nivel de evidencia.
- El agente ejecuta un protocolo.
- El agente declara falsificadores.
- El agente actualiza el mapa de patrones sin elevar heurísticas a pruebas.

---

## Criterios de aceptación para el futuro simulador

Un simulador basado en este Libro Uno debe cumplir:

- produce resultados reproducibles con la misma semilla y parámetros;
- separa `Li_2(x)` de `x/log(x)`;
- guarda cada resultado con nivel de evidencia;
- reporta contraejemplos antes que interpretaciones;
- permite cambiar ventanas, umbrales y reglas RAP;
- no presenta una observación finita como demostración infinita;
- exporta datos crudos además de conclusiones narrativas.

## Riesgos y controles

| Riesgo | Control |
| --- | --- |
| Confundir metáfora con prueba | Campo obligatorio `evidence_level`. |
| Confundir igualdad con equivalencia | Usar `=`, `~=card` y `~=str` de forma separada. |
| Confundir `Li_2(x)` con `x/log(x)` | Reportar ambos residuos con nombres distintos. |
| Forzar patrones en ruido | Comparar contra controles permutados o Poisson. |
| Convertir `kappa` en dogma | Medir sensibilidad por ventana y regla. |

## Cierre

El Libro Uno convierte la intuición del Albañil en una disciplina de medición. Goldbach se vuelve un laboratorio de estabilidad CED/RAP. Riemann se vuelve una investigación espectral de residuos y ceros. El puente operatorio se vuelve una prueba de orden, exclusión y conmutación.

La obra avanza solo cuando cada hallazgo declara qué es: observación, heurística, modelo parcial o candidato a prueba.
