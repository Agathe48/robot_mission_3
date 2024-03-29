"""
Python file for the Schedule.

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
from mesa.agent import Agent
from mesa.time import BaseScheduler

### Local imports ###

from agents import (
    RedAgent,
    YellowAgent,
    GreenAgent
)

#############
### Class ###
#############

class CustomRandomScheduler(BaseScheduler):
    
    def __init__(self, model: Model, agents = None) -> None:
        super().__init__(model, agents)

    def step(self):
        list_green_agents = list(self.model.get_agents_of_type(GreenAgent))
        list_yellow_agents = list(self.model.get_agents_of_type(YellowAgent))
        list_red_agents = list(self.model.get_agents_of_type(RedAgent))

        # Shuffle the type of agent to activate firstly, secondly and thirdly
        activation_order_type = [list_green_agents, list_yellow_agents, list_red_agents]
        rd.shuffle(activation_order_type)

        for list_type_agent in activation_order_type:
            # Shuffle the agents from the same type
            rd.shuffle(list_type_agent)
            for agent in list_type_agent:
                agent.step()
