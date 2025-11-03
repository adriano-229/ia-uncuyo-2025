# 5a) Function that assigns the majority class to all observations
biggerclass_classifier <- function(df) {
  majority_class <- df %>%
    count(inclinacion_peligrosa) %>%
    arrange(desc(n)) %>%
    slice(1) %>%
    pull(inclinacion_peligrosa)

  df %>%
    mutate(prediction_class = majority_class)
}

# 5b) Apply to validation dataset
validation_data <- read.csv("data/arbolado-mendoza-dataset-validation.csv")

validation_majority <- biggerclass_classifier(validation_data)

# Confusion-matrix counts
confusion_counts_majority <- validation_majority %>%
  summarise(
    TP = sum(inclinacion_peligrosa == 1 & prediction_class == 1),
    TN = sum(inclinacion_peligrosa == 0 & prediction_class == 0),
    FP = sum(inclinacion_peligrosa == 0 & prediction_class == 1),
    FN = sum(inclinacion_peligrosa == 1 & prediction_class == 0)
  )

print(confusion_counts_majority)

# Optional: matrix view
confusion_matrix_majority <- matrix(
  c(confusion_counts_majority$TP, confusion_counts_majority$FP,
    confusion_counts_majority$FN, confusion_counts_majority$TN),
  nrow = 2,
  byrow = TRUE,
  dimnames = list(
    "Actual" = c("Peligroso (1)", "No peligroso (0)"),
    "Predicho" = c("Peligroso (1)", "No peligroso (0)")
  )
)

print(confusion_matrix_majority)