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
        """
        Initializes the CustomRandomScheduler.

        Parameters
        ----------
        model : Model
            The model associated with this scheduler.

        agents : list of agents, optional
            List of agents to be scheduled. If None, it will be initialized as an empty list.
       
        
        Returns
        -------
        None
        """
        super().__init__(model, agents)

    def step(self):
        """
        Activate agents in a random order based on their type (green, yellow, red) at each model step.
        
        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        print("------ NEW STEP ------")
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
                print("-----------------------------")
                agent.step()
