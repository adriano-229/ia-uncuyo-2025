# ============================================================
# 5. Modelo Avanzado - XGBoost para predicción de inclinación peligrosa
# ============================================================

library(xgboost)
library(dplyr)
library(Matrix)
library(pROC)

# ------------------------------------------------------------
# 1. Cargar datasets
# ------------------------------------------------------------

train_df <- read.csv("data/kaggle/arbolado-mza-dataset/arbolado-mza-dataset.csv")
train_df <- read.csv("data/kaggle/arbolado-mza-dataset-test/arbolado-mza-dataset-test.csv")

# ------------------------------------------------------------
# 2. Preparar variables (versión robusta)
# ------------------------------------------------------------

# Identificar columnas categóricas
cat_cols <- c("altura", "diametro_tronco", "especie", "seccion")

# Alinear columnas entre train y test
common_cols <- intersect(names(train_df), names(train_df))
train_df_common <- train_df[, c(common_cols, "inclinacion_peligrosa")]
test_df_common <- train_df[, common_cols]

# Unir para aplicar el mismo encoding
full_data <- bind_rows(train_df_common %>% select(-inclinacion_peligrosa), test_df_common)
full_data[cat_cols] <- lapply(full_data[cat_cols], as.factor)

# Crear matriz dispersa
sparse_matrix <- sparse.model.matrix(~ . - 1, data = full_data)

# Separar nuevamente
n_train <- nrow(train_df_common)
train_matrix <- sparse_matrix[1:n_train, ]
test_matrix <- sparse_matrix[(n_train + 1):nrow(sparse_matrix), ]

train_label <- as.numeric(as.character(train_df_common$inclinacion_peligrosa))


# ------------------------------------------------------------
# 3. Manejo del desbalanceo de clases
# ------------------------------------------------------------

# Calcular proporción de clases
neg_count <- sum(train_label == 0)
pos_count <- sum(train_label == 1)
scale_pos_weight <- neg_count / pos_count
cat("scale_pos_weight =", scale_pos_weight, "\n")

# ------------------------------------------------------------
# 4. Definir parámetros del modelo XGBoost
# ------------------------------------------------------------

params <- list(
  objective = "binary:logistic",
  eval_metric = "auc",
  booster = "gbtree",
  eta = 0.05,              # tasa de aprendizaje
  max_depth = 6,           # profundidad máxima del árbol
  subsample = 0.8,         # fracción de filas usadas por árbol
  colsample_bytree = 0.8,  # fracción de columnas usadas por árbol
  min_child_weight = 5,    # evita sobreajuste
  gamma = 0,               # regularización mínima de pérdida
  scale_pos_weight = scale_pos_weight
)

# ------------------------------------------------------------
# 5. Entrenamiento con validación cruzada interna
# ------------------------------------------------------------

# Dividir train_matrix en train y validación (80-20)
set.seed(42)
train_size <- floor(0.8 * nrow(train_matrix))
train_indices <- sample(seq_len(nrow(train_matrix)), size = train_size)

train_subset <- train_matrix[train_indices, ]
valid_subset <- train_matrix[-train_indices, ]
train_subset_label <- train_label[train_indices]
valid_subset_label <- train_label[-train_indices]

dtrain <- xgb.DMatrix(data = train_subset, label = train_subset_label)
dvalid <- xgb.DMatrix(data = valid_subset, label = valid_subset_label)

watchlist <- list(train = dtrain, eval = dvalid)

xgb_model <- xgb.train(
  params = params,
  data = dtrain,
  nrounds = 1000,               # número máximo de iteraciones
  watchlist = watchlist,
  early_stopping_rounds = 50,   # detiene si no mejora el AUC en 50 rondas
  print_every_n = 50
)

cat("\nMejor iteración:", xgb_model$best_iteration, "\n")
cat("Mejor AUC (validación):", xgb_model$best_score, "\n")

# ------------------------------------------------------------
# 6. Evaluación final sobre validación interna
# ------------------------------------------------------------

pred_probs_valid <- predict(xgb_model, dvalid)
pred_classes_valid <- ifelse(pred_probs_valid > 0.5, 1, 0)

roc_obj <- roc(valid_subset_label, pred_probs_valid)
auc_value <- auc(roc_obj)
cat("AUC final sobre conjunto de validación:", auc_value, "\n")

TP <- sum(valid_subset_label == 1 & pred_classes_valid == 1)
TN <- sum(valid_subset_label == 0 & pred_classes_valid == 0)
FP <- sum(valid_subset_label == 0 & pred_classes_valid == 1)
FN <- sum(valid_subset_label == 1 & pred_classes_valid == 0)

metrics <- data.frame(
  Accuracy = (TP + TN) / (TP + TN + FP + FN),
  Precision = TP / (TP + FP),
  Sensitivity = TP / (TP + FN),
  Specificity = TN / (TN + FP),
  AUC = auc_value
)

print(metrics)

# ------------------------------------------------------------
# 7. Predicciones sobre el conjunto de prueba (test_matrix) y guardar
# ------------------------------------------------------------

# Entrenar modelo final con todos los datos de entrenamiento
dtrain_full <- xgb.DMatrix(data = train_matrix, label = train_label)
xgb_model_final <- xgb.train(
  params = params,
  data = dtrain_full,
  nrounds = xgb_model$best_iteration  # usar el mejor número de iteraciones
)


# Predecir sobre el test set
dtest <- xgb.DMatrix(data = test_matrix)
pred_probs_test <- predict(xgb_model_final, dtest)
pred_classes_test <- ifelse(pred_probs_test > 0.5, 1, 0)

submission <- data.frame(
  ID = train_df$id,
  inclinacion_peligrosa = pred_classes_test
)

write.csv(submission, "data/submission_xgboost.csv", row.names = FALSE)
cat("\nArchivo de envío generado: data/submission_xgboost.csv\n")
