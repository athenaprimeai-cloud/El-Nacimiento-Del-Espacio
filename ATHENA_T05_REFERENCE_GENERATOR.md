# T-05 — Generador ciego de referencia (especificación cerrada)

**Familia:** T-05 (embedding / proceso puntual en \(\mathbb{R}^d\) + selección métrica)  
**Estado:** **SPEC 1.0 CONGELADA** · generador **aún no implementado**  
**Fecha:** 2026-07-18  
**Anclas:** MD-072 · `discovery/T05_RDIV_BOUNDARY.md`  
**No es:** T-01/T-03/T-04 con pintura · Intake · P\* · Athena  

**Precondición:** frontera R-DIV aceptada → representación **sí** es nueva (checks de boundary).

---

## Pregunta de la familia

> ¿Qué sucede cuando la relación fundamental entre entidades  
> deja de ser “quién está al lado de quién”  
> y pasa a ser “a qué distancia se encuentran”?

---

## 1. Definición formal

### Generación de la geometría (generativa)

1. Fijar dimensión \(d\), número de puntos \(n\), semilla \(s\).  
2. RNG `random.Random(s)`.  
3. Muestrear i.i.d.

\[
X_i \sim \mathrm{Unif}([0,1]^d), \quad i=1,\ldots,n.
\]

(Proceso de Bernoulli / aproximación a PPP en la caja unitaria.)

**No** se usa el índice \(i\) como posición en \(\mathbb{N}\) para la regla de selección.

### Relación primaria

Distancia euclídea:

\[
\delta(i,j) = \|X_i - X_j\|_2.
\]

### Selección métrica — hard-core secuencial (tipo Matérn / RSA simple)

1. Permutación aleatoria \(\pi\) de \(\{1,\ldots,n\}\) con el **mismo** RNG (continuar el stream tras los \(X_i\), o `Random(s+1)` — **congelado:** `Random(s+1)` para \(\pi\)).  
2. \(S \leftarrow \emptyset\).  
3. Para \(i\) en orden \(\pi\):  
   - aceptar \(i\) en \(S\) **ssi** para todo \(j\in S\) ya aceptado, \(\delta(i,j) \ge \varepsilon\).  
4. Salida:  
   - etiquetas aceptadas \(S\subset\{1,\ldots,n\}\)  
   - coordenadas \(\{X_i : i\in S\}\) (para reconstruir, no para Athena)  
   - cardinalidad, densidad \(=|S|/n\)

**Umbral** \(\varepsilon \in (0,1)\) es el único parámetro de interacción métrica en ola 1.

### Por qué es generativa (no decorativa)

| Check | Cumple |
| ----- | ------ |
| Sin \(\{X_i\}\) la regla no se puede evaluar | sí |
| Sustituir \(\delta\) por \(|i-j|\) define **otra** familia | sí |
| \(\{X_i\}\) no se construyen desde primos/E00x | sí |

### Frontera de información

| Puede | No puede |
| ----- | -------- |
| \(d, n, \varepsilon, s\) | primalidad, gaps en \(\mathbb{N}\) como regla |
| \(X_i\), \(\|X_i-X_j\|\) | vecindad ordinal como sustituto de \(\delta\) |
| | leer T-01/T-03/T-04 raw, SURVIVORS, E00x |
| | ajustar \(\varepsilon\) para “parecerse” a Athena |

---

## 2. Anti-pintura (resumen)

| | |
| - | - |
| ≠ T-01 | no campo en \(\mathbb{N}\); no \(\theta,p_b\) |
| ≠ T-03 | no CA; no \(W\) |
| ≠ T-04 | no gaps i.i.d. sobre la recta; la estructura es **espacial** en \(\mathbb{R}^d\) |

---

## 3. Generador (implementación futura)

```text
discovery/t05_reference_generator.py
```

Solo: muestreo, hard-core métrico, serialización, hash.  
No analiza, no compara, no P\*.

### Firma

```text
generate_t05(n, d, epsilon, seed) -> dict
```

### Salida por corrida

```json
{
  "family": "T-05",
  "spec_version": "1.0",
  "params": { "n": ..., "d": ..., "epsilon": ..., "seed": ... },
  "occupied": [ ... etiquetas 1..n aceptadas ... ],
  "coordinates_accepted": [ [x,y,...], ... ],
  "cardinality": ...,
  "density": ...,
  "mean_nn_distance_accepted": ...
}
```

### Artefactos de ola

```text
results/T05_REFERENCE_WAVE1/
  raw_runs.jsonl
  wave_manifest.json
  sha256.txt
```

---

## 4. Config Ola 1 (archivo separado, **antes** de correr)

```text
discovery/t05_wave1_config.json
```

| Parámetro | Valores ola 1 |
| --------- | ------------- |
| \(d\) | \(2\) (fijo) |
| \(n\) | \(500,\ 1000,\ 2000\) |
| \(\varepsilon\) | \(0.03,\ 0.05,\ 0.08,\ 0.12\) |
| seeds | \(0..19\) |

Producto cartesiano; sin optimización; sin mirar Athena.

---

## 5. Análisis posterior (no en el generador)

```text
discovery/analyze_t05_wave1.py
```

Clases: NECESSARY | EMPIRICAL | SEED_DEPENDENT | UNKNOWN.

Candidatos a NECESSARY (capa posterior):

- Si \(\varepsilon \ge \sqrt{d}\), a lo sumo un punto (diámetro de \([0,1]^d\)).  
- Hard-core: min distancia entre aceptados \(\ge \varepsilon\) por construcción.  
- Densidad acotada por packing en la caja (orden \(\varepsilon^{-d}\)).

**No** forzar P\* Athena.

---

## 6. Checklist

- [x] R-DIV boundary  
- [x] Representación nueva = **SÍ**  
- [x] Spec 1.0  
- [ ] `t05_wave1_config.json`  
- [ ] `t05_reference_generator.py`  
- [ ] Ola 1 + análisis + STATUS  

---

## 7. Si no hay P\*

```text
T05_STATUS = REFERENCE_COMPLETE
PSTAR = NONE
INTAKE = NOT_ELIGIBLE
```

Habremos mostrado: **tercera representación (métrica) tampoco basta sola**  
→ reduce el espacio de mecanismos posibles.

---

# FIN — T-05 REFERENCE GENERATOR SPEC 1.0

*De la línea al espacio.  
Geometría generativa, no decorativa.  
Generador después de esta spec.*
