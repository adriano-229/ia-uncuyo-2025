# --- Generic helper to compute confusion matrix (2x2 numeric) ---
compute_confusion_matrix <- function(df, actual_col, pred_col) {
  TP <- sum(df[[actual_col]] == 1 & df[[pred_col]] == 1)
  FN <- sum(df[[actual_col]] == 1 & df[[pred_col]] == 0)
  FP <- sum(df[[actual_col]] == 0 & df[[pred_col]] == 1)
  TN <- sum(df[[actual_col]] == 0 & df[[pred_col]] == 0)

  matrix(
    c(TP, FN,
      FP, TN),
    nrow = 2,
    byrow = TRUE
  )
}

# --- Function to calculate metrics from a generic 2x2 confusion matrix ---
# Matrix structure:
# [1,1]=TP, [1,2]=FN
# [2,1]=FP, [2,2]=TN

calculate_metrics <- function(conf_matrix) {
  TP <- conf_matrix[1, 1]
  FN <- conf_matrix[1, 2]
  FP <- conf_matrix[2, 1]
  TN <- conf_matrix[2, 2]

  accuracy    <- (TP + TN) / (TP + TN + FP + FN)
  precision   <- ifelse((TP + FP) == 0, NA, TP / (TP + FP))
  sensitivity <- ifelse((TP + FN) == 0, NA, TP / (TP + FN))
  specificity <- ifelse((TN + FP) == 0, NA, TN / (TN + FP))

  data.frame(
    Accuracy = accuracy,
    Precision = precision,
    Sensitivity = sensitivity,
    Specificity = specificity,
    TP = TP, FN = FN, FP = FP, TN = TN
  )
}