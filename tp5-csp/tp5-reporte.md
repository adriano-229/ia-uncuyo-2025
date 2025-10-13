# Trabajo Práctico 5: *"Constraint Satisfaction Problems"*

# - Adriano Fabris

---

# **Ejercicio 1**

**Variables:**
$S[i,j]$, con $1 \le i,j \le 9$. Puede representarse mediante una matriz de $9 \times 9$, es decir,
existen $9 \times 9 = 81$ variables en total.

**Dominios:**
$\text{Dom}(S[i,j]) = {1, \dots, 9}$, restringido a un *singleton* (valor dado) si la celda está preasignada.

**Restricciones (binarias):**
Hay 27 restricciones en total: 9 para filas, 9 para columnas y 9 para cuadrantes.

* **Fila:** $\forall i, \forall j \ne k: ; S[i,j] \ne S[i,k]$
* **Columna:** $\forall j, \forall i \ne k: ; S[i,j] \ne S[k,j]$
* **Cuadrante:** $\forall (i,j),(k,t), (i,j)\ne(k,t)$, si
  $\lfloor (i-1)/3 \rfloor = \lfloor (k-1)/3 \rfloor$
  y
  $\lfloor (j-1)/3 \rfloor = \lfloor (t-1)/3 \rfloor$,
  entonces $S[i,j] \ne S[k,t]$.

---

# **Ejercicio 2**

<img src="images/ex2_arcs.png" title="" alt="ex2\_arcs.png" data-align="center">

---

# **Ejercicio 3 — Complejidad de AC-3**

## **Algoritmos**

```python
# Enforces consistency of A -> B, i.e., removes inconsistent values from A's domain if necessary
def enforce_arc_consistency(A, B):
    # A, B: variables of the CSP
    # Output: boolean denoting whether we updated domain of A
    removed = False
    for each a in domain[A]:
        if no value b in domain[B] allows (a, b) to satisfy the constrain between A and B:
            delete
            a
            from domain
            [A]
            removed = True
    return removed


def AC3(csp):
    # csp: a CSP with variables X1, X2, ..., Xn
    # Output: the same CSP, but with potentially reduced domains
    queue = [(Xi, Xj) for all combinations
    of
    i, j in csp(i.e., all
    arcs in csp)]
    while queue not empty:
        (Xi, Xj) = queue.remove()
        removed = enforce_arc_consistency(Xi, Xj)
        if removed:
            for Xk in neighbors[Xi]:
                queue.add((Xk, Xi))
    return csp
```

---

## **Caso 1: Grafo sin restricciones**

Sea $n$ el número de variables y $d$ el tamaño máximo del dominio.

* El número máximo de valores totales en todos los dominios es $n \cdot d$.
  Cada valor puede eliminarse **a lo sumo una vez**, por lo que el número total de eliminaciones está acotado por

  $$O(n \cdot d)$$

* Cada eliminación de un valor en una variable $X_i$ puede forzar a volver a encolar todos los arcos entrantes a $X_i$.
  En el peor caso, el grado de $X_i$ es $O(n)$, por lo que tras cada eliminación se añaden hasta:

  $$O(n)$$

  arcos.

* Así, el número total de veces que se añaden arcos a la cola está acotado por:

  $$O(n \cdot d) \cdot O(n) = O(n^2 d)$$

* Revisar un arco $(X_i, X_j)$ cuesta a lo sumo $O(d^2)$ (para cada valor en $D(X_i)$ se comprueban valores
  en $D(X_j)$).

* Por tanto, la complejidad total en el peor caso es:

  $$O(n^2 d) \cdot O(d^2) = O(n^2 d^3)$$

---

## **Caso 2: grafo de tipo árbol**

* Un árbol con $n$ nodos tiene exactamente $n - 1$ aristas, por tanto el número de arcos dirigidos es:

  $$e = 2(n - 1) = O(n)$$

* En un árbol no hay ciclos que provoquen reencolados en cadena, por lo que cada arco se revisa un número acotado de
  veces.

* Manteniendo el coste por revisión $O(d^2)$, la complejidad total en el caso de árbol queda:

  $$O(n \cdot d^2)$$

---

# **Ejercicio 4 — Problema de las N-Reinas como CSP**

## **Formulación del CSP**

* **Variables:**
  $X_i$ representa la columna en la que se coloca la reina de la fila $i$, con $i \in {1, 2, ..., N}$.

* **Dominios:**
  $D(X_i) = {1, 2, ..., N}$ (todas las columnas posibles).

* **Restricciones:**
  Para todo par $i \ne j$:

    1. $X_i \ne X_j$(no pueden compartir columna).
    2. $|X_i - X_j| \ne |i - j|$(no pueden compartir diagonal).

---

## **a) Solución con Backtracking**

Explorar el espacio de búsqueda fila por fila. En cada paso se coloca una reina en una columna posible y se verifica
consistencia con las reinas ya ubicadas.

```python
def backtracking_n_queens(N):
    soluciones = []

    def es_valida(asignacion, fila, col):
        for f_anterior in range(fila):
            c_anterior = asignacion[f_anterior]
            if c_anterior == col or abs(c_anterior - col) == abs(f_anterior - fila):
                return False
        return True

    def resolver(asignacion, fila):
        if fila == N:
            soluciones.append(asignacion.copy())
            return True
        for col in range(N):
            if es_valida(asignacion, fila, col):
                asignacion[fila] = col
                resolver(asignacion, fila + 1)
        return False

    resolver([-1] * N, 0)
    return soluciones
```

**Complejidad (peor caso):**
El backtracking puro es factorial, $O(N^N)$, ya que por cada movimiento se pueden hacer todos los demás movimientos
posibles.

---

## **b) Solución con Forward Checking**

Tras cada asignación, se eliminan de los dominios de las variables no asignadas aquellos valores inconsistentes (misma
columna o diagonal). Esto reduce el espacio de búsqueda al detectar inconsistencias de forma temprana.

```python
def forward_checking_n_queens(N):
    soluciones = []
    nodos = 0

    def fc(asignacion, dominios, fila):
        nonlocal nodos
        if fila == N:
            soluciones.append(asignacion.copy())
            return True
        for col in dominios[fila]:
            nodos += 1
            asignacion[fila] = col
            nuevos_dominios = [d.copy() for d in dominios]
            for f in range(fila + 1, N):
                if col in nuevos_dominios[f]:
                    nuevos_dominios[f].remove(col)
                diag1 = col + (f - fila)
                diag2 = col - (f - fila)
                nuevos_dominios[f] = [c for c in nuevos_dominios[f] if c not in (diag1, diag2)]
                if not nuevos_dominios[f]:
                    break
            else:
                fc(asignacion, nuevos_dominios, fila + 1)
        return False

    dominios_iniciales = [list(range(N)) for _ in range(N)]
    fc([-1] * N, dominios_iniciales, 0)
    return soluciones, nodos
```

**Complejidad:**
En el peor caso sigue siendo factorial, pero en la práctica el número de nodos explorados y el tiempo se reducen
considerablemente.

---

# **Ejercicio 5 — Análisis experimental**

## **Resultados y visualización**

Se ejecutaron ambos algoritmos (**Backtracking** y **Forward Checking**) 30 veces por tamaño de
problema ($N = 4, 8, 10$), midiendo tiempo de ejecución y cantidad de nodos explorados.
Los resultados se registraron en `tp5-Nreinas.csv` y se representaron mediante *boxplots*:

* `images/boxplot_tiempo_N.png`: distribución de tiempos por algoritmo.
* `images/boxplot_nodos_N.png`: distribución del número de nodos explorados.

---

## **Interpretación de los gráficos**

### **1. Para $N=4$**

![boxplot_nodos_4.png](images/boxplot_nodos_4.png)
![boxplot_tiempo_4.png](images/boxplot_tiempo_4.png)

* Ambos algoritmos encuentran soluciones en todos los intentos (100 % de éxito).
* Los tiempos y nodos son prácticamente idénticos: el problema es tan pequeño que el *overhead* del *forward checking*
  no se amortiza.
* Las cajas en ambos boxplots son muy estrechas, indicando baja varianza.

**Conclusión parcial:** para instancias pequeñas, la poda adicional no aporta ventaja significativa.

---

### **2. Para $N=8$**

![boxplot_nodos_8.png](images/boxplot_nodos_8.png)
![boxplot_tiempo_8.png](images/boxplot_tiempo_8.png)

* El *forward checking* explora **menos nodos** en promedio y presenta una **menor dispersión**.
* El tiempo de ejecución promedio disminuye considerablemente respecto al *backtracking* puro.
* El *boxplot* de nodos muestra una reducción consistente: el *forward checking* concentra sus valores en torno a una
  mediana mucho menor.

**Conclusión parcial:** el *forward checking* comienza a mostrar su efecto de poda; el coste adicional de mantenimiento
de dominios se compensa sobradamente por la reducción del árbol de búsqueda.

---

### **3. Para $N=10$**

![boxplot_nodos_10.png](images/boxplot_nodos_10.png)
![boxplot_tiempo_10.png](images/boxplot_tiempo_10.png)

La tendencia se acentúa.

* El *backtracking* presenta un crecimiento abrupto del número de nodos y tiempos, con alta dispersión entre
  ejecuciones (dependencia de la semilla).
* El *forward checking* mantiene tiempos y nodos más estables, con una mediana significativamente más baja.
* Los *outliers* del *backtracking* son notables, reflejando ejecuciones donde el algoritmo se atasca explorando ramas
  profundas sin poda efectiva.

**Conclusión parcial:** la ganancia del *forward checking* es clara y sostenida conforme aumenta $N$.

---

## **Conclusión final**

El crecimiento del tiempo y los nodos del *backtracking* es aproximadamente factorial en $N$, mientras que el
*forward checking* presenta un crecimiento más suave (aunque sigue siendo exponencial en el peor caso).
El *forward checking* reduce drásticamente la cantidad de nodos explorados al eliminar inconsistencias tempranas,
mejorando tanto el promedio como la estabilidad de los resultados.

---