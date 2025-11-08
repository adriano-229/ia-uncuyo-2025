library(dplyr)
library(stringr)

# ============================================================
# 1. Feature Engineering - Limpieza y preparación del dataset
# ============================================================

df <- read.csv("data/kaggle/arbolado-mza-dataset/arbolado-mza-dataset.csv", stringsAsFactors = FALSE)

# Eliminar columnas irrelevantes
df <- df %>%
  select(-id, -ultima_modificacion, -nombre_seccion)

# Simplificar texto de 'altura' y convertir a factor
df$altura <- str_extract(df$altura, "^[A-Za-z]+")
df$altura <- as.factor(df$altura)

# Mantener diametro_tronco como factor
df$diametro_tronco <- as.factor(df$diametro_tronco)

# Convertir sección a factor
df$seccion <- as.factor(df$seccion)

# Calcular frecuencia de especies
species_freq <- df %>%
  count(especie) %>%
  mutate(prop = n / sum(n))

# Agrupar especies minoritarias (<1%)
rare_species <- species_freq %>%
  filter(prop < 0.01) %>%
  pull(especie)

df$especie <- ifelse(df$especie %in% rare_species, "Otras", df$especie)
df$especie <- as.factor(df$especie)

# Normalizar variables numéricas
df <- df %>%
  mutate(
    circ_tronco_cm = (circ_tronco_cm - min(circ_tronco_cm)) / (max(circ_tronco_cm) - min(circ_tronco_cm)),
    area_seccion = (area_seccion - min(area_seccion)) / (max(area_seccion) - min(area_seccion))
  )

# Definir variable objetivo
df$inclinacion_peligrosa <- as.factor(df$inclinacion_peligrosa)

# Guardar dataset procesado
write.csv(df, "data/arbolado-mza-dataset-processed.csv", row.names = FALSE)
cat("Archivo guardado en data/arbolado-mza-dataset-processed.csv\n")
