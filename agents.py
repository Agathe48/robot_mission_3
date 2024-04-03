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

### Local imports ###

from tools.tools_constants import (
    ACT_PICK_UP,
    ACT_DROP,
    ACT_TRANSFORM,
    ACT_GO_LEFT,
    ACT_GO_RIGHT,
    ACT_GO_UP,
    ACT_GO_DOWN,
    ACT_WAIT,
    GRID_HEIGHT
)
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
        self.percepts = {}

    def step(self):
        self.update()
        list_possible_actions = self.deliberate()
        self.percepts = self.model.do(
            self, list_possible_actions=list_possible_actions)

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
        
    def convert_pos_to_tile(self, pos) -> Literal["right", "left", "down", "up"]:
        x, y = self.pos
        x_tile, y_tile = pos
        if x_tile > x:
            return "right"
        if x_tile < x:
            return "left"
        if y_tile < y:
            return "down"
        if y_tile > y:
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
            direction = self.convert_pos_to_tile(key)

            if not list_objects_tile is None:
                # When there is no Waste or WasteDisposalZone, set to 0
                if not any(isinstance(obj, Waste) or isinstance(obj, WasteDisposalZone) for obj in list_objects_tile):
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
                        dict_boolean_knowledge = self.update_positions_around_agent(
                            direction=direction,
                            dict_boolean_knowledge=dict_boolean_knowledge
                        )

                    if type(element) == Radioactivity:
                        if element.zone == "z1":
                            grid_radioactivity[key[0]][key[1]] = 1
                        elif element.zone == "z2":
                            grid_radioactivity[key[0]][key[1]] = 2
                        elif element.zone == "z3":
                            grid_radioactivity[key[0]][key[1]] = 3

            else:
                dict_boolean_knowledge = self.update_positions_around_agent(
                    direction=direction,
                    dict_boolean_knowledge=dict_boolean_knowledge
                )

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

        # print("Knowledge after of Agent", self.unique_id, self.knowledge)

    def update_positions_around_agent(self, direction, dict_boolean_knowledge):
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
        return dict_boolean_knowledge

class GreenAgent(CleaningAgent):

    def __init__(self, unique_id, model, grid_size, pos_waste_disposal):
        super().__init__(unique_id, model, grid_size, pos_waste_disposal)

    def deliberate(self):
        list_possible_actions = []

        # Get data from knowledge
        grid_knowledge, grid_radioactivity = self.knowledge.get_grids()
        left = self.knowledge.get_left()
        right = self.knowledge.get_right()
        up = self.knowledge.get_up()
        down = self.knowledge.get_down()
        transformed_waste = self.knowledge.get_transformed_waste()
        picked_up_wastes = self.knowledge.get_picked_up_wastes()

        # Check up and down cells for agents
        temp = []
        if not up:
            temp.append(ACT_GO_UP)
        if not down:
            temp.append(ACT_GO_DOWN)

        # Check if there is a waste to transform
        if len(picked_up_wastes) == 2:
            list_possible_actions.append(ACT_TRANSFORM)

        # Check if agent has a transformed waste and if it can go right or drop it
        if transformed_waste != None:
            # Check if cell at the right is in zone 2
            if grid_radioactivity[self.pos[0]+1][self.pos[1]] == 2:
                # Check if the current cell does not already contain a waste
                if grid_knowledge[self.pos[0]][self.pos[1]] == 0:
                    list_possible_actions.append(ACT_DROP)
                else :
                    if len(temp) > 0 :
                        # Randomize the order of possible moves
                        random.shuffle(temp)
                        for action in temp:
                            list_possible_actions.append(action)
                    else :
                        list_possible_actions.append(ACT_WAIT)
            else:
                # Move to the right to drop the waste
                list_possible_actions.append(ACT_GO_RIGHT)
        
        # Check if there is a waste to pick up and if we can pick up a waste (and if we don't have a transformed waste already)
        if len(picked_up_wastes) <= 1 and grid_knowledge[self.pos[0]][self.pos[1]] == 1 and transformed_waste == None:
            list_possible_actions.append(ACT_PICK_UP)

        # Check for other agent in surronding cells
        if not left :
                temp.append(ACT_GO_LEFT)
        if not right:
            # Check if cell at the right is in zone 2 (green agent can't go in zone 2)
            if grid_radioactivity[self.pos[0]+1][self.pos[1]] != 2 :
                temp.append(ACT_GO_RIGHT)

        if len(temp) > 0 :
            # Randomize the order of possible moves
            random.shuffle(temp)
            for action in temp:
                list_possible_actions.append(action)

        list_possible_actions.append(ACT_WAIT)
        print(list_possible_actions)
        return list_possible_actions
   

class YellowAgent(CleaningAgent):
    def __init__(self, unique_id, model, grid_size, pos_waste_disposal):
        super().__init__(unique_id, model, grid_size, pos_waste_disposal)
        
    def deliberate(self):
        list_possible_actions = []

        # Get data from knowledge
        grid_knowledge, grid_radioactivity = self.knowledge.get_grids()
        left = self.knowledge.get_left()
        right = self.knowledge.get_right()
        up = self.knowledge.get_up()
        down = self.knowledge.get_down()
        transformed_waste = self.knowledge.get_transformed_waste()
        picked_up_wastes = self.knowledge.get_picked_up_wastes()

        # Check up and down cells for agents
        temp = []
        if not up:
            temp.append(ACT_GO_UP)
        if not down:
            temp.append(ACT_GO_DOWN)

        # Check if there is a waste to transform
        if len(picked_up_wastes) == 2:
            list_possible_actions.append(ACT_TRANSFORM)

        # Check if agent has a transformed waste and if it can go right or drop it
        if transformed_waste != None:
            # Check if cell at the right is in zone 3
            if grid_radioactivity[self.pos[0]+1][self.pos[1]] == 3:
                # Check if the current cell does not already contain a waste
                if grid_knowledge[self.pos[0]][self.pos[1]] == 0:
                    list_possible_actions.append(ACT_DROP)
                else :
                    if len(temp) > 0 :
                        # Randomize the order of possible moves
                        random.shuffle(temp)
                        for action in temp:
                            list_possible_actions.append(action)
                    else :
                        list_possible_actions.append(ACT_WAIT)
            else:
                # Move to the right to drop the waste
                list_possible_actions.append(ACT_GO_RIGHT)
        
        # Check if there is a waste to pick up and if we can pick up a waste (and if we don't have a transformed waste already)
        if len(picked_up_wastes) <= 1 and grid_knowledge[self.pos[0]][self.pos[1]] == 2 and transformed_waste == None:
            list_possible_actions.append(ACT_PICK_UP)

        # Check for other agent in surronding cells
        if not left:
            # Check if cell at the left is in zone 2
            if grid_radioactivity[self.pos[0]-1][self.pos[1]] != 1:
                temp.append(ACT_GO_LEFT)
            # Check if the cell is in zone 1 and if it contains an yellow waste
            elif grid_knowledge[self.pos[0]-1][self.pos[1]] == 2:
                temp.append(ACT_GO_LEFT)
        if not right:
            # Check if cell at the right is in zone 2 (yellow agent can't go in zone 3)
            if grid_radioactivity[self.pos[0]+1][self.pos[1]] != 3 :
                temp.append(ACT_GO_RIGHT)

        if len(temp) > 0 :
            # Randomize the order of possible moves
            random.shuffle(temp)
            for action in temp:
                list_possible_actions.append(action)

        list_possible_actions.append(ACT_WAIT)
        print(list_possible_actions)
        return list_possible_actions

class RedAgent(CleaningAgent):
    def __init__(self, unique_id, model, grid_size, pos_waste_disposal):
        super().__init__(unique_id, model, grid_size, pos_waste_disposal)

    def deliberate(self):
        list_possible_actions = []

        list_possible_actions.append(ACT_WAIT)

        return list_possible_actions
