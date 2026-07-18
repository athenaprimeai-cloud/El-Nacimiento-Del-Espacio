# ATHENA DOMAIN-E001 — Protocolo **CONGELADO**

**Programa:** Athena (dominio) sobre kernel medido  
**Versión:** **1.0 CONGELADO**  
**Fecha:** 2026-07-17  
**No es:** demostración de primos · teoría completa · META-E  

---

## 1. Pregunta

> Si formamos el residuo de los **conteos Goldbach** \(G(N)\) (pares primos de \(N\) par) en \(N\in[4,N_{\max}]\) y su espectro de potencia FFT,  
> ¿el pico cerca de **frecuencia \(1/6\)** (periodo \(\approx 6\)) es **extremo** frente a controles nulos,  
> o es compatible con **artefacto / ruido / nulo**?

En una línea:

> **¿La firma espectral \(\sim 1/6\) en el residuo Goldbach es del objeto o de la transformación/nulo?**

---

## 2. Hipótesis

| ID | Enunciado |
| -- | --------- |
| **H-ATH-D001-01** | El pico \(\sim 1/6\) en el residuo es **extremo** frente a nulos predeclarados (apoyo **relativo** a estructura no trivial del conteo **bajo este control**). |
| **H-ATH-D001-00** | El pico **no** es extremo frente a nulos (compatible con artefacto, tendencia residual, o azar bajo el nulo). |

Ambas son éxitos del lab. “Pared pintada” es un resultado válido.

---

## 3. Señal predeclarada

| Campo | Valor |
| ----- | ----- |
| Objeto | \(G(N)=\#\{(p,q): p+q=N,\,p,q\text{ primos}\}\) para \(N\) par |
| Ventana | \(N\in[4, N_{\max}]\), \(N_{\max}=10000\) (réplica histórica G4) |
| Residuo | \(r(N)=G(N)-\overline{G}\) (media muestral sobre la ventana) |
| Espectro | potencia FFT de \(r(N)\) en el vector de \(N\) pares ordenados |
| Señal | potencia en el bin de frecuencia **más cercano a \(1/6\)** |
| Estadístico | \(T = P_{1/6} / \mathrm{median}(P_{k})\) sobre bins de frecuencia positivos (excl. DC) |

---

## 4. Controles nulos (ataques)

| ID | Nulo | Procedimiento |
| -- | ---- | ------------- |
| **N1** | Permutación | Barajar \(r(N)\) con seed \(s\); recalcular \(T\) |
| **N2** | I.i.d. | Reemplazar \(r\) por ruido gaussiano i.i.d. con misma varianza muestral; \(T\) |
| **N3** | Subventana | Calcular \(T\) en \([4,N_{\max}/2]\) y \([N_{\max}/2,N_{\max}]\); estabilidad |

Seeds nulos: \(s=0..99\) para N1 y N2 (100 réplicas cada uno).

---

## 5. Criterios de muerte / apoyo (congelados)

Sea \(T_0\) el estadístico en datos reales.  
Sea \(p_{\mathrm{N1}}\) = fracción de réplicas N1 con \(T \ge T_0\) (cola empírica).  
Idem \(p_{\mathrm{N2}}\).

| Resultado | Condición |
| --------- | --------- |
| **H-01 apoyada** (bajo control) | \(p_{\mathrm{N1}} \le 0.01\) **y** \(p_{\mathrm{N2}} \le 0.01\) **y** \(T_0\) aparece en **ambas** subventanas N3 en el **top-5** de bins (excl. DC) |
| **H-00 apoyada** | \(p_{\mathrm{N1}} > 0.05\) **o** \(p_{\mathrm{N2}} > 0.05\) **o** falla N3 (no top-5 en alguna subventana) |
| **NO_SABEMOS** | resto (zona gris entre 0.01 y 0.05, o N3 mixto) |

---

## 6. No-afirmaciones

Incluso si H-01 gana:

- **No** se afirma la distribución asintótica de primos.  
- **No** se afirma una “estructura fundamental → primos”.  
- **No** se eleva a teorema.  
- Solo: la firma \(\sim 1/6\) en **esta** ventana y **este** residual es extrema frente a **estos** nulos.

---

## 7. Kernel

Ficha Core + estados. Auditor de forma.  
Selector **no** se usa como juez (exploración abierta / señal única).

---

## 8. Ejecución

```text
Runner: scripts/run_athena_domain_e001.py
Salida: ATHENA_DOMAIN_E001/resultados/
```

---

## 9. Sello

| | |
| - | - |
| Congelado | **SÍ** |
| Prohibido | Cambiar residual/nulos post-datos; reclamar demostración de primos |

---

# FIN — DOMAIN-E001 PROTOCOL 1.0
