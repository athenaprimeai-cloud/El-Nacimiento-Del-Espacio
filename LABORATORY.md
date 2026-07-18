# Laboratorio metodológico (identidad del proyecto)

**Este documento fija el nivel de abstracción.**  
**Eras del proyecto:** `PROJECT_ERA.md` (Era I diseño = cerrada; Era II investigación = activa).

---

## Tres niveles de **objeto** + tres de **trabajo**

### Objeto

| Nivel | Qué es | Qué no es |
| ----- | ------ | --------- |
| **1. Principio rector** | Brújula; **«no sabemos»** válido | Tecnología, dominio |
| **2. Kernel metodológico** | El **laboratorio** (dominio-agnóstico) | “Athena” = nombre del lab |
| **3. Programas científicos** | Athena, … sobre el kernel | El kernel mismo |

### Trabajo

| Capa | Función |
| ---- | ------- |
| Principio rector | No se negocia en campañas |
| **Investigación del lab** (META-E) | Evidencia E-M1…E-M5 (`META_EVIDENCE_MODEL.md`) |
| **Ingeniería del lab** | Implementa regímenes ya investigados; el código **no** crea conocimiento |

> **El código nunca crea conocimiento; únicamente ejecuta un régimen de investigación.**

### Conservación epistemológica

> Una modificación solo es aceptable si **aumenta capacidades** sin **alterar el significado** de la evidencia ya obtenida.

| Implementación | Metodológico |
| -------------- | ------------ |
| No requiere necesariamente META-E si conserva el régimen | Requiere evidencia E-M* / protocolo |

### Mejoras también mueren

Ninguna optimización entra al kernel por “parecer mejor”: entra por el régimen experimental (o es solo ingeniería que **conserva** evidencia).

### Confianza

Desplazada desde personas/implementaciones hacia el **régimen experimental**.

```text
                 PRINCIPIO RECTOR
                        │
                        ▼
         KERNEL METODOLÓGICO (laboratorio)
                        │
        ┌───────────────┼───────────────┐
        ▼               ▼               ▼
     Athena         Programa X      Programa Y
   (aritmética /      (futuro)       (futuro)
    estructuras)
```

---

## Athena ya no es el laboratorio

| Antes (narrativa confusa) | Ahora (explícito) |
| ------------------------- | ----------------- |
| “Athena = todo el sistema” | **Athena = un programa** sobre el kernel |
| “IA para Goldbach” | Kernel = infraestructura; Goldbach = **banco de pruebas** del primer programa |
| Resolver Goldbach define el éxito del proyecto | El éxito del **kernel** es disciplina y robustez metodológica |

Mañana podrían existir (mismo kernel):

- **Athena** — estructuras aritméticas / residuos / Goldbach  
- **Hypatia** — geometría  
- **Noether** — álgebra  
- **Curie** — física  
- **Darwin** — biología computacional  

sin cambiar una línea **conceptual** del núcleo.

---

## Por qué Goldbach

**No** (solo):

> Porque queremos resolver Goldbach.

**Sí** (metodológicamente más fuerte):

> Porque **Athena** es el **primer programa científico** con el que validamos y estresamos el **kernel**.

Las matemáticas siguen siendo el banco de pruebas.  
El objeto científico principal del **kernel** (y del meta-programa) no es únicamente Goldbach: es el **laboratorio**.

---

## Hipótesis principal del proyecto (no de Goldbach)

> **Un laboratorio construido mediante separación explícita de funciones produce investigación más robusta que un sistema monolítico.**

Eso es una hipótesis **científica** (metodológica).  
Se mide con modos M1–M4 y métricas de proceso.  
También puede **morir** — sin abandonar la brújula.

---

## Programa meta

No estudia matemáticas de dominio.  
Estudia el **kernel**:

> ¿Esta modificación aumenta la calidad metodológica del laboratorio?

Independiente del dominio. Mismo CORE + AUDITOR.

---

## Narrativa pública (recomendada)

**No:**

> Estamos construyendo una IA para investigar matemáticas.

**Sí:**

> Estamos investigando cómo construir **laboratorios computacionales** capaces de mejorar su proceso de investigación **sin perder la capacidad de equivocarse**.

Las matemáticas (Athena / Goldbach) son el primer banco de pruebas.  
Gran parte del trabajo reciente no ha sido “resultados matemáticos”, sino **infraestructura metodológica** que permitirá confiar en esos resultados cuando lleguen.

---

## Qué permanece y qué es revisable

| Estable | Falsable / revisable |
| ------- | -------------------- |
| **Principio rector** (brújula) | Arquitectura del kernel (separación de funciones, Selector, etc.) |
| Capacidad de decir **no sabemos** | Heurísticas, pipeline, componentes |

Principios permanentes ≠ diseño revisable.

---

## Fase actual: kernel congelado · investigar (no sobreteorizar)

Ver `KERNEL_FREEZE.md`, `CONSTITUTION_AND_LAW.md`, `META_EXPERIMENTS.md`.

| | |
| - | - |
| Diseño del kernel | **Congelado** hasta evidencia meta suficiente |
| Cuello de botella | Evidencia empírica sobre el lab |
| Primera pregunta ante un cambio | **¿Qué nivel modifica?** (constitución / legislación / ingeniería) |

```text
Constitución → identidad (excepcional)
Legislación  → META-E (puede morir)
Ingeniería   → conserva evidencia (no define el lab)
```

El laboratorio es **objeto experimental**. META-E = rigor E004.2.

## Estado de implementación (referencia)

| Pieza | Rol en el mapa |
| ----- | -------------- |
| `ATHENA_PRINCIPIO_RECTOR.md` | Nivel 1 |
| `athena_core/` | Nivel 2 — kernel |
| Athena / E004.x / Goldbach | Nivel 3 — un programa |
| `META_EXPERIMENTS.md` | Validación experimental del lab |
| `ATHENA_META_PROGRAM.md` | Diseño meta / M1–M4 |

---

# FIN — LABORATORY

*El laboratorio es el kernel.  
Athena es un programa.  
Ahora: validar el lab, no ampliarlo.*
