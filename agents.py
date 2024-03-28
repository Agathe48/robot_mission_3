"""
Python file for the Agents.

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
import numpy as np
from typing import Literal

### Mesa imports ###
from mesa import Agent
from mesa.time import RandomActivation
from mesa.space import MultiGrid

### Local imports ###
from tools.tools_knowledge import AgentKnowledge
from objects import (
    Waste, 
    WasteDisposalZone
)


##############
### Agents ###
##############

class CleaningAgent(Agent):

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def random_movement(self):
        pass

    def go_left(self):
        x, y = self.pos
        self.model.grid.move_agent(self, (x - 1, y))

    def go_right(self):
        x, y = self.pos
        self.model.grid.move_agent(self, (x + 1, y))

    def go_down(self):
        x, y = self.pos
        self.model.grid.move_agent(self, (x, y + 1))

    def go_up(self):
        x, y = self.pos
        self.model.grid.move_agent(self, (x, y - 1))

    def convert_pos_to_tile(self, pos) -> Literal["right", "left", "down", "up"]:
        x, y = self.pos
        x_tile, y_tile = pos
        if x_tile > x:
            return "right"
        if x_tile < x:
            return "left"
        if y_tile > y:
            return "down"
        if y_tile < y:
            return "up"

    def update(self):
        # print("Knowledge before of Agent", self.unique_id, self.knowledge)
        print("Percepts of Agent", self.unique_id, self.percepts)

        grid_knowledge = self.knowledge.get_grid()
        dict_boolean_knowledge = {
            "left": False,
            "right": False,
            "up": False,
            "down": False
        }

        for key in self.percepts:
            list_objects_tile = self.percepts[key]
            if len(list_objects_tile) == 0:
                grid_knowledge[key[0]][key[1]] = 0
            for element in list_objects_tile:

                if type(element) == Waste:
                    if element.type_waste == "green":
                        grid_knowledge[key[0]][key[1]] = 1
                    elif element.type_waste == "yellow":
                        grid_knowledge[key[0]][key[1]] = 2
                    elif element.type_waste == "red":
                        grid_knowledge[key[0]][key[1]] = 3

                if type(element) == WasteDisposalZone:
                    grid_knowledge[key[0]][key[1]] = 4

                if type(element) in [GreenAgent, YellowAgent, RedAgent]:
                    print("Youyou")
                    direction = self.convert_pos_to_tile(key)
                    print("DIRECTION", direction)
                                    
                    if direction == "left":
                        dict_boolean_knowledge["left"] = True
                        self.knowledge.set_left(boolean_left = True)
                    if direction == "right":
                        dict_boolean_knowledge["right"] = True
                        self.knowledge.set_right(boolean_right = True)
                    if direction == "up":
                        dict_boolean_knowledge["up"] = True
                        self.knowledge.set_up(boolean_up = True)
                    if direction == "down":
                        dict_boolean_knowledge["down"] = True
                        self.knowledge.set_down(boolean_down = True)

        self.knowledge.set_grid(grid=grid_knowledge)

        for key in dict_boolean_knowledge:
            if not dict_boolean_knowledge[key]:
                if key == "left":
                    self.knowledge.set_left(boolean_left = False)
                if key == "right":
                    self.knowledge.set_right(boolean_right = False)
                if key == "up":
                    self.knowledge.set_up(boolean_up = False)
                if key == "down":
                    self.knowledge.set_down(boolean_down = False)

        print("Knowledge after of Agent", self.unique_id, self.knowledge)

class GreenAgent(CleaningAgent):

    def __init__(self, unique_id, model, grid_size):
        super().__init__(unique_id, model)
        self.grid_size = grid_size
        self.knowledge = AgentKnowledge(grid = np.zeros((grid_size[0], grid_size[1])))
        self.percepts = {}

    def step(self):
        # action = self.deliberate(self.knowledge)
        action = None # TO REMOVE
        self.percepts = self.model.do(self, action=action)
        self.update()

class YellowAgent(CleaningAgent):
    def __init__(self, unique_id, model, grid_size):
        super().__init__(unique_id, model)

    def step(self):
        pass

class RedAgent(CleaningAgent):

    def __init__(self, unique_id, model, grid_size):
        super().__init__(unique_id, model)

    def step(self):
        pass