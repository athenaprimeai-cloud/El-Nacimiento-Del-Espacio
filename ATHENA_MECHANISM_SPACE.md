# ATHENA — Espacio de mecanismos admisibles

**Estado:** documento de fase · **no** teoría · **no** operador · **no** E008  
**Fecha:** 2026-07-18  
**Anclas:** `ATHENA_SURVIVORS.md` · MD-054 · MD-055  
**Precedencia:** el contrato de supervivientes **manda**; este documento solo define **quién puede presentarse** al banco de pruebas.

---

## Tesis de fase

> **Athena ha construido una máquina de restricción empírica,  
> pero todavía no posee un mecanismo explicativo.**

Eso es más fuerte que “tenemos algunos resultados”  
y más honesto que “hemos encontrado una estructura”.

**La evidencia ya no necesita ser interpretada inmediatamente para tener valor.**

---

## Tres capas (separadas)

```text
PROTOCOLOS          qué se midió (E001–E007 congelados; no se reescriben)
      ↓
OBSERVABLES         qué ocurrió (diferencia, persistencia, réplica…)
      ↓
RESTRICCIONES       qué debe explicar ℳ (S-001…S-006 + PROHIBICIONES)
      ↓
MODELO FUTURO ℳ     candidato si sobrevive el contrato
```

| Capa | Función | No es |
| ---- | ------- | ----- |
| Protocolos | Fijar la medición | Interpretación |
| Observables | Registrar el suceso protocolar | Teoría |
| Restricciones (`SURVIVORS`) | Condiciones de contorno a ℳ | “La realidad” |
| Mecanismo ℳ | Explicar + predecir | Obligatorio todavía |

No existe todavía una teoría.  
Eso es **correcto**.

---

## Cadena actual

```text
E001  ──┐
E002  ──┤
E003  ──┤── muertos          → restricciones negativas
        │
E004  ──┤
E005  ──┤── supervivientes   → S-004, S-005
E006  ──┤
E007  ──┘── réplica          → S-006
        ↓
ATHENA_SURVIVORS  (contrato)
        ↓
ATHENA_MECHANISM_SPACE  (quién puede presentarse)
        ↓
ℳ candidato + predicción nueva prerregistrada
```

---

## Próxima pieza (no es “otro experimento” por defecto)

No necesariamente E008.

Algo más difícil y más valioso:

> **Definir la clase de mecanismos que Athena está dispuesta a considerar.**

No una teoría concreta.  
No un operador.  
No una geometría.

Solo un **espacio de candidatos**.

---

## MECANISMOS ADMISIBLES — plantilla de clase

Un objeto \(\mathcal{M}\) es **admisible a examen** (no “aceptado”) solo si declara de forma explícita y **pre-datos de cualquier predicción nueva**:

### 1. ¿Qué información puede usar?

| Permitido (ejemplos de clase) | Prohibido (hard) |
| ----------------------------- | ---------------- |
| Estructura ordinal / posicional en \(\mathbb{N}\) | Divisibilidad / gcd / factores en la **geometría** o en \(E\) (MD-035) |
| Densidad local tipo \(1/\ln n\), ruedas como **nulos**, no como aristas del objeto | Reescribir protocolos E001–E007 |
| Conjuntos de control como en SURVIVORS | Parámetros ajustados tras ver E004–E007 (P2) |
| Objetos derivados de \(M_2\), \(S(W)\), grafos ordinales **ya** en el pipeline | Resucitar S-001…S-003 sin nuevo ID (P5) |

La lista “permitido” **no** es un menú de catedral: es el techo de lo que \(\mathcal{M}\) puede invocar sin quedar descartado de entrada.

### 2. ¿Qué transformaciones puede aplicar?

Debe enumerar \(T_1,\ldots,T_k\) **antes** de la predicción nueva:

- dominio y codominio;
- si actúan sobre \(X\), sobre \(R(X)\), o sobre conjuntos de vértices;
- si son aplicables **idénticamente** a nulos (gemelos).

Si \(T\) no puede aplicarse al nulo con la misma receta → no entra (eco E003 / MD-035 espíritu).

### 3. ¿Qué parámetros puede tener?

| Regla | |
| ----- | - |
| Conjunto de parámetros \(\theta\) | Finito, declarado |
| Ajuste | Solo en datos **ajenos** a la predicción nueva, o **ninguno** (preferido en v0) |
| Post-hoc sobre E004–E007 | **Prohibido** (P2) |

Un \(\mathcal{M}\) sin parámetros libres es preferible en la primera ola.

### 4. ¿Qué significa “explicar”?

En Athena, \(\mathcal{M}\) **explica** una restricción S-xxx solo si:

1. Produce (analítica o computacionalmente) la **cualidad** exigida por S-xxx  
   (p.ej. diferencia vs control; no disolución bajo rueda 30; orden de \(S(W)\) en réplica),  
2. bajo las **mismas** definiciones operativas del protocolo citado,  
3. **sin** retocar el protocolo,  
4. y sin violar PROHIBICIONES.

“Explicar” **no** significa: relato plausible, analogía, o ajuste de curva a cuatro puntos de \(S(W)\).

### 5. ¿Qué predicción nueva debe producir?  ← crucial

Un mecanismo que **solo** reproduce E004–E007 puede ser una **descripción retrospectiva** sofisticada.

Para ganar peso real, \(\mathcal{M}\) debe generar al menos **una consecuencia nueva** tal que:

| Requisito | |
| --------- | - |
| Contenido | Observable / clasificación / orden / cota **no** ya fijada en SURVIVORS |
| Forma | Protocolo de campaña (o cláusula de campaña) **congelable** |
| Tiempo | Escrita y sellada **antes** de mirar el resultado |
| Relación con el contrato | Si se cumple, **añade** restricción (nuevo S-xxx); si falla, \(\mathcal{M}\) **muere** o se debilita según umbrales preescritos |

```text
ℳ sobrevive al contrato (S-004..S-006 + PROHIBICIONES)
        │
        ▼
ℳ emite predicción P*  (aún no en el contrato)
        │
        ▼
sello + ejecución
        │
        ├── P* se cumple  → ℳ gana peso; posible S-00k nuevo
        └── P* falla      → ℳ no era mecanismo mínimo (o está mal)
```

---

## Umbral de la siguiente fase

**No:**

> Encontrar una explicación bonita.

**Sí:**

> **Construir un mecanismo pequeño que:**  
> (a) sobreviva al contrato `ATHENA_SURVIVORS`, y  
> (b) genere una predicción que **todavía no** esté dentro del contrato.

Ahí comienza realmente la siguiente fase.

---

## Registro de candidatos (plantilla vacía)

| ID | Nombre corto | ¿Pasa banquillo S-004..S-006? | Predicción P* | Estado |
| -- | ------------ | ---------------------------- | ------------- | ------ |
| — | — | — | — | **ningún candidato** (no inventar para llenar el vacío) |

*Entrada solo vía `ATHENA_MECHANISM_INTAKE.md` (paquete 1–7 + independencia temporal).*  
*Añadir filas solo con ficha de mecanismo + hash de predicción prerregistrada.*

---

## Relación con E008+

| Acción | ¿Cuándo? |
| ------ | -------- |
| Nuevo dominio experimental | Solo si hace falta **distinguir** dos ℳ admisibles, o **testar** una P* sellada |
| Documento de mecanismo | Cuando exista un ℳ pequeño que declare 1–5 y P* |
| Catedral / operador / Riemann | **No** como siguiente paso |

---

## Montaña (actualizada)

```text
¿Operador / geometría?          ← lejos; no se reclama
        ↑
¿ℳ pequeño + P* nueva?          ← umbral de fase
        ↑
Espacio de mecanismos admisibles
        ↑
Contrato SURVIVORS
        ↑
Familia reproducida E004–E007
```

---

# FIN — ATHENA_MECHANISM_SPACE

*Sin teoría todavía.  
Con máquina de restricciones.  
El derecho a existir se gana: contrato + predicción nueva.*
