# Resultados Computacionales del Marco CED+RAP

Este documento detalla rigurosamente las observaciones y validaciones numéricas obtenidas mediante simulación en el laboratorio, estableciendo una separación estricta entre el comportamiento observado en ventanas finitas y las afirmaciones con demostración matemática general.

---

## 1. Observaciones Computacionales (Ventanas Finitas)

Las siguientes afirmaciones describen comportamientos empíricos medidos en el software del laboratorio, válidos estrictamente dentro de los rangos numéricos especificados:

### A. Calibración Cesàro de Orden 2 (Canal $C_{03}$ / Riemann Zeta)
En el experimento **G5B-005** ([Experimento 005A](file:///c:/Users/johnn/Documents/El%20Nacimiento%20del%20Espacio/docs/experimentos/experimento-005a-calibracion-cesaro.md)), sobre la ventana logarítmica de muestreo $1\,000 \le X \le 1\,000\,000$:
*   **Aproximación por Ceros Lineales ($M1$)**: Al incluir las contribuciones lineales de los primeros 49 ceros positivos de la función zeta de Riemann (hasta altura $T = 143.11$), el error cuadrático medio (RMSE) de la estimación del promedio de Cesàro disminuyó en un **$99.82\%$** en comparación con el modelo base $M0$ (que solo considera el polo principal en $X^2/24$ y el término de corrección constante de Brüdern-Kaczorowski-Perelli).
*   **Aproximación por Suma Doble ($M2$)**: Al incorporar la suma doble cruzada sobre parejas de ceros no triviales ($\rho_1, \rho_2$), el RMSE del modelo $M1$ se redujo en un **$54.15\%$** adicional en el intervalo de validación.
*   **Error de Precisión**: El error absoluto máximo entre la convolución evaluada vía FFT y las sumas directas de control en puntos seleccionados se acotó en $3.73 \times 10^{-9}$.

### B. Comportamiento de Exclusión Combinada RAP
En simulaciones preliminares sobre ventanas pequeñas ($N \le 100\,000$):
*   Se observó que la ordenación de las particiones $P_N$ mediante la pérdida combinada $L_{\text{comb}}(p, q) = \Psi(p) + \Psi(q) - \Psi(p+q)$ tiende a concentrar las parejas formadas por primos cerca de la frontera de menor pérdida.
*   No obstante, el porcentaje de coincidencia exacta entre la ruta CED-primero y RAP-primero varía sensiblemente según el umbral $r$ del filtro, lo que confirma la no-conmutatividad del par de operadores.

---

## 2. Demostraciones Matemáticas (Resultados Formales Generales)

Las siguientes afirmaciones son las únicas que cuentan con validez matemática general demostrada dentro del marco del proyecto (incluidas en la suite de pruebas unitarias como invariantes estructurales):

*   **Identidad de Primalidad RAP**: Para todo $n \in \mathbb{N}_{\ge 2}$, la condición $\Psi(n) = n$ y $\Omega(n) = 1$ es equivalente a la primalidad de $n$.
*   **Acotación Inferior de la Pérdida**: Para todo $n \in \mathbb{N}_{\ge 2}$, se cumple formalmente que $L(n) \ge 0$, con igualdad si y solo si $n$ es primo o $n = 4$.
*   **Garantía de Confluencia Estable**: Para cualquier número par $N$, la confluencia de CED de cualquier partición $(p, q) \in P_N$ es estrictamente estable ($\chi(p, q) = 0 \equiv I$).
*   **Integridad de Tipos de Evidencia**: El sistema de software garantiza, mediante contratos estáticos de TDD, que cualquier objeto que declare contener evidencia probatoria conserva de manera inmutable e infalsificable su procedencia (hashes de código, backend y autorización de origen), impidiendo la mezcla de datos reales y sintéticos en el pipeline de ejecución.

---

## 3. Estado de Pruebas y Resultados Nuevos
*   **Resultados matemáticos nuevos:** A la fecha, el marco **no ha producido ninguna demostración matemática nueva** sobre la Conjetura de Goldbach o la Hipótesis de Riemann. Las ecuaciones utilizadas son traducciones operacionales de teoremas analíticos clásicos preexistentes.
*   **Puerta de entrada L3:** El backend real matemático para calcular el winding number sobre la función completada $\Lambda_3(s)$ mediante FLINT se encuentra implementado pero bloqueado de manera inerte (`fake-only`). No se ha realizado ninguna búsqueda de ceros reales en este repositorio fuera de las tablas de datos conocidas provistas por Andrew Odlyzko.
