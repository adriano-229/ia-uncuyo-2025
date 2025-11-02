data <- read.csv("data/kaggle/arbolado-mza-dataset/arbolado-mza-dataset.csv", stringsAsFactors = FALSE)
str(data)
set.seed(1234)

train_index <- sample(seq_len(nrow(data)), size = 0.8 * nrow(data))

train_data <- data[train_index, ]
validation_data <- data[-train_index, ]

write.csv(train_data, "data/arbolado-mendoza-dataset-train.csv", row.names = FALSE)
write.csv(validation_data, "data/arbolado-mendoza-dataset-validation.csv", row.names = FALSE)