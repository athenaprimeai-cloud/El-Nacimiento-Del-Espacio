# Modelo de Juguete CED+RAP (Caso $N=8$)

Este documento presenta la construcción del objeto matemático más pequeño posible donde la no-conmutatividad de los operadores de selección CED y RAP es demostrable de forma exacta.

---

## 1. El Espacio de Partición para $N=8$

Sea $N = 8$. El espacio de particiones aditivas $P_8$ contiene exactamente tres elementos:
$$P_8 = \{ (2, 6), \; (3, 5), \; (4, 4) \}$$

---

## 2. Definición Local de los Operadores

### A. Operador CED ($\mathbf{E}$)
El operador $\mathbf{E}$ filtra las parejas cuyos componentes individuales tienen paridad disonante ($D \equiv 1 \pmod 2$):
*   Para $(2, 6)$: $\chi(2) = 0$ (estable), $\chi(6) = 0$ (estable). Pareja descartada.
*   Para $(3, 5)$: $\chi(3) = 1$ (disonante), $\chi(5) = 1$ (disonante). Pareja conservada.
*   Para $(4, 4)$: $\chi(4) = 0$ (estable), $\chi(4) = 0$ (estable). Pareja descartada.

Por tanto, al actuar sobre cualquier subconjunto $S \subseteq P_8$:
$$\mathbf{E}(S) = S \cap \{ (3, 5) \}$$

### B. Operador de Selección RAP ($\mathbf{O}_r$ para $r = 1/3$)
Calculamos la pérdida combinada $L_{\text{comb}}(p, q) = \Psi(p) + \Psi(q) - \Psi(p+q)$ para cada par de $P_8$:
1.  **Para $(2, 6)$**:
    *   $\Psi(2) = 2$
    *   $\Psi(6) = 2 + 3 = 5$
    *   $\Psi(8) = 2 + 2 + 2 = 6$
    *   $L_{\text{comb}}(2, 6) = 2 + 5 - 6 = \mathbf{1}$
2.  **Para $(3, 5)$**:
    *   $\Psi(3) = 3$
    *   $\Psi(5) = 5$
    *   $\Psi(8) = 6$
    *   $L_{\text{comb}}(3, 5) = 3 + 5 - 6 = \mathbf{2}$
3.  **Para $(4, 4)$**:
    *   $\Psi(4) = 2 + 2 = 4$
    *   $\Psi(4) = 4$
    *   $\Psi(8) = 6$
    *   $L_{\text{comb}}(4, 4) = 4 + 4 - 6 = \mathbf{2}$

Fijamos el parámetro de proporción $r = 1/3$. Para cualquier conjunto $S \subseteq P_8$, el operador $\mathbf{O}_{1/3}(S)$ ordena sus elementos de menor a mayor pérdida combinada y selecciona los primeros $\lceil 1/3 \cdot |S| \rceil$ elementos.

---

## 3. Demostración de No-Conmutatividad

Evaluamos las dos rutas posibles de aplicación de operadores sobre el conjunto completo $P_8$:

### Ruta A: RAP primero, luego CED
1.  Aplicamos primero el filtro RAP $\mathbf{O}_{1/3}$ sobre el conjunto completo $P_8$ ($|P_8| = 3$):
    *   Número de elementos a seleccionar: $\lceil 1/3 \cdot 3 \rceil = 1$.
    *   El elemento con menor pérdida es $(2, 6)$ con pérdida $1$ (los otros tienen pérdida $2$).
    *   Por lo tanto:
        $$\mathbf{O}_{1/3}(P_8) = \{ (2, 6) \}$$
2.  Aplicamos el filtro CED $\mathbf{E}$ sobre el resultado:
    $$\mathbf{E}(\mathbf{O}_{1/3}(P_8)) = \mathbf{E}(\{ (2, 6) \}) = \emptyset$$

### Ruta B: CED primero, luego RAP
1.  Aplicamos primero el filtro CED $\mathbf{E}$ sobre el conjunto completo $P_8$:
    $$\mathbf{E}(P_8) = \{ (3, 5) \}$$
2.  Aplicamos el filtro RAP $\mathbf{O}_{1/3}$ sobre el resultado ($S = \{ (3, 5) \}$, $|S| = 1$):
    *   Número de elementos a seleccionar: $\lceil 1/3 \cdot 1 \rceil = 1$.
    *   Dado que solo hay un elemento disponible, se conserva:
        $$\mathbf{O}_{1/3}(\mathbf{E}(P_8)) = \mathbf{O}_{1/3}(\{ (3, 5) \}) = \{ (3, 5) \}$$

---

## Conclusion y Medida del Conmutador

Dado que:
$$\mathbf{E}(\mathbf{O}_{1/3}(P_8)) = \emptyset \quad \neq \quad \mathbf{O}_{1/3}(\mathbf{E}(P_8)) = \{ (3, 5) \}$$

Los operadores **no conmutan** sobre $P_8$. La distancia de Jaccard inversa (medida del conmutador $d_8$) es:
$$d_8(\mathbf{E}, \mathbf{O}_{1/3}) = 1 - \frac{|\emptyset \cap \{ (3, 5) \}|}{|\emptyset \cup \{ (3, 5) \}|} = 1 - \frac{0}{1} = \mathbf{1}$$

Este modelo demuestra que en la escala elemental $N=8$, la información de paridad (CED) e integridad de factores (RAP) interfiere de forma destructiva o constructiva dependiendo puramente del orden de su evaluación.
