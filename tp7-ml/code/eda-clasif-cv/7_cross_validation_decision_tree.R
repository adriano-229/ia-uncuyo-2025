
train_df <- read.csv("data/arbolado-mendoza-dataset-train.csv")

create_folds <- function(df, k=10, seed=42) {
  set.seed(seed)
  n <- nrow(df)
  indices <- sample(1:n)  # mezcla aleatoria
  folds <- split(indices, cut(seq_along(indices), breaks=k, labels=FALSE))
  names(folds) <- paste0("Fold", 1:k)
  return(folds)
}


confusion_metrics <- function(actual, predicted) {
  TP <- sum(actual == 1 & predicted == 1, na.rm=TRUE)
  TN <- sum(actual == 0 & predicted == 0, na.rm=TRUE)
  FP <- sum(actual == 0 & predicted == 1, na.rm=TRUE)
  FN <- sum(actual == 1 & predicted == 0, na.rm=TRUE)
  
  Accuracy <- (TP + TN) / (TP + TN + FP + FN)
  Precision <- ifelse((TP + FP)==0, NA, TP / (TP + FP))
  Sensitivity <- ifelse((TP + FN)==0, NA, TP / (TP + FN))
  Specificity <- ifelse((TN + FP)==0, NA, TN / (TN + FP))
  
  return(c(Accuracy=Accuracy, Precision=Precision, Sensitivity=Sensitivity, Specificity=Specificity))
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

# ============================================================
# Ejecutar validación cruzada
# ============================================================

set.seed(42)  # usar la misma semilla que en el caso de prueba
cv_results <- cross_validation(train_df, k=10)
cat("\nMétricas por fold:\n")
print(cv_results$metrics_by_fold)
cat("\nMedia de métricas:\n")
print(cv_results$mean)
cat("\nDesviación estándar de métricas:\n")
print(cv_results$sd)


cat("\nACCURACY:    proportion of correct predictions over all predictions.             (TP+TN)/(TP+TN+FP+FN)")
cat("\nPRECISION:   proportion of positive identifications that were actually correct.  TP/(TP+FP)")
cat("\nSENSITIVITY: proportion of actual positives that were correctly identified.      TP/(TP+FN)")
cat("\nSPECIFICITY: proportion of actual negatives that were correctly identified.      TN/(TN+FP)")

