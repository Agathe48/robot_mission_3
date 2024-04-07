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

### Local imports ###

from tools.tools_constants import (
    ACT_PICK_UP,
    ACT_DROP_TRANSFORMED_WASTE,
    ACT_DROP_ONE_WASTE,
    ACT_TRANSFORM,
    ACT_GO_LEFT,
    ACT_GO_RIGHT,
    ACT_GO_UP,
    ACT_GO_DOWN,
    ACT_WAIT
)
from tools.tools_knowledge import AgentKnowledge
from objects import (
    Waste,
    WasteDisposalZone,
    Radioactivity
)
from communication.agent.CommunicatingAgent import CommunicatingAgent

##############
### Agents ###
##############

class CleaningAgent(CommunicatingAgent):
    
    def __init__(self, unique_id, model, grid_size, pos_waste_disposal):
        """
        Initializes the Agent object with provided parameters.

        Parameters
        ----------
        unique_id : int
            A unique identifier for the agent.
            
        model : Model
            The model in which the agent is being initialized.
            
        grid_size : tuple
            A tuple specifying the size of the grid environment (rows, columns).
            
        pos_waste_disposal : tuple 
            A tuple specifying the position of the waste disposal zone in the grid (row, column).

        Returns
        -------
        None
        """
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
        """
        Performs a step in the agent's decision-making process.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        # Update agent's knowledge
        self.update()
        # Determine all possible actions based on current knowledge
        list_possible_actions = self.deliberate()
        # Perform the action and update the percepts
        self.percepts = self.model.do(
            self, list_possible_actions=list_possible_actions)
        # Update the knowledge of the agent with the consequences of the action
        self.update_knowledge_with_action(self.percepts["action_done"])
      
    def convert_pos_to_tile(self, pos) -> Literal["right", "left", "down", "up"]:
        """
        Converts a position to a directional tile.

        Parameters
        ----------
        pos : tuple
            A tuple representing the position to be converted (x, y).

        Returns
        -------
        str
            A string representing the direction ('right', 'left', 'down', 'up').
        """

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

    def update_knowledge_with_action(self, performed_action):
        action = performed_action["action"]
        my_object = performed_action["object"]

        if action == ACT_PICK_UP:
            picked_up_waste = self.knowledge.get_picked_up_wastes()
            picked_up_waste.append(my_object)
            self.knowledge.set_picked_up_wastes(picked_up_waste)

        if action == ACT_DROP_TRANSFORMED_WASTE:
            self.knowledge.set_transformed_waste(transformed_waste = None)

        if action == ACT_DROP_ONE_WASTE:
            self.knowledge.set_picked_up_wastes(picked_up_wastes = [])

        if action == ACT_TRANSFORM:
            self.knowledge.set_transformed_waste(transformed_waste = my_object)
            self.knowledge.set_picked_up_wastes(picked_up_wastes = [])


    def update(self):
        """
        Updates the agent's knowledge based on its percepts

        Parameters
        ----------
        None

        Returns
        -------
        None 
        """

        print("Percepts of Agent", self.unique_id, self.percepts)

        grid_knowledge, grid_radioactivity = self.knowledge.get_grids()
        dict_boolean_knowledge = {
            "left": True,
            "right": True,
            "up": True,
            "down": True
        }

        for key in self.percepts["positions"]:
            list_objects_tile = self.percepts["positions"][key]
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
            if dict_boolean_knowledge[key]:
                if key == "left":
                    self.knowledge.set_left(boolean_left = True)
                if key == "right":
                    self.knowledge.set_right(boolean_right = True)
                if key == "up":
                    self.knowledge.set_up(boolean_up = True)
                if key == "down":
                    self.knowledge.set_down(boolean_down = True)

        # print("Knowledge after of Agent", self.unique_id, self.knowledge)

    def update_positions_around_agent(self, direction, dict_boolean_knowledge):

        """
        Updates the boolean knowledge about adjacent positions around the agent.

        Parameters
        ----------
        direction : str
            The direction of the adjacent position.
        dict_boolean_knowledge : dict
            A dictionary representing the boolean knowledge about adjacent positions.

        Returns
        -------
        dict_boolean_knowledge : dict
                Updated boolean knowledge dictionary.
        """
        if direction == "left":
            dict_boolean_knowledge["left"] = False
            self.knowledge.set_left(boolean_left = False)
        if direction == "right":
            dict_boolean_knowledge["right"] = False
            self.knowledge.set_right(boolean_right = False)
        if direction == "up":
            dict_boolean_knowledge["up"] = False
            self.knowledge.set_up(boolean_up = False)
        if direction == "down":
            dict_boolean_knowledge["down"] = False
            self.knowledge.set_down(boolean_down = False)
        return dict_boolean_knowledge

class GreenAgent(CleaningAgent):
    
    def __init__(self, unique_id, model, grid_size, pos_waste_disposal):
        """
        Initializes the Green Agent with provided parameters.

        Parameters
        ----------
        unique_id : int
            A unique identifier for the agent.
            
        model : Model
            The model in which the agent is being initialized.
            
        grid_size : tuple
            A tuple specifying the size of the grid environment (rows, columns).
            
        pos_waste_disposal : tuple 
            A tuple specifying the position of the waste disposal zone in the grid (row, column).

        Returns
        -------
        None
        """

        super().__init__(unique_id, model, grid_size, pos_waste_disposal)

    def deliberate(self):
        """
        Determines all possible actions based o the current knowledge of the environment.

        Parameters
        ----------
        None

        Returns
        -------
            list_possible_actions : list
                 A list of possible actions the agent can take based on its knowledge.
        """
        list_possible_actions = []

        # Get data from knowledge
        grid_knowledge, grid_radioactivity = self.knowledge.get_grids()
        left = self.knowledge.get_left()
        right = self.knowledge.get_right()
        up = self.knowledge.get_up()
        down = self.knowledge.get_down()
        transformed_waste = self.knowledge.get_transformed_waste()
        picked_up_wastes = self.knowledge.get_picked_up_wastes()

        # Check up and down available directions
        list_available_act_directions = []
        if up:
            list_available_act_directions.append(ACT_GO_UP)
        if down:
            list_available_act_directions.append(ACT_GO_DOWN)

        # Check if there is a waste to transform
        if len(picked_up_wastes) == 2:
            list_possible_actions.append(ACT_TRANSFORM)

        # Check if agent has a transformed waste and if it can go right or drop it
        if transformed_waste != None:
            # Check if cell at the right is in zone 2
            if grid_radioactivity[self.pos[0]+1][self.pos[1]] == 2:
                # Check if the current cell does not already contain a waste
                if grid_knowledge[self.pos[0]][self.pos[1]] == 0:
                    list_possible_actions.append(ACT_DROP_TRANSFORMED_WASTE)
                else:
                    if len(list_available_act_directions) > 0:
                        # Randomize the order of possible moves
                        random.shuffle(list_available_act_directions)
                        for action in list_available_act_directions:
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
        if left:
            list_available_act_directions.append(ACT_GO_LEFT)
        if right:
            # Check if cell at the right is in zone 2 (green agent can't go in zone 2)
            if grid_radioactivity[self.pos[0]+1][self.pos[1]] != 2:
                list_available_act_directions.append(ACT_GO_RIGHT)

        if len(list_available_act_directions) > 0:
            list_best_directions = []
            for act_direction in list_available_act_directions:
                # Check if there is a waste in the right cell and favor this direction
                if act_direction == ACT_GO_RIGHT and grid_knowledge[self.pos[0]+1][self.pos[1]] == 1:
                    list_best_directions.append(act_direction)
                    list_available_act_directions.remove(act_direction)
                # Check if there is a waste in the left cell and favor this direction
                if act_direction == ACT_GO_LEFT and grid_knowledge[self.pos[0]-1][self.pos[1]] == 1:
                    list_best_directions.append(act_direction)
                    list_available_act_directions.remove(act_direction)
                # Check if there is a waste in the up cell and favor this direction
                if act_direction == ACT_GO_UP and grid_knowledge[self.pos[0]][self.pos[1]+1] == 1:
                    list_best_directions.append(act_direction)
                    list_available_act_directions.remove(act_direction)
                # Check if there is a waste in the down cell and favor this direction
                if act_direction == ACT_GO_DOWN and grid_knowledge[self.pos[0]][self.pos[1]-1] == 1:
                    list_best_directions.append(act_direction)
                    list_available_act_directions.remove(act_direction)

            # Randomize the order of possible best moves
            if len(list_best_directions) > 0:
                random.shuffle(list_best_directions)
                for action in list_best_directions:
                    list_possible_actions.append(action)

            # Randomize the order of possible moves
            if len(list_available_act_directions) > 0:
                random.shuffle(list_available_act_directions)
                for action in list_available_act_directions:
                    list_possible_actions.append(action)

        list_possible_actions.append(ACT_WAIT)
        list_possible_actions.append(ACT_DROP_ONE_WASTE)
        print("Green agent", self.unique_id, "has the possible actions :", list_possible_actions)
        return list_possible_actions

class YellowAgent(CleaningAgent):

    def __init__(self, unique_id, model, grid_size, pos_waste_disposal):
        """
        Initializes the Yellow Agent with provided parameters.

        Parameters
        ----------
        unique_id : int
            A unique identifier for the agent.
            
        model : Model
            The model in which the agent is being initialized.
            
        grid_size : tuple
            A tuple specifying the size of the grid environment (rows, columns).
                
        pos_waste_disposal : tuple 
            A tuple specifying the position of the waste disposal zone in the grid (row, column).

        Returns
        -------
        None
        """
        super().__init__(unique_id, model, grid_size, pos_waste_disposal)
        
    def deliberate(self):
        """
        Determines all possible actions based o the current knowledge of the environment.

        Parameters
        ----------
        None

        Returns
        -------
        list_possible_actions : list
            A list of possible actions the agent can take based on its knowledge.
        """
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
        list_available_act_directions = []
        if up:
            list_available_act_directions.append(ACT_GO_UP)
        if down:
            list_available_act_directions.append(ACT_GO_DOWN)

        # Check if there is a waste to transform
        if len(picked_up_wastes) == 2:
            list_possible_actions.append(ACT_TRANSFORM)

        # Check if agent has a transformed waste and if it can go right or drop it
        if transformed_waste != None:
            # Check if cell at the right is in zone 3
            if grid_radioactivity[self.pos[0]+1][self.pos[1]] == 3:
                # Check if the current cell does not already contain a waste
                if grid_knowledge[self.pos[0]][self.pos[1]] == 0:
                    list_possible_actions.append(ACT_DROP_TRANSFORMED_WASTE)
                else :
                    if len(list_available_act_directions) > 0 :
                        # Randomize the order of possible moves
                        random.shuffle(list_available_act_directions)
                        for action in list_available_act_directions:
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
        if left:
            # Check if cell at the left is in zone 2
            if grid_radioactivity[self.pos[0]-1][self.pos[1]] != 1:
                list_available_act_directions.append(ACT_GO_LEFT)
            # Check if the cell is in zone 1 and if it contains an yellow waste
            elif grid_knowledge[self.pos[0]-1][self.pos[1]] == 2:
                list_available_act_directions.append(ACT_GO_LEFT)
        if right:
            # Check if cell at the right is in zone 2 (yellow agent can't go in zone 3)
            if grid_radioactivity[self.pos[0]+1][self.pos[1]] != 3 :
                list_available_act_directions.append(ACT_GO_RIGHT)

        if len(list_available_act_directions) > 0:
            list_best_directions = []
            for act_direction in list_available_act_directions:
                # Check if there is a waste in the right cell and favor this direction
                if act_direction == ACT_GO_RIGHT and grid_knowledge[self.pos[0]+1][self.pos[1]] == 2:
                    list_best_directions.append(act_direction)
                    list_available_act_directions.remove(act_direction)
                # Check if there is a waste in the left cell and favor this direction
                if act_direction == ACT_GO_LEFT and grid_knowledge[self.pos[0]-1][self.pos[1]] == 2:
                    list_best_directions.append(act_direction)
                    list_available_act_directions.remove(act_direction)
                # Check if there is a waste in the up cell and favor this direction
                if act_direction == ACT_GO_UP and grid_knowledge[self.pos[0]][self.pos[1]+1] == 2:
                    list_best_directions.append(act_direction)
                    list_available_act_directions.remove(act_direction)
                # Check if there is a waste in the down cell and favor this direction
                if act_direction == ACT_GO_DOWN and grid_knowledge[self.pos[0]][self.pos[1]-1] == 2:
                    list_best_directions.append(act_direction)
                    list_available_act_directions.remove(act_direction)

            # Randomize the order of possible best moves
            if len(list_best_directions) > 0:
                random.shuffle(list_best_directions)
                for action in list_best_directions:
                    list_possible_actions.append(action)

            # Randomize the order of possible moves
            if len(list_available_act_directions) > 0:
                random.shuffle(list_available_act_directions)
                for action in list_available_act_directions:
                    list_possible_actions.append(action)

        list_possible_actions.append(ACT_WAIT)
        list_possible_actions.append(ACT_DROP_ONE_WASTE)
        print("Yellow agent", self.unique_id, "has the possible actions :", list_possible_actions)
        return list_possible_actions

class RedAgent(CleaningAgent):

    def __init__(self, unique_id, model, grid_size, pos_waste_disposal):
        """
        Initializes the Red Agent with provided parameters.

        Parameters
        ----------
        unique_id : int
            A unique identifier for the agent.
            
        model : Model
            The model in which the agent is being initialized.
            
        grid_size : tuple
            A tuple specifying the size of the grid environment (rows, columns).
            
        pos_waste_disposal : tuple 
            A tuple specifying the position of the waste disposal zone in the grid (row, column).

        Returns
        -------
            None
        """
        super().__init__(unique_id, model, grid_size, pos_waste_disposal)

    def deliberate(self):
        """
        Determines all possible actions based o the current knowledge of the environment.

        Parameters
        ----------
        None

        Returns
        -------
        list_possible_actions : list
            A list of possible actions the agent can take based on its knowledge.
        """
        list_possible_actions = []

        # Get data from knowledge
        grid_knowledge, grid_radioactivity = self.knowledge.get_grids()
        left = self.knowledge.get_left()
        right = self.knowledge.get_right()
        up = self.knowledge.get_up()
        down = self.knowledge.get_down()
        picked_up_wastes = self.knowledge.get_picked_up_wastes()

        # Check up and down cells for agents
        list_available_act_directions = []
        if up:
            list_available_act_directions.append(ACT_GO_UP)
        if down:
            list_available_act_directions.append(ACT_GO_DOWN)
        
        # If we picked up a waste, go to waste disposal zone to drop it
        if len(picked_up_wastes) == 1:
            if grid_knowledge[self.pos[0]][self.pos[1]] == 4:
                list_possible_actions.append(ACT_DROP_ONE_WASTE)
            else:
                # The agent goes to the waste disposal zone column
                if right:
                    list_possible_actions.append(ACT_GO_RIGHT)
                else:
                    waste_disposal_zone_position = np.where(grid_knowledge == 4)
                    # If the Waste dispozal zone is above the agent
                    if waste_disposal_zone_position[1] > self.pos[1]:
                        if up:
                            list_possible_actions.append(ACT_GO_UP)
                        # If the agent can't go up, it waits
                        else:
                            list_possible_actions.append(ACT_WAIT)
                    # If the Waste dispozal zone is below the agent
                    else:
                        if down:
                            list_possible_actions.append(ACT_GO_DOWN)
                        # If the agent can't go down, it waits
                        else:
                            list_possible_actions.append(ACT_WAIT)

        # Check if there is a waste to pick up and if we can pick up a waste
        if len(picked_up_wastes) <= 0 and grid_knowledge[self.pos[0]][self.pos[1]] == 3:
            list_possible_actions.append(ACT_PICK_UP)

        # Check for other agent in surronding cells
        if left:
            # Check if cell at the left is in zone 3
            if grid_radioactivity[self.pos[0]-1][self.pos[1]] != 2:
                list_available_act_directions.append(ACT_GO_LEFT)
            # Check if the cell is in zone 2 and if it contains a red waste
            elif grid_knowledge[self.pos[0]-1][self.pos[1]] == 3:
                list_available_act_directions.append(ACT_GO_LEFT)
        if right:
            list_available_act_directions.append(ACT_GO_RIGHT)

        if len(list_available_act_directions) > 0:
            list_best_directions = []
            for act_direction in list_available_act_directions:
                # Check if there is a waste in the right cell and favor this direction
                if act_direction == ACT_GO_RIGHT and grid_knowledge[self.pos[0]+1][self.pos[1]] == 3:
                    list_best_directions.append(act_direction)
                    list_available_act_directions.remove(act_direction)
                # Check if there is a waste in the left cell and favor this direction
                if act_direction == ACT_GO_LEFT and grid_knowledge[self.pos[0]-1][self.pos[1]] == 3:
                    list_best_directions.append(act_direction)
                    list_available_act_directions.remove(act_direction)
                # Check if there is a waste in the up cell and favor this direction
                if act_direction == ACT_GO_UP and grid_knowledge[self.pos[0]][self.pos[1]+1] == 3:
                    list_best_directions.append(act_direction)
                    list_available_act_directions.remove(act_direction)
                # Check if there is a waste in the down cell and favor this direction
                if act_direction == ACT_GO_DOWN and grid_knowledge[self.pos[0]][self.pos[1]-1] == 3:
                    list_best_directions.append(act_direction)
                    list_available_act_directions.remove(act_direction)

            # Randomize the order of possible best moves
            if len(list_best_directions) > 0:
                random.shuffle(list_best_directions)
                for action in list_best_directions:
                    list_possible_actions.append(action)

            # Randomize the order of possible moves
            if len(list_available_act_directions) > 0:
                random.shuffle(list_available_act_directions)
                for action in list_available_act_directions:
                    list_possible_actions.append(action)

        list_possible_actions.append(ACT_WAIT)
        print("Red agent", self.unique_id, "has the possible actions :", list_possible_actions)
        return list_possible_actions



class ChiefGreenAgent(GreenAgent):
    def __init__(self, unique_id, model, grid_size, pos_waste_disposal):
        super().__init__(unique_id, model, grid_size, pos_waste_disposal)
    
    def step(self):
        super().step()
    
class ChiefYellowAgent(YellowAgent):
    def __init__(self, unique_id, model, grid_size, pos_waste_disposal):
        super().__init__(unique_id, model, grid_size, pos_waste_disposal)
    
    def step(self):
        super().step()
    
class ChiefRedAgent(RedAgent):
    def __init__(self, unique_id, model, grid_size, pos_waste_disposal):
        super().__init__(unique_id, model, grid_size, pos_waste_disposal)
    
    def step(self):
        super().step()