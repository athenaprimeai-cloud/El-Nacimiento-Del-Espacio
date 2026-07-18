# T-01 — Generador ciego de referencia (especificación cerrada)

**Familia:** T-01 (ocupación binaria + exclusión / regla local)  
**Estado:** **ESPECIFICACIÓN CONGELADA** · **código del generador: no implementado aún**  
**Fecha:** 2026-07-18  
**Anclas:** MD-061 · MD-062 · `ATHENA_MECHANISM_DISCOVERY.md` · `ATHENA_MECHANISM_TAXONOMY.md`  
**No es:** candidato de Intake · explicación de E004–E007 · E008  

---

## Misión de este ladrillo

Un solo **vehículo de prueba** de la carretera Phase III:

```text
FAMILIA T-01
   ↓
REGLA (este documento)
   ↓
GENERACIÓN CIEGA          ← implementado después de congelar esta spec
   ↓
COMPORTAMIENTO
   ↓
CONSECUENCIA NECESARIA
   ↓
P* (si se deduce de las reglas)
   ↓
INTAKE (si procede)
```

**No** diez generadores.  
**No** ajustar la regla mirando Athena.

---

## Regla fundamental de ceguera

> **El generador no puede leer**  
> `ATHENA_SURVIVORS.md`, resultados E001–E007,  
> `classification.json` históricos, ni ningún informe de dominio Athena  
> **durante la generación ni durante el ajuste de parámetros.**

Separación lógica (y, al implementar, de imports/paths):

```text
┌──────────────────────┐
│ DISCOVERY INPUT      │
│ este documento       │
│ semilla              │
│ N, k, params de spec │
└──────────┬───────────┘
           ↓
      GENERADOR T-01
           ↓
      salida bruta (conjunto / trayectoria)
           ↓
      (fase posterior, otro módulo)
      propiedades emergentes
           ↓
      (solo si hay consecuencia necesaria)
      P* → INTAKE
```

El generador produce un **objeto abstracto** (configuración / conjunto).  
**No** “se parece a los primos”.  
**No** se optimiza para S-004.

---

## 1. Definición formal de la familia

### Espacio de estados

\[
x = (x_1,\ldots,x_N) \in \{0,1\}^N
\]

Interpretación: \(x_i=1\) = posición \(i\) **ocupada**.

### Estado inicial

Fijado por semilla \(s\):

\[
x_i^{(0)} =
\begin{cases}
1 & \text{con probabilidad } p_{\mathrm{init}} \text{ (Bernoulli indep.)}\\
0 & \text{en caso contrario}
\end{cases}
\]

RNG: `random.Random(s)` (Python stdlib) o equivalente documentado;  
secuencia de \(N\) draws en orden \(i=1..N\).

**Parámetro:** \(p_{\mathrm{init}} \in (0,1)\) — valor por defecto de referencia: \(p_{\mathrm{init}}=1/2\).

### Vecindad

Radio entero \(r \ge 0\):

\[
\mathcal{N}(i) = \{ j : 1 \le j \le N,\ 0 < |j-i| \le r \}
\]

(solo ordinal; **sin** módulos aritméticos de factores).

### Regla de transición (determinista dado el estado)

Actualización **síncrona** un paso \(t \to t+1\):

\[
x_i^{(t+1)} =
\begin{cases}
0 & \text{si } \displaystyle\sum_{j\in\mathcal{N}(i)} x_j^{(t)} \ge \theta \\[6pt]
1 & \text{si } \displaystyle\sum_{j\in\mathcal{N}(i)} x_j^{(t)} < \theta
\ \text{ y }\ \bigl(x_i^{(t)}=1\ \text{ o }\ U_{t,i} < p_{\mathrm{birth}}\bigr) \\[4pt]
0 & \text{en otro caso}
\end{cases}
\]

donde \(U_{t,i}\) son i.i.d. Uniform(0,1) con RNG `Random(s + 1 + t)`  
y se consumen en orden \(i=1..N\) para cada \(t\).

**Lectura informal (no normativa):**  
demasiados vecinos ocupados → muerte (exclusión local);  
pocos vecinos → se mantiene o nace con probabilidad \(p_{\mathrm{birth}}\).

### Criterio de parada

Tras \(T\) pasos síncronos:

\[
x^{\mathrm{final}} = x^{(T)}
\]

### Salida

\[
S = \{ i \in \{1,\ldots,N\} : x_i^{\mathrm{final}} = 1 \}
\]

Objeto abstracto: **conjunto de posiciones ocupadas**.  
Opcional (archivo): trayectoria completa o solo \(S\) + metadatos.

### Información permitida / prohibida (frontera)

| Puede usar | No puede usar |
| ---------- | ------------- |
| \(N, r, \theta, p_{\mathrm{init}}, p_{\mathrm{birth}}, T, s\) | primalidad de \(i\) |
| \(x_j\) en vecindad ordinal | \(\gcd\), factores, criba |
| RNG de semillas documentadas | lectura de SURVIVORS / E00x |
| | “ajustar para parecer primos” |

**MD-035:** este ℳ **genera** un conjunto; no redefine aristas del grafo Athena con aritmética.

---

## 2. Generador mínimo (spec de implementación)

### Nombre de módulo (futuro)

```text
discovery/t01_reference_generator.py
```

**Prohibido en ese módulo:**

```text
import / open de:
  ATHENA_SURVIVORS*
  ATHENA_DOMAIN_*
  **/classification.json  (dominio Athena)
  META_DECISION_LOG
  cualquier path con resultados históricos
```

Permitido: `random`, `json`, `pathlib` solo para **escribir** salida bajo  
`discovery_runs/t01/…`.

### Firma

```text
generate_t01(
    N: int,
    r: int,
    theta: int,
    p_init: float,
    p_birth: float,
    T: int,
    seed: int
) -> dict
```

### Salida bruta (JSON por corrida)

```json
{
  "family": "T-01",
  "spec_version": "1.0",
  "params": { "N": ..., "r": ..., "theta": ..., "p_init": ..., "p_birth": ..., "T": ..., "seed": ... },
  "occupied": [ ... enteros ordenados ... ],
  "cardinality": ...,
  "density": ...
}
```

Archivo: `discovery_runs/t01/run_N{N}_s{seed}_….json`

### Reproducibilidad

Misma versión de spec + mismos params + misma semilla → **bit-idéntico** `occupied`  
(en Python 3.11+ con el RNG y orden de draws de esta spec).

---

## 3. Parámetros de referencia (cerrados para la primera ola)

No se exploran grillas enormes. Una **rejilla mínima** predeclarada:

| Parámetro | Valores de referencia (ola 1) |
| --------- | ----------------------------- |
| \(N\) | \(1000,\ 5000,\ 10000\) |
| \(r\) | \(1,\ 2,\ 3\) |
| \(\theta\) | \(1,\ 2,\ 3\) (con \(\theta \le 2r\)) |
| \(p_{\mathrm{init}}\) | \(0.5\) |
| \(p_{\mathrm{birth}}\) | \(0.1,\ 0.3\) |
| \(T\) | \(10,\ 50\) |
| seeds | \(0, 1, 2, \ldots, 19\) (20 seeds) |

**Congelado:** no añadir valores a la ola 1 **después** de mirar propiedades emergentes  
sin abrir **ola 2** con nuevo ID de spec (`spec_version` 1.1+ y nota en historial).

---

## 4. Distribución de parámetros

Ola 1 = **producto cartesiano filtrado** de la tabla  
(excluir \(\theta > 2r\)).  
No muestreo bayesiano; no optimización.

---

## 5. Informe de propiedades emergentes (módulo separado)

**Después** de generar salidas brutas, un analizador **también ciego a E00x**  
puede computar solo propiedades **intrínsecas** del conjunto \(S\):

| Propiedad | Definición |
| --------- | ---------- |
| densidad | \(\|S\|/N\) |
| gap medio / var | diferencias ordenadas de \(S\) |
| autocorrelación de la serie indicadora | lag \(1..L\) |
| fracción de pares a distancia \(\le k_0\) | \(k_0 \in \{1,2,5,10\}\) |
| estabilidad | correlación Jaccard de \(S\) entre \(N\) y \(N'\) (submuestreo o corridas emparejadas) |

**Prohibido en el analizador de la ola 1:**  
comparar con primos, con Goldbach, con classification Athena, con \(M_2\) de E004.

Ese bridge, si existe, es **otro módulo** y **otra fase** (post-comportamiento, pre-Intake).

---

## 6. Consecuencia necesaria → P\* (proceso, no lista inventada)

### Secuencia correcta (congelada)

```text
REGLA (este doc)
  → GENERACIÓN CIEGA
  → COMPORTAMIENTO (propiedades intrínsecas)
  → CONSECUENCIA NECESARIA (derivada de la regla o observada como regularidad del ℳ)
  → P*  (solo si es nueva, cuantificable, peligrosa)
  → INTAKE
```

### Prohibido

> Inventar P\* **después** de ver que el mecanismo “se parece” a algo de Athena.

### Permitido como **tipos** de consecuencia (plantilla; no son P\* aún)

Hasta que haya corridas, solo se admiten **formas** de P\* derivadas del ℳ:

| Tipo | Ejemplo de forma (no valor) |
| ---- | --------------------------- |
| C1 | Monotonía de densidad al variar \(r\) o \(\theta\) con resto fijo |
| C2 | Saturación de gap medio cuando \(T \ge T_0\) |
| C3 | Colapso de ocupación si \(\theta=1, r\ge r_0\) |
| C4 | Estabilidad Jaccard \(> \alpha\) entre \(N\) y \(2N\) bajo mismos params relativos |

Una P\* real se escribe **solo** cuando una de estas (u otra deducida)  
queda **cuantificada** y sellada **antes** del test Athena / experimento nuevo.

---

## 7. Sin modificar el mecanismo después de observar

Una vez generada la ola 1:

- No cambiar la regla de transición.  
- No cambiar la rejilla de params de la ola 1.  
- Observaciones → informe; si se quiere otra regla → **T-01b** o `spec_version` 2.0, no reescritura silenciosa.

---

## 8. Checklist pre-código

- [x] Familia elegida: **T-01**  
- [x] Spec 1.0 cerrada (este documento)  
- [ ] Implementar `discovery/t01_reference_generator.py` **solo** con esta spec  
- [ ] Audit: cero imports/paths Athena  
- [ ] Correr ola 1 → `discovery_runs/t01/`  
- [ ] Informe de propiedades intrínsecas  
- [ ] Solo entonces: consecuencia necesaria / P\* / Intake si aplica  

---

## 9. Por qué T-01 (y no T-03 en este ladrillo)

| | T-01 | T-03 |
| - | ---- | ---- |
| Salida | conjunto de ocupación natural | también, tras \(T\) pasos |
| Exclusión local | explícita en la regla | depende de \(f\) |
| Primer vehículo | más simple de auditar MD-035 | más espacio de reglas |

T-03 queda en taxonomía para el **segundo** vehículo, no en paralelo masivo.

---

## Historial

| Fecha | Cambio |
| ----- | ------ |
| 2026-07-18 | Spec 1.0 congelada; código pendiente |

---

# FIN — T-01 REFERENCE GENERATOR SPEC 1.0

*Un vehículo.  
Ciego.  
Abstracto.  
P\* solo como consecuencia, no como maquillaje.*
