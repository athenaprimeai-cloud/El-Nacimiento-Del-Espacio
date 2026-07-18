# Legislación: Selector v0.1

**Nivel:** legislación metodológica (falsable) — **no** constitución  
**Estado:** **SOPORTADO CON LIMITACIONES**  
**Trayectoria de evidencia:** META-E001 + META-E002b  

---

## Lectura correcta (no sobreinterpretar)

| No decir | Sí decir |
| -------- | -------- |
| El Selector falló / es malo | Tiene **beneficio** de economía y **coste** de diversidad medidos |
| El lab investiga mejor | Bajo controles sintéticos: −85 % presupuesto + **compresión** del espacio |
| Selector = juez final | Selector = **prioriza presupuesto**; la zona excluida es **memoria de diversidad** |

Murió la interpretación ingenua:

> “La eficiencia viene **solo** de eliminar ruido.”

---

## Perfil acumulado

| Propiedad | Estado | Fuente |
| --------- | ------ | ------ |
| Economía experimental | Evidencia **positiva** (E-M2 fuerte) | META-E001, re-confirmado E002b |
| Integridad del protocolo | Evidencia **positiva** (E-M1 fuerte) | META-E001, E002b |
| Conservación de diversidad | **Problema detectado** | META-E002b |
| Generalización del patrón | **Apoyo a transversalidad** (3 dominios sintéticos) | META-E004 |
| Robustez en dominio real Athena | Pendiente | E00x / META futuro |

**Lectura:** Selector = **régimen de aplicación** (excelente en redundancia; peligroso en exploración abierta). No bueno/malo.

### Intercambio documentado

```text
Costo computacional ↓   puede comprar   Costo epistemológico ↑
```

Optimizar la búsqueda puede **estrechar** la búsqueda.

---

## Rol en el pipeline

```text
Selector
   → prioriza presupuesto (grupo A)

Archivo de excluidos
   → conserva diversidad (columna de no evaluados = memoria, no basura)
```

Tensión incorporada: **explorar barato** vs **no quedar ciego**.

---

## Mapa de validez (META-E002b + META-E004)

| | |
| - | - |
| **Excelente para** | eliminar redundancia / recortar presupuesto |
| **Peligroso para** | territorios desconocidos / diversidad de caminos |
| **Aceptado** | Solo si se acepta pérdida fuerte de diversidad de OPEN |
| **Limitado** | Exploración con alta redundancia; **requiere** muestreo de excluidos |
| **No recomendado** | Búsqueda abierta de estructuras raras / diversidad como activo |

META-E004: el patrón de compresión **reaparece** en math_struct, engineering y creative (generadores **distintos** de E002b).

---

## Qué no hacer ahora

- Selector v2 por entusiasmo  
- Convertir Selector en constitución  
- Eliminarlo a ciegas (el beneficio E-M2 sigue siendo real bajo control)  
- Decir “el lab ve más claro”  
- Asumir que E002b **generaliza** (eso es **META-E004**)  

---

## Historial de versiones (fósil)

| Versión | Estado | Evidencia |
| ------- | ------ | --------- |
| **v0.1** | **Vigente con limitaciones** | E001 economía+integridad; E002b diversidad comprimida |

Futuras v1, v2: compiten con v0.1 bajo META-E; nunca “definitivas”.

---

## Logro de E002b (más que rendimiento)

> ¿Puede una mejora metodológica convertirse en fuente de error?

**Sí.** Y el lab lo detectó **antes** de convertirla en infraestructura dominante.

---

# FIN — LEGISLATION SELECTOR v0.1

*Soportado con limitaciones.  
La columna excluida es memoria de diversidad.*
