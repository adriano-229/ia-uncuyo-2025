# **Trabajo Práctico 7B - Desafío Kaggle: Peligrosidad del Arbolado Público de Mendoza**

## **Universidad Nacional de Cuyo**

### **Facultad de Ingeniería**

#### **Licenciatura en Ciencias de la Computación**

**Alumno:** Adriano Fabris

---

## **1. Descripción del proceso de preprocesamiento**

El dataset original (`arbolado-mza-dataset.csv`) contiene información georreferenciada del arbolado público de la Ciudad
de Mendoza, incluyendo atributos físicos, de localización y administrativos de cada árbol, junto con una variable
binaria `inclinacion_peligrosa` que indica si el árbol presenta una inclinación considerada peligrosa.

El objetivo del preprocesamiento fue garantizar que los datos estuvieran en un formato consistente y adecuado para el
entrenamiento de modelos de clasificación supervisada. Las transformaciones aplicadas fueron las siguientes:

### **1.1 Eliminación y selección de variables**

Se eliminaron las columnas que no aportaban información útil para el modelo predictivo o introducían ruido:

* `id`: identificador sin relación con la inclinación.
* `ultima_modificacion`: variable temporal sin relevancia predictiva directa.
* `nombre_seccion`: redundante con la variable `seccion`.

### **1.2 Transformación de variables categóricas**

Las variables categóricas fueron convertidas a factores para que los algoritmos las interpretaran como categorías
discretas. Entre ellas:

* `altura` (recodificada para conservar solo el descriptor principal, e.g. “Bajo”, “Medio”, “Alto”).
* `diametro_tronco`, `seccion` y `especie`.

En el caso de `especie`, se detectaron **31 categorías diferentes**, pero con una fuerte desproporción: las especies
“Morera” y “Fresno europeo” concentran más del 50% de las observaciones, mientras que las menos frecuentes representan
menos del 1% cada una.
Para evitar una matriz dispersa y mejorar la generalización, se agruparon las especies minoritarias bajo una nueva
categoría **"Otras"**.

### **1.3 Normalización de variables numéricas**

Se normalizaron al rango (0, 1) las variables:

* `circ_tronco_cm`
* `area_seccion`

Esto se realizó para garantizar una escala comparable entre variables de distinta magnitud, especialmente relevante para
algoritmos basados en árboles de decisión y gradiente.

### **1.4 Manejo del desbalanceo de clases**

El dataset presenta un fuerte desbalance:

* `inclinacion_peligrosa = 0` → 88.8%
* `inclinacion_peligrosa = 1` → 11.2%

Para mitigar este efecto se implementó el parámetro `scale_pos_weight` en el modelo XGBoost, calculado como la razón
entre las clases negativas y positivas, forzando así al modelo a penalizar más los errores de la clase minoritaria.

---

## **Modelo avanzado: XGBoost**

### **2. Resultados obtenidos sobre el conjunto de validación**

Se aplicó un modelo **XGBoost (Extreme Gradient Boosting)**, un método de *ensemble learning* que combina múltiples
árboles de decisión débiles optimizados secuencialmente para minimizar el error global.

Parámetros principales:

* `eta = 0.05` (tasa de aprendizaje)
* `max_depth = 6`
* `subsample = 0.8`
* `colsample_bytree = 0.8`
* `min_child_weight = 5`
* `scale_pos_weight = 7.9` (ajustado al desbalance real)

Durante el entrenamiento se utilizó una validación interna (80/20) dentro del conjunto de entrenamiento para evitar
sobreajuste, con *early stopping* si el AUC no mejoraba tras 50 iteraciones.

Resultados sobre el conjunto de validación interna:

| Métrica              | Valor      |
|----------------------|------------|
| Accuracy             | 0.742      |
| Precision            | 0.253      |
| Sensitivity (Recall) | 0.681      |
| Specificity          | 0.750      |
| **AUC**              | **0.7827** |

La métrica AUC superó ampliamente el umbral exigido (0.69), indicando una buena capacidad discriminativa entre árboles
peligrosos y no peligrosos.

---

### **3. Resultados obtenidos en Kaggle**

Tras entrenar el modelo final con **el 100% del conjunto de entrenamiento**, se aplicó sobre el archivo de evaluación
oficial `arbolado-mza-dataset-test.csv`.

El archivo de envío generado tuvo el formato:

```
ID,inclinacion_peligrosa
1,0
2,0
3,1
...
```

El puntaje obtenido en la plataforma **Kaggle** fue:

> **AUC = 0.71801**

Este resultado confirma la capacidad del modelo para generalizar en datos no vistos, manteniendo un desempeño sólido en
un entorno de evaluación independiente.

---

## **4. Descripción detallada del algoritmo propuesto**

El algoritmo final se basó en **XGBoost**, una técnica de *gradient boosting* orientada a minimizar una función de
pérdida mediante la combinación de árboles de decisión optimizados secuencialmente. Cada nuevo árbol corrige los errores
residuales de los anteriores.

### **Principios teóricos:**

En cada iteración, el modelo minimiza una función de costo ( L(\theta) ), que combina el error de predicción y una
penalización por complejidad del modelo:

[
L(\theta) = \sum_i l(y_i, \hat{y}_i) + \sum_k \Omega(f_k)
]

donde

* ( l(y_i, \hat{y}_i) ) mide la diferencia entre la etiqueta real y la predicha,
* ( \Omega(f_k) = \gamma T + \frac{1}{2}\lambda ||w||^2 ) controla la complejidad del árbol ( f_k ),
* y el modelo final es la suma de árboles ( \hat{y}_i = \sum_k f_k(x_i) ).

Cada árbol se construye a partir del gradiente y el hessiano (segunda derivada) de la función de pérdida, permitiendo un
descenso más eficiente que el *boosting* clásico.

### **Ventajas principales:**

* Control de sobreajuste mediante regularización y *early stopping*.
* Alta eficiencia computacional gracias a su estructura en bloques y paralelización.
* Buen manejo del desbalance de clases con `scale_pos_weight`.
* Capacidad para combinar variables numéricas y categóricas codificadas.

### **Motivo de elección:**

Entre las alternativas evaluadas (árbol de decisión y Random Forest), XGBoost mostró la mejor combinación entre
rendimiento (AUC > 0.78 en validación) y estabilidad de resultados, superando ampliamente el umbral exigido en el
desafío.

---

## **Conclusiones**

El proceso completo de preprocesamiento, ajuste y validación permitió obtener un modelo predictivo robusto con buena
capacidad de generalización.
El resultado en Kaggle (AUC = 0.71801) demuestra que, a pesar del desbalance de clases y la alta heterogeneidad del
dataset, el modelo logra discriminar correctamente entre árboles con y sin inclinación peligrosa.

---