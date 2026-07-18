# ATHENA DOMAIN-E003 — Pregunta (criterio de identidad de \(\mathcal{T}\))

**Estado:** pregunta + protocolo **ejecutados** · ver `ATHENA_DOMAIN_E003_REPORT.md` (H-01 **MUERTA** / DESAPARECE)  
**Después de:** DOMAIN-E001 (sombra 1/6 → **MUERTA**) · DOMAIN-E002 (entropía espectral bajo \(\mathcal{R}\) → **DESAPARECE**)  
**No es:** operador de Riemann · variedad · “ya tenemos geometría”  

---

## El filo de la navaja

La dificultad **no** es medir si una transformación conserva algo.

La dificultad es **definir qué significa conservar la identidad del objeto**  
sin introducir la respuesta dentro de la pregunta.

Athena **no** debe preguntar:

> ¿La transformación conserva la señal?

porque eso ya asume que sabemos cuál es la señal.

Debe preguntar:

> **¿La transformación conserva las relaciones que definen al objeto antes de observarlo?**

La palabra clave es:

**relación**, no apariencia.

---

## Separación fundamental

\[
X = \text{objeto aritmético}
\qquad
R(X) = \text{representación observada}
\]

La transformación **no** actúa sobre \(X\). Actúa sobre la representación:

\[
Y = \mathcal{T}(R(X))
\]

Debe existir un mapa inverso **conceptual** \(R^{-1}\) tal que:

\[
R^{-1}\!\big(\mathcal{T}(R(X))\big) \approx X
\]

No necesariamente reconstrucción numérica exacta.  
**Conservación de identidad estructural.**

---

## Tres pruebas de admisibilidad (antes de permitir \(\mathcal{T}_i\))

### 1. Invariante de definición

\(\mathcal{T}\) debe conservar la propiedad que **define** el objeto.

Ejemplo Goldbach:

\[
X(N)=\{(p,q):p+q=N\}
\]

Válido: cambiar escala, coordenadas, ventana de observación.  
**Inválido:** alterar \(p+q=N\). Eso crea **otro** objeto.

### 2. Test de reconstrucción

Tras \(Y=\mathcal{T}(R(X))\):

> ¿Puede recuperarse la **información definitoria** (no toda la señal)?

- Compresión con pérdida: puede matar amplitudes y mantener relaciones.  
- Permutación aleatoria: puede mantener histogramas y **destruir** relaciones.

Lección del Selector (E002 / META):

```text
mantener estadísticas  ≠  mantener identidad
```

### 3. Transformación contra gemelos nulos

No basta \(D(X,\mathcal{T}(X))\).  
Cualquier objeto complejo puede parecer estable.

Necesitamos el **mismo** \(\mathcal{T}\) sobre el nulo:

```text
Objeto real ──T──►  distancia Δ_real
Modelo nulo ──T──►  distancia Δ_nulo
```

- Si ambos sobreviven igual → no hay estructura diferencial.  
- Si el real conserva lo que el nulo pierde → aparece una **sombra**.

---

## Poda de transformaciones candidatas

| \(\mathcal{T}\) | Veredicto de lab | Motivo |
| --------------- | ---------------- | ------ |
| **Dilatación escalar** | Potencialmente admisible | Peligro: interpolación puede fabricar continuidad. Evaluar con **varios** interpoladores y registrar dependencia. |
| **Ventana dinámica** | **Más limpia** | No cambia el objeto; solo la región observada. Analogía Riemann: no cambia la función, cambia el dominio de exploración. |
| **Cambio de base** | Exploratoria, **no** primera prueba | Una base puede introducir geometría artificial (patrón “profundo” solo en base 2). |

### Corrección lab (pre-ejecución)

- **Sin interpolación al comparar soportes** ≠ obligación de inventar pesos.  
- **FASE 1:** ventanas **rectangulares** (transparentes; borde duro aceptado).  
- **FASE 2 (solo si hay sombra):** Hann/Hamming como **auditoría de borde**, no como búsqueda.  
- Cinco ventanas = **un** instrumento, cinco campos de visión (misma escala, distintas posiciones) — no cinco morfologías.  
- Instrumento de comparación: discrepancia \(D_q\) con \(q=1/2\), **no** “distancia métrica \(L^{1/2}\)”.

---

## Criterio operativo \(\mathcal{G}_{\mathrm{adm}}\)

Una transformación entra a \(\mathcal{G}_{\mathrm{adm}}\) si cumple:

\[
\boxed{
\begin{aligned}
&1.\quad \text{Preserva la definición del objeto}\\
&2.\quad \text{No aumenta información}\\
&3.\quad \text{No introduce una estructura externa}\\
&4.\quad \text{Puede aplicarse idénticamente a nulos}\\
&5.\quad \text{Tiene interpretación reversible conceptual}
\end{aligned}
}
\]

---

## Pregunta de DOMAIN-E003 (humilde)

**No:**

> ¿Cuál es la sombra / la variedad / el operador?

**Sí:**

> ¿Existe diferencia entre  
> \(\Delta_{\mathrm{real}}=d\!\big(R(X),\mathcal{T}(R(X))\big)\)  
> y  
> \(\Delta_{\mathrm{nulo}}=d\!\big(R(X_n),\mathcal{T}(R(X_n))\big)\)  
> bajo transformaciones \(\mathcal{T}\in\mathcal{G}_{\mathrm{adm}}\)?

### Consecuencia filosófica (limpia)

| Resultado | Lectura |
| --------- | ------- |
| \(\Delta_{\mathrm{real}}\approx\Delta_{\mathrm{nulo}}\) | La geometría sigue siendo **hipótesis**. |
| \(\Delta_{\mathrm{real}}<\Delta_{\mathrm{nulo}}\) bajo múltiples \(\mathcal{T}_i\) | Primera evidencia de **resistencia intrínseca**. |

No tenemos aún una variedad.  
Pero por primera vez buscamos una **pared que proyecta sombra aunque cambiemos la lámpara**.

---

## Relación con E001 / E002

| Campaña | Pregunta | Resultado |
| ------- | -------- | --------- |
| E001 | ¿Esta sombra (1/6) es del objeto? | MUERTA bajo control |
| E002 | ¿Se conserva \(P\) al cambiar la luz? | DESAPARECE (no diferencial) |
| **E003** | **¿Qué lámparas son legítimas, y hay resistencia diferencial de identidad?** | *abierta* |

E002 midió conservación de una **apariencia espectral** bajo un \(\mathcal{R}\) ya elegido.  
E003 fija el **filtro de legitimidad** de \(\mathcal{T}\) y mide **resistencia de identidad** (relación), no “¿se ve igual \(P\)?”.

---

## Hipótesis (borrador → congeladas en protocolo)

| ID | Enunciado |
| -- | --------- |
| **H-ATH-D003-01** | Bajo \(\mathcal{T}\in\mathcal{G}_{\mathrm{adm}}\) predeclaradas, \(\Delta_{\mathrm{real}}\) es **sistemáticamente menor** que \(\Delta_{\mathrm{nulo}}\) (resistencia intrínseca bajo control). |
| **H-ATH-D003-00** | \(\Delta_{\mathrm{real}}\approx\Delta_{\mathrm{nulo}}\) (o el real es **menos** resistente): no hay sombra diferencial bajo este control. |

Ambas son éxitos del lab.

---

## Montaña

```text
¿estructura generativa?
        ↑
¿pared que proyecta sombra al mover la lámpara?  ← E003
        ↑
E002: esta P no se conserva diferencialmente
        ↑
E001: esta sombra 1/6 no
```

---

## Uso del lab

Ficha Core · nulos gemelos con el **mismo** \(\mathcal{T}\) · muerte · NO_SABEMOS.  
Selector **no** juez de exploración abierta.  
Auditor de forma; semántica en protocolo e informe.  
**No** operadores. **No** catedral.

---

## Siguiente

Congelar protocolo: familia \(\mathcal{G}_{\mathrm{adm}}\) de campaña 1 (ventanas primero), distancia \(d\), nulos, umbrales.  
Ejecutar. Archivar. Sin variedad.

---

# FIN — DOMAIN-E003 PREGUNTA

*Relación, no apariencia.  
La lámpara no define la pared — pero una pared real no desaparece al mover la lámpara.*
