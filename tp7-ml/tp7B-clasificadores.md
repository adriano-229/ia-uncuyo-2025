# Inteligencia Artificial - TP7B - Parte 1: Clasificadores

## Universidad Nacional de Cuyo  
### Facultad de Ingeniería  
#### Licenciatura en Ciencias de la Computación  
##### Alumno: Adriano Fabris  

---

### **i) Clasificador Aleatorio**

---

#### Matriz de confusión

| **Actual / Predicho** | **Peligroso (1)** | **No peligroso (0)** |
| --------------------- | ----------------: | -------------------: |
| **Peligroso (1)**     |               364 |                  352 |
| **No peligroso (0)**  |              2844 |                 2823 |

---

#### Métricas


| Métrica                 | Valor |
|-------------------------| ----- |
| **Accuracy**            | 0.499 |
| **Precision**           | 0.113 |
| **Sensitivity**         | 0.508 |
| **Specificity**         | 0.498 |

---

### **ii) Clasificador por Clase Mayoritaria**

---

#### Matriz de confusión

| **Actual / Predicho** | **Peligroso (1)** | **No peligroso (0)** |
| --------------------- | ----------------: | -------------------: |
| **Peligroso (1)**     |                 0 |                  716 |
| **No peligroso (0)**  |                 0 |                 5667 |

---

#### Métricas

| Métrica                 | Valor |
|-------------------------| ----- |
| **Accuracy**            | 0.888 |
| **Precision**           | —     |
| **Sensitivity**         | 0.000 |
| **Specificity**         | 1.000 |

---