# --- Random classifier functions ---
add_random_prob <- function(df) {
  df %>% mutate(prediction_prob = runif(n()))
}

random_classifier <- function(df) {
  df %>% mutate(prediction_class = ifelse(prediction_prob > 0.5, 1, 0))
}

# --- Apply to validation dataset ---
validation_data <- read.csv("data/arbolado-mendoza-dataset-validation.csv")

validation_pred <- validation_data %>%
  add_random_prob() %>%
  random_classifier()

# --- Compute confusion matrix ---
confusion_counts <- validation_pred %>%
  summarise(
    TP = sum(inclinacion_peligrosa == 1 & prediction_class == 1),
    TN = sum(inclinacion_peligrosa == 0 & prediction_class == 0),
    FP = sum(inclinacion_peligrosa == 0 & prediction_class == 1),
    FN = sum(inclinacion_peligrosa == 1 & prediction_class == 0)
  )

print(confusion_counts)

confusion_matrix <- matrix(
  c(confusion_counts$TP, confusion_counts$FP,
    confusion_counts$FN, confusion_counts$TN),
  nrow = 2,
  byrow = TRUE,
  dimnames = list(
    "Actual" = c("Peligroso (1)", "No peligroso (0)"),
    "Predicho" = c("Peligroso (1)", "No peligroso (0)")
  )
)

print(confusion_matrix)
