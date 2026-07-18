# ATHENA — EXPLORER (PASO 3)

**Estado:** autorizado · objetivo **redefinido**  
**No es:** generador de conocimiento · juez · archivista · IA obligatoria  
**Es:** proveedor de **presión exploratoria** sobre el kernel  

---

## Madurez previa (no se reabre)

> **El kernel metodológico de Athena se considera estable para los casos evaluados.  
> Las siguientes fases extienden capacidades; no redefinen el método.**

Consecuencias:

| Si… | Entonces… |
| --- | --------- |
| PASO 3 falla | El kernel **sigue** válido |
| El explorador propone basura | Problema del **explorador**, no del método |
| El LLM desaparece | El **laboratorio** (CORE+AUDITOR) sigue existiendo |

Método desacoplado de la tecnología de exploración.

---

## Objetivo (no “generador de candidatos” como conocimiento)

**No:**

> Generador de hipótesis / “encontró algo brillante”.

**Sí:**

> **Proveedor de presión exploratoria.**

```text
Entrada:
    Pregunta (ID + texto)

Salida:
    Lista de candidatos
    (cada uno: X / Y / Z / W o rechazo por ficha incompleta)
```

| Puede | No puede |
| ----- | -------- |
| Aumentar el territorio explorado | Decidir |
| Proponer fichas / candidatos | Puntuar “mérito científico” |
| Generar volumen (ruido incluido) | Archivar estados terminales |
| | Interpretar resultados de control |
| | Saltar el auditor |

Ni siquiera “sabe” si un candidato merece existir.  
Solo alimenta al kernel.

---

## Criterio de éxito (cambio cualitativo)

**No es:**

> Encontró una hipótesis brillante.

**Es:**

> Generó N candidatos y el kernel **rechazó / absorbió** la mayoría **sin romperse**  
> (auditor PASS; sin reescritura post-hoc; sin borrar muertes).

Un laboratorio científico debe **soportar ruido**.  
PASO 3 mide eso.

---

## Implementación mínima (v0.1) — hecha

Sin LLM. Explorador **sintético** de presión.

Código: `athena_core/explorer.py` · `scripts/run_explorer_pressure.py`

### Resultado registrado (N=100)

```text
aceptados: 20
rechazados: 80  (INCOMPLETE_FICHA)
auditor: PASS
paso3_success: true
```

Éxito = kernel soportó ruido. **No** se reclama hipótesis brillante.

---

## Relación con el kernel

```text
Explorador  →  presión (candidatos)
CORE        →  escribe disciplina
AUDITOR     →  lee disciplina
Registro    →  válido o FAIL
```

Si el explorador “falla” como fuente de ideas, el kernel **no** se reescribe.

---

# FIN — EXPLORER

*Presión, no conocimiento.  
Éxito = el kernel no se degrada bajo ruido.*
