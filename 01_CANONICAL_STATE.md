# 01 Canonical State

**Identidad:** `LABORATORY.md` · **Eras:** `PROJECT_ERA.md`

```text
ERA I   Diseño del laboratorio     CERRADA
ERA II  Investigación del laboratorio  ACTIVA
```

> El laboratorio ya no evoluciona por imaginación; evoluciona por evidencia.

Era I cerrada **no** porque el diseño sea perfecto, sino porque el diseño **ya no es la herramienta de progreso**.  
Un fallo futuro del kernel es **legislación** (Era II), no reabrir Era I.

**Kernel CONGELADO.**  
```text
ERA I      Diseño del lab                   CERRADA
ERA II     Investigación del lab            ACTIVA
META-E001  Economía + integridad            CERRADO
META-E002b Diversidad / zona excluida       CERRADO
META-E004  ¿Generaliza el patrón?           CERRADO (sí, bajo 3 dominios sintéticos)
Selector v0.1  SOPORTADO CON LIMITACIONES   (riesgo de diversidad transversal)
```

**Lab medido.**  
**DOMAIN-E001:** pico 1/6 residual media → **MUERTA** vs nulos.  
**DOMAIN-E002:** entropía espectral bajo \(\mathcal{R}\) → **DESAPARECE** (no diferencial vs nulos); H-01 MUERTA.  
**Montaña abierta.** No simetría global asumida. Siguiente: otro \(P\) (nuevo ID) o canal residual documentado.

```text
CANONICAL_PHASE_SOURCE = 01_CANONICAL_STATE.md

LATEST_COMPLETED_PHASE = 006H18
LATEST_RESULT = 006H18_CANONICAL_PHASE_FIELD_DISAMBIGUATION_PATCH_PASS

LATEST_GOVERNANCE_PHASE = 006H18

PROJECT_LATEST_RUNTIME_PHASE = 006H16
PROJECT_LATEST_RUNTIME_RESULT = 006H16_L3_REAL_BACKEND_ADAPTER_IMPLEMENTATION_FAKE_ONLY_PASS

006H16_HERMES_AUDIT = ACCEPTED_WITH_EXTERNAL_FROZEN_INVENTORY_DEBT
006H17_HERMES_AUDIT = ACCEPTED_WITH_CANONICAL_PHASE_FIELD_AMBIGUITY

ACTIVE_EXECUTION_PHASE = none
NEXT_PHASE_AUTHORIZED = false

OPEN_EXTERNAL_DEBT = stale_006E8_documented_inventory

L3_READY_FOR_REAL_BACKEND_CODE_STATIC_AUDIT = true
L3_READY_FOR_REAL_BACKEND_REAL_SMOKE = false
L3_READY_FOR_REAL_EXECUTION = false

MATHEMATICAL_PROOF = false
H2_CERTIFIED = false
006F = blocked
REAL_FLINT_EXECUTION = forbidden
ZERO_CERTIFICATION = forbidden
ZERO_TABLES = not_generated
DOWNSTREAM_USE = forbidden
NOVELTY_CLAIM = false
```

Agents and templates must derive the current phase from this file:

```text
CURRENT_PHASE =
  ACTIVE_EXECUTION_PHASE
  if ACTIVE_EXECUTION_PHASE != none
  else LATEST_COMPLETED_PHASE

ACTIVE_EXECUTION_PHASE = none
CURRENT_PHASE = 006H18
```

This state file is governance metadata only. It does not authorize execution,
does not modify any mathematical claim, does not open H2 or 006F, and does not
resolve the external frozen 006E8 documented-inventory debt.
