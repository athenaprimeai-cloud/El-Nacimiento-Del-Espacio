# T-04 — Generador ciego de referencia (especificación cerrada)

**Familia:** T-04 (proceso de renovación / gaps paramétricos)  
**Estado:** **ESPECIFICACIÓN CONGELADA**  
**Fecha:** 2026-07-18  
**Anclas:** MD-068 · MD-069 · `ATHENA_MECHANISM_DISCOVERY_SYNTHESIS.md`  
**No es:** T-01 con otra pintura · T-03 con otra tabla · candidato Intake · explicación Athena  

---

## 0. Tabla de frontera (R-DIV) — **antes** de la regla

| Eje | T-01 | T-03 | **T-04 debe ser** |
| --- | ---- | ---- | ----------------- |
| Dinámica | estocástica local (vecindad) | determinista CA | **proceso de puntos por renovación de gaps** |
| Azar | continuo en cada paso (birth) | solo inicial | **en los gaps** (secuencia de incrementos), no en una rejilla de bits |
| Estado | campo binario \(x\in\{0,1\}^N\) | campo binario \(x\in\{0,1\}^N\) | **conjunto de posiciones** construido por suma de gaps (no campo evolutivo) |
| Interacción | exclusión / conteo de vecinos | tabla local \(f\) | **sin interacción espacial de vecindad**: cada gap i.i.d. (o markov de orden 0 en la ola 1) |
| Evolución | actualización síncrona del campo | actualización síncrona del campo | **no hay “tiempo de CA”**: un solo barrido de renovación hasta cubrir \(\{1..N\}\) |

### Frase de control

> **Si T-04 puede describirse honestamente como “T-01 con…” o “T-03 con…”, no es T-04.**

| ¿Es “T-01 con…”? | **No** — no hay campo \(x_i\), no hay \(\theta\), no hay birth local |
| ¿Es “T-03 con…”? | **No** — no hay tabla \(f\), no hay pasos síncronos, no hay \(W\) |

### Ceguera de diseño

No leer: raw/analysis T-01 o T-03, SURVIVORS, E00x, classification.  
Solo: Phase III general, MD-035, esta spec, config de ola.

---

## Misión

```text
HUECO (renovación / gaps)
  ↓
DIVERSIDAD ESTRUCTURAL (tabla §0)
  ↓
SPEC (este documento)
  ↓
GENERADOR CIEGO
  ↓
DATOS → PROPIEDADES → NECESSARY → ¿P*?
```

No se exige hipótesis Athena.  
Solo cartografiar una **región no cubierta**.

---

## 1. Definición formal de la familia

### Objeto de salida

Un conjunto finito

\[
S \subset \{1,2,\ldots,N\}
\]

interpretado como posiciones **ocupadas** / **eventos de renovación**.

### Generación (proceso de renovación clásico en la recta discreta)

1. Fijar \(N \in \mathbb{N}\), semilla \(s\), ley de gaps \(\mathcal{L}(\alpha)\) con parámetros \(\alpha\).  
2. RNG: `random.Random(s)`.  
3. Sea \(p_0 = 0\) (origen auxiliar; **no** forma parte de \(S\) salvo regla opcional — **ola 1: \(p_0=0\) no incluido en \(S\)**).  
4. Mientras el último punto \(p < N\):  
   - extraer gap \(G \sim \mathcal{L}(\alpha)\), entero \(\ge 1\);  
   - \(p \leftarrow p + G\);  
   - si \(1 \le p \le N\), añadir \(p\) a \(S\);  
   - si \(p > N\), parar (no añadir).  
5. Salida: \(S\) ordenado, cardinalidad, densidad \(|S|/N\).

**No hay** bucle de tiempo \(t=0..T\) sobre un campo binario.

### Ley de gaps — ola 1 (cerrada)

**Solo una subfamilia en ola 1** (mínima, no grilla infinita):

#### \(\mathcal{L}\) = geométrica en \(\{1,2,\ldots\}\)

\[
\mathbb{P}(G = k) = (1-q)^{k-1} q, \quad k=1,2,\ldots
\quad q \in (0,1)
\]

Implementación:  
`G = 1 + floor(log(U) / log(1-q))` con \(U\sim\mathrm{Unif}(0,1)\),  
o equivalente `rng.geometric(q)` si se documenta convención (éxitos: número de trials hasta primer éxito = G).

**Python:** usar

```text
G = 0
while True:
    G += 1
    if rng.random() < q:
        break
```

(ensayo-Bernoulli hasta éxito; \(G\ge 1\)).

### Parámetros de la familia

| Símbolo | Significado |
| ------- | ----------- |
| \(N\) | horizonte |
| \(q\) | parámetro de la geométrica |
| \(s\) | semilla del RNG |

**No hay** \(r, \theta, W, T, p_{\mathrm{birth}}\) de T-01/T-03.

### Frontera de información

| Puede | No puede |
| ----- | -------- |
| \(N, q, s\) | primalidad de posiciones |
| draws i.i.d. de gaps | gcd / factores |
| | vecindad / CA / exclusión T-01 |
| | leer Athena o T-01/T-03 results |

---

## 2. Generador mínimo

```text
discovery/t04_reference_generator.py
```

Solo: generación, semillas, serialización, hash, metadatos.  
**No** analiza, no compara, no busca P\*.

### Firma

```text
generate_t04(N, q, seed) -> dict
```

### Salida por corrida

```json
{
  "family": "T-04",
  "spec_version": "1.0",
  "params": { "N": ..., "q": ..., "seed": ..., "gap_law": "geometric" },
  "occupied": [ ... ],
  "cardinality": ...,
  "density": ...,
  "n_gaps_drawn": ...,
  "mean_gap_realized": ...
}
```

### Artefactos de ola

```text
results/T04_REFERENCE_WAVE1/
  raw_runs.jsonl
  wave_manifest.json
  sha256.txt
```

---

## 3. Config Ola 1 (archivo separado)

```text
discovery/t04_wave1_config.json
```

| Parámetro | Valores |
| --------- | ------- |
| \(N\) | \(1000,\ 5000,\ 10000\) |
| \(q\) | \(0.1,\ 0.2,\ 0.3,\ 0.5\) |
| seeds | \(0..19\) |

Producto cartesiano; sin optimización.

**Esperanza teórica de gap:** \(\mathbb{E}[G]=1/q\).  
Densidad esperada de renovaciones \(\approx q\) (para gran \(N\)).  
Eso es **cartografía**, no P\* Athena.

---

## 4. Análisis (módulo posterior)

```text
discovery/analyze_t04_wave1.py
```

Clases: NECESSARY | EMPIRICAL | SEED_DEPENDENT | UNKNOWN.

Candidatos a NECESSARY (demostrar en capa posterior, no inventar P\*):

- \(\mathbb{E}[|S|]/N \to q\) cuando \(N\to\infty\) (renovación elemental).  
- Gaps i.i.d. ⇒ no hay correlación espacial de vecindad tipo CA.  
- Independencia de “empaquetamiento por exclusión síncrona” (anti-T-01).

---

## 5. P\* e Intake

Misma disciplina:

```text
REGLA → RAW → PROPIEDADES → NECESSARY
  → ¿P* peligrosa no trivial hacia Athena? 
  → si no: REFERENCE_COMPLETE
```

**Sin obligación** de P\*.

---

## 6. Checklist

- [x] Tabla de frontera R-DIV  
- [x] Spec 1.0  
- [x] No es T-01/T-03 con…  
- [ ] Generador + ola 1  
- [ ] Análisis + capa necesaria / STATUS  

---

# FIN — T-04 REFERENCE GENERATOR SPEC 1.0

*Hueco: renovación.  
No bits que evolucionan.  
Puntos que se suman.*
