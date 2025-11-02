
train_data <- read.csv("data/arbolado-mendoza-dataset-train.csv")

bin_width <- 9

# Define breaks (from min to max, rounded)
breaks_seq <- seq(floor(min(train_data$circ_tronco_cm, na.rm = TRUE)),
                  ceiling(max(train_data$circ_tronco_cm, na.rm = TRUE)),
                  by = bin_width)

# Assign each observation to a bin
train_data <- train_data %>%
  mutate(bin = cut(circ_tronco_cm, breaks = breaks_seq, include.lowest = TRUE))

# Frequency table
freq_table <- train_data %>%
  group_by(bin) %>%
  summarise(frequency = n()) %>%
  arrange(bin)

print(freq_table)

# Histogram
ggplot(train_data, aes(x = circ_tronco_cm)) +
  geom_histogram(binwidth = bin_width, fill = "steelblue", color = "white") +
  labs(title = paste("Distribución de circ_tronco_cm (binwidth =", bin_width, ")"),
       x = "Circunferencia del tronco (cm)",
       y = "Frecuencia") +
  theme_minimal()
