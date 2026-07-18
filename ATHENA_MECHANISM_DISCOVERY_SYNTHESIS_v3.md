# ATHENA — Síntesis de Mechanism Discovery v3

**Estado:** **SYNTHESIS v3** · MD-074  
**Fecha:** 2026-07-18  
**No es:** apertura de T-06 · Intake · P\* · catálogo de generadores  

---

## Frase de etapa

> **Cinco vehículos han demostrado que pueden moverse.  
> Ninguno ha demostrado que sabe adónde va.**

Y eso **ya es información**.

---

## 1. Mapa de cobertura T-01…T-05

```text
T-01  campo binario + estocasticidad local     REFERENCE_COMPLETE  P*=NONE
T-03  campo binario + determinismo CA          REFERENCE_COMPLETE  P*=NONE
T-04  proceso de puntos + renovación i.i.d.    REFERENCE_COMPLETE  P*=NONE
T-05  puntos en ℝ² + geometría métrica         REFERENCE_COMPLETE  P*=NONE
        │
        └── todos: Intake vacío
```

| ID | Representación | Interacción | Dinámica | Memoria / historia |
| -- | -------------- | ----------- | -------- | ------------------ |
| T-01 | campo binario 1D | vecindad / conteo | estocástica síncrona | **no** (Markov en config) |
| T-03 | campo binario 1D | tabla \(f\) | determinista síncrona | **no** (estado = config actual) |
| T-04 | puntos en \(\mathbb{N}\) | ninguna (i.i.d.) | renovación (un barrido) | **no** (gaps sin historial) |
| T-05 | puntos en \(\mathbb{R}^d\) | distancia métrica | hard-core secuencial | **no** (solo posiciones + orden de llegada) |

### Lectura

| Fracasaron como | No fracasaron como |
| ---------------- | ------------------ |
| **candidatos** (P\*=NONE) | **experimentos de cartografía** |

T-01…T-05 **no fallaron** como Phase III.  
**Ninguno** produjo hipótesis Athena.

---

## 2. Ejes ya cubiertos

| Eje | Cubierto por |
| --- | ------------ |
| Campo binario + azar local | T-01 |
| Campo binario + determinismo CA | T-03 |
| Proceso de puntos en la recta (gaps) | T-04 |
| Geometría métrica en \(\mathbb{R}^d\) | T-05 |
| Exclusión / packing (varias formas) | T-01 (paramétrico), T-05 (métrico) |
| Matemática necesaria rica **sin** P\* | los cuatro |

### Propiedad acumulada

```text
nueva clase → nueva matemática  ≠  nueva explicación / P*
```

La diversidad creció. El registro de candidatos **sigue vacío**.

---

## 3. Eje aún ausente

```text
T-01 / T-03 / T-04 / T-05
        │
        ├── producen estado
        ├── producen evolución (o generación)
        ├── producen restricciones / packing / renovación / CA
        └── no producen memoria de historia estructural
```

| Ausente | Significado |
| ------- | ----------- |
| **Estado histórico / memoria** | la regla no depende de un estado interno \(s_t\) que resuma trayectoria |
| **Dependencia temporal no trivial** | más allá del “paso \(t\)” Markov en la config o del orden de llegada en hard-core |
| **Consecuencia global que no esté en el estado instantáneo** | p.ej. invariante que requiera historial |

**Nota:** el orden de llegada en T-05 es aleatorio y se usa en la selección, pero **no** es memoria estructural acumulada de la regla a lo largo de una evolución; es un dispositivo de thinning de un solo paso.

---

## 4. Restricción negativa de la carretera (congelada)

> **No abrir una nueva familia  
> si no introduce una relación estructural  
> que pueda, en principio, producir una P\*.**

No basta con:

- otro campo binario;
- otra dinámica local;
- otra renovación de gaps;
- otra geometría métrica;
- otra regla de exclusión;
- más matemática necesaria “rica” del mismo tipo.

Todo eso **ya se cartografió** y **no bastó** para una apuesta Athena.

### Pregunta agresiva de v3

**No:**

> ¿Qué otro mecanismo podemos ejecutar?

**Sí:**

> **¿Qué clase de mecanismo podría producir una P\*  
> sin que nosotros le indiquemos qué patrón buscar?**

---

## 5. Criterio de apertura T-06 / T-08 (si se abre)

T-06 (memoria finita) / T-08 (contacto-infección) solo son **candidatos de hueco** si:

### Debe

| # | Criterio |
| - | -------- |
| M1 | La **memoria es parte de la regla** (estado \(s_t\) o historial finito **necesario** para decidir) |
| M2 | Existe al menos una **consecuencia necesaria global** que **no** se deduce del estado instantáneo de ocupación solo |
| M3 | Tabla R-DIV: no es T-01/T-03/T-04/T-05 “con un contador decorativo” |
| M4 | Misma ceguera Phase III (no Athena, no raw previos) |
| M5 | Sin obligación de P\*, pero **con posibilidad estructural** de P\* (a diferencia de re-ejecutar packing) |

### No debe

| # | Anti-criterio |
| - | ------------- |
| A1 | \(s_t\) que no altera la decisión (decoración) |
| A2 | Reimplementar T-01 con un contador de pasos |
| A3 | “Memoria” = solo seed o solo orden de llegada ya visto en T-05 |
| A4 | Abrir T-06 solo para alargar el catálogo |

### Pregunta de control para la spec T-06

> **¿Puede una regla local con memoria interna generar una consecuencia global necesaria  
> que no exista en el estado instantáneo?**

Si la respuesta honesta es **no** (o solo trivialidades) → no abrir, o cerrar como REFERENCE sin pretender eje nuevo.

---

## 6. Lo que ya sabemos de Phase III (restricción negativa)

No basta, **por sí solo**, con:

| Clase de idea | Resultado en el mapa |
| ------------- | -------------------- |
| Campo binario | T-01, T-03 → sin P\* |
| Dinámica local | T-01 → sin P\* |
| Dinámica determinista | T-03 → sin P\* |
| Renovación de gaps | T-04 → sin P\* |
| Geometría métrica | T-05 → sin P\* |
| Regla de exclusión / packing | T-01, T-05 → sin P\* |
| Matemática necesaria rica | N\* en todos → sin P\* Athena |

**Distinción crítica:**

> **T-01–T-05 cartografían mecanismos.  
> Ninguno ha producido todavía una hipótesis.**

---

## 7. Decisión v3 (congelada)

| Acción | ¿Ahora? |
| ------ | ------- |
| Abrir T-06 inmediatamente | **no** |
| Abrir T-0x por acumulación | **no** |
| Síntesis v3 (este documento) | **sí** |
| Intake / E008 / P\* fabricada | **no** |
| Próxima familia | solo si pasa §5 (hueco de **memoria/historia**) u otro hueco con **posibilidad estructural de P\*** documentada |

### Frase operativa

> El próximo vehículo no debería ser simplemente otro motor.  
> Debería incorporar una **dimensión estructural que los anteriores no podían tener**.

Por ahora: **memoria / historia estructural** es el hueco nombrado;  
**no** se abre hasta spec R-DIV + M1–M5.

---

## 8. Tablero

```text
┌────────────────────────────────────┐
│ PHASE III                          │
├────────────────────────────────────┤
│ T-01 … T-05 cartografiados         │ ✓
│ Representaciones: 3                │ ✓
│ P* / Intake                        │ ✗
│ Síntesis v3                        │ ✓
│ T-06                               │ no abierto
└────────────────────────────────────┘
```

---

## Historial

| Fecha | Evento |
| ----- | ------ |
| 2026-07-18 | v1 post T-01·T-03 |
| 2026-07-18 | v2 post T-04 |
| 2026-07-18 | v3 post T-05: eje memoria ausente; restricción negativa; no T-06 aún |

---

# FIN — SYNTHESIS v3

*Cinco motores se mueven.  
Ninguno lleva dirección Athena.  
El siguiente ladrillo, si llega, trae una dimensión que estos no tenían.*
