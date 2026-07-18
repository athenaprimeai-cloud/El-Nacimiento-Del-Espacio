# Legislación: Auditor v0.1

**Nivel:** legislación metodológica  
**Estado:** **SOPORTADO CON LÍMITES DE CAPA**  
**Evidencia:** META-E003  

---

## Perfil

| Capa | Estado |
| ---- | ------ |
| Integridad documental / estructural | **Fuerte** |
| Escala (corrupción entre muchas fichas) | **Fuerte** (bajo A4) |
| Interpretación semántica | **Limitada** — no cubierta |
| Elección de métricas / supuestos | **Abierta** — no cubierta |
| NO_SABEMOS | No castigado (correcto) |

---

## Uso correcto

```text
Auditor automático  →  forma del protocolo
        +
Revisión de supuestos / semántica (humano u otra capa futura)
        →  significado del experimento
```

Ningún guardián automático actual puede vigilar del todo lo que **comparte como supuesto**.

---

## No hacer

- Tratar PASS del Auditor como “hipótesis verdadera”  
- Eliminar el Auditor (E-M1 se degrada)  
- Confiar solo en el Auditor para E-M3 global  

---

# FIN — LEGISLATION AUDITOR v0.1
