# ATHENA — KERNEL VALIDATION (PASO 2.5)

**Estado:** autorizado · medición del diseño  
**No es:** PASO 3 · IA · nuevos descubrimientos  
**Es:** intentar **falsar** la suficiencia del kernel con investigaciones reales  

> Antes de ampliar el laboratorio, demostrar que el propio laboratorio  
> no necesita cambiar para explicar lo que ya hizo.

**Pregunta:**

> ¿El kernel es suficiente para describir investigaciones reales **sin** añadir reglas nuevas?

---

## Por qué esta pausa

| Hasta PASO 1 | Ejecutar el método |
| ------------ | ------------------ |
| PASO 2 | Inspeccionar el lab sin interpretar ciencia |
| **PASO 2.5** | ¿El diseño describe **cómo investigamos** de verdad? |

Dos caminos tras PASO 2:

| Camino A | PASO 3 generador de candidatos (plan original) |
| -------- | ---------------------------------------------- |
| **Camino B** | Validar el kernel con casos reales (**elegido**) |

Si el kernel no cabe E004.x, se descubre la limitación **antes** de la IA.  
Si cabe, PASO 3 deja de ser apuesta y pasa a ser extensión de un núcleo estable.

---

## Casos de prueba

| ID | Caso | Estado esperado en kernel |
| -- | ---- | ------------------------- |
| KV-01 | E004.1 H0 (independencia de M) | **MUERTA** (H1_strong) |
| KV-02 | E004.1 hecho H-E004-01 (M importa) | **SOPORTADA_BAJO_CONTROL** |
| KV-03 | E004.2 H-E004-03 (solo alfabeto) | **DEBILITADA** o **MUERTA** (outcome A) |
| KV-04 | E004.2 H-E004-02 (proyector / aritmética, apoyo relativo) | **SOPORTADA_BAJO_CONTROL** (relativo, dominio del control) |
| KV-05 | Hipótesis fallida genérica (toy) | **MUERTA** con razón |
| KV-06 | Hipótesis indeterminada | **NO_SABEMOS** |

**PASS de 2.5:** todos representables **solo** con CORE + AUDITOR, sin cambiar contratos ni añadir estados.

**FAIL de 2.5:** hace falta una regla nueva del protocolo para caber un caso.

---

## Qué se demuestra / no

Si PASS:

- El kernel describe el ciclo de E004.x y casos negativos  
- Dominio-agnóstico en la práctica, no solo en el papel  

Si no se demuestra (y no se reclama):

- Estructuras matemáticas profundas  
- Generación de hipótesis  
- Crítica superhumana  

---

## Artefactos

```text
scripts/validate_athena_kernel.py
data/athena_kernel_validation/KERNEL_VALIDATION_REPORT.json
tests/test_athena_kernel_validation.py
```

## Resultado del ejercicio (registrado)

```text
kernel_validation: PASS
all_cases_fit: true
auditor_verdict: PASS
new_protocol_rules_added: false
```

| Caso | Estado en kernel |
| ---- | ---------------- |
| KV-01 E004.1 H0 | MUERTA |
| KV-02 H-E004-01 | SOPORTADA_BAJO_CONTROL |
| KV-03 H-E004-03 | DEBILITADA |
| KV-04 H-E004-02 núcleo | SOPORTADA_BAJO_CONTROL (relativo / dominio control) |
| KV-05 fallida toy | MUERTA |
| KV-06 indeterminada | NO_SABEMOS |

**Conclusión de 2.5:** el kernel bastó para describir investigaciones reales **sin** reglas nuevas.  
**No se abrió** PASO 3. **No** se reclama ciencia nueva.

---

# FIN — KERNEL VALIDATION

*El diseño se midió. Cabía. Aún no se amplía.*
