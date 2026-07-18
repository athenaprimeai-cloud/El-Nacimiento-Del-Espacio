# ATHENA DOMAIN-E004 — Pregunta (¿hay material para una pared?)

**Estado:** ejecutado + **addendum revisor** · H-01 solo vs C1 uniforme · H-00 **NO muerta** (pendiente Cramér / E005) · ver `ATHENA_DOMAIN_E004_ADDENDUM_REVIEW.md`  
**Después de:** E001 pico · E002 conservación · E003 resistencia de identidad — **tres cadáveres**  
**No es:** operador oculto · Hamiltoniano · “geometría de primos” · Hilbert–Pólya · Riemann todavía  

---

## Frontera post E001–E003

Ya no se busca una “sombra” en una señal.

Se evita **construir una sombra artificial con la propia linterna**.

```text
E001  "hay un pico"                    → muerto
E002  "hay una métrica conservada"     → muerto
E003  "hay resistencia de identidad"   → muerto
```

El siguiente experimento no busca la pared.  
Busca si existe **material** del que una pared pudiera estar hecha.

---

## Decisiones de orientación (MD-034 · MD-035 · MD-036)

### MD-034 — No invertir la dualidad sin declararlo

**No** (como afirmación):

\[
\text{primos} \rightarrow \text{espectro}
\]

**Sí** (marco legítimo):

\[
\text{objeto aritmético} \;\leftrightarrow\; \text{representación espectral}
\]

Relación conocida (literatura, no Athena-as-proof):

\[
\text{ceros de }\zeta(s)
\;\longrightarrow\;
\text{oscilaciones en la distribución de primos}
\]

(vía fórmula explícita).

El lab **puede** preguntar si existe una representación alternativa donde una estructura discreta produzca un espectro compatible con la estadística de los ceros.  
**No puede** afirmar que los primos *son* el espectro hasta construir el puente.

```text
HIPÓTESIS  "Los primos poseen una geometría espectral propia"
ESTADO     NO DEMOSTRADA · NO DESCARTADA
```

### MD-035 — Regla anti-contrabando aritmético

Prohibido definir aristas (o pesos) con:

```text
p | n
gcd(p, n) = 1   (como regla de geometría “nueva”)
factor(n)
comparte factores / divide a / …
```

y luego decir “descubrimos una geometría de primos”.  
Eso es **divisibilidad con traje espectral**.

**Grafo permitido:** relaciones **externas** al conocimiento primo.

\[
V = \{1,2,\ldots,N\}
\]

Ejemplos de \(E\) legítima:

| Familia | Regla |
| ------- | ----- |
| Vecindad ordinal | \((i,j)\in E \iff 0 < \|i-j\| \le k\) |
| Distancia embebida | \((i,j)\in E \iff d(i,j) < \varepsilon\) |
| Tras transformación geométrica previa | cercanía de \(T(i),T(j)\) **sin** factorización |

La **etiqueta** “pertenece al conjunto \(S\)” (primos, control, …) se usa solo para **seleccionar el subconjunto de vértices** a medir — no para definir \(E\).

### MD-036 — Controles negativos obligatorios

Un detector que “solo funciona en primos” no basta. Debe confrontarse con:

| Universo | Conjunto | Rol |
| -------- | -------- | --- |
| Real | \(P =\) primos \(\le N\) | objeto |
| Impostor 1 | misma cardinalidad / densidad aproximada, aleatorio | sin estructura conocida |
| Impostor 2 | semiprimos \(\{pq\}\) | estructura multiplicativa **distinta** |
| Impostor 3 | secuencia artificial (p.ej. Ulam / regla generativa) | estructura no prima |

Criterio **no** es “¿el grafo de primos tiene alguna propiedad?”  
(casi todo conjunto finito tiene alguna).

Criterio:

\[
\Delta(P,\,S_{\mathrm{control}}) \gg 0
\quad\text{y}\quad
\text{la firma de }P\text{ no se reduce a densidad/orden}
\]

---

## Pregunta de DOMAIN-E004

**No:**

> ¿Cuál es el operador / Hamiltoniano / geometría de los primos?

**Sí:**

> **¿Existe una estructura espectral emergente en una representación no aritmética de los naturales que discrimine el conjunto de primos frente a conjuntos de control predeclarados?**

---

## Esquema (un ladrillo)

```text
X = ℕ_{1..N}     (sin información prima en la geometría)
        │
        ▼
   G(X) grafo con E ∈ familia permitida (MD-035)
        │
        ▼
   L_G = D − A     (o L inducida en S ⊂ V)
        │
        ▼
   una métrica espectral M(·)  (una sola en campaña 1)
        │
        ▼
   M(P)  vs  M(C1), M(C2), M(C3)  (+ réplicas de C1)
```

---

## Hipótesis (borrador → protocolo)

| ID | Enunciado |
| -- | --------- |
| **H-ATH-D004-00** | El espectro (vía \(M\)) depende solo de densidad / disposición ordinal: \(D(P,C)\approx 0\) bajo controles. |
| **H-ATH-D004-01** | Existe firma espectral estable que distingue primos: \(D(P,C) > D_{\mathrm{nulo}}\) bajo múltiples controles. |

Ambas son éxitos del lab.

---

## Disciplina quirúrgica (recomendación de lab)

Antes de ejecutar:

- \(N\) bajo primero (\(10^4\)–\(10^5\))  
- **una** familia de grafos  
- **una** métrica espectral  
- controles **congelados antes** de mirar resultados  
- sin Hilbert–Pólya, sin modularidad, sin Riemann todavía  

Primero: ¿existe el ladrillo?  
Después: ¿pertenece a una catedral?

---

## Montaña

```text
¿estructura generativa → primos?
        ↑
¿hay material (firma espectral no aritmética vs controles)?  ← E004
        ↑
E003: resistencia de identidad no
E002: conservación de P no
E001: pico 1/6 no
```

---

# FIN — DOMAIN-E004 PREGUNTA

*No la pared.  
El material — si es que hay material.*
