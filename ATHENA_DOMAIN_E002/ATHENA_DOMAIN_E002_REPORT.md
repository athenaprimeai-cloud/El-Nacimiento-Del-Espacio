# ATHENA DOMAIN-E002 — Informe de cierre

**Protocolo:** v1.0 **CONGELADO**  
**Ejecución:** `scripts/run_athena_domain_e002.py`  
**Fuente:** `resultados/classification.json`  

---

## 1. Pregunta

> ¿La entropía espectral del residual Goldbach se **conserva** bajo representaciones legítimas \(\mathcal{R}\) de forma **diferencial** respecto a nulos?

No un pico. Una propiedad de **forma** espectral bajo cambio de “coordenadas”.

---

## 2. Ficha de salida

| Campo | Valor |
| ----- | ----- |
| **Propiedad \(P\)** | Entropía espectral normalizada (excl. DC) |
| **Familia \(T\)** | T0 media · T1 mitad baja · T2 mitad alta · T3 detrend lineal · T4 log-media |
| **Rango** | \(N\) par \(\in[4,10000]\) |
| **Nulos** | N1 permutación · N2 bootstrap de bloques \(B=50\) · 100 seeds c/u |
| **\(\Delta_0\)** | **0.101** |
| **\(p_{\mathrm{N1}}\)** | **1.00** (todos los nulos \(\Delta\le\Delta_0\)) |
| **\(p_{\mathrm{N2}}\)** | **1.00** |
| **Interpretación** | **DESAPARECE** |

### \(P\) por representación

| \(T\) | \(P\) |
| ----- | ----- |
| T0 mean | 0.376 |
| T1 half-low | 0.377 |
| T2 half-high | 0.275 |
| T3 linear | 0.300 |
| T4 log-mean | 0.407 |

Hay variación real entre \(T\) (\(\Delta_0\approx 0.10\)), pero **los nulos son al menos tan estables**: no hay conservación **diferencial**.

---

## 3. Veredicto

| ID | Estado |
| -- | ------ |
| **H-ATH-D002-01** (conservación diferencial) | **MUERTA** |
| **H-ATH-D002-00** (no diferencial / artefacto de régimen) | **SOPORTADA_BAJO_CONTROL** |

**Código:** `H00_NO_DIFFERENTIAL_CONSERVATION`

---

## 4. Lecturas

### Permitido

- Bajo **esta** \(P\) y **esta** \(\mathcal{R}\), no hay invarianza interesante frente a nulos.  
- “Invarianza” no se regala: una estadística puede ser estable en nulos por ser gruesa o por el método.  
- Ladrillo: **esta** simetría candidata no sostiene la búsqueda de una geometría a partir de ella.

### Prohibido

- “No existe ninguna conservación en los primos.”  
- “Riemann está refutado.”  
- Reutilizar el mismo \(P\) con otro relato sin **nuevo ID**.  
- Saltar a un operador porque “debe haber simetría”.

---

## 5. Montaña

```text
¿estructura generativa?
        ↑
¿conservación observable?  ← E002: esta P no
        ↑
E001: sombra 1/6 (residual media) no
```

Siguiente ladrillo: **otro** \(P\) (correlaciones largas, estructura modular, …) con **nuevo** DOMAIN-E00x — o un canal residual ya documentado como más rico — no catedral.

---

## 6. Lab

El auto en la carretera: otra puerta golpeada; otra pared pintada **bajo control**.  
Huella en el kernel. Montaña intacta.

---

# FIN — DOMAIN-E002 REPORT

*No toda supervivencia es profundidad.  
Esta conservación no fue diferencial. Un ladrillo, no una catedral.*
