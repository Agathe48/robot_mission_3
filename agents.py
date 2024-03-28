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
    WasteDisposalZone,
    Radioactivity
)


##############
### Agents ###
##############

class CleaningAgent(Agent):

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


    # Mouvement
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

    # Picking up waste
    def pick_up(self):
        x,y = self.pos
        this_cell = self.model.grid.get_cell_list_contents([(x,y)])

        current_waste_count = sum(isinstance(obj, Waste) for obj in this_cell)
        if current_waste_count <= 1:
            for obj in this_cell:
                if isinstance(obj, Waste):
                    self.model.schedule.remove_agent(obj)
                    break

    # Dropping waste
    def drop(self):
        x,y = self.pos
        waste = Waste()
        this_cell = self.model.grid.get_cell_list_contents([(x,y)])
        if this_cell.is_empty():
            self.model.grid.place_agent(waste, (x,y))
        else:
            # Find nearby empty cell to drop waste
            neighbors = self.model.grid.get_neighborhood((x, y), moore = False , include_center=False)
            empty_cells = [cell for cell in neighbors if self.model.grid.is_cell_empty(cell)]

            if empty_cells:
                # Move to the first empty cell found
                new_position = self.random.choice(empty_cells)
                self.model.grid.move_agent(self, new_position)
                # Drop waste at the new position
                self.drop()

    """
    # Another version of dropping waste
    def drop_waste(self):
        x, y = self.pos
        if self.model.grid.is_cell_empty((x, y)):
            waste = Waste()  # Create a new Waste object
            self.model.grid.place_agent(waste, (x, y))
    """

    # Transforming waste
    def transform(self):
        x, y = self.pos
        this_cell = self.model.grid.get_cell_list_contents([(x, y)])
        for obj in this_cell:
            if isinstance(obj, Waste):
                if obj.type_waste == "green":
                    obj.type_waste = "yellow"
                elif obj.type_waste == "yellow":
                    obj.type_waste = "red"
                break



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

    def __init__(self, unique_id, model, grid_size):
        super().__init__(unique_id, model, grid_size)
        self.green_waste_count = 0
        self.yellow_waste_count = 0
"""
    def deliberate(self):
        if self.green_waste_count < 2 :
            self.pick_up()
        elif self.green_waste_count == 2:
            self.transform()
        elif self.yellow_waste_count == 1:
            self.move_to_z1_frontiere()
        else:
            self.random_movement()

    def move_to_z1_frontiere(self):
        x, y = self.pos
        zone = self.model.grid.get_cell_list_contents([(x, y)])[0].zone

        # Move right until the next cell is in zone z2
        while zone != "z2":
            self.go_right()
            x += 1
            zone = self.model.grid.get_cell_list_contents([(x, y)])[0].zone
"""      

class YellowAgent(CleaningAgent):
    def __init__(self, unique_id, model, grid_size):
        super().__init__(unique_id, model, grid_size)
        self.yellow_waste_count = 0
        self.red_waste_count = 0

class RedAgent(CleaningAgent):

    def __init__(self, unique_id, model, grid_size):
        super().__init__(unique_id, model, grid_size)
        self.red_waste_count = 0

