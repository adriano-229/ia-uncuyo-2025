# TP3 — Informe comparativo de algoritmos de búsqueda

## 1. Contexto del problema

El entorno evaluado corresponde a variantes del FrozenLake de tamaño 100×100, con dos escenarios de costo:

1. Escenario 1: todas las acciones cuestan 1.
2. Escenario 2: los movimientos izquierda/derecha cuestan 1, mientras que arriba/abajo cuestan 10.

Se ejecutaron los algoritmos Random, BFS, DFS, DLS (con límites 300, 400 y 500), UCS y A\* sobre distintos entornos aleatorios (`env_n`). Las métricas registradas fueron: número de estados explorados (`states_n`), número de pasos de la solución (`actions_count`), costo acumulado (`actions_cost`), tiempo de ejecución (`time`) y un indicador de si se encontró solución (`solution_found`).

---

## 2. Figuras

* `[actions_cost_boxplot.png]`: distribución del costo de las soluciones.
* `[actions_count_boxplot.png]`: distribución de la cantidad de pasos.
* `[states_n_boxplot.png]`: distribución de estados explorados.
* `[time_boxplot.png]`: distribución de los tiempos de ejecución.

---

## 3. Resultados observados

El algoritmo Random nunca logró encontrar una solución válida, por lo que se descarta de inmediato.

BFS, UCS y A\* resolvieron siempre el problema en ambos escenarios. En el primero, donde todos los costos son iguales, los tres encontraron la misma solución de 198 pasos con costo 198. En el segundo, también coincidieron con una solución de 198 pasos y costo 1089. La diferencia se observa en el esfuerzo de búsqueda y el tiempo: BFS y UCS expandieron prácticamente todo el espacio (alrededor de 9998 estados), mientras que A\* exploró algo menos, en torno al 10% menos de estados, pero con un tiempo de ejecución que duplicó al de BFS. UCS se comportó de forma muy similar a BFS, aunque ligeramente más lento por el uso de estructuras de prioridad.

DFS, en cambio, siempre encontró una solución, pero de baja calidad: caminos mucho más largos, entre 400 y 1800 pasos en el escenario 1, y costos de hasta 13.000 en el escenario 2. DLS mostró un desempeño muy dependiente del límite: con 300 nunca encontró solución, con 400 y 500 sí, pero en general los caminos resultaron más largos y costosos que los de BFS, UCS o A\*.

---

## 4. Conclusión

El análisis muestra que los algoritmos que siempre encuentran soluciones óptimas son BFS, UCS y A\*. BFS se destaca por su rapidez y simplicidad: alrededor de 0.036–0.04 segundos por ejecución, con soluciones siempre óptimas. UCS expande prácticamente la misma cantidad de estados, pero tarda algo más (0.045–0.05 segundos). A\* reduce el número de estados explorados en aproximadamente un 10%, pero esta ganancia viene acompañada de un tiempo de ejecución dos veces mayor (0.08–0.12 segundos).

Para el problema planteado en este trabajo práctico, con escenarios de tamaño moderado, el algoritmo más adecuado es **BFS**. Ofrece un equilibrio ideal entre velocidad y calidad de las soluciones, sin necesidad de incurrir en la sobrecarga heurística de A\*. No obstante, A\* resulta especialmente prometedor para problemas de mayor escala, donde el ahorro en la exploración podría crecer significativamente y compensar con creces su mayor tiempo de cálculo. UCS queda como una opción intermedia: válido en entornos con costos arbitrarios, pero sin ventajas claras frente a BFS en este dominio concreto.

En síntesis, BFS es el mejor algoritmo para el problema planteado, aunque A\* debe considerarse la mejor alternativa cuando se apunta a escenarios más complejos y sobre todo, de mayor tamaño.

---
