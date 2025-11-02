train_data <- read.csv("data/arbolado-mendoza-dataset-train.csv")

section_risk <- train_data %>%
  group_by(seccion, nombre_seccion) %>%
  summarise(
    total = n(),
    peligrosos = sum(inclinacion_peligrosa == 1),
    proporcion = peligrosos / total
  ) %>%
  arrange(desc(proporcion))

print(section_risk)

# Visualization
ggplot(section_risk, aes(x = reorder(nombre_seccion, -proporcion), y = proporcion)) +
  geom_col(fill = "steelblue") +
  labs(title = "Proporción de árboles peligrosos por sección",
       x = "Sección",
       y = "Proporción de inclinación peligrosa") +
  theme_minimal() +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))
