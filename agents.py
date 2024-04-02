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
import random

### Mesa imports ###
from mesa import Agent
from mesa.time import RandomActivation
from mesa.space import MultiGrid

### Local imports ###
from tools.tools_knowledge import AgentKnowledge
from objects import (
    Waste,
    WasteDisposalZone,
    Radioactivity
)


##############
### Agents ###
##############

class CleaningAgent(Agent):

    def __init__(self, unique_id, model, grid_size, pos_waste_disposal):
        super().__init__(unique_id, model)
        self.grid_size = grid_size
        # Initialise waste diposal zone position in knowledge
        grid_knowledge = np.zeros((grid_size[0], grid_size[1]))
        grid_knowledge[pos_waste_disposal[0]][pos_waste_disposal[1]] = 4
        self.knowledge = AgentKnowledge(
            grid_knowledge=grid_knowledge,
            grid_radioactivity=np.zeros((grid_size[0], grid_size[1])))
        print(self.knowledge)
        self.percepts = {}

    def step(self):
        # action = self.deliberate(self.knowledge)
        action = None # TO REMOVE
        self.percepts = self.model.do(self, action=action)
        self.update()

    # Mouvement
    def random_movement(self):
        possible_moves = [(1, 0), (-1, 0), (0, 1), (0, -1)]  # Right, Left, Down, Up
        random.shuffle(possible_moves)  # Randomize the order of possible moves
        x, y = self.pos
        for dx, dy in possible_moves:
            new_x, new_y = x + dx, y + dy
            if self.model.grid.is_cell_empty((new_x, new_y)):
                self.model.grid.move_agent(self, (new_x, new_y))
                break

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
    
    # Picking up waste
    def pick_up(self):
        x,y = self.pos
        this_cell = self.model.grid.get_cell_list_contents([(x,y)])

        current_waste_count = self.knowledge.get_nb_wastes()
    
        for obj in this_cell:
            if isinstance(obj, Waste):
                self.model.schedule.remove_agent(obj)
                self.knowledge.set_nb_wastes(nb_wastes = current_waste_count + 1)
                
    # Dropping waste
    def drop(self):
        x,y = self.pos
        waste = Waste()        
        self.model.grid.place_agent(waste, (x,y))
        self.knowledge.set_nb_wastes(nb_wastes = 0)
        self.knowledge.set_transformed_waste(boolean_transform_waste = False)
        
    # Transforming waste
    def transform(self):
        x, y = self.pos
        this_cell = self.model.grid.get_cell_list_contents([(x, y)])
        for obj in this_cell:
            if isinstance(obj, Waste):
                if obj.type_waste == "green":
                    obj.type_waste = "yellow"
                    self.knowledge.set_transformed_waste(boolean_transform_waste = True)
                    self.knowledge.set_nb_wastes(nb_wastes = 1)
                elif obj.type_waste == "yellow":
                    obj.type_waste = "red"
                    self.knowledge.set_transformed_waste(boolean_transform_waste = True)
                    self.knowledge.set_nb_wastes(nb_wastes = 1)
                break

    # Wait action
    def wait(self):
        pass

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

        grid_knowledge, grid_radioactivity = self.knowledge.get_grids()
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

                if type(element) == Radioactivity:
                    if element.zone == "z1":
                        grid_radioactivity[key[0]][key[1]] = 1
                    elif element.zone == "z2":
                        grid_radioactivity[key[0]][key[1]] = 2
                    elif element.zone == "z3":
                        grid_radioactivity[key[0]][key[1]] = 3

        self.knowledge.set_grids(grid_knowledge=grid_knowledge, grid_radioactivity=grid_radioactivity)

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

    def __init__(self, unique_id, model, grid_size, pos_waste_disposal):
        super().__init__(unique_id, model, grid_size, pos_waste_disposal)
        self.green_waste_count = 0
        self.yellow_waste_count = 0     

class YellowAgent(CleaningAgent):
    def __init__(self, unique_id, model, grid_size, pos_waste_disposal):
        super().__init__(unique_id, model, grid_size, pos_waste_disposal)
        self.yellow_waste_count = 0
        self.red_waste_count = 0

class RedAgent(CleaningAgent):
    def __init__(self, unique_id, model, grid_size, pos_waste_disposal):
        super().__init__(unique_id, model, grid_size, pos_waste_disposal)
        self.red_waste_count = 0



        


