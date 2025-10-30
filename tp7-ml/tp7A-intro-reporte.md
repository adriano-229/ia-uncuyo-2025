# Universidad Nacional de Cuyo

**Facultad de Ingeniería – Licenciatura en Ciencias de la Computación**  

## Trabajo Práctico 7A – Introducción al Aprendizaje Automático

**Materia:** Inteligencia Artificial I  
**Autor:** Adriano Fabris  
**Año:** 2025  

---

### Ejercicio 1

**Según el caso, ¿qué se comportaría mejor, un método flexible o uno inflexible? Justifique.**

Para responder a este ejercicio me valgo de los conceptos expuestos en la primera clasificación de los enfoques de aprendizaje estadístico que hace el autor: los *parametrizados* y los *no parametrizados*.

**a) n grande, p pequeño**  
Un enfoque más flexible sería más adecuado, ya que se contrarresta la poca “disponibilidad” de comprensión de las observaciones a partir de los predictores. 

En otras palabras, puede (no siempre) ser difícil comprender un fenómeno con pocas variables explicativas, por más ejemplos que se tengan.  
Según el autor:  

> “But non-parametric approaches do suffer from a major disadvantage: since they do not reduce the problem of estimating f to a small number of parameters, a very large number of observations (far more than is typically needed for a parametric approach) is required in order to obtain an accurate estimate for f.”  

En la sección estudiada, un enfoque no paramétrico se asume más flexible que uno paramétrico.

**b) n pequeño, p grande**  
En contraposición al caso anterior, un enfoque menos flexible —posiblemente paramétrico— se comportaría mejor, ya que asume un comportamiento predeterminado entre los predictores y la respuesta, disminuyendo la complejidad del problema desde el principio. Esto suele ser adecuado cuando la cantidad de predictores es alta en comparación con $n$.

**c) La relación entre X e Y es altamente no lineal**  
El autor menciona que no existe “el método universal” (*no free lunch*), sino que depende, entre otros factores, de la naturaleza del problema y del objetivo (predecir o inferir).  
Para ejemplificar, se cita la predicción del valor de una acción, donde un enfoque flexible —una función que se adapte mucho a los valores observados— parece intuitivamente adecuado, sin embargo en la práctica no siempre es así: en ciertos casos, un método con cierta inflexibilidad resulta más estable y generalizable para la predicción.

**d) La varianza de los términos de error es alta**  
Cuando existe un error irreducible considerable, la cota de precisión será baja y condicionará la calidad de las respuestas $Y$. Esto sugiere que un enfoque flexible —al intentar modelar el ruido— no sería conveniente. En este caso, un método más inflexible no alteraría significativamente el error existente y, por lo tanto, sería más apropiado.

---

### Ejercicio 2

**Distinguir los siguientes problemas según si son de clasificación o regresión, de inferencia o predicción. Identificar n y p.**

“Clasificación” y “regresión” describen el tipo de salida que el modelo produce (clase o valor continuo).  
“Inferencia” y “predicción” describen el propósito con el que se utiliza el modelo.

**a)** Regresión – Inferencia – \(n = 500, p = 4\)  
**b)** Clasificación – Predicción – \(n = 20, p = 14\)  
**c)** Regresión – Predicción – \(n = 52\) (número de semanas en un año), \(p = 4\)

---

### Ejercicio 3

**Ventajas y desventajas de aplicar un método flexible (frente a uno inflexible).**

Cuando el interés principal es la **inferencia**, los modelos restrictivos son más fáciles de interpretar —como en una regresión lineal, donde se puede entender la relación entre $X$ e $Y$. En cambio, si el enfoque es muy flexible, las estimaciones y la interpretación se vuelven más complejas.

En **predicción**, puede parecer intuitivo que el método más flexible sea el que mejor estime, pero no siempre es así. Surge aquí el concepto de overfitting, entendido como una adaptación excesiva a los datos de entrenamiento, incluyendo el ruido, lo que reduce la confiabilidad del modelo.

---

### Ejercicio 4

**Diferencias entre un enfoque paramétrico y uno no paramétrico.**

Un enfoque **paramétrico** reduce el problema de estimar $f$ a la estimación de un conjunto de parámetros, asumiendo una forma funcional determinada. En general, a menor número de parámetros, menor flexibilidad y menor riesgo de sobreajuste (*overfitting*).  

Por el contrario, un enfoque **no paramétrico** no asume una forma particular para $f$, buscando que la función se ajuste a las observaciones con cierta suavidad (*smoothness*). Este tipo de enfoque puede captar relaciones más complejas, pero a costa de mayor varianza y riesgo de sobreajuste.

En resumen:

- Los **métodos paramétricos** son más interpretables y estables con pocos datos.  
- Los **no paramétricos** son más flexibles y adecuados para capturar relaciones no lineales, aunque requieren muchas observaciones para generalizar correctamente.

---

### Ejercicio 5

**Método de los K vecinos más cercanos (KNN).**

#### a) Distancia euclidiana del punto $P(0,0,0)$ respecto de las observaciones

| Obs | Clase Obs | Distancia |
| --- | --------- | --------- |
| 1   | Rojo      | 3.00      |
| 2   | Rojo      | 2.00      |
| 3   | Rojo      | 3.16      |
| 4   | Verde     | 2.24      |
| 5   | Verde     | 1.41      |
| 6   | Rojo      | 1.73      |

#### b) \(K = 1\)

El punto 5 (verde) es el más cercano, con distancia 1.41.  
**Predicción:** Verde.

#### c) \(K = 3\) con distancia ponderada

Se utiliza la función de decaimiento $w_i = 1/d_i$ para ponderar la votación según la cercanía.

| Obs | Clase | Distancia | Peso |
| --- | ----- | --------- | ---- |
| 5   | Verde | 1.41      | 0.71 |
| 6   | Rojo  | 1.73      | 0.58 |
| 2   | Rojo  | 2.00      | 0.50 |

Suma ponderada (Rojo): 1.08  
Suma ponderada (Verde): 0.71  

**Predicción:** Rojo.

*Nota:* si se usara una función de decaimiento más pronunciada, como $w_i = (1/d_i)^3$, la observación más cercana tendría aún más influencia, y el punto $P$ podría clasificarse como **Verde**.

#### d) Relación entre K y la forma del límite de decisión

Si el límite de decisión es **altamente no lineal**, conviene usar un **K pequeño**, ya que las observaciones más cercanas aportan información más relevante en regiones irregulares del espacio.  
Por el contrario, si el límite es **suave y definido**, un **K grande** permite promediar sobre más vecinos, reduciendo ruido y mejorando la estabilidad de la clasificación.

<img title="" src="https://media.geeksforgeeks.org/wp-content/uploads/20250804203325949273/Visualizing-Classifier-Decision-Boundaries.webp" alt="Visualizing Classifier Decision Boundaries - GeeksforGeeks" data-align="center" width="550">

---
