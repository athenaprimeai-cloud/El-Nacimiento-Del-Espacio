# ATHENA — RECORD DESIGN (Fase 5)

**Capa:** diseño del **registro** · memoria permanente · **no** base de datos implementada · **no** agentes · **no** motor  
**Depende de:** Fases 0–4  
- `ATHENA_PRINCIPIO_RECTOR.md`  
- `ATHENA_INSTRUMENT_DESIGN.md`  
- `ATHENA_EXPLORATION_DESIGN.md`  
- `ATHENA_ATTACK_DESIGN.md`  
- `ATHENA_CONTROL_DESIGN.md`  
**Programa:** B (Athena)  
**Programa A:** **no** se modifica  

---

## Lugar en el mapa

```text
FASE 0 — Brújula        ✅  criterio rector
FASE 1 — Instrumento    ✅  unidad mínima de investigación
FASE 2 — Exploración    ✅  terreno definido
FASE 3 — Ataque         ✅  prueba de resistencia
FASE 4 — Control        ✅  ejecución interpretable
FASE 5 — Registro       ⬅  este documento · última pieza de diseño
Motor: apagado
```

### Pregunta de Fase 5

> **¿Cómo conserva Athena conocimiento sin convertir memoria en acumulación de autoridad?**

Un sistema que experimenta pero **no** conserva memoria **repite** ciclos.  
Un sistema que solo recuerda **éxitos** desarrolla **amnesia selectiva**.  
Un sistema que trata el archivo como **verdad** convierte la memoria en **autoridad**.

Fase 5 diseña la memoria para evitar los tres fallos.

---

## Ciclo completo (salida de Fase 5)

```text
Pregunta
   ↓
Hipótesis
   ↓
Ataques
   ↓
Controles
   ↓
Resultado
   ↓
Registro permanente
   ↓
Nuevo conocimiento o nueva incertidumbre
```

Arquitectura cerrada en **diseño**:

```text
Brújula → Instrumento → Exploración → Ataque → Control → Registro
```

---

## 1. Registro de existencia

Todo objeto investigado necesita **identidad**.  
Nada puede aparecer como “descubrimiento nuevo” si ya fue evaluado.

### Campos mínimos

```text
ID:                      (único, estable)
fecha:
programa:                (B · Athena; nunca mezclar con A sin marcar)
versión del instrumento:
origen:                  (humano / función / residual / campaña)
tipo de objeto:          (pregunta | candidato | hipótesis | ataque | control | resultado)
estado actual:
enlaces:                 (padres / hijos / rivales)
```

### Reglas

| Regla | |
| ----- | - |
| Sin ID no hay objeto en el laboratorio | |
| Re-proponer lo ya evaluado exige **referencia** al ID previo | |
| “Nuevo” sin búsqueda en registro = error de proceso | |
| El ID **no** otorga autoridad; solo **trazabilidad** | |

---

## 2. Registro de hipótesis

La memoria **no** guarda solo sobrevivientes.  
Una hipótesis **muerta** también es conocimiento.

### Contenido mínimo por hipótesis

```text
Hipótesis ID:
- propuesta
- predicciones (*a priori*)
- forma de morir (W)
- ataques recibidos (IDs + tipo + estado)
- controles ejecutados (IDs + marco congelado)
- resultado / estado bajo cada control
- razón de muerte o debilitamiento (si aplica)
- dominio y no-afirmaciones
- versión del instrumento al proponer y al cerrar
```

### Estados (alineados a Fase 4)

```text
abierta | reforzada bajo control X | debilitada | muerta
indeterminada | requiere nuevo ataque | residual
```

### Regla anti-amnesia

| Guardar | No borrar |
| ------- | --------- |
| Hipótesis muertas | “para no desanimar” |
| Controles que fallaron en discriminar | “porque no salió bonito” |
| Ataques fallidos del Crítico | “porque no mataron a la favorita” |

---

## 3. Registro de decisiones

Separar **siempre**:

```text
Dato:
"ocurrió X"
(artefacto, métrica, hash, control ID)

Decisión:
"interpretamos X como Y bajo estas reglas"
(protocolo ID, umbrales, orden de decisión)
```

### Por qué importa

| Si se mezcla | Efecto |
| ------------ | ------ |
| Interpretación antigua se lee como hecho | Autoridad fantasma |
| “Sabemos que…” sin control ID | Historia sin ancla |
| Reinterpretar X sin nuevo control | Negociación post-datos (viola Fase 4) |

### Campos mínimos de una decisión

```text
Decisión ID:
dato_refs:           (IDs de resultados / artefactos)
reglas_refs:         (protocolo / umbrales / orden)
interpretación Y:
estado de hipótesis resultante:
quién/qué decidió:   (traza, no autoridad)
fecha:
```

**Dato** se conserva aunque cambie la decisión futura.  
**Decisión** nueva = nuevo ID, no reescritura silenciosa del dato.

---

## 4. Registro de versiones

Un cambio en el instrumento **cambia el contexto**.  
No se mezclan generaciones del laboratorio.

```text
Instrumento v1
    ↓
resultado R1  (válido bajo v1)

Instrumento v2
    ↓
resultado R2  (válido bajo v2; no “corrige” R1 en silencio)
```

### Reglas

| Regla | |
| ----- | - |
| Todo resultado lleva `instrumento_versión` | |
| Comparar R1 y R2 exige declarar si el instrumento es comparable | |
| “Replicación” con otra versión = **nuevo** control, no continuidad oculta | |
| Changelog del instrumento es parte del registro | |

Lección transferible de PEP-D: motor/protocolo congelados hacen comparables las campañas.  
Aquí la **versión** es el sello de comparabilidad.

---

## 5. Memoria negativa

La pieza más importante para Athena.

Registrar explícitamente:

| Memoria negativa | Ejemplo |
| ---------------- | ------- |
| Qué **falló** | Control no discriminó; REF falló; bug de entrada |
| Qué explicación **perdió** | Hipótesis ID muerta o debilitada + razón W |
| Qué caminos fueron **cerrados** | Dominio descartado; rival eliminada bajo control X |
| Qué controles ya mostraron **límites** | Umbral ciego; constructo débil; n_drift no resuelto |

### Propósito

```text
Laboratorio que solo recuerda éxitos
    → amnesia selectiva
    → repite errores
    → protege narrativas

Laboratorio con memoria negativa
    → no reabre caminos muertos sin nuevo ID
    → no “descubre” lo ya enterrado
    → preserva la capacidad de equivocarse otra vez
```

La memoria negativa **no** es vergüenza.  
Es **mapa del terreno cerrado**.

---

## 6. Memoria no es autoridad

| Memoria permite | Memoria **no** permite |
| --------------- | ---------------------- |
| Recuperar qué se hizo y bajo qué reglas | Declarar verdad por antigüedad |
| Evitar duplicar trabajo ciego | Proteger una hipótesis porque “ya se archivó como reforzada” |
| Enseñar al Crítico caminos ya atacados | Bloquear un nuevo ataque legítimo con marco nuevo |
| Auditar decisiones | Sustituir un control fallido por una narrativa de archivo |

**Principio:**

> El registro **conserva** conocimiento y derrotas.  
> **No** corona reyes.

Ante un “descubrimiento” recuperado del archivo:

```text
No:  Está en el registro → es cierto.
Sí:  Está en el registro → esto se evaluó así, bajo estas reglas;
     ¿sigue vivo el marco? ¿hace falta nuevo ataque?
```

---

## 7. Paquete mínimo de un ciclo cerrado

Al terminar un ciclo (pregunta → … → resultado), el Archivista debe poder reconstruir:

```text
1. Existencia (IDs)
2. Hipótesis (ficha + estados)
3. Ataques (propuestos / exitosos / fallidos)
4. Controles (marco congelado + ejecución reproducible)
5. Datos vs decisiones (separados)
6. Versión de instrumento
7. Memoria negativa del ciclo
8. Nueva incertidumbre o cierre de camino
```

Si falta un bloque → el ciclo **no** está cerrado para Athena (aunque haya un plot bonito).

---

## 8. Qué no se hace en este documento

- Implementar base de datos, git policies o UI  
- Automatizar el Archivista  
- Migrar artefactos de Goldbach al nuevo esquema  
- Tocar PEP-D (su Decision Log / informes son **análogos** de A, no este registro B)  
- Encender el motor  

---

## Después de Fase 5 — cambio de pregunta

**Documento de frontera:** `ATHENA_AUTOMATION_BOUNDARY.md`

**Ya no:** ¿Cómo hacemos agentes? / ¿Qué puede hacer una IA?

**Sí:** ¿Qué parte del ciclo se **delega** sin destruir el **fallo correcto**?

Orden: método primero · máquinas después · asistentes en circuito, no mente autónoma.

---

## Estado

```text
FASE 0–5  ✅  diseño completo del ciclo Athena
Motor:    apagado
Agentes:  no implementados
PEP-D:    separado · sin cambios
```

```text
Brújula → Instrumento → Exploración → Ataque → Control → Registro
```

Método listo en papel.  
Máquina todavía apagada.  
Ese es el orden correcto.

---

# FIN — ATHENA RECORD DESIGN (Fase 5)

*Memoria sin autoridad.  
Éxitos y muertes con el mismo peso.  
Amnesia selectiva prohibida.*
