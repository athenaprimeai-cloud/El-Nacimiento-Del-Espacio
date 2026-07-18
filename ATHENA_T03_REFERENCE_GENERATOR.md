# T-03 — Generador ciego de referencia (especificación cerrada)

**Familia:** T-03 (autómata celular elemental / totalístico binario 1D)  
**Estado:** **ESPECIFICACIÓN CONGELADA** · código **no** implementado aún  
**Fecha:** 2026-07-18  
**Anclas:** MD-065 · Phase III · `ATHENA_MECHANISM_TAXONOMY.md`  
**No es:** candidato Intake · variante de T-01 · explicación Athena  

---

## Condición de apertura (MD-065)

> **T-03 debe ser una clase de dinámica realmente distinta de T-01,  
> no el mismo vehículo con otra pintura.**

| | T-01 (cerrado) | T-03 (este doc) |
| - | -------------- | --------------- |
| Tipo | Exclusión + nacimiento probabilista | **Regla local determinista finita** sobre vecindad binaria |
| Aleatorio | init + births cada paso | **solo** estado inicial (la transición es determinista) |
| Memoria de regla | umbrales \(\theta, p_{\mathrm{birth}}\) | **tabla** \(f:\{0,1\}^{2r+1}\to\{0,1\}\) o código de Wolfram si \(r=1\) |
| Objeto | conjunto ocupación | trayectoria + ocupación final |

### Ceguera de diseño experimental

> **Al diseñar e implementar T-03 no se permite mirar**  
> resultados de T-01 (raw/analysis), ni SURVIVORS, ni E001–E007,  
> salvo las **reglas generales** de Phase III (MD-035, ceguera, pipeline).

Las restricciones TR-01…TR-04 de T-01 sirven solo para **declarar diferencia de clase**,  
no para copiar parámetros ni “mejorar” empaquetamiento.

---

## Misión

Segundo vehículo de la carretera:

```text
T-03 SPEC (este documento)
  ↓
GENERACIÓN CIEGA
  ↓
DATOS BRUTOS
  ↓
PROPIEDADES (NECESSARY / EMPIRICAL / …)
  ↓
CONSECUENCIAS NECESARIAS
  ↓
¿P*?  → solo si no trivial y peligrosa
  ↓
INTAKE o REFERENCE_COMPLETE
```

---

## 1. Definición formal de la familia

### Espacio de estados

\[
x^{(t)} = (x_1^{(t)},\ldots,x_N^{(t)}) \in \{0,1\}^N
\]

### Radio y vecindad (condición periódica o borde muerto — **fijado**)

**Borde:** **nulo** (fuera de \(\{1..N\}\) se lee como 0).  
No periódico en la spec 1.0 (evita otra familia de simetrías).

Radio entero \(r \ge 1\):

\[
\eta_i^{(t)} = \bigl(x_{i-r}^{(t)},\ldots,x_i^{(t)},\ldots,x_{i+r}^{(t)}\bigr)
\quad\text{con }x_j:=0\text{ si }j\notin\{1..N\}.
\]

### Regla de transición — **determinista y síncrona**

\[
x_i^{(t+1)} = f\bigl(\eta_i^{(t)}\bigr)
\]

donde

\[
f : \{0,1\}^{2r+1} \to \{0,1\}
\]

está dada por una **tabla completa** de \(2^{2r+1}\) bits  
(o, si \(r=1\), por un **código de Wolfram** \(W\in\{0,\ldots,255\}\) en la codificación estándar).

**Síncrono:** todas las lecturas desde \(x^{(t)}\); ninguna escritura intermedia.

### Codificación de \(f\) (ola de referencia)

**Modo A (preferido ola 1):** \(r=1\), regla de Wolfram \(W\).

Bit \(k\) de \(W\) (0-based, LSB = vecindad 000) define \(f\) sobre el entero  
\(4x_{i-1}+2x_i+x_{i+1}\).

**Modo B (fuera de ola 1):** \(r>1\), tabla explícita de longitud \(2^{2r+1}\)  
— requiere `spec_version` 1.1+ y config de ola propia.

### Estado inicial

Bernoulli i.i.d. con probabilidad \(p_{\mathrm{init}}\), RNG `Random(seed)`, orden \(i=1..N\).

### Criterio de parada

Tras \(T\) pasos síncronos: \(x^{(T)}\).

### Salida

\[
S = \{ i : x_i^{(T)} = 1 \}
\]

más resumen de trayectoria (densidad por \(t\), opcional).

### Frontera de información

| Puede | No puede |
| ----- | -------- |
| \(N, r, W\) (o tabla \(f\)), \(p_{\mathrm{init}}, T, seed\) | primalidad, gcd, factores |
| Vecindad ordinal binaria | leer T-01 raw/analysis |
| | leer SURVIVORS / E00x |
| | ajustar \(W\) mirando Athena o T-01 |

---

## 2. Por qué no es “T-01 con otra pintura”

| Criterio de diferencia | Cumple |
| ---------------------- | ------ |
| Transición determinista vs estocástica de birth | sí |
| Regla = tabla booleana finita, no umbral de conteo + \(p_{\mathrm{birth}}\) | sí |
| Sin parámetro de “exclusión por conteo \(\theta\)” | sí |
| Clase clásica distinta (CA elemental) | sí |

Si alguien reimplementa T-01 simulando births con una tabla — **rechazo de clase** en review Phase III.

---

## 3. Generador mínimo (spec de implementación futura)

```text
discovery/t03_reference_generator.py
```

**Prohibido en el módulo:**

- paths/imports a `ATHENA_DOMAIN_*`, `ATHENA_SURVIVORS*`, `classification.json`
- lectura de `results/T01_*` o `discovery/T01_*` datos

**Permitido:** `random`, `json`, escribir bajo `results/T03_REFERENCE_WAVE1/`.

### Firma

```text
generate_t03(N, W, p_init, T, seed) -> dict
  # r fijo = 1 en ola 1
```

### Actualización síncrona

```text
for t in range(T):
    x_next[i] = f(neighborhood(x, i))  for all i   # from x only
    x = x_next
```

Nunca actualizar in-place de izquierda a derecha para la decisión.

---

## 4. Config de Ola 1 (archivo separado, no altera la familia)

```text
discovery/t03_wave1_config.json
```

Rejilla **cerrada** propuesta (congelar al crear el JSON, antes de correr):

| Parámetro | Valores ola 1 |
| --------- | ------------- |
| \(N\) | \(1000,\ 5000,\ 10000\) |
| \(r\) | \(1\) (fijo) |
| \(W\) | conjunto **pequeño predeclarado** de códigos Wolfram (ver abajo) |
| \(p_{\mathrm{init}}\) | \(0.5\) |
| \(T\) | \(10,\ 50,\ 100\) |
| seeds | \(0..19\) |

### Conjunto \(W\) de ola 1 (cerrado, no “los que se vean interesantes después”)

Códigos clásicos de referencia de la literatura CA, **elegidos por diversidad de clase**  
(no por resultado de T-01 ni Athena):

```text
W ∈ { 0, 4, 22, 30, 54, 90, 110, 126, 150, 184 }
```

- 0: nulo  
- 4, 22: clase limitada  
- 30, 90, 150: caóticos / aditivos  
- 54, 110, 126: complejos / borde  
- 184: tráfico elemental  

**Prohibido:** añadir un \(W\) a la ola 1 después de ver salidas sin abrir `wave2`.

---

## 5. Salida bruta

```text
results/T03_REFERENCE_WAVE1/
  raw_runs.jsonl
  wave_manifest.json
  sha256.txt
```

Cada registro: `params`, `occupied`, `cardinality`, `density`, `trajectory_summary.density_by_t`.

---

## 6. Análisis (módulo separado, después)

```text
discovery/analyze_t03_wave1.py
```

Clases: `NECESSARY | EMPIRICAL | SEED_DEPENDENT | UNKNOWN`

**NECESSARY** solo con justificación desde \(f\) / \(W\), no “salió en 20/20 seeds”.

Ejemplos de candidatos a demostrar (no asumir):

- reglas nulas / homicidas globales  
- conservación de paridad (reglas aditivas mod 2)  
- densidades límite en reglas de tráfico (184)

---

## 7. P\* e Intake

Misma disciplina que T-01:

```text
REGLA → GENERACIÓN → COMPORTAMIENTO → CONSECUENCIA NECESARIA
  → ¿P* peligrosa no trivial? → INTAKE
  → si no → REFERENCE_COMPLETE
```

**No** inventar P\* porque se parezca a primos o a T-01.

---

## 8. Checklist

- [x] Clase distinta de T-01 declarada  
- [x] Spec 1.0 cerrada  
- [x] Ceguera T-01/Athena en diseño  
- [ ] `t03_wave1_config.json`  
- [ ] `t03_reference_generator.py`  
- [ ] Ola 1 + análisis  
- [ ] Capa necesaria / cierre de estado  

---

## Historial

| Fecha | Cambio |
| ----- | ------ |
| 2026-07-18 | Spec 1.0; T-01 REFERENCE_COMPLETE; T-03 abierto |

---

# FIN — T-03 REFERENCE GENERATOR SPEC 1.0

*Otro vehículo.  
Otra clase.  
Misma aduana al final — si alguna vez hay P\*.*
