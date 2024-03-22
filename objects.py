"""
Python file for the Objects.

Group 3:
- Oumaima CHATER
- Laure-Emilie MARTIN
- Agathe PLU
- Agathe POULAIN
"""

from typing import Literal
import random as rd

### Mesa imports ###
from mesa import Agent
from mesa.time import RandomActivation
from mesa.space import MultiGrid

class Radioactivity(Agent): # un par case avec un niveau de radioactivité
    """ An objet for the radioactivity of the area."""
    def __init__(self, unique_id, model, zone : Literal["z1", "z2", "z3"], radioactivity_level):
        super().__init__(unique_id, model)
        self.zone = zone
        self.radioactivity_level = radioactivity_level

    def step(self):
        pass

