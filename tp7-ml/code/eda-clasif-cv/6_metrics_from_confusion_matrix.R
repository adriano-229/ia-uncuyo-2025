conf_matrix_random   <- compute_confusion_matrix(validation_pred, "inclinacion_peligrosa", "prediction_class")
conf_matrix_majority <- compute_confusion_matrix(validation_majority, "inclinacion_peligrosa", "prediction_class")


# assuming conf_matrix_random and conf_matrix_majority exist
metrics_random   <- calculate_metrics(conf_matrix_random)
metrics_majority <- calculate_metrics(conf_matrix_majority)

metrics_all <- rbind(
  cbind(Modelo = "Random", metrics_random),
  cbind(Modelo = "Bigger Class", metrics_majority)
)

print(metrics_all)
