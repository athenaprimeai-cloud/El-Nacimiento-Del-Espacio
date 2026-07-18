# ATHENA DOMAIN-E007 — Pregunta (estabilidad de la curva \(S(W)\))

**Estado:** pregunta de dominio · **no** protocolo congelado · **no** ejecución  
**Después de:** E006 PERSISTE + CURVE_MONOTONE + lectura lab (MD-048)  
**No es:** \(N=10^6\) por vanidad · grafo nuevo · nulos HL · operador  

---

## Pregunta

**No:**

> ¿Cuál es la geometría generativa / el operador?

**Sí:**

> **¿Es estable la curva**  
> \(S(W)=|M_2(P)-\mathrm{median}\,M_2(\mathrm{Cramér\text{-}rueda}_W)|\)  
> para \(W\in\{1,2,6,30\}\)  
> al repetir el **mismo** protocolo E006 en **otro** \(N\)?

En una línea:

> **¿Cuatro puntos de una ley, o un accidente de una escala?**

---

## Por qué esto y no “más grande”

E006 no distingue:

| A | B |
| - | - |
| Núcleo residual tras rueda | Reescalado del observable |

Una réplica de **estabilidad** de \(S(W)\) acota ambos sin inventar métricas.

---

## Diseño mínimo (borrador — a congelar en protocolo)

| Campo | Propuesta |
| ----- | --------- |
| Protocolo base | **idéntico** E006 (grafo, \(M_2\), ruedas, B, mitades, §5) |
| \(N\) réplica | p.ej. \(5\cdot 10^4\) **y/o** \(2\cdot 10^5\) (elegir uno principal + satélite) |
| \(k(N)\) | misma política \(k=\mathrm{round}(\ln N)\) |
| Veredicto principal | ¿monotonía de \(S(W)\) se reproduce? ¿\(p_{\mathrm{range}}^{(30)}\) sigue ≤ 0.01 + mitades? |
| No | nuevos observables · HL · bases · dilataciones |

### Hipótesis (borrador)

| ID | Enunciado |
| -- | --------- |
| **H-ATH-D007-00** | La curva / el extremo vs W=30 es **accidente de escala** \(N=10^5\): no se reproduce. |
| **H-ATH-D007-01** | La curva es **estable**: monotonía (o al menos no creciente) y material vs W=30 se reproducen bajo control. |

---

## Relación con MD-048

Primero estabilidad.  
Solo después: ley de \(S(W)\) (exponencial / log / potencia / saturación) o nulos más afilados (HL).

---

## Montaña

```text
¿mecanismo mínimo E004+E006 (sin contrabando)?
        ↑
¿S(W) estable en N?  ← E007
        ↑
E006: PERSISTE rueda 30 + curva monótona
```

---

## Siguiente

Congelar protocolo E007 (un \(N\) principal, umbrales de “reproducción”, sello GitLab).  
Ejecutar. Lectura mecánica. Sin catedral.

---

# FIN — DOMAIN-E007 PREGUNTA

*No más lámpara.  
La misma lámpara, otra ventana de N.*
