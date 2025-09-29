# ia-uncuyo-2025
[
O(n·d) \cdot O(n) = O(n^2 d)
]

---

### 5. Costo de revisar un arco

Cada vez que revisás un arco, el procedimiento `enforce_arc_consistency` puede costar hasta **O(d²)**, porque para cada valor en el dominio de `Xi` se comparan todos los posibles valores en `Xj`.

---

### 6. Complejidad total

Ahora multiplicás:

* Número de revisiones de arcos: **O(n² d)**
* Costo por revisión: **O(d²)**

Total:

[
O(n^2 d^3)
]

---
