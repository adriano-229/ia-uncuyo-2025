import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from base_agent import BaseAgent


class SimpleReflexAgent(BaseAgent):
    """
    Agente Serpentina Adriano (no usé IA):

    La lógica de este agente reflexivo simple busca garantizar que, siempre que sea posible
    dado el número de acciones restantes, se efectúe una normalización hacia la esquina
    superior izquierda (0,0), para luego iniciar el recorrido en serpentina. De esta forma
    se evita el uso de memoria adicional (banderas o estados internos), y el agente sigue
    siendo puramente reflexivo simple.

    Definiciones:
    - n: tamaño de la grilla (n x n).
    - (x, y): posición actual absoluta del agente.
    - (x0, y0): posición inicial.
    - remaining_actions: acciones que le restan al agente.
    - remaining_cells: cantidad de celdas necesarias para alcanzar la normalización
      desde (x0,y0) hasta (0,0), dada por:

    remaining_cells = n*(y0-1) + (n-x0)

    Política del agente:
    1. Si remaining_actions > remaining_cells, conviene normalizar verticalmente.
       Para ello:
          - Si y > 0 y x > 0: avanzar hacia la izquierda.
          - Si y > 0 y x = 0: avanzar hacia arriba.
          - Si y = 0: avanzar hacia la izquierda hasta llegar a (0,0).
    2. Si remaining_actions ≤ remaining_cells, se descarta la normalización y se inicia
       directamente el recorrido en serpentina desde la posición actual.
    3. Una vez alcanzada la esquina superior izquierda (0,0), el agente, sin necesidad de
       estado adicional, queda naturalmente limitado por la condición anterior a iniciar
       el movimiento en serpentina.

    Nota: El agente sigue siendo un reflex simple porque cada decisión se basa únicamente
    en la percepción instantánea de su posición y en parámetros del entorno consultados
    en ese mismo ciclo (n, remaining_actions). No se almacenan banderas ni se conserva
    información de pasos previos.

    Limitación: Este diseño logra eliminar el uso de memoria explícita, pero introduce
    una restricción: en el punto (0,0) la regla de normalización puede continuar siendo
    válida, aunque ya no existan movimientos útiles hacia arriba o hacia la izquierda.
    La transición hacia el modo serpentina ocurre entonces por la propia geometría de
    la grilla (al no poder desplazarse más en dichas direcciones), y no por una memoria
    interna que indique "normalización finalizada". Este comportamiento es coherente
    con el paradigma reflexivo simple, aunque menos eficiente que una variante con
    estado interno mínimo, un flag que indique "normalización completada".
    """

    def __init__(self, server_url="http://localhost:5000", **kwargs):
        super().__init__(server_url, "SimpleReflexAgent", **kwargs)

    def get_strategy_description(self):
        return "Este agente intenta normalizar su posición a (0,0) antes de comenzar el recorrido en serpentina."

    def think(self):
        if not self.is_connected():
            return False

        perception = self.get_perception()
        if not perception or perception.get('is_finished', True):
            return False

        if perception.get('is_dirty', False):
            return self.suck()

        # Obtener información del entorno
        x, y = perception.get('position')
        grid = self.get_environment_state().get('grid')
        remaining_actions = perception.get('actions_remaining', 0)
        height, width = len(grid), len(grid[0])

        # Costo de recorrer en serpentina desde la posición actual
        map_remaining = (height - y - 1) * width
        if y % 2 == 0:
            # fila par: izquierda → derecha
            map_remaining += width - x
        else:
            # fila impar: derecha → izquierda
            map_remaining += x + 1

        # Asumimos que la suciedad es del 50%, porque no podemos calcularla en el momento ya que el algoritmo comienza
        # a "tropezar": empieza serpentina + limpia + calcula + se arrepiente + normaliza +  calcula + se arrepiente...
        # hasta que quedan solos aquellas acciones necesarias para barrer el resto del mapa.

        # Decidir si conviene normalizar
        should_normalize = remaining_actions > map_remaining * (1 + 0.5)

        # Fase de normalización hacia (0,0)
        if should_normalize and (x >= 0 or y >= 0):
            if y > 0:
                return self.up()
            elif x > 0:
                return self.left()
            else:
                return self.idle()

        # Fase de serpentina (cuando no conviene normalizar o ya estamos en (0,0))
        return self._serpentine_movement(x, y, height, width)

    def _serpentine_movement(self, x, y, height, width):
        """
        Movimiento en serpentina:
        - Filas pares: izquierda a derecha
        - Filas impares: derecha a izquierda
        - Al final de fila, bajar
        """
        if y == height - 1:
            if (y % 2 == 0 and x == width - 1) or (y % 2 == 1 and x == 0):
                return self.idle()

        if y % 2 == 0:  # fila par: mover derecha
            if x < width - 1:
                return self.right()
            elif y < height - 1:
                return self.down()
            else:
                return self.idle()
        else:  # fila impar: mover izquierda
            if x > 0:
                return self.left()
            elif y < height - 1:
                return self.down()
            else:
                return self.idle()


# Alias para compatibilidad
SerpentineAgent = SimpleReflexAgent
