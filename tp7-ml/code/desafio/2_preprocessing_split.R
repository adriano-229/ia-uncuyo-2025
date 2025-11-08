library(dplyr)

# ============================================================
# 2. División Train/Validation - Dataset procesado
# ============================================================

data <- read.csv("data/arbolado-mza-dataset-processed.csv", stringsAsFactors = FALSE)
data$inclinacion_peligrosa <- as.factor(data$inclinacion_peligrosa)

set.seed(1234)
train_index <- sample(seq_len(nrow(data)), size = 0.8 * nrow(data))

train_data <- data[train_index, ]
validation_data <- data[-train_index, ]

write.csv(train_data, "data/arbolado-mza-dataset-train.csv", row.names = FALSE)
write.csv(validation_data, "data/arbolado-mza-dataset-validation.csv", row.names = FALSE)

cat("Generados:\n - data/arbolado-mza-dataset-train.csv\n - data/arbolado-mza-dataset-validation.csv\n")
