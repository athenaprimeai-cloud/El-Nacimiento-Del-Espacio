# ATHENA — Intake de mecanismos (aduana)

**Estado:** **ley de entrada** · vigente con MD-058 · refinada MD-059  
**Fecha:** 2026-07-18  
**Hermanos:** `ATHENA_MECHANISM_SPACE.md` · `ATHENA_SURVIVORS.md` · `ATHENA_PHASE_STATUS.md`  
**No es:** catálogo de ideas · fábrica de candidatos · promoción de E004–E007 a explicación  

---

## Cómo llegan las cuatro cosas

**No se “descubren” dentro de Athena. Las trae el candidato.**

Cuando aparezca una hipótesis, entra como **paquete cerrado**:

```text
┌─────────────────────────────────────────────┐
│        ATHENA MECHANISM INTAKE              │
├─────────────────────────────────────────────┤
│ 1. REGLAS                                   │
│    Qué hace exactamente ℳ                   │
│                                             │
│ 2. INFORMACIÓN                              │
│    Qué puede usar y qué tiene prohibido     │
│                                             │
│ 3. EXPLICACIÓN                               │
│    Cómo produce S-004 + S-005 + S-006       │
│    sin ajustar el mecanismo después         │
│                                             │
│ 4. P*                                        │
│    Qué predice antes de ver el nuevo dato   │
└─────────────────────────────────────────────┘
```

(Paquete completo de registro: también **OPERACIÓN**, **PARÁMETROS**, **MUERTE** — ver § Paquete 1–7.)

---

## Las cuatro no tienen el mismo estatus

### 1. Las reglas llegan como **definición**

El candidato debe poder escribirse **antes** de ejecutarlo:

> Dado este objeto de entrada, aplico estas transformaciones,  
> con estos parámetros, produciendo este estado.

**Sin:**

- “el algoritmo aprende lo que necesite”;  
- parámetros elegidos después;  
- excepciones para acomodar E004–E007;  
- una capa oculta que pueda absorber cualquier resultado.  

**Criterio de implementabilidad:**  
si no podemos implementar **exactamente** las reglas desde el documento,  
**todavía no tenemos un mecanismo**.

---

### 2. La información llega como **frontera**

El candidato declara:

> \(\mathcal{M}\) puede ver **A, B y C**.  
> \(\mathcal{M}\) no puede ver **D, E ni F**.

**MD-035 es crucial.** No basta con decir “no uso divisibilidad”.  
Hay que poder **auditar el código y el flujo de información**.

Pregunta operativa:

> **¿Qué información tuvo acceso a tener el mecanismo antes de producir su resultado?**

Eso convierte la independencia en algo **verificable**, no ceremonial.

---

### 3. La explicación llega como **cadena causal**

No basta con:

> “Mi modelo produce una curva parecida.”

Debe mostrar algo de la forma:

```text
REGLA LOCAL
    ↓
ESTADO / DINÁMICA
    ↓
PROPIEDAD NECESARIA
    ↓
OBSERVABLE
    ↓
S-004 + S-005 + S-006
```

**Filtro de piezas:**

> Si eliminamos una pieza de la regla, ¿desaparece alguna consecuencia?

Si la respuesta es “no, todo sigue igual”, esa pieza es **decoración**.

La explicación debe **generar restricciones**, no solo acomodarse a ellas.

---

### 4. P\* llega como **apuesta**

Pieza que convierte al candidato en candidato **real**.

El proponente dice:

> Bajo estas condiciones **nuevas**, **antes** de observar los datos, predigo **X**.

X debe ser lo bastante preciso para **poder morir**.

| No | Sí (ejemplos de forma, no de contenido) |
| -- | --------------------------------------- |
| “Espero que aparezca algo interesante.” | “Si cambiamos \(N\) así, A>B se conserva y C cruza este umbral.” |
| | “Bajo esta \(T\), el observable cambia monótonamente en esta dirección.” |
| | “El efecto desaparece bajo X y persiste bajo Y.” |

La predicción no necesita ser espectacular.  
**Necesita ser peligrosa.**

---

## Arquitectura de cuatro capas

```text
┌─────────────────────────────────────────┐
│  HISTORIAL                              │
│  E001–E007                              │
│  Qué ocurrió                            │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│  RESTRICCIONES                          │
│  S-004–S-006 (+ muertos S-001–S-003)    │
│  Qué debe explicar                      │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│  ADUANA                                 │
│  ATHENA_MECHANISM_INTAKE                │
│  Qué debe declarar                       │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│  CANDIDATO ℳ                            │
│  Reglas + Información + Explicación + P*│
└─────────────────────────────────────────┘
                    ↓
              SELLO → TEST
```

El candidato **no** nace de mirar los datos y escribir una historia.

Nace de una intuición **externa** (matemática, física, computacional, geométrica, …)  
formulable de manera **independiente**. Después se le pregunta:

> Muy bien. Ahora que existes, ¿qué puedes explicar  
> y qué predices que **todavía no** hemos medido?

Si no puede responder → no es un mecanismo.  
Es una intuición interesante **esperando convertirse** en uno.

---

## Disciplina: no fabricar al visitante

> **No debemos inventar un candidato para llenar el vacío.**

```text
CANDIDATO ℳ
    ↓
¿existe actualmente?
    ↓
NO
```

### Lo que NO se promueve a mecanismo

Grafos ordinales, Laplacianos, \(M_2\), ruedas de Cramér, clustering, gaps,  
espectros, resonancias, geometría, ni ninguna explicación que **solo reorganice** E004–E007.

Eso es historial / material posible — no explicación.

```text
E004–E007 → regularidad → ℳ a medida → “explicación”
= post-hoc con traje de gala
```

---

## Paquete de registro completo (ℳ-ID, 1–7)

```text
ℳ-ID

1. REGLAS        definición completa y finita (implementable)
2. INFORMACIÓN   qué puede / no puede leer (auditable)
3. OPERACIÓN     qué transforma, conserva, produce
4. EXPLICACIÓN   cadena causal → S-004 + S-005 + S-006
5. PARÁMETROS    lista completa y cerrada
6. P*            predicción nueva, cuantificable, sellable, peligrosa
7. MUERTE        resultado que falsaría ℳ
```

Más:

- **Independencia temporal de las REGLAS:**  
  ¿Podríamos haber escrito \(\mathcal{M}\) antes de conocer los supervivientes?  
  Si no → **MODELO RETROSPECTIVO** (no explicación primaria).

---

## Flujo de aduana

```text
Paquete 1–7
    → ¿P* sellable?           no → RECHAZO
    → ¿Reglas implementables? no → aún no es mecanismo
    → ¿Frontera de info auditable? no → RECHAZO
    → ¿Independencia temporal? no → MODELO RETROSPECTIVO
    → ¿SURVIVORS + PROHIBICIONES? no → RECHAZO
    → CANDIDATO ELEGIBLE
    → sello P* → protocolo → hash → ejecución
    → P* falla → ℳ cae | P* acierta → ℳ gana peso
```

---

## Registro

| ℳ-ID | Tipo | P\* | Estado | Notas |
| ---- | ---- | -- | ------ | ----- |
| — | — | — | **ningún candidato** | vacío a propósito |

---

## Estado del laboratorio

```text
┌───────────────────────────────┐
│ ATHENA                        │
├───────────────────────────────┤
│ Protocolos / historial        │ ✓
│ Observables                   │ ✓
│ Survivors / contrato          │ ✓
│ Espacio de mecanismos         │ ✓
│ Intake / aduana (4 estatus)   │ ✓
│ Mecanismo candidato           │ ✗
│ P*                            │ ✗
└───────────────────────────────┘
```

---

## Frase de fase

> **No falta un experimento.  
> Falta una hipótesis que acepte el riesgo de ser falsada.**

Puede venir de cualquier dirección. No tiene que ser “sobre primos”.  
Puede ser dinámica, transformación, conservación, geometría, sistema discreto,  
o algo inesperado.

**Deberá entrar por la misma puerta.**

> **No buscamos una idea que parezca explicar Athena.  
> Buscamos una regla que, al ser ejecutada, obligue a Athena  
> a comportarse de una manera que todavía no conocemos.**

---

## Postura

```text
No:  "Tenemos una idea, veamos si puede convertirse en mecanismo."
Sí:  "Aquí están mis reglas, mi frontera de información,
      mi cadena causal, y la predicción que puede matarme."
```

**Silencio productivo** hasta el primer visitante con paquete cerrado.

---

# FIN — ATHENA_MECHANISM_INTAKE

*Las cuatro cosas las trae el candidato.  
Reglas = definición. Info = frontera. Explicación = causal. P\* = apuesta.  
Peligrosa, no espectacular.*
