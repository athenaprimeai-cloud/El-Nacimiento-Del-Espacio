# ATHENA DOMAIN-E004 — Addendum de revisor (bisturí)

**Fecha:** 2026-07-17  
**Estado:** **corrección de veredicto** · no reescribe números de `classification.json`  
**No es:** ejecución de E005 · catedral  

---

## Veredicto protocolar E004 c1 (histórico, no borrado)

Bajo el protocolo v1.0 **tal como estaba escrito** (C1 = uniforme equicardinal):

- \(M(P)\) extremo vs C1 uniforme  
- separado de C2 “primeros \(m\) semiprimos” y C3 Ulam por umbrales congelados  

Eso **sigue siendo un hecho de corrida**.  
No se reescribe el JSON.

---

## Cuatro objeciones — resolución

### 1. Composición de C1 decide todo — **ACEPTADA · bloquea muerte de H-00**

| C1 en E004 | Problema |
| ---------- | -------- |
| Uniforme sobre \(\{1..N\}\), equicardinal | Los primos tienen gradiente \(\sim 1/\log n\). Uniforme **no**. |

Un \(z\approx -5.84\) vs uniformes puede ser **solo el gradiente de densidad**  
(información nivel teorema de los números primos), no “material” más allá de densidad.

**Asesino legítimo de H-00** (hipótesis central de réplica, prerregistrada en E005):

> **Control de Cramér:** incluir cada \(n\in\{2..N\}\) con probabilidad \(1/\log n\)  
> (o réplica condicional a cardinalidad \(\approx\pi(N)\)),  
> misma densidad **local**, sin estructura de gaps primos.

| Si… | Lectura |
| --- | ------- |
| \(M(P)\approx M(\mathrm{Cramér})\) | Ladrillo = densidad + independencia. Punto. |
| \(M(P)\) se distingue de Cramér bajo control | Material **candidato** más allá del modelo de Cramér (aún no operador). |

**Estado H-ATH-D004-00:** **NO MUERTA.**  
Solo queda **debilitada la subhipótesis** “uniforme equicardinal basta como nulo de densidad”.

**Estado H-ATH-D004-01:** **SOPORTADA solo bajo nulo C1-uniforme**  
(no se eleva a “material vs densidad local”).

---

### 2. \(p=0\) no existe — **ACEPTADA · corrección de informe**

Con \(B=100\) réplicas, el reporte honesto es:

\[
p \le \frac{1}{B+1} = \frac{1}{101} \approx 0.0099
\]

(p de rango / cota de Monte Carlo, no “probabilidad cero”).

Además \(z\approx -5.84\) **presume normalidad** de la distribución nula de \(M_2\);  
con \(n=100\) **no hay soporte** para esa cola como evidencia gaussiana.

**Regla a partir de E005:**

- reportar **p de rango** (o \(p\le 1/(B+1)\) si ningún nulo alcanza)  
- \(B \in [10^3,10^4]\) si \(M_2\) es forma cerrada (barato)  
- \(z\) solo como descriptivo opcional, **no** como veredicto

---

### 3. C2 tiene confusión de densidad — **ACEPTADA · contraste E004 C2 no informa lo que MD-036 quería**

E004 tomó los **primeros** \(m\) semiprimos \(\le N\).  
Eso equicardinaliza el **conteo**, pero concentra el soporte en un intervalo inicial  
donde la densidad de semiprimos es alta → \(M(C2)\approx 36\) puede ser **densidad pura**.

| Corrección E005 | |
| --------------- | - |
| C2 | muestra de \(m\) semiprimos **uniformes entre todos los semiprimos \(\le N\)** (o con perfil de densidad local comparable), no el prefijo |

Hasta entonces: \(D_{P,C2}\) de E004 se marca **no concluyente** para MD-036.

---

### 4. \(k=10\) no es inocente en la réplica — **ACEPTADA · prerregistro obligatorio**

Gap medio de primos \(\sim\log N\):

| \(N\) | \(\log N\) (nat. approx) | vs \(k=10\) |
| ----- | ------------------------ | ----------- |
| \(10^4\) | \(\approx 9.2\) | \(k\) ≈ escala del gap medio |
| \(10^5\) | \(\approx 11.5\) | \(k\) fijo **cruza** de régimen |

Réplica con \(k\) fijo y \(N\) mayor **no es réplica**: es **otro régimen**.

**Decisión prerregistrada (E005), elegir una y no ambas a conveniencia post-hoc:**

| Política | Significado |
| -------- | ----------- |
| **A — \(k\) fijo** | Probar cambio de régimen; **predecir dirección** del cambio de \(M(P)-M(\mathrm{Cramér})\) antes de correr |
| **B — \(k = c\cdot\log N\)** | Réplica de **escala** (misma posición relativa al gap medio); \(c\) congelado (p.ej. \(c=1\)) |

E005 c1 adopta **B** como réplica de escala principal;  
una corrida satélite A queda documentada aparte si se desea, con predicción escrita **antes**.

---

## Ancla de calibración (expectativa, no veredicto)

A escala del gap medio, gaps de primos ≈ Poisson-like (Gallagher, bajo Hardy–Littlewood);  
el modelo de Cramér reproduce gran parte de esa estadística.

**Escenario más probable del programa:** E005 **mata** el material contra Cramér.

Eso **no** sería fracaso: sería el primer resultado limpio —

```text
M₂ ordinal no ve nada más allá de densidad (+ independencia tipo Cramér)
```

Lo interesante empieza **solo** si sobrevive Cramér.

---

## Veredicto enmendado (lab)

| ID | Estado enmendado |
| -- | ---------------- |
| H-ATH-D004-01 | **SOPORTADA_BAJO_CONTROL_C1_UNIFORME** únicamente; no “material profundo” |
| H-ATH-D004-00 | **NO_MUERTA** · reabierta como hipótesis central vs **Cramér** en E005 |
| Código E004 c1 | `H01_VS_UNIFORM_ONLY__H00_PENDING_CRAMER` |

Números de corrida: válidos.  
Interpretación “H-00 muerta / material de pared”: **retirada**.

---

## Infraestructura (candado)

Los artefactos viven en:

```text
C:\Users\johnn\Documents\El Nacimiento del Espacio\
```

Ese árbol **no** es un repositorio git (sin `.git` al revisar).  
Sin commit/remote, el prerregistro **no** es candado compartido.

Ver sección de acción en respuesta de lab / MD-039.

---

# FIN — E004 ADDENDUM REVIEW

*El bisturí no borra la corrida.  
Corrige lo que la corrida no podía matar.*
