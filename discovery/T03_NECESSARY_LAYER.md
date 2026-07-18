# T-03 — Capa de consecuencias necesarias

**Fecha:** 2026-07-18  
**Anclas:** MD-066 · MD-067  
**Fuente:** regla de Wolfram elemental \(r=1\), borde nulo (spec 1.0)  
**No es:** otra ola · comparación Athena · comparación T-01 · búsqueda de patrones · P\*  

---

## Pregunta

> ¿Qué fronteras de \(W\), \(T\) o del estado inicial **obligan matemáticamente**  
> a un comportamiento determinado?

Solo auditoría de la **regla**.  
No re-ejecutar la ola para “encontrar” similitudes.

---

## N1–N3 (ola 1) — reafirmadas

| ID | Afirmación | Clase |
| -- | ---------- | ----- |
| N1 | \(W=0\) ⇒ \(x^{(t)}=0\) para todo \(t\ge 1\) | NECESSARY |
| N2 | \((N,W,p_{\mathrm{init}},T,seed)\) fija trayectoria única | NECESSARY |
| N3 | \(W\in\{90,150\}\) ⇒ evolución lineal sobre \(\mathrm{GF}(2)\) (XOR) | NECESSARY |

N1 es **paramétrica** (\(W=0\)) pero **trivial** para P\* de Intake.

---

## Consecuencias paramétricas adicionales

### N4 — Punto fijo nulo (quiescencia de 0)

**Condición:** bit 0 de \(W\) es 0, i.e. \(f(000)=0\)  
(equivale a \(W\) par).

**Afirmación:** la configuración idénticamente cero es un **punto fijo**:

\[
x\equiv 0 \;\Rightarrow\; x'=0.
\]

**Prueba:** cada vecindad es 000; \(f(000)=0\). ∎

**Ola 1:** todos los \(W\) del config son **pares** ⇒ N4 aplica a **toda** la rejilla de referencia.

**Clase:** NECESSARY (paramétrica: \(W\) par).  
**¿P\*?** No — fija la clase de reglas, no una apuesta experimental nueva.

---

### N5 — Cono de luz (velocidad máxima 1)

**Condición:** \(r=1\), borde nulo, cualquier \(W\).

**Afirmación:** el valor \(x_i^{(T)}\) es función solo de

\[
\bigl\{x_j^{(0)} : |j-i| \le T\bigr\}
\]

(y de ceros de borde si la ventana sale de \(\{1..N\}\)).

**Prueba:** inducción en \(t\); cada paso depende solo de radio 1. ∎

**Clase:** NECESSARY (geométrica de la vecindad).  
**¿P\*?** No para Athena — es estructura de CA, no predicción de dominio.

---

### N6 — Aniquilación global en un paso (familia de \(W\))

**Condición:** \(f\equiv 0\), i.e. \(W=0\) (caso extremo de “todos los 8 bits de salida son 0”).

**Afirmación:** igual que N1: un paso borra cualquier configuración.

Más general (no usado en ola 1 salvo W=0): si \(f(v)=0\) para todo \(v\in\{0,1\}^3\), mismo resultado.

**Clase:** NECESSARY.  
**¿P\*?** Trivial.

---

### N7 — Superposición (aditividad)

**Condición:** \(W\in\{90,150\}\) (lineales sobre \(\mathrm{GF}(2)\)).

**Afirmación:** si \(x^{(0)}, y^{(0)}\) son condiciones iniciales y \(z^{(0)}=x^{(0)}\oplus y^{(0)}\) (XOR bit a bit), entonces para todo \(t\),

\[
z^{(t)} = x^{(t)} \oplus y^{(t)}.
\]

**Prueba:** \(f\) es lineal; la evolución conmuta con XOR. ∎

**Clase:** NECESSARY (paramétrica en \(W\)).  
**¿P\* Athena?** No sin contrabando: es álgebra del CA, no S-004…S-006.

---

### N8 — Identidad y traslaciones (fuera de la rejilla, frontera de clase)

Para cartografía (no presentes en `W_list` de ola 1, pero **necesarios como límites de la familia**):

| \(W\) | Comportamiento | Clase |
| ----- | -------------- | ----- |
| 204 | \(f=\) centro ⇒ \(x^{(t)}=x^{(0)}\) para todo \(t\) | NECESSARY si \(W=204\) |
| 170 | shift left (con borde nulo: se vacía por la derecha) | NECESSARY si \(W=170\) |
| 240 | shift right (análogo) | NECESSARY si \(W=240\) |

No se “buscan” en datos; se **registran** como fronteras de la clase T-03.  
Ola 1 **no** los incluye ⇒ no se inventan métricas post-hoc sobre ellos.

---

### N9 — Lo que **no** es necesario (anti-teoremas útiles)

| Afirmación falsa | Por qué falla |
| ---------------- | ------------- |
| “Todo \(W\) par extingue” | N4 solo fija el vacío; no borra configs no nulas (p.ej. W=30) |
| “Densidad final independiente del seed” | Determinismo + init aleatorio ⇒ S1 es posible y se observó |
| “Empaquetamiento / gap mínimo” | No hay \(\theta\) ni exclusión por conteo (eso era T-01) |
| “Misma densidad para todo \(W\)” | Falso en general; E2 es empírico |

Estas fronteras **impiden** copiar lecciones de T-01 sobre T-03.

---

## Revisión de E1–E2 / S1 / U1

| ID | Estatus tras capa | Notas |
| -- | ----------------- | ----- |
| E1 | EMPIRICAL (apoyo a N1) | No nueva; solo verifica W=0 |
| E2 | EMPIRICAL | Densidad vs \(W\); sin forma cerrada universal |
| S1 | SEED_DEPENDENT | Compatible con N2 + init Bernoulli |
| U1 | UNKNOWN | Horizonte largo / clase IV; no mitologizar |

Ninguno se eleva a P\*.

---

## ¿Consecuencia necesaria **no trivial** → P\* / Intake?

| Candidata | ¿No trivial para cartografía? | ¿P\* Athena / Intake? |
| --------- | ----------------------------- | --------------------- |
| N1, N4, N6 | no (trivial / local) | **no** |
| N2 | no (definición) | **no** |
| N3, N7 | **sí** (estructura lineal) | **no** sin contrabando a S-00x |
| N5 | moderada (cono de luz) | **no** |
| N8 | cartografía de clase | no en ola 1 |
| E2 | empírico | **no** |

### Decisión

```text
¿CONSECUENCIA NECESARIA NUEVA PARA INTAKE / P* ATHENA?
        └── NO

T03_STATUS = REFERENCE_COMPLETE
PSTAR       = NONE
INTAKE      = NOT_ELIGIBLE
```

T-03 se **archiva** como segunda clase dinámica explorada.  
Matemática válida (N3–N7) **sin** hipótesis Athena.

---

## Regla Phase III (reafirmada)

> Un mecanismo puede producir matemática válida  
> sin producir una hipótesis Athena.

> No toda familia debe convertirse en candidato.  
> No ponerle alas a cada bicicleta.

---

## Carretera (estado)

```text
T-01  REFERENCE_COMPLETE  (estocástica exclusión/birth)
T-03  REFERENCE_COMPLETE  (CA determinista Wolfram)
        ↓
  sin P*, sin Intake
        ↓
  siguiente vehículo distinto (taxonomía) o pausa Phase III
```

---

# FIN — T-03 NECESSARY LAYER

*Auditar la regla.  
No forzar la apuesta.  
Archivar si no hay P\*.*
