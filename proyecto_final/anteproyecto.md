# **Anteproyecto IA1 - 2025**

## **Multi-Agent / Public Goods Prisoner’s Dilemma**

**Código:** `QOOPERATE`
**Integrantes:** Emiliano Germani, Julia Kröpfl y Adriano Fabris

---

## **Objetivo**

El proyecto busca explorar el surgimiento o colapso de la cooperación en sociedades artificiales dinámicas compuestas
por agentes que aprenden mediante refuerzo, evaluando cómo la estructura social (topología de red) y el alcance de la
información local influyen en su comportamiento colectivo.

La meta principal es observar bajo qué condiciones emergen patrones estables de cooperación en entornos donde los
individuos actúan racionalmente pero con información limitada, y cómo el aprendizaje local puede conducir a resultados
globales cooperativos o egoístas.

---

## **Teoría Involucrada**

El trabajo se apoya en dos ejes conceptuales: el **aprendizaje por refuerzo** y la **teoría de juegos evolutiva**.

En el primero, cada agente aplica el algoritmo **Q-Learning**, cuya regla de actualización se expresa como:

$$
Q(s,a) \leftarrow Q(s,a) + \alpha \big(r + \gamma \max_{a'} Q(s',a') - Q(s,a)\big)
$$

donde $\alpha$ es la tasa de aprendizaje, $\gamma$ el factor de descuento, $r$ la recompensa inmediata y $(s,a)$ el par
estado-acción.
En un entorno multiagente, cada individuo percibe un _entorno no estacionario_, ya que los demás también aprenden y
adaptan su política, generando una dinámica colectiva cambiante. Por tanto, el objetivo no es la convergencia del
aprendizaje, que ya no está garantizada, sino la observación y el análisis del comportamiento adaptativo del sistema.

Desde la teoría de juegos, cada interacción se modela como un **Dilema del Prisionero iterado (IPD)**, donde ambos
agentes
eligen entre cooperar (C) o desatender (D).
La matriz de recompensas cumple $T > R > P > S$, con $T$ (tentación), $R$ (recompensa mutua), $P$ (castigo mutuo)
y $S$ (pérdida del cooperador).

Las simulaciones se realizarán sobre tres **topologías de interacción**:
una red regular (lattice bidimensional), una red aleatoria tipo Erdős–Rényi y una red de mundo pequeño (Watts–Strogatz).
Cada configuración impone diferentes grados de conectividad y clustering, lo que posiblemente afecte la propagación y
estabilidad de la cooperación.

| Propiedad  | Red regular o lattice (LA)                                                                      | Erdős–Rényi (ER)                                                                   | Watts–Strogatz (WS)                                                                            |
|------------|-------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------|
| Estructura | Altamente ordenada y regular. Cada nodo tiene el mismo número de vecinos conectados localmente. | Las aristas se colocan entre dos nodos cualesquiera con una probabilidad fija $p$. | Comienza como una red regular; luego algunas aristas se reconfiguran con probabilidad $\beta$. |

---

## **Descripción del Framework**

El entorno modelará una población de $N$ agentes, cada uno de los cuales interactúa con sus vecinos definidos por la
red. En cada ronda, cada agente juega un Dilema del Prisionero con sus contactos, elige su acción $a_t \in {C, D}$
siguiendo una política $\varepsilon$-greedy y actualiza su tabla $Q$ en base a la recompensa media obtenida.

El **estado local** $s$ estará definido por un conjunto reducido de variables:

* última acción propia,
* promedio de cooperación de los vecinos,
* recompensa promedio reciente,
* y variabilidad local de recompensas.

Estas variables se discretizarán para mantener un espacio de estados manejable.

La implementación se realizará en el lenguaje de programación Python 3, utilizando las librerías NumPy, NetworkX,
Pandas, Matplotlib y Seaborn, y eventualmente Axelrod-Python para comparar con estrategias clásicas (Tit-for-Tat,
Always Defect, etc.).

---

## **Métricas de Evaluación**

El análisis se basará en métricas que reflejen tanto la cooperación colectiva como la equidad y estabilidad del sistema:

1. Tasa global de cooperación:
   $$
   C_t = \frac{\text{número de cooperaciones en el tiempo } t}{\text{número total de interacciones en } t}
   $$

2. Promedio de recompensas por agente:
   $$
   \bar{R}*t = \frac{1}{N}\sum*{i=1}^{N} r_i(t)
   $$

3. Índice de desigualdad (Gini):
   $$
   G = \frac{\sum_i \sum_j |r_i - r_j|}{2n^2\bar{r}}
   $$

4. Estabilidad temporal (volatilidad):
   $$
   \sigma_C^2 = \text{Var}(C_t)
   $$

5. Tiempo hasta estabilización:
   $$
   |C_{t+\Delta} - C_t| < \varepsilon
   $$

---

## **Hipótesis**

### Hipótesis Fundamentales

**H1. Efecto de la estructura:** la topología de la red afecta significativamente el nivel final de cooperación. En
otras
palabras, _¿la forma en que los agentes están conectados influye en su capacidad para cooperar?_

**H2. Efecto del aprendizaje:** una tasa de aprendizaje moderada ($0.05 < \alpha < 0.3$) permite mayor estabilidad que
valores extremos. O sea, _¿se puede favorecer la convergencia hacia el equilibrio dinámico?_

**H3. Exploración controlada:** valores intermedios de $\varepsilon$ (entre 0.05 y 0.2) favorecen el equilibrio entre
exploración y cooperación sostenida. Es decir, _¿cómo impacta la cantidad de exploración en la cooperación a
largo plazo?_

### Hipótesis Alternativas

HA1. La presencia de agentes aleatorios puede prevenir el colapso total de la cooperación.

HA2. La inclusión de información extendida (vecinos de segundo orden) puede fortalecer la cooperación.

HA3. La desigualdad de recompensas aumenta con el grado medio de conectividad de la red.

---

## **Experimentos según Hipótesis**

**E0:** análisis base del entorno

- Objetivo: comprobar el correcto funcionamiento del entorno y la dinámica de aprendizaje.
- Diseño: población pequeña–mediana (por ejemplo ~10%–25% del tamaño objetivo), topología con vecinos locales (lattice).
- Parámetros iniciales en rangos razonables: $\alpha$ en rango bajo–moderado, $\varepsilon$ en rango bajo. Iteraciones
  cortas a moderadas (una fracción de la corrida final).
- Actividad: ejecutar varias corridas con distintas semillas y registrar la evolución de $C_t$ y $\bar{R}_t$.
- Resultado esperado: dinámica coherente (sin errores), aparición de fluctuaciones de cooperación propias del entorno no
  estacionario.

**E1 para H1:** Efecto de la topología sobre la cooperación

- Objetivo: contrastar la hipótesis de que la estructura de la red impacta la cooperación.
- Diseño: comparar tres familias de topologías (regular/local, aleatoria, small-world). Usar tamaños representativos (
  por
  ejemplo “pequeño / mediano / grande” relativos al hardware). Para redes aleatorias variad el parámetro de conexión en
  un
  rango (bajo → medio → alto).
- Actividad: para cada familia, ejecutar varias repeticiones y obtener métricas agregadas (promedio y dispersión
  de $C_{final}$, Gini, varianza temporal).

**E2 para H2:** Sensibilidad a la tasa de aprendizaje ($\alpha$)

- Objetivo: evaluar cómo la velocidad de aprendizaje influye en la estabilidad colectiva.
- Diseño: mantener una topología fija (p. ej. lattice o small-world) y barrer $\alpha$ sobre un rango que vaya de
  “muy
  bajo” a “alto” (por ejemplo: valores relativos como 0.01–0.5, o describir porcentualmente: 1%–50% del máximo
  práctico).
  Mantener $\varepsilon$ y $\gamma$ constantes.
- Actividad: para cada rango de $\alpha$, medir la varianza temporal de $C_t$ y el tiempo hasta que las oscilaciones se
  atenúen.

**E3 para H3:** Exploración controlada (barrido de $\varepsilon$)

- Objetivo: determinar efectos de distintos niveles de exploración sobre la cooperación.
- Diseño: elegir un rango de $\varepsilon$ que vaya desde “muy bajo” hasta “moderadamente alto” (por ejemplo 1%–30% en
  términos relativos).
- Topología: preferentemente una red con conectividad media.
- Actividad: medir estabilidad ($\sigma_C^2$), $C_{final}$ y frecuencia de cambios de política. Repetir en varios
  escenarios para ver consistencia.

| Etapa                                       | Descripción                                                                             | Duración estimada |
|---------------------------------------------|-----------------------------------------------------------------------------------------|-------------------|
| **1. Definición conceptual**                | Revisión bibliográfica, definición de recompensas, topologías y variables de estado.    | 3 días            |
| **2. Implementación del entorno**           | Creación del modelo de red, funciones de payoff e inicialización de agentes.            | 5 días            |
| **3. Implementación del agente Q-Learning** | Definición de la política ε-greedy, actualización de Q-table y estructura de episodios. | 5 días            |
| **4. Experimento 0**                        | Integración completa del entorno y logging de resultados.                               | 5 días            |
| **5. Experimentos 1, 2 y 3**                | Ajuste fino y automatización de corridas.                                               | 7 días            |
| **6. Análisis de resultados**               | Cálculo de métricas, visualización y comparación de escenarios.                         | 3 días            |
| **7. Elaboración del Reporte**              | Revisión de resultados, discusión y refutación de hipótesis                             | 2 días            |

---

## **Cronograma Tentativo**

![cronograma.png](cronograma.png)

---

## **Material de Referencia**

**Libros**
Russell, S. & Norvig, P. (2021). *Artificial Intelligence: A Modern Approach* (4ª ed.).
Axelrod, R. (1984). *The Evolution of Cooperation*. Basic Books.

**Papers**
Shoham, Y. et al. (2007). *If multi-agent learning is the answer, what is the question?* *Artificial Intelligence*.

**Videos**
Veritasium (2022). *This game theory problem will change the way you see the
world*. [YouTube](https://www.youtube.com/watch?v=mScpHTIi-kM)
Veritasium (2023). *Something Strange Happens When You Trace How Connected We
Are*. [YouTube](https://www.youtube.com/watch?v=CYlon2tvywA&t=500s)

---