# ATHENA DOMAIN-E001 — Informe de cierre

**Protocolo:** v1.0 **CONGELADO**  
**Ejecución:** `scripts/run_athena_domain_e001.py`  
**Datos:** `artifacts/goldbach/goldbach_partitions_4_10000.csv` (G4, \(N\le 10000\))  
**Fuente:** `resultados/classification.json`  

---

## 0. Por qué esta campaña

No porque hubiera matemática nueva ya descubierta.  
Sino para **salir del garaje**: atacar la montaña (primos / Goldbach residual) con el kernel, y poder declarar **pared pintada** o **puerta resistente**.

---

## 1. Pregunta

> ¿El pico espectral \(\sim 1/6\) del residuo \(G(N)-\overline{G}\) es **extremo** frente a permutación y ruido gaussiano i.i.d., y estable en subventanas?

---

## 2. Resultados

| Estadístico | Valor |
| ----------- | ----- |
| \(n\) (pares) | 4999 |
| \(f^\star\) (bin más cercano a \(1/6\)) | **0.166633…** (k=833) |
| \(T_0 = P_{1/6}/\mathrm{median}(P)\) | **0.807** |
| \(p_{\mathrm{N1}}\) (permutación, 100 réplicas) | **0.59** |
| \(p_{\mathrm{N2}}\) (Gauss i.i.d., 100) | **0.59** |
| N3 top-5 en ambas mitades | **false** |

---

## 3. Veredicto (reglas predeclaradas)

| ID | Estado |
| -- | ------ |
| **H-ATH-D001-01** | **MUERTA** |
| **H-ATH-D001-00** | **SOPORTADA_BAJO_CONTROL** |

**Código:** `H00_COMPATIBLE_WITH_NULL_OR_UNSTABLE`

Bajo **este** residual (media muestral) y **este** estadístico \(T\), la firma \(\sim 1/6\) **no** es extrema frente a los nulos.  
Es compatible con **artefacto / nulo / inestabilidad** en el sentido del protocolo.

---

## 4. Lecturas permitidas / prohibidas

### Permitido

- “Pared pintada” para **esta** formulación (residuo de media + \(T\) + nulos N1–N3).  
- El lab hizo lo que debía: la hipótesis **murió** sin reescribir umbrales.  
- Observaciones históricas con **otros** residuales (suavizado, desingularizado) **no** quedan automáticamente invalidadas: son **otros regímenes** (nuevo DOMAIN-E si se atacan).

### Prohibido

- “Los primos no tienen estructura.”  
- “Goldbach está resuelto / refutado.”  
- “El pico 1/6 nunca existió en ningún canal.”  
- Enamorarse del pico de resúmenes previos sin pasar por nulos **de este** protocolo.

---

## 5. Kernel

Hipótesis registrada y cerrada como **MUERTA** con razón en el Core  
(`resultados/kernel/`).

---

## 6. Relación con la montaña

La pregunta grande (**¿estructura profunda → primos?**) **sigue abierta**.

DOMAIN-E001 solo limpia **una** puerta sospechosa:

```text
residuo de media + firma 1/6 + estos nulos  →  no extrema
```

Siguiente peldaño natural: atacar un canal **ya documentado** como más fuerte (p.ej. residuo suavizado / desingularizado del artefacto G4-002), con **nuevo ID** de campaña y nulos propios — no reescribir E001.

---

## 7. Cumplimiento del propósito del lab

| | |
| - | - |
| Señal interesante histórica | sí (pico ~1/6 en resúmenes previos) |
| Controles | sí |
| Muerte posible | **ocurrida** |
| Huella | sí |

El auto **salió del garaje**. El cinturón funcionó: no se construyó teoría sobre una señal que, bajo este control, no supera el nulo.

---

# FIN — DOMAIN-E001 REPORT

*Pared pintada bajo este control.  
La montaña sigue. El lab también.*
