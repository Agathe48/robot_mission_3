"""
Python file for the Objects.

Group 3:
- Oumaima CHATER
- Laure-Emilie MARTIN
- Agathe PLU
- Agathe POULAIN
"""

###############
### Imports ###
###############

from typing import Literal
import random as rd

### Mesa imports ###
from mesa import Agent
from mesa.time import RandomActivation
from mesa.space import MultiGrid


###############
### Objects ###
###############

class Radioactivity(Agent): # un par case avec un niveau de radioactivité
    """ An objet for the radioactivity of the area."""
    def __init__(self, unique_id, model, zone : Literal["z1", "z2", "z3"], radioactivity_level):
        super().__init__(unique_id, model)
        self.zone = zone
        self.radioactivity_level = radioactivity_level

    def step(self):
        pass

class Waste(Agent):
    def __init__(self, unique_id, model, type_waste : Literal["green", "yellow", "red"]):
        super().__init__(unique_id, model)
        self.type_waste = type_waste

    def step(self):
        pass

class WasteDisposalZone(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        pass
