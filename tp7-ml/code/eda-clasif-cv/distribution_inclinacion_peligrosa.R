library(dplyr)
library(ggplot2)

# Load train dataset (using relative path now)
train_data <- read.csv("data/arbolado-mendoza-dataset-train.csv")

# Count how many per class
class_dist <- train_data %>%
  group_by(inclinacion_peligrosa) %>%
  summarise(count = n()) %>%
  mutate(percent = 100 * count / sum(count))

print(class_dist)

# Bar plot
ggplot(class_dist, aes(x = factor(inclinacion_peligrosa), y = count, fill = factor(inclinacion_peligrosa))) +
  geom_col() +
  labs(title = "Distribución de la variable inclinacion_peligrosa",
       x = "Clase (0 = no peligrosa, 1 = peligrosa)",
       y = "Cantidad de árboles") +
  theme_minimal() +
  theme(legend.position = "none")
