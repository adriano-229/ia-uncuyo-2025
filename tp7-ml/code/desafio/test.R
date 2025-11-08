# carga
df <- read.csv("data/kaggle/arbolado-mza-dataset/arbolado-mza-dataset.csv", stringsAsFactors = FALSE)

# 1) resumen general y tipos
str(df)
summary(df)

# 2) conteos únicos y NA por variable
sapply(df, function(x) sum(is.na(x)))
sapply(df, function(x) length(unique(x)))

# 3) top especies (freq) y cuántas especies hay
esp_tab <- sort(table(df$especie), decreasing = TRUE)
head(esp_tab, 20)        # 20 especies más frecuentes
length(esp_tab)          # número total de especies

# 4) seccion vs nombre_seccion
table(df$seccion)        # distribución por número de sección
table(df$nombre_seccion) # distribución por nombre (puede ser redundante)

# 5) circ_tronco_cm — rango y outliers
summary(df$circ_tronco_cm)
quantile(df$circ_tronco_cm, probs = c(0, 0.01, 0.05, 0.25, 0.5, 0.75, 0.95, 0.99, 1), na.rm=TRUE)
sum(is.na(df$circ_tronco_cm))

# 6) lat/long ranges and missing
summary(df$lat); summary(df$long)
sum(is.na(df$lat)); sum(is.na(df$long))

# 7) diametro_tronco unique values
unique(df$diametro_tronco)
table(df$diametro_tronco)

# 8) clase balance
table(df$inclinacion_peligrosa)
prop.table(table(df$inclinacion_peligrosa))

# 9) small check: proporción de filas donde especie es NA or empty
sum(trimws(df$especie) == "" | is.na(df$especie))

df %>%
  count(especie, sort = TRUE) %>%
  mutate(percent = round(n / sum(n) * 100, 2))

