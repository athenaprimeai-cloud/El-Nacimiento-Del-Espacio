# Definiciones Matemáticas del Marco CED+RAP

Este documento detalla formalmente los objetos, funciones y operadores del sistema de manera axiomática y secuencial, libre de narrativa y de terminología filosófica.

---

## 1. Conjunto Base y Espacio de Particiones

Sea $\mathbb{N}_{\ge 2} = \{2, 3, 4, 5, \dots\}$ el conjunto de los números enteros mayores o iguales a 2.

Para cada entero par $N \in 2\mathbb{N}_{\ge 2}$ tal que $N \ge 4$, se define el **espacio de particiones aditivas de dos términos** $P_N$ como:
$$P_N = \{(p, q) \in \mathbb{N}_{\ge 2} \times \mathbb{N}_{\ge 2} \mid p \le q \text{ y } p + q = N\}$$

El conjunto potencia de $P_N$, denotado por $\mathcal{P}(P_N)$, es el dominio y codominio de los operadores de selección definidos en este marco.

---

## 2. Mapa algebraico CED (Confluencia de Entidades Distintivas)

Sea $\mathbb{Z}_2 = \{0, 1\}$ el grupo cíclico de orden 2 con la suma módulo 2. Se define el homomorfismo de grupos $\chi: \mathbb{Z} \to \mathbb{Z}_2$ mediante:
$$\chi(n) = n \pmod 2$$

Identificamos los elementos de $\mathbb{Z}_2$ con los estados:
*   $0 \equiv I$ (Estabilidad)
*   $1 \equiv D$ (Disonancia)

### A. Confluencia sobre pares de partición
Dado un par $(p, q) \in P_N$, se define su confluencia $\chi(p, q) \in \mathbb{Z}_2$ como la suma de sus componentes en $\mathbb{Z}_2$:
$$\chi(p, q) = \chi(p) + \chi(q) \pmod 2$$

*Propiedad:* Para todo par $(p, q) \in P_N$, dado que $p + q = N$ y $N$ es par:
$$p \equiv q \pmod 2 \implies \chi(p) = \chi(q) \implies \chi(p, q) = 0 \equiv I$$
Por tanto, toda partición de un número par tiene confluencia estable.

---

## 3. Descriptores Aritméticos RAP (Resonancia Aritmética Primordial)

Sea $n \in \mathbb{N}_{\ge 2}$ con factorización única en factores primos $n = \prod_{i=1}^k p_i^{a_i}$, donde $p_i$ son primos distintos y $a_i \ge 1$.

### A. Potencial Aritmético ($\Psi$)
Se define el mapa aditivo $\Psi: \mathbb{N}_{\ge 2} \to \mathbb{N}$ (equivalente a la función aritmética $sopfr(n)$):
$$\Psi(n) = \sum_{i=1}^k a_i p_i$$

### B. Grado de Integridad ($\Omega$)
Se define la función omega mayúscula $\Omega: \mathbb{N}_{\ge 2} \to \mathbb{N}$:
$$\Omega(n) = \sum_{i=1}^k a_i$$

### C. Pérdida Aritmética ($L$)
Se define la función de pérdida $L: \mathbb{N}_{\ge 2} \to \mathbb{N}_0$:
$$L(n) = n - \Psi(n)$$

*Propiedad:* Para todo $n \in \mathbb{N}_{\ge 2}$, se cumple $L(n) \ge 0$.
*Demostración:* Se deduce directamente de la desigualdad $p^a \ge a p$ para todo primo $p \ge 2$ y exponente $a \ge 1$, y la propiedad de que el producto de tales factores es mayor o igual a su suma.

### D. Criterio de Primalidad
Un número $n \in \mathbb{N}_{\ge 2}$ es primo si y solo si:
$$\Psi(n) = n \quad \text{y} \quad \Omega(n) = 1$$

---

## 4. Operadores sobre el Espacio de Particiones

Se definen operadores de selección $\mathbf{T}: \mathcal{P}(P_N) \to \mathcal{P}(P_N)$.

### A. Operador CED ($\mathbf{E}$)
Filtra un subconjunto de particiones conservando únicamente aquellas cuyos componentes son ambos de tipo disonante ($D$):
$$\mathbf{E}(S) = \{(p, q) \in S \mid \chi(p) = 1 \text{ y } \chi(q) = 1\}$$
*(Obsérvese que para $p, q \ge 3$, esto equivale a filtrar parejas de números impares).*

### B. Operador de Selección RAP ($\mathbf{O}_r$)
Sea $r \in (0, 1]$ un parámetro de proporción. Dado el conjunto de particiones $S \subseteq P_N$, se define la métrica de **pérdida de confluencia combinada** para cada par $(p, q) \in S$:
$$L_{\text{comb}}(p, q) = \Psi(p) + \Psi(q) - \Psi(p+q)$$

El operador $\mathbf{O}_r(S)$ ordena los elementos de $S$ en orden ascendente según $L_{\text{comb}}(p, q)$ y selecciona la fracción superior de tamaño $\lceil r \cdot |S| \rceil$. Si existen empates en la frontera de corte, se incluyen todos los elementos empatados.

### C. Conmutador Experimental ($\kappa_W$)
El conmutador mide el grado de no-conmutatividad de los operadores $\mathbf{E}$ y $\mathbf{O}_r$. Para un número par $N$, se calcula la distancia de Jaccard inversa:
$$d_N(\mathbf{E}, \mathbf{O}_r) = 1 - \frac{|\mathbf{E}(\mathbf{O}_r(P_N)) \cap \mathbf{O}_r(\mathbf{E}(P_N))|}{|\mathbf{E}(\mathbf{O}_r(P_N)) \cup \mathbf{O}_r(\mathbf{E}(P_N))|}$$

Para una ventana de enteros pares $W = \{N \in 2\mathbb{N} \mid A \le N \le B\}$, la constante experimental es:
$$\kappa_W = \frac{1}{|W|} \sum_{N \in W} d_N(\mathbf{E}, \mathbf{O}_r)$$

---

## 5. El Operador Conjetural $H$ y el Certificador de Winding

### A. Operador Espectral $H$ (Conjetural)
En analogía con la conjetura de Hilbert-Pólya, se conjetura la existencia de un operador lineal autoadjunto $H$ actuando sobre un espacio de Hilbert separable $\mathcal{H}$ con producto interno $\langle \cdot, \cdot \rangle$, tal que los valores propios (espectro) $\lambda_n$ de $H$ están en correspondencia biyectiva con las partes imaginarias $\gamma_n$ de los ceros no triviales de la función L de Dirichlet modulo 3, $L(1/2 + i\gamma_n, \chi_3)$.

*Estado actual:* El operador $H$ no está construido explícitamente ni representado matricialmente en este marco.

### B. Certificador Riguroso de Ceros de Riemann (Concreto)
En ausencia de una construcción explícita de $H$, el marco utiliza un certificador local basado en el principio del argumento para la función L completada $\Lambda_3(s)$:
$$\Lambda_3(s) = \left(\frac{3}{\pi}\right)^{\frac{s+1}{2}} \Gamma\left(\frac{s+1}{2}\right) L(s, \chi_3)$$

Dado un contorno rectangular $\gamma$ en el plano complejo que no interseca ningún cero de $\Lambda_3(s)$, el número de ceros $N_z$ dentro del contorno se calcula y certifica mediante la integral de contorno rigurosa evaluada usando aritmética de intervalos (biblioteca `Arb` / `python-flint`):
$$N_z = \frac{1}{2\pi i} \oint_{\gamma} \frac{\Lambda_3'(s)}{\Lambda_3(s)} \, ds$$
Esta integral se calcula descomponiendo $\gamma$ en segmentos dirigidos y evaluando la variación del argumento del vector complejo a lo largo de cada tramo de forma inclusiva y acotada.
