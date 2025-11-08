library(rpart)
library(pROC)

# ============================================================
# 3. Modelo Base - Árbol de Decisión
# ============================================================

train_df <- read.csv("data/arbolado-mza-dataset-train.csv")
validation_df <- read.csv("data/arbolado-mza-dataset-validation.csv")

# Convertir variables categóricas
factor_cols <- c("altura", "diametro_tronco", "especie", "seccion")
train_df[factor_cols] <- lapply(train_df[factor_cols], as.factor)
validation_df[factor_cols] <- lapply(validation_df[factor_cols], factor, levels = levels(train_df$especie))

train_df$inclinacion_peligrosa <- as.factor(train_df$inclinacion_peligrosa)
validation_df$inclinacion_peligrosa <- as.factor(validation_df$inclinacion_peligrosa)

# Definir fórmula
formula_tree <- inclinacion_peligrosa ~ altura + circ_tronco_cm + lat + long +
                 seccion + especie + diametro_tronco + area_seccion

# Entrenamiento con prior balanceado
tree_model <- rpart(
  formula_tree,
  data = train_df,
  method = "class",
  parms = list(prior = c(0.5, 0.5)),
  control = rpart.control(cp = 0.0005, minsplit = 20, minbucket = 10, maxdepth = 10)
)

cat("Número de nodos del árbol:", nrow(tree_model$frame), "\n")

# Predicción sobre validación
pred_probs <- predict(tree_model, validation_df, type = "prob")[, 2]
pred_classes <- ifelse(pred_probs > 0.5, 1, 0)
actual <- as.numeric(as.character(validation_df$inclinacion_peligrosa))

# Métricas de rendimiento
roc_obj <- roc(actual, pred_probs)
auc_value <- auc(roc_obj)
cat("AUC =", auc_value, "\n")

TP <- sum(actual == 1 & pred_classes == 1)
TN <- sum(actual == 0 & pred_classes == 0)
FP <- sum(actual == 0 & pred_classes == 1)
FN <- sum(actual == 1 & pred_classes == 0)

metrics <- data.frame(
  Accuracy = (TP + TN) / (TP + TN + FP + FN),
  Precision = TP / (TP + FP),
  Sensitivity = TP / (TP + FN),
  Specificity = TN / (TN + FP),
  AUC = auc_value
)

print(metrics)

# Guardar predicciones en formato Kaggle
submission <- data.frame(ID = seq_len(nrow(validation_df)),
                         inclinacion_peligrosa = pred_classes)
write.csv(submission, "data/submission_decision_tree.csv", row.names = FALSE)
cat("Archivo de envío generado: data/submission_decision_tree.csv\n")
