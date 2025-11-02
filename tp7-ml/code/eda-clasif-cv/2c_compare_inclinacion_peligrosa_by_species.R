train_data <- read.csv("data/arbolado-mendoza-dataset-train.csv")

species_risk <- train_data %>%
  group_by(especie) %>%
  summarise(
    total = n(),
    peligrosos = sum(inclinacion_peligrosa == 1),
    proporcion = peligrosos / total
  ) %>%
  filter(total > 50) %>%  # filter out rare species for clearer visualization
  arrange(desc(proporcion))

print(head(species_risk, 10))  # top 10 most risky species

# Visualization (top 10 also)
ggplot(species_risk[1:10, ], aes(x = reorder(especie, -proporcion), y = proporcion)) +
  geom_col(fill = "darkorange") +
  labs(title = "Proporción de árboles peligrosos por especie (Top 10)",
       x = "Especie",
       y = "Proporción de inclinación peligrosa") +
  theme_minimal() +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))

