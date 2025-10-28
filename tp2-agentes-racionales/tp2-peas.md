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

El agente es un bot (o conjunto de bots) que participa en una partida de CS en modo clásico, pudiendo actuar como
terrorista o contra-terrorista.  
Conoce algunas acciones y reglas básicas del juego (por ejemplo, el tiempo exacto del plantado de bomba, objetivos de
cada equipo) y toma decisiones para cumplir con ellas.  
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
  Aunque el agente conoce con anterioridad y exactitud el mapa, durante la partida solo percibe lo que la interfaz (UI)
  permite, lo que evita comportamientos irrealistas.

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
  Aunque todos los valores son discretos, los *quantums* de acciones clave son tan pequeños que resultan prácticamente
  continuos.  
  Ejemplos:

    - Continuo: caminar, apuntar, agacharse, lanzar un objeto.
    - Discreto: lanzar o no lanzar una granada; el tiempo entre disparos de una ráfaga sostenida es siempre el mismo.

- **Parcialmente conocido**  
  El agente posee conocimientos mínimos para un comportamiento normal, pero adapta su rendimiento según las
  condiciones.  
  Ejemplo: si la probabilidad de estar a tres rondas de diferencia en victorias es mucho menor a lo esperado y sigue
  disminuyendo, tomará medidas compensatorias (aumentar velocidad de apuntado, precisión, etc.).

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
    - Patrones mínimos de avance (por ejemplo, avanzar hacia una zona despejada por al menos 5 segundos sería esperado;
      caminar frente a una pared más de 1 segundo no lo sería).

---

# Exploración submarina (ROV SuBastian)

## Descripción del agente

El agente descrito es el sistema que controla el **ROV SuBastian**, un vehículo operado remotamente (ROV) diseñado para
exploración científica en ambientes marinos profundos. El ROV es manejado desde el buque de investigación **R/V Falkor (
too)** mediante una conexión por cable (*tether*), que provee energía, controles y transmisión de datos en tiempo real.
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

* **Parcialmente observable**: el operador tiene solo la visión y datos que los sensores del ROV proveen en tiempo real.
  No hay percepción directa del entorno completo.
* **Monoagente** (despliegue autónomo del ROV) aunque interactúa con el ecosistema marino.
* **Estocástico**: condiciones oceánicas (corrientes, visibilidad, temperatura) son variables e impredecibles.
* **Secuencial**: cada movimiento y acción (recolectar muestra, maniobrar) afecta el resultado de la misión.
* **Dinámico**: los cambios ambientales —como corrientes marinas o presencia de fauna— evolucionan durante la misión.
* **Continuo**: posición, orientación, control de velocidad y brazos manipulares varían de forma fluida.
* **Parcialmente conocido**: se conocen medidas y límites técnicos del ROV, pero las condiciones reales del entorno y la
  biodiversidad son desconocidas y deben explorarse.

### A — Actuadores

* Propulsión mediante thrusters: avance, retroceso, desplazamiento lateral y vertical.
* Control de cámara y luces: pan, tilt, zoom (PZT), activación de iluminación.
* Operación de brazos manipuladores para toma de muestras (agua, sedimento, organismos).
* Gestión de instrumentos secundarios: despliegue de sensores adicionales o herramientas según la misión.

### S — Sensores

* Cámaras UHD (incluyendo 4K) y sensores ópticos iluminación LED para captura visual.
* Sensores oceanográficos: CTD (conductividad, temperatura, profundidad), oxígeno, presión.
* Feed en tiempo real a través del cable al buque y, potencialmente, hacia tierra mediante satélite (divestreaming).
* Datos operativos: profundidad actual, orientación del ROV, estado y disponibilidad de brazos manipuladores, batería,
  etc.

---

## Comprar y vender tokens crypto

### Descripción del agente

El agente es un bot de trading automatizado que opera dentro de un **exchange** (por ejemplo, Binance o Coinbase). Su objetivo es comprar y vender un token específico según señales del mercado y una estrategia predefinida (por ejemplo, *mean reversion*, *momentum*, o arbitraje simple).
El sistema funciona de forma continua, analizando datos en tiempo real y ejecutando operaciones en milisegundos, algo imposible de sostener manualmente por un humano.

---

### P — Medidas de Performance

* **Rentabilidad neta** al cierre de cada ciclo de operación o periodo temporal definido.
* **Relación ganancia/pérdida (Sharpe ratio, profit factor)**: mide si las ganancias compensan el riesgo asumido.
* **Porcentaje de operaciones exitosas** frente al total ejecutado.
* **Costos de operación**: comisiones, *slippage*, o pérdidas por órdenes mal ejecutadas.
* **Estabilidad de la estrategia**: cuánto se mantiene la rentabilidad frente a cambios de mercado.

---

### E — Entorno

* **Parcialmente observable:** el bot tiene acceso a datos públicos del exchange (precio, volumen, *order book*), pero no puede ver las intenciones ocultas de los demás participantes ni predecir movimientos externos del mercado.
* **Multiagente:** el entorno involucra miles de otros bots y traders humanos compitiendo al mismo tiempo.
* **Estocástico:** los precios fluctúan con volatilidad impredecible. Noticias, tweets o decisiones institucionales cambian las condiciones sin aviso.
* **Secuencial:** cada operación depende del resultado anterior; vender antes o después modifica todo el flujo de ganancias.
* **Dinámico:** los precios, la liquidez y las tendencias se actualizan constantemente, incluso cuando el agente no actúa.
* **Continuo:** los precios cambian en tiempo real y las órdenes pueden ejecutarse a cualquier fracción de segundo.
* **Parcialmente conocido:** el agente entiende las reglas del exchange y las estructuras de precios, pero no puede conocer ni modelar por completo el comportamiento del mercado.

---

### A — Actuadores

* Envío y cancelación de órdenes de compra/venta.
* Ajuste dinámico del volumen de operación según riesgo.
* Actualización de estrategias en caliente (por ejemplo, cambiar *take profit* o *stop loss*).
* Registro de logs o métricas para análisis posterior.

---

### S — Sensores

* Flujo de datos en tiempo real del exchange (precio, volumen, *order book*).
* Indicadores técnicos derivados (EMA, RSI, MACD, etc.).
* Noticias o señales externas que afecten el mercado (si el bot las contempla).
* Estado interno: capital disponible, posiciones abiertas, rendimiento histórico.

---

## Practicar tenis contra una pared

### Descripción del agente

El agente es un jugador humano o robot que entrena solo, golpeando pelotas de tenis contra una pared para mejorar la precisión, la consistencia y la velocidad de reacción.
El objetivo no es ganar, sino **pulir la técnica y el control**, lo que convierte la tarea en un entorno muy interesante por su simplicidad física y su profundidad en aprendizaje motor.

---

### P — Medidas de Performance

* **Precisión del golpe:** mantener una trayectoria controlada y un punto de impacto estable.
* **Número de devoluciones consecutivas sin error:** medida directa de consistencia.
* **Velocidad de reacción y ajuste postural** tras cada golpe.
* **Control de la fuerza:** evitar que la pelota rebote demasiado cerca o lejos.
* **Duración total del rally** sin perder el ritmo.

---

### E — Entorno

* **Parcialmente observable:** el jugador percibe la pelota y la pared, pero no todas las microvariaciones en rebote o viento.
* **Monoagente:** el único actor es el jugador.
* **Determinista con componentes estocásticos:** en condiciones ideales, el rebote sigue leyes físicas fijas, aunque el spin o el viento pueden alterar resultados.
* **Secuencial:** cada golpe depende del anterior. Un error en la postura afecta el rebote siguiente.
* **Dinámico:** la pelota está siempre en movimiento y requiere reacción constante.
* **Continuo:** tanto la posición, el ángulo del golpe y la trayectoria son variables continuas.
* **Conocido:** las reglas físicas del entorno son claras y repetibles, aunque el jugador puede no controlarlas completamente.

---

### A — Actuadores

* Movimiento de piernas, tronco y brazos.
* Ajuste de ángulo y fuerza del golpe.
* Desplazamientos laterales o hacia atrás para posicionarse antes del impacto.

---

### S — Sensores

* Vista: seguimiento de la pelota.
* Oído: sonido del impacto contra la raqueta o pared.
* Propiocepción: orientación corporal, fuerza aplicada.
* Tacto: sensación del agarre y la vibración en el impacto.

---

## Realizar un salto de altura

### Descripción del agente

El agente es un robot atleta diseñado para competir o entrenar en salto de altura.
Debe coordinar carrera, impulso, técnica y caída sin derribar la barra, optimizando energía y precisión.
El entorno combina factores biomecánicos y físicos, donde pequeños desajustes cambian el resultado por completo.

---

### P — Medidas de Performance

* **Altura superada sin contacto con la barra.**
* **Regularidad en el desempeño:** número de intentos exitosos consecutivos.
* **Eficiencia del salto:** altura obtenida vs. energía empleada.
* **Corrección técnica:** cumplimiento del patrón de despegue, vuelo y caída según protocolo (p. ej. técnica Fosbury).
* **Aterrizaje seguro** sin daño estructural o desbalance.

---

### E — Entorno

* **Totalmente observable:** el robot conoce la posición exacta de la barra, la zona de impulso y la colchoneta.
* **Monoagente:** solo un participante ejecuta la tarea.
* **Determinista:** la física del salto es predecible si se controlan las variables, aunque puede haber error sensorial o mecánico.
* **Secuencial:** el resultado depende de una cadena de acciones (carrera, impulso, arco, caída).
* **Estático:** el entorno no cambia durante el salto.
* **Continuo:** posición, velocidad, fuerza y ángulo de impulso son magnitudes continuas.
* **Conocido:** el agente tiene modelos precisos de la mecánica corporal y las condiciones del entorno.

---

### A — Actuadores

* Motores para carrera, impulso y control de orientación corporal.
* Articulaciones en piernas, cadera y espalda para generar el arco.
* Sistema de amortiguación para aterrizaje.

---

### S — Sensores

* Acelerómetros y giroscopios para orientación y equilibrio.
* Cámaras o sensores de distancia para ubicar la barra.
* Sensores de presión y contacto en pies para medir impulso.
* Retroalimentación propioceptiva del movimiento articular.

---

## Pujar por un artículo en una subasta

### Descripción del agente

El agente representa a un comprador (humano o bot) en una subasta en línea o presencial.
Su objetivo es ganar el artículo deseado al menor precio posible, decidiendo **cuándo** y **cuánto** ofertar según la evolución de la puja y el comportamiento de los competidores.
Es un entorno con información pública parcial y mucha estrategia.

---

### P — Medidas de Performance

* **Éxito en la adquisición:** obtener el artículo.
* **Relación valor/precio:** cuánto vale realmente el bien frente a lo pagado.
* **Número de pujas necesarias:** optimizar recursos y evitar sobrepujar.
* **Tasa de victorias:** porcentaje de subastas ganadas en relación con las participadas.
* **Tiempo de reacción:** velocidad para ofertar ante nuevas pujas.

---

### E — Entorno

* **Parcialmente observable:** se conocen las pujas visibles y el precio actual, pero no la disposición o presupuesto de los demás jugadores.
* **Multiagente:** múltiples participantes compiten en simultáneo.
* **Estocástico:** no puede predecirse con certeza cuándo o cuánto ofertará cada competidor.
* **Secuencial:** cada decisión de puja depende del estado actual y del historial previo.
* **Dinámico:** los precios cambian constantemente y el tiempo disponible se reduce.
* **Discreto:** las acciones (ofertar, esperar, retirarse) son finitas y se ejecutan en pasos definidos.
* **Parcialmente conocido:** el agente conoce las reglas del sistema (incrementos mínimos, tiempos), pero no la estrategia de los demás.

---

### A — Actuadores

* Envío de una puja (con un monto definido).
* Retiro o pausa de la participación.
* Ajuste de estrategia según evolución (por ejemplo, esperar hasta el final o sobrepujar a propósito).

---

### S — Sensores

* Precio actual del artículo.
* Tiempo restante de subasta.
* Historial de pujas (quién ofertó, cuándo y cuánto).
* Señales del entorno: número de participantes activos, patrones de comportamiento, mensajes del sistema.

---