# T-01 — Capa de consecuencias necesarias (paramétricas)

**Fecha:** 2026-07-18  
**Ancla:** MD-063 · MD-064  
**Fuente de datos:** `results/T01_REFERENCE_WAVE1/` (solo para contrastar empírico; las **NECESSARY** se demuestran desde la regla)  
**No es:** P\* sellada · Intake · puente a Athena  

---

## Pregunta de esta capa

> ¿Alguna propiedad empírica de T-01 puede convertirse en **consecuencia necesaria**  
> de su dinámica (frontera en \((r,\theta,p_{\mathrm{birth}},\ldots)\)),  
> o es solo efecto contingente de la rejilla?

**No** forzar P\*.  
**No** explicar Athena.

---

## Recordatorio de la regla (spec 1.0)

Actualización **síncrona**:

\[
x_i^{t+1}=
\begin{cases}
0 & \text{si }\mathrm{ns}_i(t)\ge\theta\\
1 & \text{si }\mathrm{ns}_i(t)<\theta\text{ y }(x_i^t=1\text{ o }U_{t,i}<p_{\mathrm{birth}})\\
0 & \text{si no}
\end{cases}
\]

\(\mathrm{ns}_i =\) número de ocupados en \(0<|j-i|\le r\).

---

## N1–N3 (ola 1) — locales, triviales para P\*

| ID | Afirmación | Estatus |
| -- | ---------- | ------- |
| N1 | Si \(\forall i,\ \mathrm{ns}_i\ge\theta\), entonces \(x^{t+1}\equiv 0\) | NECESSARY (local) |
| N2 | Si \(\mathrm{ns}_i<\theta\) y \(x_i=1\), entonces \(x_i^{t+1}=1\) | NECESSARY (local) |
| N3 | Si \(x_i=0\) y \(\mathrm{ns}_i<\theta\), entonces \(x_i^{t+1}=1\) iff \(U<p_{\mathrm{birth}}\) | NECESSARY (local) |

Válidas, pero **demasiado triviales** para una P\* fuerte de Intake.

---

## Consecuencias paramétricas **necesarias** (nuevas en esta capa)

### N4 — Sin nacimientos, la densidad no crece

**Hipótesis paramétrica:** \(p_{\mathrm{birth}}=0\).

**Afirmación:** para todo \(t\ge 0\),

\[
\sum_i x_i^{t+1} \le \sum_i x_i^{t}.
\]

**Prueba:** con \(p_{\mathrm{birth}}=0\), la única forma de obtener \(x_i^{t+1}=1\) es \(x_i^t=1\) y \(\mathrm{ns}_i<\theta\).  
Ningún sitio vacío se enciende. Los ocupados solo pueden apagarse. ∎

**Clase:** NECESSARY (paramétrica: \(p_{\mathrm{birth}}=0\)).

*Nota:* la Ola 1 **no** incluye \(p_{\mathrm{birth}}=0\); es consecuencia de la **regla**, no del grid.

---

### N5 — Sin nacimientos y \(\theta=1\): empaquetamiento duro tras un paso

**Hipótesis:** \(p_{\mathrm{birth}}=0\), \(\theta=1\).

**Afirmación:** para todo \(t\ge 0\), el soporte de \(x^{t+1}\) es un **conjunto independiente**  
en el grafo de camino con aristas entre \(i\sim j\) si \(0<|i-j|\le r\):  
dos ocupados cualesquiera satisfacen \(|i-j|\ge r+1\).

**Prueba:** supóngase \(x_i^{t+1}=x_j^{t+1}=1\) con \(0<|i-j|\le r\).  
Para que \(i\) quede 1 hace falta \(\mathrm{ns}_i(t)<1\), i.e. \(\mathrm{ns}_i(t)=0\), y \(x_i^t=1\) (no hay birth).  
Pero \(x_j^t=1\) (idem) y \(j\in\mathcal{N}(i)\) ⇒ \(\mathrm{ns}_i(t)\ge 1\), contradicción. ∎

**Corolario de densidad:** para \(t\ge 1\),

\[
\frac{1}{N}\sum_i x_i^{t} \le \frac{\lceil N/(r+1)\rceil}{N} \le \frac{1}{r+1}+\frac{1}{N}.
\]

**Clase:** NECESSARY (paramétrica: \(p_{\mathrm{birth}}=0,\ \theta=1\)).

---

### N6 — Techo de vecinos

**Afirmación:** en el interior, \(\mathrm{ns}_i \le 2r\). Por tanto, si \(\theta > 2r\), la rama de muerte **nunca** se activa  
(en sitios con menos de \(2r\) vecinos, el techo es aún menor).

**Clase:** NECESSARY (geométrica).  
La Ola 1 **excluyó** \(\theta>2r\) por config; la regla lo implica de todos modos.

---

### N7 — Nacimientos síncronos **rompen** el empaquetamiento (anti-teorema)

**Afirmación:** si \(p_{\mathrm{birth}}>0\) y \(\theta=1\), **no** es necesario que \(x^{t+1}\) sea independiente.

**Contraejemplo constructivo:** dos sitios vacíos \(i,j\) con \(|i-j|\le r\), ambos con \(\mathrm{ns}=0\) en \(t\),  
ambos con \(U_{t,\cdot}<p_{\mathrm{birth}}\) ⇒ ambos pasan a 1 en \(t+1\) y violan el gap \(r+1\).

**Clase:** NECESSARY (límite de N5): la frontera \(p_{\mathrm{birth}}=0\) es **esencial**.

Esto **impide** elevar “empaquetamiento siempre” a consecuencia de toda la familia T-01.

---

## Revisión de E1–E2 (empíricos de la Ola 1)

### E1 — “extinción bajo alta exclusión”

En la Ola 1 completa, la tasa de extinción agregada por \(\theta\) es **0**  
(ninguna de las 1920 corridas terminó en configuración vacía a \(T\in\{10,50\}\)).

**Conclusión:** E1 **no** se eleva a necesaria; en esta rejilla ni siquiera es un efecto empírico fuerte.  
Queda como **EMPIRICAL débil / no sostenido** para la Ola 1.

No hay frontera del tipo “\((r,\theta,p_{\mathrm{birth}}) \Rightarrow\) extinción obligada” visible en estos datos,  
y la regla **no** fuerza extinción global salvo N1 (configuración ya saturada de vecinos).

### E2 — densidad T=10 vs T=50

Sigue **EMPIRICAL**: depende de celda de parámetros; no hay demostración de monotonía universal en \(T\).

No se eleva a NECESSARY en esta capa.

### S1 — semilla

Sigue **SEED_DEPENDENT**. No es predicción por sí sola.

### U1

Sigue **UNKNOWN**. No se mitologiza.

---

## ¿Hay consecuencia necesaria **nueva y no trivial** lista para P\*?

| Candidata | ¿Nueva? | ¿No trivial? | ¿Lista para P\* Athena? |
| --------- | ------- | ------------ | ------------------------ |
| N1–N3 | no (ya en ola 1) | no | no |
| N4–N5 | **sí** (paramétricas) | **moderada** | **no aún** — valen como teoremas de la familia T-01, pero P\* de Intake debe arriesgar un escenario **nuevo** medible fuera del historial Athena; N4–N5 se demuestran sin experimento |
| N6–N7 | sí (límites) | clarifican frontera | no como P\* de Athena |
| E1–E2 | — | no elevadas | no |

### Lectura Phase III

T-01 **sí** tiene consecuencias paramétricas no triviales **dentro de su propio mundo**  
(cuando \(p_{\mathrm{birth}}=0\), \(\theta=1\): empaquetamiento + cota de densidad).

Eso **no** basta para abrir Intake ni sellar P\* frente a Athena:

- P\* debe ser apuesta sobre datos **aún no medidos** en un protocolo sellable;  
- N4–N5 son **matemática de la regla**, no predicción experimental nueva del programa Athena;  
- forzar “P\* = los primos empaquetan” sería contrabando conceptual.

**Decisión:**

```text
¿CONSECUENCIA NECESARIA NUEVA PARA INTAKE / P* ATHENA?
    └── NO (en el sentido del contrato de Intake)

T-01 permanece REFERENCIA DE CARRETERA.
Se archiva N4–N7 como cartografía del mecanismo.
No se fabrica P*.
```

---

## Frontera matemática (resumen operativo)

```text
p_birth = 0  ∧  θ = 1
        ↓
empaquetamiento duro (gap ≥ r+1) para t ≥ 1
densidad ≤ 1/(r+1) + O(1/N)

p_birth > 0  ∧  θ = 1
        ↓
empaquetamiento NO necesario (births síncronos)
```

Eso es **cartografía de T-01**, no explicación de S-004…S-006.

---

## Siguiente movimiento legítimo (Phase III)

1. **Archivar T-01** como vehículo de referencia + capa N4–N7.  
2. **No** Intake.  
3. Opcional: ola especial \(p_{\mathrm{birth}}=0\) solo para **verificar** N4–N5 numéricamente (no para inventar P\*).  
4. O pasar al **segundo vehículo** de la taxonomía (p.ej. T-03) con la misma disciplina.

---

## Regla de fase (reafirmada)

> No toda familia de mecanismos tiene que convertirse en candidato.  
> Algunas cartografían el espacio.  
> Solo una con predicción nueva, independiente y peligrosa entra por la Aduana.

T-01 cumplió: mecanismo ciego, datos sellados, análisis sin teoría forzada.

---

# FIN — T-01 NECESSARY LAYER

*Primero el mecanismo.  
Luego a qué está obligado.  
No a qué nos gustaría que explicara.*
