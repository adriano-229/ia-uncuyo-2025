# Trabajo Práctico 2 — Diseño del Agente

## PEAS

Para diseñar un agente deben identificarse los **PEAS**:

- **P**: Medidas de Performance  
- **E**: Entorno  
- **A**: Actuadores  
- **S**: Sensores  

Un **Agente Inteligente** es aquel que *maximiza* un conjunto de medidas de performance.  
Cada medida puede tener un peso que la haga destacar del resto.

---

## Clasificación de los entornos

**Totalmente observables vs. Parcialmente observables**  
¿El agente tiene acceso completo al estado del entorno en cada instante?

**Monoagente vs. Multiagente**  
¿Cuántos agentes habitan y afectan el estado del entorno, incluso sin comunicación entre ellos?

**Deterministas vs. Estocásticos**  
Dado un estado y una acción, ¿el próximo estado es siempre el mismo?  
¿O existe aleatoriedad o incertidumbre?

**Episódicos vs. Secuenciales**  
¿Las decisiones afectan solo resultados inmediatos o también futuros?

**Estáticos vs. Dinámicos**  
¿El entorno cambia solo por las acciones del agente (estático) o también por sí mismo (dinámico)?

**Discretos vs. Continuos**  
¿Los estados, acciones y tiempo se describen por valores discretos o continuos?

**Conocidos vs. Desconocidos**  
¿El agente conoce completamente las reglas del entorno o debe aprenderlas a partir de la interacción?

---

## Caso de análisis: Jugar al CS

### Descripción del agente

El agente es un bot (o conjunto de bots) que participa en una partida de CS en modo clásico, pudiendo actuar como terrorista o contra-terrorista.  
Conoce algunas acciones y reglas básicas del juego (por ejemplo, el tiempo exacto del plantado de bomba, objetivos de cada equipo) y toma decisiones para cumplir con ellas.  
Puede configurarse en distintos niveles de dificultad, lo que ajusta las cotas de rendimiento esperadas.

---

## P — Medidas de Performance

Las medidas se priorizan según su importancia relativa:

1. Porcentaje de identificación correcta de enemigos y tiempo de identificación.
2. Porcentaje de tiros acertados.
3. Dinero gastado en la ronda.
4. Resultado de la ronda: en un modelo ideal sería consecuencia de las demás medidas y no un objetivo independiente.

---

## E — Entorno

**Tipos y justificación:**

- **Parcialmente observable**  
  Aunque el agente conoce con anterioridad y exactitud el mapa, durante la partida solo percibe lo que la interfaz (UI) permite, lo que evita comportamientos irrealistas.

- **Multiagente**  
  Ya que existen dos o más bots en la partida, no tendría sentido que sólo sea un bot en toda la partida.

- **Estocástico**  
  
  - La mecánica de dispersión de disparos incluye un componente aleatorio.  
  - La presencia de jugadores humanos introduce comportamiento externo impredecible.

- **Secuencial**  
  Ejemplos:  
  
  - Una granada se lanza y solo se activa al caer; en el trayecto puede desviarse (componente estocástico).  
  - Avanzar un “quantum” hacia una dirección que implique caer por un precipicio.  
  - Gastar dinero ahora reduce recursos futuros.

- **Dinámico**  
  Otros jugadores alteran el estado del entorno mientras el agente actúa.

- **Continuo**  
  Aunque todos los valores son discretos, los *quantums* de acciones clave son tan pequeños que resultan prácticamente continuos.  
  Ejemplos:  
  
  - Continuo: caminar, apuntar, agacharse, lanzar un objeto.  
  - Discreto: lanzar o no lanzar una granada; el tiempo entre disparos de una ráfaga sostenida es siempre el mismo.

- **Parcialmente conocido**  
  El agente posee conocimientos mínimos para un comportamiento normal, pero adapta su rendimiento según las condiciones.  
  Ejemplo: si la probabilidad de estar a tres rondas de diferencia en victorias es mucho menor a lo esperado y sigue disminuyendo, tomará medidas compensatorias (aumentar velocidad de apuntado, precisión, etc.).

---

## A — Actuadores

- Movimientos y combinaciones: avanzar, retroceder, izquierda, derecha, saltar, agacharse.
- Acciones: lanzar granada, disparar, plantar/desactivar bomba.
- Gestión de armas: cambiar, recargar.
- Desplazamiento táctico:  
  - Avanzar hacia la zona de colocación de la bomba.  
  - Acercarse a puntos con alta densidad de aliados o enemigos.

---

## S — Sensores

- **Interfaz de usuario (UI):** campo de visión, barra de vida, dinero, tiempo restante, mapa y minimapa, etc.
- **Datos predeterminados:**  
  - Tiempo exacto para plantar o desactivar bomba.  
  - Tiempos de lanzamiento y activación de granadas.  
  - Objetivos de cada equipo.  
  - Patrones mínimos de avance (por ejemplo, avanzar hacia una zona despejada por al menos 5 segundos sería esperado; caminar frente a una pared más de 1 segundo no lo sería).

---

# Exploración submarina (ROV SuBastian)

## Descripción del agente

El agente descrito es el sistema que controla el **ROV SuBastian**, un vehículo operado remotamente (ROV) diseñado para exploración científica en ambientes marinos profundos. El ROV es manejado desde el buque de investigación **R/V Falkor (too)** mediante una conexión por cable (*tether*), que provee energía, controles y transmisión de datos en tiempo real.
Se utilizó en la campaña “Underwater Oases of Mar del Plata Canyon: Talud Continental IV” (jul-ago 2025).

---

## PEAS

### P — Medidas de Performance

* Calidad y resolución de las imágenes/video obtenidas (HD/4K).
* Precisión y calidad de muestras biológicas, geológicas, sedimentos, agua y eDNA.
* Cobertura y duración de la misión (profundidad alcanzada, tiempo efectivo de exploración).
* Éxito en muestreo sin alterar o dañar los ecosistemas observados.
* Eficiencia de operación: tiempo entre inmersiones, errores operativos mínimos.

### E — Entorno

* **Parcialmente observable**: el operador tiene solo la visión y datos que los sensores del ROV proveen en tiempo real. No hay percepción directa del entorno completo.
* **Monoagente** (despliegue autónomo del ROV) aunque interactúa con el ecosistema marino.
* **Estocástico**: condiciones oceánicas (corrientes, visibilidad, temperatura) son variables e impredecibles.
* **Secuencial**: cada movimiento y acción (recolectar muestra, maniobrar) afecta el resultado de la misión.
* **Dinámico**: los cambios ambientales —como corrientes marinas o presencia de fauna— evolucionan durante la misión.
* **Continuo**: posición, orientación, control de velocidad y brazos manipulares varían de forma fluida.
* **Parcialmente conocido**: se conocen medidas y límites técnicos del ROV, pero las condiciones reales del entorno y la biodiversidad son desconocidas y deben explorarse.

### A — Actuadores

* Propulsión mediante thrusters: avance, retroceso, desplazamiento lateral y vertical.
* Control de cámara y luces: pan, tilt, zoom (PZT), activación de iluminación.
* Operación de brazos manipuladores para toma de muestras (agua, sedimento, organismos).
* Gestión de instrumentos secundarios: despliegue de sensores adicionales o herramientas según la misión.

### S — Sensores

* Cámaras UHD (incluyendo 4K) y sensores ópticos iluminación LED para captura visual.
* Sensores oceanográficos: CTD (conductividad, temperatura, profundidad), oxígeno, presión.
* Feed en tiempo real a través del cable al buque y, potencialmente, hacia tierra mediante satélite (divestreaming).
* Datos operativos: profundidad actual, orientación del ROV, estado y disponibilidad de brazos manipuladores, batería, etc.

---


## Comprar y vender tokens crypto
Descripción del agente: Sistema automatizado (bot) que opera en un exchange comprando y vendiendo un token específico según señales del mercado.
PEAS:
P: Rentabilidad neta, relación ganancia/pérdida, número de operaciones exitosas.
E: Mercado de criptomonedas, variaciones de precio, liquidez, comisiones.
A: Ejecución de órdenes de compra/venta, cancelación de órdenes, ajuste de volumen.
S: Datos de precios en tiempo real, indicadores técnicos, profundidad de mercado, historial de transacciones.

---

## Practicar tenis contra una pared
Descripción del agente: Jugador que ejecuta golpes de tenis contra una pared para entrenar control y consistencia.
PEAS:
P: Precisión de los golpes, número de devoluciones consecutivas, velocidad de reacción.
E: Pared, pelota, superficie de la cancha, condiciones climáticas.
A: Movimiento de brazos, piernas y tronco, golpeo con la raqueta.
S: Vista, oído, sensaciones propioceptivas y táctiles.

---

## Realizar un salto de altura
Descripción del agente: robot atleta que ejecuta un salto para superar una barra horizontal sin derribarla.
PEAS:
P: Altura superada, técnica correcta, regularidad en el desempeño.
E: Barra de altura, zona de impulso, colchoneta, condiciones ambientales.
A: Carrera de impulso, despegue, arco del cuerpo, caída.
S: Vista, equilibrio, propiocepción, feedback táctil.

---

## Pujar por un artículo en una subasta
Descripción del agente: Participante (humano o software) que decide cuándo y cuánto ofertar por un artículo.
PEAS:
P: Ganar el artículo al menor precio posible, relación valor/precio.
E: Sala o plataforma de subasta, otros pujadores, reglas de puja.
A: Realizar ofertas, retirarse de la puja.
S: Precio actual, historial de pujas, tiempo restante, señales de comportamiento de competidores.

---
