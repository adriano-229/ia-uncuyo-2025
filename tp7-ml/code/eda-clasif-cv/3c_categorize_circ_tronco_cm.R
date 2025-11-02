
train_data <- read.csv("data/arbolado-mendoza-dataset-train.csv")

# Create categorical version of circ_tronco_cm
train_data <- train_data %>%
  mutate(
    circ_tronco_cm_cat = case_when(
      circ_tronco_cm < 10  ~ "bajo",
      circ_tronco_cm < 100 ~ "medio",
      circ_tronco_cm < 180 ~ "alto",
      TRUE                 ~ "muy_alto"
    )
  )

# Frequency table
print(table(train_data$circ_tronco_cm_cat))

# Visualization 1: count per category
ggplot(train_data, aes(x = circ_tronco_cm_cat, fill = circ_tronco_cm_cat)) +
  geom_bar() +
  labs(title = "Frecuencia por categoría de circ_tronco_cm",
       x = "Categoría",
       y = "Cantidad de árboles") +
  theme_minimal() +
  theme(legend.position = "none")

# Visualization 2: proportion of dangerous trees within each category
ggplot(train_data, aes(x = circ_tronco_cm_cat, fill = factor(inclinacion_peligrosa))) +
  geom_bar(position = "fill") +
  labs(title = "Proporción de árboles peligrosos por categoría de circ_tronco_cm",
       x = "Categoría de circ_tronco_cm",
       y = "Proporción",
       fill = "Peligrosidad") +
  theme_minimal()
