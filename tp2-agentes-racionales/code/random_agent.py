import os
import random
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from base_agent import BaseAgent


class RandomAgent(BaseAgent):
    """Random agent that moves randomly but always cleans dirt when found."""

    def __init__(self, server_url="http://localhost:5000", **kwargs):
        super().__init__(server_url, "RandomAgent", **kwargs)

    def get_strategy_description(self):
        return "Random agent that moves randomly  but always cleans dirt when found"

    def think(self):
        if not self.is_connected():
            return False

        perception = self.get_perception()
        if not perception or perception.get('is_finished', True):
            return False

        # Always clean dirt if present at current location
        if perception.get('is_dirty', False):
            return self.suck()

        # Otherwise, randomly choose a movement action
        movement_actions = [self.up, self.down, self.left, self.right]
        chosen_action = random.choice(movement_actions)

        return chosen_action()
