# ATHENA DOMAIN-E003 — Informe de cierre

**Protocolo:** v1.0 **CONGELADO** (rectangular · \(D_{1/2}\) · borde en FASE 2)  
**Ejecución:** `scripts/run_athena_domain_e003.py`  
**Fuente:** `resultados/classification.json`  

---

## 1. Pregunta

> Al mover el campo de visión con ventanas **rectangulares** admisibles (misma escala, cinco posiciones),  
> ¿la discrepancia espectral fraccionaria \(D_{1/2}\) entre residual global restringido y residual local  
> es **menor** en el objeto real que en nulos gemelos bajo el **mismo** \(\mathcal{T}\)?

No: “¿hay un patrón bonito en alguna ventana?”  
Sí: **¿la estructura acompaña al objeto al mover la lámpara?**

---

## 2. Ficha de salida

| Campo | Valor |
| ----- | ----- |
| **Objeto** | \(G(N)\) Goldbach, \(N\) par \(\in[4,10000]\) |
| **\(R\)** | residual media |
| **\(\mathcal{G}_{\mathrm{adm}}\)** | W1–W5 rectangulares, \(L=\lfloor n/2\rfloor\), 5 posiciones |
| **Instrumento** | \(D_{1/2}\) discrepancia espectral fraccionaria (excl. DC; **no** métrica clásica) |
| **\(\Delta_{\mathrm{real}}\)** | **4.541** |
| **median \(\Delta_{\mathrm{nulo}}\) N1** | **0.316** |
| **median \(\Delta_{\mathrm{nulo}}\) N2** | **1.879** |
| **\(p_{\mathrm{N1}}\)** | **1.00** |
| **\(p_{\mathrm{N2}}\)** | **0.99** |
| **FASE 2 borde** | **NO_EJECUTADA** |
| **Interpretación** | **DESAPARECE** |

### \(\Delta\) por ventana (real)

| \(W\) | intervalo \([a,b)\) | \(\Delta^{(i)}\) |
| ----- | ------------------- | ---------------- |
| W1 | [0, 2499) | 19.402 |
| W2 | [625, 3124) | 4.541 |
| W3 | [1250, 3749) | 0.279 |
| W4 | [1875, 4374) | 3.391 |
| W5 | [2500, 4999) | 7.380 |

El real **varía más** al mover el campo de visión que los nulos (en mediana).  
Eso es lo **opuesto** de resistencia de identidad bajo este control.

---

## 3. Veredicto

| ID | Estado |
| -- | ------ |
| **H-ATH-D003-01** (resistencia diferencial de identidad) | **MUERTA** |
| **H-ATH-D003-00** (no diferencial / lámpara o régimen) | **SOPORTADA_BAJO_CONTROL** |

**Código:** `H00_NO_DIFFERENTIAL_IDENTITY_RESISTANCE`

---

## 4. Lecturas

### Permitido

- Bajo **estas** ventanas rectangulares y **esta** \(D_{1/2}\), no hay sombra de resistencia: el real no es más estable que los nulos al cambiar dominio.  
- De hecho \(\Delta_{\mathrm{real}} > \mathrm{median}\,\Delta_{\mathrm{nulo}}\) en N1 y N2: el objeto “se mueve” **más** que el nulo al recortar. Compatible con no-estacionariedad del residual Goldbach (nivel/forma cambian con \(N\)) frente a nulos más homogéneos tras permutar o reordenar bloques.  
- FASE 2 (Hann/Hamming) **correctamente no abierta**: no hay sombra que auditar por borde.  
- Un instrumento transparente (rectangular) que **no** inventa geometría por pesos: el cadáver es legible.

### Prohibido

- “No existe estructura en primos/Goldbach.”  
- “El borde rectangular mató la sombra” — no se afirmó sombra; no se abrió FASE 2.  
- Reutilizar el mismo \(D_q\) + mismas \(W\) con otro relato sin **nuevo ID**.  
- Saltar a operador o dilatación “porque debe haber resistencia”.  
- Llamar a \(D_{1/2}\) una métrica del espacio de objetos.

---

## 5. Corrección metodológica aplicada (pre-ejecución)

| Decisión | Aplicada |
| -------- | -------- |
| Ventana primaria rectangular | Sí |
| Un instrumento, cinco posiciones | Sí (\(L=n/2\), starts equiespaciados) |
| \(D_q\), \(q=1/2\), no “distancia \(L^{1/2}\)” | Sí |
| Suavizado solo en FASE 2 si hay sombra | Sí → no ejecutada |
| No fabricar instrumento perfecto antes del primer cadáver | Sí |

---

## 6. Montaña

```text
¿estructura generativa?
        ↑
¿pared al mover lámparas admisibles?  ← E003: esta no
        ↑
E002: esta P no se conserva diferencialmente
        ↑
E001: esta sombra 1/6 no
```

Siguiente ladrillo: **otro** instrumento o canal (firma modular, correlaciones largas, E003b dilatación con multi-interpolador, otro \(q\) o \(D\)) con **nuevo ID** — no catedral.

---

## 7. Lab

Era II: el instrumento rectangular mereció existir lo suficiente para **morir con claridad**.  
Huella en el kernel. Montaña intacta.  
No se suavizó para buscar señal. No se abrió auditoría de borde sin cadáver previo de resistencia.

---

# FIN — DOMAIN-E003 REPORT

*La lámpara rectangular no inventó una pared.  
Tampoco la encontró.*
