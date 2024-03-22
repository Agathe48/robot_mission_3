"""
Python file for the Model.

Group 3:
- Oumaima CHATER
- Laure-Emilie MARTIN
- Agathe PLU
- Agathe POULAIN
"""

###############
### Imports ###
###############

### Python imports ###

import random as rd

### Mesa imports ###

from mesa import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid

### Local imports ###

from objects import Radioactivity
from tools.tools_constants import (
    GRID_HEIGHT,
    GRID_WIDTH
)

#############
### Model ###
#############

class Area(Model):
    """A model with some number of agents."""
   # density is used only for illustartion
    def __init__(self, nb_agents, width=GRID_WIDTH, height=GRID_HEIGHT, density=0.8):
        super().__init__()
        self.nb_agents = nb_agents
        self.width = width
        self.height = height
        self.grid = MultiGrid(self.width, self.height, True)
        self.schedule = RandomActivation(self)
        # self.density= width/height #used only for illustration for the slider density
        
        # Create agents
        for i in range(self.height):
            for j in range(self.width):
                a = Radioactivity(unique_id = [i , j], model=self, zone = "z1", radioactivity_level=rd.random()/3)
                self.schedule.add(a)
                self.grid.place_agent(a, (j, i))

        # self.datacollector = DataCollector(
        #     model_reporters={"Gini": compute_gini},
        #     agent_reporters={"Wealth": "wealth"})
        
        # self.running = True

    def step(self):
        self.schedule.step()
        # self.datacollector.collect(self)
        
    def run_model(self, step_count=100):
        model = Area(nb_agents = 1)  # 50 agents in our example
        for i in range(step_count):
            self.step()


        
