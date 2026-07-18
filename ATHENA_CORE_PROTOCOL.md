# ATHENA — CORE PROTOCOL (PASO 1)

**Estado:** autorizado · implementación mínima  
**No es:** Athena investigando · IA · agentes · descubrimiento  
**Es:** prueba de que la disciplina puede existir como estructura ejecutable  

> ATHENA_CORE_PROTOCOL no es Athena investigando.  
> Es Athena demostrando que puede **conservar su propia disciplina**.

**Pregunta del paso:**

> ¿Puede una máquina **obligarnos** a mantener el mismo estándar cuando investigamos?

---

## Contrato de alcance

```text
ENTRA:
- estructura de preguntas
- fichas de hipótesis
- predicciones previas
- criterios de muerte / debilitamiento
- estados
- registro

NO ENTRA:
- modelos IA
- búsqueda matemática
- generación automática
- optimización
- agentes
```

Primera piedra: **esqueleto con columna vertebral**, no cerebro.  
Motor de investigación: **apagado**. Solo frenos.

---

## Ciclo mínimo

```text
Crear pregunta
      ↓
Crear hipótesis
      ↓
Definir: qué predice / qué debilita / qué mata
      ↓
Registrar resultado (bajo control declarado)
      ↓
Asignar estado
      ↓
Archivar
```

### Estados permitidos

```text
SOPORTADA_BAJO_CONTROL
DEBILITADA
MUERTA
INDETERMINADA
NO_SABEMOS
```

*(Nota: se usa SOPORTADA_… con O; “soportada” = apoyo bajo control, no verdad universal.)*

---

## Tests de integridad (no matemáticas)

| ID | Intento | Esperado |
| -- | ------- | -------- |
| FT-CORE-01 | Cambiar predicción después del resultado | **rechazado** |
| FT-CORE-02 | Borrar hipótesis muerta | **rechazado** |
| FT-CORE-03 | Cerrar hipótesis sin control | **bloqueado** |

Si el núcleo sobrevive: primera evidencia de que el método puede vivir fuera del documento.

---

## Código

```text
athena_core/          paquete Python
tests/test_athena_core_protocol.py
data/athena_core/     registro persistente (JSON)
```

Uso:

```text
cd "El Nacimiento del Espacio"
python -m athena_core.cli ...
```

---

# FIN — CORE PROTOCOL

*Árbitro de papel digital. Impone disciplina. No opina.*
