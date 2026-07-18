# Hipótesis Central del Marco CED+RAP

Este documento consolida y formaliza el núcleo matemático y experimental del proyecto, aislando las hipótesis rigurosas y predicciones falsables de cualquier consideración ontológica o filosófica. Su estructura define el experimento central en ejecución dentro del laboratorio del Albañil.

---

## 1. Problema

El proyecto busca explicar el comportamiento espectral y la distribución de regularidades e irregularidades en los números primos, centrándose en tres frentes interconectados:
1. Las oscilaciones locales y asintóticas de la función contadora de primos $\pi(x)$ frente a sus tendencias de primer y segundo orden ($x/\log(x)$ y $\text{Li}_2(x)$).
2. La estructura espectral de los ceros no triviales de la función zeta de Riemann $\zeta(s)$ en la línea crítica $\text{Re}(s) = 1/2$ y su concordancia con las leyes de repulsión de niveles de matrices aleatorias (GUE).
3. La preservación de representaciones del tipo $p + q = N$ (particiones de Goldbach) como un fenómeno de estabilidad y simetría espectral.

---

## 2. Hipótesis Central

Existe un operador espectral/geométrico $H$ asociado a la estructura de los números primos cuya dinámica de conmutación no trivial determina simultáneamente la distribución asintótica de los ceros de Riemann y la emergencia de la aritmética prima.

Específicamente, se plantea que la tensión entre la paridad de los estados de distinción y el ordenamiento de factores primos puede cuantificarse mediante un conmutador experimental $[\mathbf{E}, \mathbf{O}] = i\kappa$, cuya estabilidad y límite de escala mide el acoplamiento entre la estructura multiplicativa y aditiva de los números naturales.

---

## 3. Definiciones Matemáticas

### A. Confluencia de Entidades Distintivas (CED)
Para cualquier número natural $n \ge 1$, se define el mapa de paridad algebraico en el grupo cíclico $\mathbb{Z}_2$:
$$\chi_{\text{CED}}(n) = n \pmod 2$$

Donde:
*   $\chi_{\text{CED}}(n) = 0$ define el estado de **Estabilidad ($I$)**.
*   $\chi_{\text{CED}}(n) = 1$ define el estado de **Disonancia ($D$)**.

### B. Resonancia Aritmética Primordial (RAP)
Para cualquier entero $n \ge 2$ con factorización única $n = \prod p_i^{a_i}$, se definen tres descriptores:
1.  **Potencial RAP ($\Psi$)**: la suma ponderada de sus factores primos.
    $$\Psi(n) = \sum a_i p_i$$
2.  **Integridad RAP ($\Omega$)**: el número total de factores primos con multiplicidad.
    $$\Omega(n) = \sum a_i$$
3.  **Pérdida RAP ($L$)**: la dispersión de valor acumulado respecto al valor nominal.
    $$L(n) = n - \Psi(n)$$

*Nota: Un entero $n \ge 2$ es primo si y solo si $\Psi(n) = n$ y $\Omega(n) = 1$.*

### C. Conmutador Experimental ($\kappa_W$)
Dada una ventana de enteros pares $W$ y el conjunto de particiones aditivas $P_N = \{(a, b) \mid a \le b, \; a + b = N\}$ para cada $N \in W$:
*   **Ruta 1 ($\mathbf{R}_1$)**: Proyectar los estados estables CED tras ordenar/recortar por un operador RAP ($\mathbf{O}_r$):
    $$\mathbf{R}_1(N) = \mathbf{E}(\mathbf{O}_r(P_N))$$
*   **Ruta 2 ($\mathbf{R}_2$)**: Ordenar/recortar por $\mathbf{O}_r$ tras proyectar el estado de paridad CED ($\mathbf{E}$):
    $$\mathbf{R}_2(N) = \mathbf{O}_r(\mathbf{E}(P_N))$$

La constante experimental del conmutador se define sobre la ventana $W$ usando la diferencia simétrica normalizada (distancia de Jaccard inversa):
$$\kappa_W = \frac{1}{|W|} \sum_{N \in W} \left( 1 - \frac{|\mathbf{R}_1(N) \cap \mathbf{R}_2(N)|}{|\mathbf{R}_1(N) \cup \mathbf{R}_2(N)|} \right)$$

---

## 4. Predicciones

Si la hipótesis central es correcta, se deben cumplir las siguientes propiedades bajo simulación rigurosa:

*   **P1 (Convergencia de Escala)**: Para una regla de recorte RAP estable $r$, la constante $\kappa_W$ converge asintóticamente a un valor fijo $\kappa_\infty$ al crecer el límite superior de la ventana $W$ ($W \to \infty$), en lugar de dispersarse de forma caótica.
*   **P2 (Filtro de Exclusión Equivalente)**: El censo de representaciones de Goldbach asintóticamente no se altera cuando el filtro estricto de primalidad ($\Omega(p) = \Omega(q) = 1$) es reemplazado por un filtro dinámico basado únicamente en recortar los candidatos de menor pérdida RAP ($L(n)$).
*   **P3 (Coincidencia Espectral GUE)**: Los ceros no triviales de $\zeta(1/2 + i\gamma)$ aislados rigurosamente mediante el cómputo de incrementos de argumento en contornos del plano complejo mostrarán un espaciado local cuyo histograma coincide asintóticamente con la distribución de Wigner-Dyson (GUE).

---

## 5. Cómo Refutar el Modelo

El modelo CED+RAP se considerará refutado si ocurre cualquiera de los siguientes hallazgos experimentales o formales:

1.  **Dispersión de $\kappa_W$**: Que al expandir las ventanas de análisis numérico, el conmutador $\kappa_W$ diverja de forma inestable o dependa caóticamente del tamaño de la muestra, demostrando que $[\mathbf{E}, \mathbf{O}]$ no constituye un operador bien definido.
2.  **Falsificación de Goldbach**: El hallazgo de un entero par $N$ tal que $g(N) = 0$ (cero particiones primas en el censo).
3.  **Fuga de la Línea Crítica**: El aislamiento riguroso (mediante el backend de intervalos `Arb` de Flint) de un cero de la función zeta o de la función L de Dirichlet fuera del eje central $\text{Re}(s) = 1/2$, o una discrepancia matemática entre el winding number acumulado en el contorno y el conteo de ceros trivial/no trivial esperado.
4.  **Indiferenciabilidad contra Ruido**: Que el análisis espectral (FFT) del residuo de particiones de Goldbach suavizado no presente periodicidades modulares y sea estadísticamente indistinguible de una serie sintética construida con ruido blanco o procesos de Poisson permutados de control.
