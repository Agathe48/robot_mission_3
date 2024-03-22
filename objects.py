"""
Python file for the Objects.

Group 3:
- Oumaima CHATER
- Laure-Emilie MARTIN
- Agathe PLU
- Agathe POULAIN
"""

### Mesa imports ###
from mesa import Agent
from mesa.time import RandomActivation
from mesa.space import MultiGrid


### Areas ###
class GreenArea(Agent):
    """ An objet for the green area."""
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        pass

### Wastes ###
