library(rpart)
library(dplyr)

# ============================================================
# 4. Validación Cruzada - Árbol de Decisión
# ============================================================

create_folds <- function(df, k = 10, seed = 42) {
  set.seed(seed)
  n <- nrow(df)
  indices <- sample(1:n)
  folds <- split(indices, cut(seq_along(indices), breaks = k, labels = FALSE))
  names(folds) <- paste0("Fold", 1:k)
  return(folds)
}

confusion_metrics <- function(actual, predicted) {
  TP <- sum(actual == 1 & predicted == 1, na.rm = TRUE)
  TN <- sum(actual == 0 & predicted == 0, na.rm = TRUE)
  FP <- sum(actual == 0 & predicted == 1, na.rm = TRUE)
  FN <- sum(actual == 1 & predicted == 0, na.rm = TRUE)
  Accuracy <- (TP + TN) / (TP + TN + FP + FN)
  Precision <- ifelse((TP + FP) == 0, NA, TP / (TP + FP))
  Sensitivity <- ifelse((TP + FN) == 0, NA, TP / (TP + FN))
  Specificity <- ifelse((TN + FP) == 0, NA, TN / (TN + FP))
  return(c(Accuracy, Precision, Sensitivity, Specificity))
}

cross_validation <- function(df, k = 10, seed = 42) {
  folds <- create_folds(df, k, seed)
  metrics_list <- list()
  factor_cols <- c("seccion", "especie", "altura", "diametro_tronco")

  for (i in 1:k) {
    test_idx <- folds[[i]]
    train_idx <- setdiff(seq_len(nrow(df)), test_idx)
    train_fold <- df[train_idx, ]
    test_fold <- df[test_idx, ]

    train_fold[factor_cols] <- lapply(train_fold[factor_cols], as.factor)
    test_fold[factor_cols] <- Map(factor, test_fold[factor_cols], levels = lapply(train_fold[factor_cols], levels))

    train_fold$inclinacion_peligrosa <- as.factor(train_fold$inclinacion_peligrosa)
    test_fold$inclinacion_peligrosa <- as.factor(test_fold$inclinacion_peligrosa)

    model <- rpart(
      inclinacion_peligrosa ~ altura + circ_tronco_cm + lat + long +
        seccion + especie + diametro_tronco + area_seccion,
      data = train_fold,
      method = "class",
      parms = list(prior = c(0.5, 0.5)),
      control = rpart.control(cp = 0.0005, minsplit = 20, minbucket = 10, maxdepth = 10)
    )

    preds <- predict(model, test_fold, type = "class")
    preds_num <- as.numeric(as.character(preds))
    actual_num <- as.numeric(as.character(test_fold$inclinacion_peligrosa))
    metrics_list[[i]] <- confusion_metrics(actual_num, preds_num)
    cat("Fold", i, ":", nrow(model$frame), "nodos\n")
  }

  metrics_df <- as.data.frame(do.call(rbind, metrics_list))
  colnames(metrics_df) <- c("Accuracy", "Precision", "Sensitivity", "Specificity")
  mean_metrics <- colMeans(metrics_df, na.rm = TRUE)
  sd_metrics <- apply(metrics_df, 2, sd, na.rm = TRUE)
  return(list(metrics_by_fold = metrics_df, mean = mean_metrics, sd = sd_metrics))
}

train_df <- read.csv("data/arbolado-mza-dataset-train.csv")
set.seed(42)
cv_results <- cross_validation(train_df, k = 10)
print(cv_results$mean)
print(cv_results$sd)
