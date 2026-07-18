# ATHENA DOMAIN-E003 — Protocolo **CONGELADO**

**Clase:** dominio Athena · identidad de \(\mathcal{T}\) · resistencia diferencial  
**Versión:** **1.0 CONGELADO** (corrección lab: rectangular + \(D_q\) + borde en fase 2)  
**Fecha:** 2026-07-17  
**No es:** operador · catedral · reabrir E001/E002 con el mismo \(P\) y otro relato  

---

## 1. Pregunta

> Bajo transformaciones \(\mathcal{T}\in\mathcal{G}_{\mathrm{adm}}\) predeclaradas (que conservan la **definición** del objeto, no su apariencia),  
> ¿la **discrepancia de identidad**  
> \(\Delta = D_q\big(R(X),\mathcal{T}(R(X))\big)\)  
> es **sistemáticamente menor** en el objeto real que en gemelos nulos sometidos al **mismo** \(\mathcal{T}\)?

En una línea:

> **¿Hay resistencia intrínseca al mover la lámpara, o solo la lámpara?**

---

## 2. Objeto \(X\) y representación \(R\)

```text
X  =  G(N)  conteos Goldbach, N par ∈ [4, N_max]
N_max = 10000
fuente: artifacts/goldbach/goldbach_partitions_4_10000.csv

R(X) = r  residual media sobre la ventana completa:
       r(N) = G(N) - mean(G)   (índices ordenados de N pares)
```

**Definición que no puede romperse:** \(G(N)=\#\{(p,q):p+q=N,\,p,q\text{ primos}\}\).  
Ningún \(\mathcal{T}\) reescribe esa definición; solo actúa sobre \(R(X)\).

---

## 3. \(\mathcal{G}_{\mathrm{adm}}\) — reglas de entrada (congeladas)

| # | Regla | Operacionalización en E003 |
| - | ----- | -------------------------- |
| 1 | Preserva la definición del objeto | No altera la construcción de \(G\); solo cambia el dominio de observación |
| 2 | No aumenta información | No introduce muestras nuevas de primos; no rellena con modelo generativo |
| 3 | No introduce estructura externa | **Sin** pesos suavizantes en la medición principal; sin bases artificiales |
| 4 | Aplicable idénticamente a nulos | Misma receta sobre \(G_{\mathrm{nulo}}\) |
| 5 | Reversible conceptual | Se entiende qué se perdió (región no vista) y qué se conservó (definición de \(G\)) |

---

## 4. Ventanas — campaña 1 (FASE 1)

### Principio

> La transformación cambia el **dominio**, no la identidad.

### Forma primaria: **rectangular**

\[
W_k(n)=
\begin{cases}
1 & n\in[a_k,b_k]\\
0 & \text{fuera}
\end{cases}
\]

**Motivo:** máxima transparencia. No introduce pesos externos. No altera amplitudes relativas **dentro** del dominio.  
Si aparece diferencia real vs nulo, **no** fue una función de ponderación inventando geometría.

**Costo:** borde duro (Gibbs). **No** se “arregla” en la medición principal.

### Morfología: un instrumento, cinco campos de visión

Las cinco ventanas **no** son cinco formas distintas (cinco instrumentos).  
Son la **misma regla rectangular**, con **posiciones** distintas y **misma escala**:

```text
W1 ██████████
W2   ██████████
W3      ██████████
W4          ██████████
W5              ██████████
```

Operacionalización congelada (índices \(0..n-1\), \(n=\#\{N\text{ par}\}\)):

| Parámetro | Valor |
| --------- | ----- |
| Longitud \(L\) | \(\lfloor n/2\rfloor\) (misma escala) |
| Inicios \(a_i\) | \(0,\;\lfloor m/4\rfloor,\;\lfloor 2m/4\rfloor,\;\lfloor 3m/4\rfloor,\; m\) donde \(m=n-L\) |
| Intervalo \(I_i\) | \([a_i,\,a_i+L)\) |

Pregunta operativa:

> ¿La estructura **acompaña** al objeto cuando movemos el campo de visión?

**No:** ¿qué ventana produce el patrón más bonito?

### Sin interpolación al comparar soportes

Para cada \(I_i\):

- \(r|_{I_i}\): subserie del residual **global** restringida a \(I_i\)  
- \(r_i\): residual **recalculado** (media local de \(G\) en \(I_i\))  

Misma longitud; **sin** re-muestreo interpolado.

### Fuera de campaña 1 (no ejecutado aquí)

| \(\mathcal{T}\) | Estado |
| --------------- | ------ |
| Dilatación escalar + multi-interpolador | E003b |
| Cambio de base | Exploratoria |

---

## 5. Instrumento: discrepancia espectral fraccionaria \(D_q\)

**No** se llama “distancia \(L^{1/2}\)” (evita heredar axiomas métricos innecesarios).

Sean \(S_1,S_2\) densidades de potencia FFT **normalizadas** (excl. DC):

\[
S_k = \frac{|U_k|^2}{\sum_{j\ge 1}|U_j|^2}
\]

\[
D_q(S_1,S_2)
=
\left(
\sum_k |S_1(k)-S_2(k)|^q
\right)^{1/q}
\qquad
q=\frac12
\]

**Nombre en informes:** *discrepancia espectral fraccionaria* \(D_{1/2}\).  
No se afirma que \(D_q\) sea una métrica clásica.

Para cada ventana \(i\):

\[
\Delta^{(i)}
=
D_{1/2}\!\big(
S(r|_{I_i}),\;
S(r_i)
\big)
\]

---

## 6. Estadístico de resistencia

\[
\Delta_{\mathrm{real}}
=
\mathrm{median}_{i\in\{W1..W5\}}\;\Delta^{(i)}_{\mathrm{real}}
\]

Para cada réplica nula \(s\), el **mismo** pipeline:

\[
\Delta_{\mathrm{nulo},s}
=
\mathrm{median}_{i}\;\Delta^{(i)}_{s}
\]

\[
\delta_s = \Delta_{\mathrm{nulo},s} - \Delta_{\mathrm{real}}
\]

\(p =\) fracción de seeds con \(\delta_s \le 0\)  
(nulo tan o más “resistente”: \(\Delta_{\mathrm{nulo}}\le\Delta_{\mathrm{real}}\)).

---

## 7. Nulos gemelos

| ID | Nulo | Procedimiento |
| -- | ---- | ------------- |
| **N1** | Permutación de \(G\) | Barajar \(G\) (seed \(s\)); ventanas idénticas |
| **N2** | Bootstrap de bloques | Bloques \(B=50\); mismo pipeline |

Seeds: \(s=0..99\).

---

## 8. Criterios de veredicto (FASE 1)

| Resultado | Condición |
| --------- | --------- |
| **H-01 PERSISTE** | \(p_{\mathrm{N1}}\le 0.05\) **y** \(p_{\mathrm{N2}}\le 0.05\) **y** \(\Delta_{\mathrm{real}} < \mathrm{median}_s\Delta_{\mathrm{nulo},s}\) en **ambos** nulos |
| **H-00 DESAPARECE** | \(p_{\mathrm{N1}}>0.10\) **o** \(p_{\mathrm{N2}}>0.10\) **o** \(\Delta_{\mathrm{real}} \ge \mathrm{median}_s\Delta_{\mathrm{nulo}}\) en algún nulo de forma no marginal |
| **NO_SABEMOS** | resto |

---

## 9. FASE 2 — auditoría de borde (solo si hay sombra)

**No** se mezcla con la medición principal.  
**No** se usa para “buscar” señal.

```text
Corrida principal (rectangular)
        |
        v
Δ_real vs Δ_nulo
        |
        +---- no diferencia → no abrir FASE 2 (probable no-sombra)
        |
        +---- sí diferencia → auditar borde
                    |
                    v
              W_Hann, W_Hamming
                    |
                    v
              ¿la diferencia sobrevive?
```

Razón metodológica:

| Si… | Riesgo |
| --- | ------ |
| Suavizado desde el inicio | Matar señal real |
| Borde duro siempre sin auditoría | Crear señal falsa |
| **Separar fases** | No elegir un bando a ciegas |

FASE 2 **no** se ejecuta en v1.0 salvo veredicto PERSISTE (o NO_SABEMOS con \(\Delta_{\mathrm{real}}\) claramente menor en mediana). Código puede dejar el hook; no forma parte de la búsqueda.

---

## 10. Ficha de salida (obligatoria)

```text
Objeto:          G(N) Goldbach, N par ∈ [4,10000]
R:               residual media
G_adm campaña:   W1–W5 rectangulares, L=n/2, 5 posiciones
instrumento:     D_{1/2} discrepancia espectral fraccionaria (excl. DC)
Δ_real:          …
median Δ_nulo N1 / N2: …
p_N1 / p_N2:     …
FASE 2 borde:    NO_EJECUTADA | (si PERSISTE: resultados Hann/Hamming)
Interpretación:  PERSISTE | DESAPARECE | NO_SABEMOS
```

---

## 11. No-afirmaciones

Incluso PERSISTE:

- no variedad · no operador · no “estructura → primos”  
- solo resistencia diferencial bajo **estas** ventanas rectangulares y **esta** \(D_{1/2}\)  
- no legitimar dilataciones/bases sin nuevo ID  
- \(D_q\) no se eleva a métrica del espacio de objetos

---

## 12. Ejecución

```text
scripts/run_athena_domain_e003.py
ATHENA_DOMAIN_E003/resultados/
```

---

## 13. Deuda explícita

- FASE 2 Hann/Hamming: solo si FASE 1 deja sombra.  
- Dilatación / base: E003b+.  
- Otros instrumentos de discrepancia: **nuevo ID**.

---

# FIN — DOMAIN-E003 PROTOCOL 1.0

*Era II no fabrica el instrumento perfecto.  
Descubre qué instrumentos merecen existir.*
