# Inteligencia Artificial - TP7B - Parte 1: Cross-Validation y Análisis de Resultados

## Universidad Nacional de Cuyo  
### Facultad de Ingeniería  
#### Licenciatura en Ciencias de la Computación  
##### Alumno: Adriano Fabris  

---

### i) Código de las funciones create_folds() y cross_validation().

```r
create_folds <- function(df, k=10, seed=42) {
  set.seed(seed)
  n <- nrow(df)
  indices <- sample(1:n)  # mezcla aleatoria
  folds <- split(indices, cut(seq_along(indices), breaks=k, labels=FALSE))
  names(folds) <- paste0("Fold", 1:k)
  return(folds)
}

cross_validation <- function(df, k=10, seed=42) {
  folds <- create_folds(df, k, seed)
  metrics_list <- list()

  for(i in 1:k) {
    test_idx <- folds[[i]]
    train_idx <- setdiff(seq_len(nrow(df)), test_idx)
    
    train_fold <- df[train_idx, ]
    test_fold <- df[test_idx, ]
    
    # Convertir variables categóricas a factores (igual que en el caso de prueba)
    train_fold$inclinacion_peligrosa <- as.factor(train_fold$inclinacion_peligrosa)
    train_fold$especie <- as.factor(train_fold$especie)
    train_fold$seccion <- as.factor(train_fold$seccion)
    train_fold$altura <- as.factor(train_fold$altura)

    test_fold$inclinacion_peligrosa <- as.factor(test_fold$inclinacion_peligrosa)

    # Alinear levels de factores entre train y test
    test_fold$especie <- factor(test_fold$especie, levels=levels(train_fold$especie))
    test_fold$seccion <- factor(test_fold$seccion, levels=levels(train_fold$seccion))
    test_fold$altura <- factor(test_fold$altura, levels=levels(train_fold$altura))

    # Definir fórmula de modelado
    train_formula <- formula(inclinacion_peligrosa ~ altura + circ_tronco_cm + lat + long + seccion + especie)

    # Usar los mismos parámetros agresivos que en el caso de prueba
    tree_model <- rpart(train_formula, data=train_fold, method="class", parms = list(prior = c(0.5, 0.5)),
                       control=rpart.control(cp=0.0002, minsplit=30, minbucket=10, maxdepth=10))

    # Predecir sobre test
    predictions <- predict(tree_model, test_fold, type='class', na.action=na.pass)

    # Convertir a numérico (igual que en el caso de prueba)
    predictions_num <- as.numeric(as.character(predictions))

    # Reemplazar NAs con 0 (igual que en el caso de prueba)
    predictions_num[is.na(predictions_num)] <- 0

    # Calcular métricas
    actual_num <- as.numeric(as.character(test_fold$inclinacion_peligrosa))
    metrics <- confusion_metrics(actual=actual_num, predicted=predictions_num)
    metrics_list[[i]] <- metrics

    cat('Fold', i, '- Number of nodes:', nrow(tree_model$frame), '\n')
  }

  # Convertir lista a dataframe
  metrics_df <- do.call(rbind, metrics_list)

  # Calcular media y desviación estándar por métrica
  mean_metrics <- colMeans(metrics_df, na.rm=TRUE)
  sd_metrics <- apply(metrics_df, 2, sd, na.rm=TRUE)

  return(list(metrics_by_fold=metrics_df, mean=mean_metrics, sd=sd_metrics))
}
```

---

### ii) Análisis de los resultados y pruebas realizadas

En una primera instancia, el modelo de árbol de decisión fue entrenado utilizando los siguientes parámetros:

```r
control = rpart.control(cp = 0.0001, minsplit = 10, minbucket = 3, maxdepth = 10)
````

y sin especificar ponderaciones de clase (`prior`).
Bajo esta configuración, la media de las métricas obtenidas en la validación cruzada fue:

| Métrica     | Media | Desviación estándar |
| ----------- | ----- | ------------------- |
| Accuracy    | 0.879 | 0.006               |
| Precision   | 0.230 | 0.078               |
| Sensitivity | 0.035 | 0.017               |
| Specificity | 0.986 | 0.003               |

El modelo alcanzó una exactitud elevada, pero con una sensibilidad prácticamente nula.
Esto indica que el árbol predijo casi siempre la clase mayoritaria (“no peligroso”), sin capacidad para identificar casos verdaderamente peligrosos.
La causa principal es el **fuerte desbalance de clases** (89 % clase 0, 11 % clase 1), que induce al modelo a optimizar su pureza global privilegiando la clase más frecuente.

---

Para abordar este problema, se ajustaron tanto los parámetros de complejidad como las ponderaciones de clase:

```r
parms = list(prior = c(0.5, 0.5)),
control = rpart.control(cp = 0.0005, minsplit = 20, minbucket = 10, maxdepth = 10)
```

El parámetro `prior` equilibró la influencia de ambas clases durante el aprendizaje, asignando igual peso a los casos peligrosos y no peligrosos.
Los valores más conservadores de `cp`, `minsplit` y `minbucket` limitaron la profundidad y el tamaño mínimo de los nodos, evitando un sobreajuste excesivo tras reequilibrar las clases.

Con esta configuración, los resultados promedio de la validación cruzada fueron:

| Métrica     | Media | Desviación estándar |
| ----------- | ----- | ------------------- |
| Accuracy    | 0.700 | 0.010               |
| Precision   | 0.225 | 0.013               |
| Sensitivity | 0.688 | 0.030               |
| Specificity | 0.702 | 0.014               |

---

La comparación entre ambas configuraciones muestra un cambio cualitativo importante.
Si bien la exactitud general disminuyó, el modelo adquirió la capacidad de **detectar correctamente la mayoría de los árboles peligrosos** (sensibilidad ≈ 0.69), manteniendo una especificidad equilibrada (≈ 0.70).
Esto refleja un comportamiento mucho más apropiado para un sistema de alerta o diagnóstico de riesgo, donde los falsos negativos (no detectar un árbol peligroso) resultan más costosos que los falsos positivos.

---

### Conclusión
El proceso de ajuste evidenció que el desbalance de clases afecta de manera crítica el desempeño de los árboles de decisión.
El uso de ponderaciones equilibradas y una calibración cuidadosa de la complejidad del árbol permitió mejorar drásticamente la sensibilidad sin comprometer en exceso la precisión general, logrando un compromiso más útil para la aplicación práctica del modelo.

---