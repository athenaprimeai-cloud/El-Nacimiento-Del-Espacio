# ATHENA — INTERFACE CONTRACTS

**Capa:** ingeniería metodológica · **fronteras** entre roles · **no** implementación · **no** motor  
**Entrada:** brújula · método 0–5 · frontera de automatización · arquitectura conceptual  
**Programa:** B (Athena)  

---

## Lugar en el mapa

```text
ATHENA

Brújula                         ✅
Método 0–5                      ✅
Frontera de automatización      ✅
Arquitectura conceptual         ✅
Interfaces y contratos          ⬅  este documento
Pruebas de fallo                →  ATHENA_FAILURE_TESTS.md
Implementación                  ❌  no iniciada
Motor                           apagado
Agentes                         no creados
```

```text
Diseño
   ↓
Contratos          ⬅ aquí
   ↓
Pruebas de fallo
   ↓
Implementación mínima
   ↓
Primer ciclo real
```

Este documento **no** describe agentes.  
Describe **fronteras**: qué puede y qué **no** puede cada función.

---

## Propiedad central del laboratorio

```text
No buscamos un sistema que siempre responda.

Buscamos un sistema capaz de distinguir:
- sé algo,
- tengo evidencia parcial,
- una hipótesis sobrevivió,
- no puedo decidir todavía.
```

**“No puedo decidir todavía”** no es un fallo del laboratorio.  
Es una **salida válida**.

---

## Principio de contrato

| Todo contrato define | |
| -------------------- | - |
| **Puede** | Acciones y salidas permitidas |
| **No puede** | Acciones que constituirían auto-coronación o post-hoc |
| **Emite** | Tipo de objeto (interfaz) |
| **No cierra** | Qué estados de conocimiento le están prohibidos |

```text
Ningún componente produce conocimiento final.
El ciclo completo produce evaluación.
```

---

## Contrato Explorador

### Puede

- Generar **candidatos** (formato X / evidencia Y / predicción Z / forma de morir W)
- Proponer transformaciones sobre entradas válidas (Fase 2)
- Sugerir experimentos o líneas de exploración
- Enumerar regularidades **sin** declarar estructura

### No puede

- Elevar un candidato a **conclusión** o “hallazgo”
- Asignar estado `reforzada` / `muerta` / `verdadera`
- Omitir forma de morir W
- Cambiar métricas o dominio “porque el patrón se ve mejor”

### Emite

```text
Candidato(ID, X, Y, Z, W, origen, dominio)
```

### No cierra

Conocimiento final · significado matemático · verdad

---

## Contrato Crítico

### Puede

- Atacar supuestos de un candidato o hipótesis
- Buscar artefactos, bordes, confusiones, sobreclaims
- Proponer fallos y formas de muerte operativas
- Registrar ataques fallidos (el Crítico también puede perder)

### No puede

- Declarar **falsedad absoluta** sin marco de control
- Redefinir la hipótesis para que el ataque “gane”
- Cambiar reglas o umbrales del marco
- Sustituir un control por una opinión

### Emite

```text
Ataque(ID, tipo, hipótesis_ref, procedimiento, forma_de_morir, estado)
```

### No cierra

`falso definitivo` · verdad de la rival · borrado de la favorita del registro

---

## Contrato Diseñador

### Puede

- Convertir ataques / preguntas en **controles** con comparación
- Declarar brazos, variables congeladas, métricas, umbrales de medición y decisión
- Preparar marco **congelable** pre-ejecución

### No puede

- Cambiar la **pregunta** para salvar una hipótesis
- Mover umbrales después de ver datos
- Ejecutar 100 variantes y quedarse con la que “funciona”
- Omitir rival / nulo cuando el ataque lo exige

### Emite

```text
ControlDraft(ID, marco_congelado, brazos, métricas, umbrales, ataque_ref)
```

### No cierra

Confirmación de la hipótesis · “éxito” narrativo · reinterpretación post-hoc

---

## Contrato Auditor

### Puede

- **Bloquear** ejecución si falta ficha, ataque, marco o se detecta post-hoc
- Detectar violaciones de protocolo y saltos de fase
- Verificar que la brújula / contratos no fueron alterados por un resultado
- Exigir registro de muertes e indeterminación

### No puede

- Decidir la **interpretación matemática final**
- “Perdonar” una violación porque el resultado es interesante
- Reescribir el protocolo en nombre de la eficiencia
- Sustituir al ciclo como juez de verdad

### Emite

```text
Audit(ID, ciclo_ref, cumplimiento: sí|no, violaciones[], acción: permitir|bloquear)
```

### No cierra

Significado de X · verdad de la hipótesis · borrado de evidencia incómoda

---

## Contrato Registro (Archivista)

### Puede

- Conservar historia **completa**: candidatos, hipótesis vivas y **muertas**, ataques, controles, datos, decisiones
- Versionar instrumento y enlazar IDs
- Exponer memoria negativa y límites conocidos
- Separar **dato** (“ocurrió X”) de **decisión** (“interpretamos X como Y bajo reglas R”)

### No puede

- Convertir **frecuencia de aparición** en autoridad
- Convertir “está en el archivo” en “es cierto”
- Borrar o enterrar hipótesis muertas
- Mezclar generaciones de instrumento sin marcar

### Emite / conserva

```text
Registro(existencia, hipótesis, ataques, controles, datos, decisiones, versiones, memoria_negativa)
```

### No cierra

Creencia obligatoria · trono de verdad · amnesia selectiva

---

## Matriz de autoridad (resumen)

| Rol | Puede bloquear ciclo | Puede emitir verdad | Puede emitir “no sabemos” |
| --- | -------------------- | ------------------- | ------------------------- |
| Explorador | No | No | Solo como candidez del candidato |
| Crítico | No (propone muerte) | No | Sí (ataque fallido / indeterminado) |
| Diseñador | No | No | Sí (diseño no discrimina) |
| Auditor | **Sí** | No | Sí (bloqueo / violación) |
| Registro | No | No | **Sí** (estado residual / indeterminado permanente) |
| **Ciclo completo** | — | Evaluación bajo dominio | **Salida válida** |

---

## Encadenamiento obligatorio

```text
Explorador → Candidato
     ↓
Crítico → Ataque
     ↓
Diseñador → ControlDraft
     ↓
Auditor → permitir | bloquear
     ↓
[Ejecución solo si permitir]
     ↓
Registro → dato + decisión + estado (incl. no sabemos)
```

Cualquier atajo (Explorador → Registro como hallazgo) es **violación de contrato**.

---

## Qué no se hace aquí

- Implementar los roles  
- Elegir LLM o orquestador  
- Ejecutar el primer ciclo automático  
- Debilitar “no sabemos” para “parecer más inteligente”  

---

## Siguiente pieza

`ATHENA_FAILURE_TESTS.md` — probar que el sistema **sabe fallar correctamente** antes de encenderlo.

---

# FIN — ATHENA INTERFACE CONTRACTS

*Fronteras, no personalidades.  
El ciclo evalúa. Ningún rol corona.*
