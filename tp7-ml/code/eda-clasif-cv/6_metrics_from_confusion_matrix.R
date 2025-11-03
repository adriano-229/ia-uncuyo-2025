# Define metrics as functions
accuracy <- function(TP, TN, FP, FN) {
  (TP + TN) / (TP + TN + FP + FN)
}

precision <- function(TP, FP) {
  ifelse((TP + FP) == 0, NA, TP / (TP + FP))
}

sensitivity <- function(TP, FN) {
  ifelse((TP + FN) == 0, NA, TP / (TP + FN))
}

specificity <- function(TN, FP) {
  ifelse((TN + FP) == 0, NA, TN / (TN + FP))
}

# Example: metrics for random classifier
TP_r <- 360   # replace with your actual counts
TN_r <- 356
FP_r <- 2857
FN_r <- 250
metrics_random <- data.frame(
  Model = "Random",
  Accuracy = accuracy(TP_r, TN_r, FP_r, FN_r),
  Precision = precision(TP_r, FP_r),
  Sensitivity = sensitivity(TP_r, FN_r),
  Specificity = specificity(TN_r, FP_r)
)

# Example: metrics for majority classifier
TP_m <- 0
TN_m <- 5667
FP_m <- 0
FN_m <- 716
metrics_majority <- data.frame(
  Model = "Bigger Class",
  Accuracy = accuracy(TP_m, TN_m, FP_m, FN_m),
  Precision = precision(TP_m, FP_m),
  Sensitivity = sensitivity(TP_m, FN_m),
  Specificity = specificity(TN_m, FP_m)
)

# Combine and print
metrics_all <- rbind(metrics_random, metrics_majority)
print(metrics_all)
