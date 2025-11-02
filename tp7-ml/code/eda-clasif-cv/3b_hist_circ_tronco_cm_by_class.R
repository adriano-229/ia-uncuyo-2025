train_data <- read.csv("data/arbolado-mendoza-dataset-train.csv")

bin_width <- 20

ggplot(train_data, aes(x = circ_tronco_cm, fill = factor(inclinacion_peligrosa))) +
  geom_histogram(binwidth = bin_width, position = "identity", alpha = 0.6, color = "white") +
  labs(title = paste0("Distribución de circ_tronco_cm (binwidth = ", bin_width, ") separada por inclinación peligrosa"),
       x = "Circunferencia del tronco (cm)",
       y = "Frecuencia",
       fill = "Peligrosidad") +
  theme_minimal()