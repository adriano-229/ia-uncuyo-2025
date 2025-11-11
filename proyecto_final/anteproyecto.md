# **Anteproyecto IA1 - 2025**

## **Multi-Agent / Public Goods Prisoner’s Dilemma**

**Código**: `QOOPERATE`

**Integrantes:** Emiliano Germani, Julia Kröpfl y Adriano Fabris

---

## **Objetivo**

El presente trabajo busca explorar el surgimiento o colapso de la cooperación en sociedades artificiales dinámicas
compuestas por agentes que aprenden mediante refuerzo, evaluando cómo la estructura social (topología de red) y el
alcance de la información local influyen en su comportamiento colectivo.

---

## **Teoría Involucrada**

El desarrollo se apoya en dos ejes teóricos principales: el aprendizaje por refuerzo y la teoría de juegos evolutiva.

En primer lugar, los agentes utilizan el algoritmo de **Q-Learning**, cuya actualización se define como:

$$
Q(s,a) \leftarrow Q(s,a) + \alpha \big(r + \gamma \max_{a'} Q(s',a') - Q(s,a)\big)
$$

donde $\alpha$ representa la tasa de aprendizaje, $\gamma$ el factor de descuento, $r$ la recompensa inmediata y $(s,a)$
el par estado-acción. En entornos multiagente esta formulación se aplica de manera independiente, asumiendo que cada
agente percibe un entorno parcialmente observable y no estacionario, dado que los demás agentes también aprenden y
modifican su conducta. En consecuencia, no se garantiza la convergencia del aprendizaje, sino que se estudia su
comportamiento adaptativo dentro de un equilibrio dinámico.

Desde la perspectiva de la teoría de juegos, cada interacción entre dos agentes se modela mediante el **Dilema del
Prisionero**, donde ambos pueden elegir entre cooperar (C) o defectar (D). La matriz de recompensas cumple la
relación $T > R > P > S$, siendo $T$ la tentación (defectar cuando el otro coopera), $R$ la recompensa mutua por
cooperación, $P$ el castigo mutuo por defection y $S$ la pérdida del cooperador cuando el otro defecta. Esta relación
hace que la elección individual racional conduzca a un resultado colectivo subóptimo.

Los agentes estarán distribuidos en distintas **topologías de interacción**, que limitarán con quiénes pueden jugar y
observar. Se evaluarán tres configuraciones representativas: una red regular bidimensional (lattice), una red aleatoria
tipo Erdős–Rényi y una red de mundo pequeño (Watts–Strogatz). Cada una presenta un grado diferente de conectividad y
redundancia, lo que influye en la propagación del comportamiento cooperativo.

---

## **Descripción del Framework**

El proyecto se enmarca en el estudio de sistemas multiagente y teoría de juegos, con énfasis en el Dilema del Prisionero
Iterado (IPD) y sus extensiones al ámbito público (Public Goods Game). Se pretende analizar, mediante simulación y
aprendizaje autónomo, en qué condiciones los agentes tienden a cooperar o actuar de manera egoísta, y cómo dichas
tendencias se ven afectadas por la conectividad, la información disponible y los parámetros del aprendizaje.

El entorno simulará una sociedad de $N$ agentes interconectados. En cada ronda, cada agente juega un Dilema del
Prisionero con sus vecinos definidos por la topología de red. Cada uno de ellos aplica el algoritmo Q-Learning de forma
independiente, seleccionando una acción $a_t \in {C, D}$ según una política ε-greedy y actualizando su Q-table con base
en la recompensa media obtenida por las interacciones locales.

El estado local $s$ que percibe cada agente estará compuesto por un conjunto acotado de variables: la última acción
propia, el promedio de cooperación de los vecinos recientes, la recompensa media acumulada en una ventana temporal corta
y la varianza local de recompensas, que actúa como un indicador de estabilidad del entorno. Estas variables podrán
discretizarse para mantener un tamaño razonable de la tabla Q, ajustándose según los recursos disponibles y los tiempos
de simulación.

El entorno es inherentemente **no estacionario**, ya que la dinámica general surge del aprendizaje simultáneo de los
agentes. Las distribuciones de estados y recompensas cambian a lo largo del tiempo, por lo que el objetivo no es
alcanzar una convergencia fija, sino observar si emerge un equilibrio dinámico y sostenible entre cooperación y
defection.

La implementación se realizará en Python 3, utilizando las librerías NumPy (operaciones numéricas), NetworkX (generación
y gestión de redes), Pandas (análisis de datos), Matplotlib y Seaborn (visualización de resultados), y opcionalmente
Axelrod-Python, que permitirá comparar los resultados obtenidos con estrategias clásicas.

---

## **Métricas de Evaluación**

El análisis se basará en un conjunto de métricas que permiten describir la dinámica global y local del sistema:

La **tasa de cooperación global** se define como la proporción de acciones cooperativas en relación con el total de
interacciones por ronda:

$$
C_t = \frac{\text{número de cooperaciones en el tiempo } t}{\text{número total de interacciones en } t}
$$

y describe el nivel medio de cooperación en la población.

El **promedio de recompensas por agente** mide la eficiencia colectiva del sistema:

$$
\bar{R}*t = \frac{1}{N}\sum*{i=1}^{N} r_i(t)
$$

donde $r_i(t)$ representa la recompensa del agente $i$ en la ronda $t$.

La **desigualdad de recompensas** se estimará mediante el índice de Gini:

$$
G = \frac{\sum_i \sum_j |r_i - r_j|}{2n^2\bar{r}}
$$

siendo $\bar{r}$ el promedio de recompensas de la población y $n$ el número total de agentes.

La **estabilidad temporal** o volatilidad del sistema se calculará como la varianza de la tasa de cooperación:

$$
\sigma_C^2 = \text{Var}(C_t)
$$

Una baja varianza indica un comportamiento social estable, mientras que valores altos reflejan adaptaciones constantes o
fluctuaciones caóticas.

Por último, se medirá el **tiempo hasta estabilización**, definido como el número de iteraciones necesarias para que

$$
|C_{t+\Delta} - C_t| < \varepsilon
$$

durante un intervalo temporal $\Delta$. Esta métrica permite identificar cuándo el sistema alcanza un estado de
equilibrio o pseudo-convergencia.

---

## **Hipótesis a Evaluar**

1. La estructura de la red influye significativamente en el nivel final de cooperación alcanzado por la población.
2. La inclusión de información extendida (por ejemplo, sobre vecinos de segundo orden) favorece la cooperación
   sostenida.
3. Una tasa de aprendizaje baja ($\alpha$ pequeña) mejora la estabilidad de la cooperación frente a un entorno
   cambiante.
4. La presencia de agentes con comportamiento aleatorio puede evitar el colapso total de la cooperación.
5. El grado medio de la red afecta la desigualdad de recompensas en el sistema.
6. Los parámetros de exploración ($\varepsilon$) determinan si el sistema converge hacia patrones estables o cíclicos de
   cooperación.

---

## **Cronograma Tentativo**

![cronograma.png](cronograma.png)

---

## **Material de Referencia**

**Libros**

- Russell, S. & Norvig, P. (2021). *Artificial Intelligence: A Modern Approach* (4ª ed.).
- Axelrod, R. (1984). *The Evolution of Cooperation*. Basic Books.

**Papers**

- Shoham, Y. et al. (2007). *If multi-agent learning is the answer, what is the question?* *Artificial Intelligence*.

**Videos**

- Veritasium (2022). *This game theory problem will change the way you see the
  world*. [YouTube](https://www.youtube.com/watch?v=mScpHTIi-kM)
- Veritasium (2023). *Something Strange Happens When You Trace How Connected We
  Are*. [YouTube](https://www.youtube.com/watch?v=CYlon2tvywA&t=500s)

---
