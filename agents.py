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
import random as rd

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
    ACT_WAIT,
    STOP_COVERING
)
from tools.tools_knowledge import (
    AgentKnowledge,
    ChiefAgentKnowledge
)
from objects import (
    Waste,
    WasteDisposalZone,
    Radioactivity
)
from communication.agent.CommunicatingAgent import CommunicatingAgent
from communication.message.Message import Message
from communication.message.MessagePerformative import MessagePerformative

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
        # Initialise waste disposal zone position in knowledge
        grid_knowledge = np.full((grid_size[0], grid_size[1]), 9)
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
        # Receive the orders from the chief
        self.receive_orders()
        # Determine all possible actions based on current knowledge
        list_possible_actions = self.deliberate()
        # Perform the action and update the percepts
        self.percepts = self.model.do(
            self, list_possible_actions=list_possible_actions)
        # Update agent's knowledge
        self.update()
        # Send the percepts to the chief
        self.send_percepts_and_data()

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
        bool_covering = self.knowledge.get_bool_covering()

        if action == ACT_PICK_UP:
            picked_up_waste = self.knowledge.get_picked_up_wastes()
            picked_up_waste.append(my_object)
            self.knowledge.set_picked_up_wastes(picked_up_waste)
            if type(self) in [ChiefRedAgent, RedAgent]:
                self.knowledge.set_target_position(target_position = None)

        if action == ACT_DROP_TRANSFORMED_WASTE:
            self.knowledge.set_transformed_waste(transformed_waste = None)

        if action == ACT_DROP_ONE_WASTE:
            self.knowledge.set_picked_up_wastes(picked_up_wastes = [])

        if action == ACT_TRANSFORM:
            self.knowledge.set_transformed_waste(transformed_waste = my_object)
            self.knowledge.set_picked_up_wastes(picked_up_wastes = [])
            # If the agent is not in covering mode, set the target position to None so he can drop it on the border
            if not bool_covering:
                self.knowledge.set_target_position(target_position = None)

        self.update_knowledge_target_position()

    def update(self):
        """
        Updates the agent's knowledge based on its percepts.

        Parameters
        ----------
        None

        Returns
        -------
        None 
        """
        grid_knowledge, grid_radioactivity = self.knowledge.get_grids()

        for key in self.percepts["positions"]:
            list_objects_tile = self.percepts["positions"][key]

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

                    if type(element) == Radioactivity:
                        if element.zone == "z1":
                            grid_radioactivity[key[0]][key[1]] = 1
                        elif element.zone == "z2":
                            grid_radioactivity[key[0]][key[1]] = 2
                        elif element.zone == "z3":
                            grid_radioactivity[key[0]][key[1]] = 3

        self.knowledge.set_grids(grid_knowledge=grid_knowledge, grid_radioactivity=grid_radioactivity)

        # Update the knowledge of the agent with the consequences of the action
        self.update_knowledge_with_action(self.percepts["action_done"])

        # print("Knowledge after of Agent", self.unique_id, np.flip(grid_knowledge.T,0))
    
    def send_percepts_and_data(self):
        """
        Sends the agent's percepts to the its chief.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        # Get agent's data
        agent_nb_wastes = len(self.knowledge.get_picked_up_wastes())
        agent_transformed_waste = self.knowledge.get_transformed_waste()
        agent_position = self.pos
        bool_covering = self.knowledge.get_bool_covering()
        direction_covering = self.knowledge.get_direction_covering()
        target_position = self.knowledge.get_target_position()
        # Create the percepts and data to send
        percepts_and_data = self.percepts.copy()
        percepts_and_data["nb_wastes"] = agent_nb_wastes
        percepts_and_data["transformed_waste"] = agent_transformed_waste
        percepts_and_data["position"] = agent_position
        percepts_and_data["bool_covering"] = bool_covering
        percepts_and_data["direction_covering"] = direction_covering
        percepts_and_data["target_position"] = target_position
        percepts_and_data["action"] = self.percepts["action_done"]["action"]

        agent_color = DICT_CLASS_COLOR[type(self)]
        dict_chiefs = self.knowledge.get_dict_chiefs()
        chief = dict_chiefs[agent_color]

        self.send_message(Message(self.get_name(), chief.get_name(), MessagePerformative.SEND_PERCEPTS_AND_DATA, percepts_and_data))

    def treat_order(self, content):
        # The chief asks the agent to stop covering
        if content == STOP_COVERING:
            self.knowledge.set_bool_covering(bool_covering=False)
        # The chief is sending a target position to reach for the agent
        elif type(content) == tuple:
            self.knowledge.set_target_position(target_position=content)

        print("Agent", self.unique_id, "received order :", content)

    def receive_orders(self):
        list_messages = self.get_new_messages()
        message: Message
        for message in list_messages:
            # The message is an order from the chief
            if message.get_performative() == MessagePerformative.SEND_ORDERS:
                self.treat_order(content=message.get_content())

    def get_specificities_type_agent(self):
        """
        Returns the number of wastes max, the type of waste, the left zone type and the right zone type for the agent.

        Parameters
        ----------
        None

        Returns
        -------
        number_waste_max : int
            The maximal number of wastes an agent can take (2 for green and yellow, 1 for red)

        type_waste : int
            The code name of the type of waste the agent can take (1 for green, 2 for yellow, 3 for red)

        left_zone : None | int
            The number of the left zone (None for green, 1 for yellow and 2 for red)

        right_zone : None | int
            The number of the right zone (2 for green, 3 for yellow and None for red)
        """
        if type(self) in [GreenAgent, ChiefGreenAgent]:
            number_wastes_max = 2
            type_waste = 1
            left_zone = None
            right_zone = 2
        elif type(self) in [YellowAgent, ChiefYellowAgent]:
            number_wastes_max = 2
            type_waste = 2
            left_zone = 1
            right_zone = 3
        else:
            number_wastes_max = 1
            type_waste = 3
            left_zone = 2
            right_zone = None
        return number_wastes_max, type_waste, left_zone, right_zone

    def can_drop_transformed_waste(self):
        # Retrieve data from knowledge
        grid_knowledge, grid_radioactivity = self.knowledge.get_grids()
        transformed_waste = self.knowledge.get_transformed_waste()

        if transformed_waste is not None:
            if grid_knowledge[self.pos[0]][self.pos[1]] == 0:
                _, _, _, right_zone = self.get_specificities_type_agent()
                if grid_radioactivity[self.pos[0]+1][self.pos[1]] == right_zone:
                    return True
        return False

    def can_drop_one_waste(self):
        # Retrieve data from knowledge
        grid_knowledge, _ = self.knowledge.get_grids()
        picked_up_wastes = self.knowledge.get_picked_up_wastes()

        # The agent can drop a single waste if the tile is empty and if it has one and only one waste
        return len(picked_up_wastes) == 1 and grid_knowledge[self.pos[0]][self.pos[1]] == 4

    def can_transform(self):
        # Retrieve data from knowledge
        picked_up_wastes = self.knowledge.get_picked_up_wastes()
        transformed_waste = self.knowledge.get_transformed_waste()

        return len(picked_up_wastes) == 2 and transformed_waste is None

    def can_pick_up(self):
        # Retrieve data from knowledge
        grid_knowledge, _ = self.knowledge.get_grids()
        picked_up_wastes = self.knowledge.get_picked_up_wastes()
        transformed_waste = self.knowledge.get_transformed_waste()
        number_wastes_max, type_waste, _, _ = self.get_specificities_type_agent()

        return len(picked_up_wastes) < number_wastes_max and transformed_waste is None and grid_knowledge[self.pos[0]][self.pos[1]] == type_waste

    def can_go_up(self):
        grid_knowledge, _ = self.knowledge.get_grids()
        grid_height = grid_knowledge.shape[1]
        actual_position = self.pos

        return actual_position[1] + 1 < grid_height

    def can_go_down(self):
        actual_position = self.pos

        return actual_position[1] > 0

    def can_go_right(self):
        _, grid_radioactivity = self.knowledge.get_grids()
        actual_position = self.pos
        _, _, _, right_zone = self.get_specificities_type_agent()
        
        if actual_position[0] + 1 < grid_radioactivity.shape[0]:
            return int(grid_radioactivity[actual_position[0]+1][actual_position[1]]) != right_zone
        return False

    def can_go_left(self):
        _, grid_radioactivity = self.knowledge.get_grids()
        actual_position = self.pos
        _, _, left_zone, _ = self.get_specificities_type_agent()
        
        if actual_position[0] > 0:
            return int(grid_radioactivity[actual_position[0]-1][actual_position[1]]) != left_zone
        return False

    def deliberate_go_to_pick_close_waste(self):
        grid_knowledge, _ = self.knowledge.get_grids()
        _, type_waste, _, _ = self.get_specificities_type_agent()
    
        list_available_act_directions = []
        if self.can_go_right():
            list_available_act_directions.append(ACT_GO_RIGHT)
        if self.can_go_left():
            list_available_act_directions.append(ACT_GO_LEFT)
        if self.can_go_down():
            list_available_act_directions.append(ACT_GO_DOWN)
        if self.can_go_up():
            list_available_act_directions.append(ACT_GO_UP)

        if len(list_available_act_directions) > 0:
            list_best_directions = []
            for act_direction in list_available_act_directions:
                # Check if there is a waste in the right cell and favor this direction
                if act_direction == ACT_GO_RIGHT and grid_knowledge[self.pos[0]+1][self.pos[1]] == type_waste:
                    list_best_directions.append(act_direction)
                    list_available_act_directions.remove(act_direction)
                # Check if there is a waste in the left cell and favor this direction
                if act_direction == ACT_GO_LEFT and grid_knowledge[self.pos[0]-1][self.pos[1]] == type_waste:
                    list_best_directions.append(act_direction)
                    list_available_act_directions.remove(act_direction)
                # Check if there is a waste in the up cell and favor this direction
                if act_direction == ACT_GO_UP and grid_knowledge[self.pos[0]][self.pos[1]+1] == type_waste:
                    list_best_directions.append(act_direction)
                    list_available_act_directions.remove(act_direction)
                # Check if there is a waste in the down cell and favor this direction
                if act_direction == ACT_GO_DOWN and grid_knowledge[self.pos[0]][self.pos[1]-1] == type_waste:
                    list_best_directions.append(act_direction)
                    list_available_act_directions.remove(act_direction)

            # Randomize the order of possible best moves
            if len(list_best_directions) > 0:
                rd.shuffle(list_best_directions)

        return list_best_directions

    def deliberate_go_to_target(self):
        # Retrieve data from knowledge
        target_position = self.knowledge.get_target_position()
        bool_covering = self.knowledge.get_bool_covering()

        actual_position = self.pos

        list_possible_actions = []

        # Non blocking actions when going to a target
        if self.can_drop_transformed_waste():
            list_possible_actions.append(ACT_DROP_TRANSFORMED_WASTE)
        if self.can_pick_up():
            list_possible_actions.append(ACT_PICK_UP)
        if self.can_transform():
            list_possible_actions.append(ACT_TRANSFORM)
        if type(self) == RedAgent and self.can_drop_one_waste():
            list_possible_actions.append(ACT_DROP_ONE_WASTE)

        # The agent can pick up a waste close to him if he is not in covering mode
        if not bool_covering:
            list_new_possible_actions = self.deliberate_go_to_pick_close_waste()
            for action in list_new_possible_actions:
                list_possible_actions.append(action)

        # If the agent has not precise a target position for width
        if target_position[0] is None:
            if self.can_go_right():
                list_possible_actions.append(ACT_GO_RIGHT)
        # If the target position is to the right of the agent, move right
        elif target_position[0] > actual_position[0]:
            if self.can_go_right():
                list_possible_actions.append(ACT_GO_RIGHT)
        # If the target position is to the left of the agent, move left
        elif target_position[0] < actual_position[0]:
            if self.can_go_left():
                list_possible_actions.append(ACT_GO_LEFT)

        # If the target position is above the agent, move up
        if target_position[1] > actual_position[1]:
            list_possible_actions.append(ACT_GO_UP)
        # If the target position is below the agent, move down
        elif target_position[1] < actual_position[1]:
            list_possible_actions.append(ACT_GO_DOWN)

        return list_possible_actions

    def deliberate_covering(self):
        # Get data from knowledge
        direction_covering = self.knowledge.get_direction_covering()
        
        list_possible_actions = []
        # If the agent has not started covering its assigned row, it must reach the position
        if direction_covering is None:
            list_possible_actions = self.deliberate_go_to_target()

            # If the agent is blocked by another agent, move laterally randomly (we add these directions)
            list_movement_temp = []
            if self.can_go_right():
                list_movement_temp.append(ACT_GO_RIGHT)
            if self.can_go_left():
                list_movement_temp.append(ACT_GO_LEFT)
            rd.shuffle(list_movement_temp)
            for element in list_movement_temp:
                list_possible_actions.append(element)            
                
        # If the agent is in mode covering and ready to do it
        else:
            # Check if there is a waste to transform
            if self.can_transform():
                list_possible_actions.append(ACT_TRANSFORM)
            # Check if agent has a transformed waste and drop it
            if self.can_drop_transformed_waste():
                list_possible_actions.append(ACT_DROP_TRANSFORMED_WASTE)
            # Check if there is a waste to pick up and if we can pick up a waste
            if self.can_pick_up():
                list_possible_actions.append(ACT_PICK_UP)
            # Check if the red agent is moving on the trash in order to drop the waste
            if type(self) == RedAgent and self.can_drop_one_waste():
                list_possible_actions.append(ACT_DROP_ONE_WASTE)

            # Clean the column in the direction from its position
            if direction_covering == "right":
                if self.can_go_right():
                    list_possible_actions.append(ACT_GO_RIGHT)

            elif direction_covering == "left":
                if self.can_go_left():
                    list_possible_actions.append(ACT_GO_LEFT)

        return list_possible_actions
    
    def update_knowledge_target_position(self):
        _, grid_radioactivity = self.knowledge.get_grids()
        bool_covering = self.knowledge.get_bool_covering()
        direction_covering = self.knowledge.get_direction_covering()
        _, _, left_zone, right_zone = self.get_specificities_type_agent()
        
        actual_position = self.pos

        # Set target position back to None when this position is reached (may the column be precised or not)
        target_position = self.knowledge.get_target_position()
        if actual_position == target_position or (target_position is not None and actual_position[1] == target_position[1] and target_position[0] is None):
            if bool_covering:
                # When target position is reached, set the direction to cover
                if direction_covering is None:
                    if actual_position[0] == 0:
                        direction_covering = "right"
                    elif grid_radioactivity[actual_position[0] - 1][actual_position[1]] == left_zone:
                        direction_covering = "right"
                    else:
                        if actual_position[0] + 1 < grid_radioactivity.shape[0]:
                            if grid_radioactivity[actual_position[0] + 1][actual_position[1]] == right_zone or actual_position == target_position:
                                direction_covering = "left"
                        else:
                            direction_covering = "left"
                    self.knowledge.set_direction_covering(direction_covering)
            target_position = None
            self.knowledge.set_target_position(target_position)

        else:
            if bool_covering:
                # If covering line is done, set direction_covering back to None
                if actual_position[0] == 0 and direction_covering != "right":
                    direction_covering = None
                elif actual_position[0] + 1 == grid_radioactivity.shape[0]:
                    if direction_covering != "left":
                        direction_covering = None
                elif (grid_radioactivity[actual_position[0] + 1][actual_position[1]] == right_zone and direction_covering != "left") or (grid_radioactivity[actual_position[0] - 1][actual_position[1]] == left_zone and direction_covering != "right"):
                    direction_covering = None
                self.knowledge.set_direction_covering(direction_covering)

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
        transformed_waste = self.knowledge.get_transformed_waste()
        bool_covering = self.knowledge.get_bool_covering()
        target_position = self.knowledge.get_target_position()

        # If the agent is in covering mode
        if bool_covering:
            list_possible_actions = super().deliberate_covering()

        # If the agent is in normal mode
        else:
            # If the agent has a target position to reach
            if target_position is not None:
                list_possible_actions = self.deliberate_go_to_target()

            # If the agent has no target position to reach
            else:
                # Check up and down available directions
                list_available_act_directions = []

                if self.can_go_up():
                    list_available_act_directions.append(ACT_GO_UP)
                if self.can_go_down():
                    list_available_act_directions.append(ACT_GO_DOWN)

                # Check if there is a waste to transform
                if self.can_transform():
                    list_possible_actions.append(ACT_TRANSFORM)

                # Check if agent has a transformed waste and if it can go right or drop it
                if transformed_waste is not None:
                    # Check if cell at the right is in zone 2
                    if grid_radioactivity[self.pos[0]+1][self.pos[1]] == 2:
                        # Check if the current cell does not already contain a waste
                        if grid_knowledge[self.pos[0]][self.pos[1]] == 0:
                            list_possible_actions.append(ACT_DROP_TRANSFORMED_WASTE)
                        else:
                            if len(list_available_act_directions) > 0:
                                # Randomize the order of possible moves
                                rd.shuffle(list_available_act_directions)
                                for action in list_available_act_directions:
                                    list_possible_actions.append(action)
                            else:
                                list_possible_actions.append(ACT_WAIT)
                    else:
                        # Move to the right to drop the waste
                        list_possible_actions.append(ACT_GO_RIGHT)
                
                # Check if there is a waste to pick up and if we can pick up a waste (and if we don't have a transformed waste already)
                if self.can_pick_up():
                    list_possible_actions.append(ACT_PICK_UP)

                if self.can_go_left():
                    list_available_act_directions.append(ACT_GO_LEFT)
                if self.can_go_right():
                    list_available_act_directions.append(ACT_GO_RIGHT)

                # Possible best moves if there is a waste close
                list_new_possible_actions = self.deliberate_go_to_pick_close_waste()
                for action in list_new_possible_actions:
                        list_possible_actions.append(action)

                # Randomize the order of possible moves
                if len(list_available_act_directions) > 0:
                    rd.shuffle(list_available_act_directions)
                    for action in list_available_act_directions:
                        list_possible_actions.append(action)

        list_possible_actions.append(ACT_WAIT)
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
        transformed_waste = self.knowledge.get_transformed_waste()
        bool_covering = self.knowledge.get_bool_covering()
        target_position = self.knowledge.get_target_position()

        # If the agent is in covering mode
        if bool_covering:
            list_possible_actions = super().deliberate_covering()

        # If the agent is in normal mode
        else: 
            # If the agent has a target position to reach
            if target_position is not None:
                list_possible_actions = self.deliberate_go_to_target()

            # If the agent has no target position to reach
            else:
                # Check up and down cells for agents
                list_available_act_directions = []
                if self.can_go_up():
                    list_available_act_directions.append(ACT_GO_UP)
                if self.can_go_down():
                    list_available_act_directions.append(ACT_GO_DOWN)

                # Check if there is a waste to transform
                if self.can_transform():
                    list_possible_actions.append(ACT_TRANSFORM)

                # Check if agent has a transformed waste and if it can go right or drop it
                if transformed_waste != None:
                    # Check if cell at the right is in zone 3
                    if grid_radioactivity[self.pos[0]+1][self.pos[1]] == 3:
                        # Check if the current cell does not already contain a waste
                        if grid_knowledge[self.pos[0]][self.pos[1]] == 0:
                            list_possible_actions.append(ACT_DROP_TRANSFORMED_WASTE)
                        else:
                            if len(list_available_act_directions) > 0 :
                                # Randomize the order of possible moves
                                rd.shuffle(list_available_act_directions)
                                for action in list_available_act_directions:
                                    list_possible_actions.append(action)
                            else:
                                list_possible_actions.append(ACT_WAIT)
                    else:
                        # Move to the right to drop the waste
                        list_possible_actions.append(ACT_GO_RIGHT)
                
                # Pick up the waste if the conditions are filled
                if self.can_pick_up():
                    list_possible_actions.append(ACT_PICK_UP)

                # Check if cell at the left is still in zone 2
                if self.can_go_left():
                    list_available_act_directions.append(ACT_GO_LEFT)
                # Check if the cell is in zone 1 and if it contains an yellow waste
                elif grid_knowledge[self.pos[0]-1][self.pos[1]] == 2:
                    list_available_act_directions.append(ACT_GO_LEFT)
                if self.can_go_right():
                    # Check if cell at the right is in zone 2 (yellow agent can't go in zone 3)
                    if grid_radioactivity[self.pos[0]+1][self.pos[1]] != 3 :
                        list_available_act_directions.append(ACT_GO_RIGHT)

                # Possible best moves if there is an agent close
                list_new_possible_actions = self.deliberate_go_to_pick_close_waste()
                for action in list_new_possible_actions:
                        list_possible_actions.append(action)

                # Randomize the order of possible moves
                if len(list_available_act_directions) > 0:
                    rd.shuffle(list_available_act_directions)
                    for action in list_available_act_directions:
                        list_possible_actions.append(action)

        list_possible_actions.append(ACT_WAIT)
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
        Determines all possible actions based on the current knowledge of the environment.

        Parameters
        ----------
        None

        Returns
        -------
        list_possible_actions : list
            A list of possible actions the agent can take based on its knowledge.
        """
        # Get data from knowledge
        grid_knowledge, _ = self.knowledge.get_grids()
        picked_up_wastes = self.knowledge.get_picked_up_wastes()
        bool_covering = self.knowledge.get_bool_covering()
        target_position = self.knowledge.get_target_position()

        # If the agent is in mode covering but not at the good start position yet
        if bool_covering:
            list_possible_actions = super().deliberate_covering()

        # If the agent is in normal mode
        else:
            # If the agent has a target position to reach
            if target_position is not None:
                list_possible_actions = self.deliberate_go_to_target()

            # If the agent has no target position to reach
            else:
                # Check up and down available directions
                list_available_act_directions = []

                # Check up and down cells for agents
                list_available_act_directions = []
                if self.can_go_up():
                    list_available_act_directions.append(ACT_GO_UP)
                if self.can_go_down():
                    list_available_act_directions.append(ACT_GO_DOWN)
                
                # If we picked up a waste, go to waste disposal zone to drop it
                if len(picked_up_wastes) == 1:
                    if grid_knowledge[self.pos[0]][self.pos[1]] == 4:
                        list_possible_actions.append(ACT_DROP_ONE_WASTE)
                    else:
                        # The agent goes to the waste disposal zone column
                        if self.can_go_right():
                            list_possible_actions.append(ACT_GO_RIGHT)
                        else:
                            waste_disposal_zone_position = np.where(grid_knowledge == 4)
                            # If the Waste disposal zone is above the agent
                            if waste_disposal_zone_position[1] > self.pos[1]:
                                if self.can_go_up():
                                    list_possible_actions.append(ACT_GO_UP)
                            # If the Waste disposal zone is below the agent
                            else:
                                if self.can_go_down():
                                    list_possible_actions.append(ACT_GO_DOWN)

                # Check if there is a waste to pick up and if we can pick up a waste
                if self.can_pick_up():
                    list_possible_actions.append(ACT_PICK_UP)

                # Check if cell at the left is in zone 3
                if self.can_go_left():
                    list_available_act_directions.append(ACT_GO_LEFT)
                # Check if the cell is in zone 2 and if it contains a red waste
                elif grid_knowledge[self.pos[0]-1][self.pos[1]] == 3:
                    list_available_act_directions.append(ACT_GO_LEFT)
                if self.can_go_right():
                    list_available_act_directions.append(ACT_GO_RIGHT)

                # Possible best moves if there is a waste close
                list_new_possible_actions = self.deliberate_go_to_pick_close_waste()
                for action in list_new_possible_actions:
                        list_possible_actions.append(action)

                # Randomize the order of possible moves
                if len(list_available_act_directions) > 0:
                    rd.shuffle(list_available_act_directions)
                    for action in list_available_act_directions:
                        list_possible_actions.append(action)

        list_possible_actions.append(ACT_WAIT)
        print("Red agent", self.unique_id, "has the possible actions :", list_possible_actions)
        return list_possible_actions

class Chief(CleaningAgent):
    
    def __init__(self, unique_id, model, grid_size, pos_waste_disposal):
        """
        Initializes the Chief Agent with provided parameters.

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

        self.grid_size = grid_size
        # Initialise waste disposal zone position in knowledge
        grid_knowledge = np.full((grid_size[0], grid_size[1]), 9)
        grid_knowledge[pos_waste_disposal[0]][pos_waste_disposal[1]] = 4
        self.knowledge = ChiefAgentKnowledge(
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
        # Receive the messages
        self.receive_messages()
        # Update chief knowledge with the agents perception
        self.update_chief_with_agents_knowledge()
        # Send important information to the superior chief
        self.send_information_chief()
        # Update chief knowledge with the information from other chiefs
        self.update_chief_information_knowledge()
        # Send orders to the other agents
        self.send_orders()
        # Receive the orders he just sent to himself
        self.receive_orders()
        # Determine all possible actions based on current knowledge
        list_possible_actions = self.deliberate()
        # Perform the action and update the percepts
        self.percepts = self.model.do(
            self, list_possible_actions=list_possible_actions)
        # Do the update from the CleaningAgent class
        self.update()

    def receive_messages(self):
        list_messages = self.get_new_messages()
        self.list_received_percepts_and_data = []
        self.list_information_chief = []
        message: Message
        for message in list_messages:
            other_agent = message.get_exp()

            # The chief has received the percept from an agent
            if message.get_performative() == MessagePerformative.SEND_PERCEPTS_AND_DATA:
                percepts = message.get_content()
                # Store the percepts to later update its knowledge
                self.list_received_percepts_and_data.append({"agent" : other_agent, "percepts" : percepts})

            elif message.get_performative() == MessagePerformative.SEND_INFORMATION_CHIEF_DROP:
                content = message.get_content()
                self.list_information_chief.append({"chief": other_agent, "information": content})

        print("Chief", self.unique_id, "received messages as perceived and data :", self.list_received_percepts_and_data)
        print("Chief", self.unique_id, "received messages as information from other chief :", self.list_information_chief)

    def update(self):
        """
        Updates the chief agent's knowledge based on its percepts.

        Parameters
        ----------
        None

        Returns
        -------
        None 
        """
        # Do the update from the Chief class
        super().update()
        self.update_left_right_column()
        grid_knowledge, grid_radioactivity = self.knowledge.get_grids()
        bool_cleaned_right_column = self.knowledge.get_bool_cleaned_right_column()
        direction_clean_right_column = self.knowledge.get_direction_clean_right_column()
        _, _, _, right_zone = self.get_specificities_type_agent()
        grid_height = grid_knowledge.shape[1]

        actual_position = self.pos

        if not bool_cleaned_right_column:

            # Update the boolean when he has finish to clean the right column
            if direction_clean_right_column == "up" and actual_position[1] == grid_height - 1 :
                bool_cleaned_right_column = True
                self.knowledge.set_bool_cleaned_right_column(bool_cleaned_right_column)
            if direction_clean_right_column == "down" and actual_position[1] == 0:
                bool_cleaned_right_column = True
                self.knowledge.set_bool_cleaned_right_column(bool_cleaned_right_column)
            
            # Update the direction to clean right column if he has reach one of the starting positions
            if direction_clean_right_column is None and grid_radioactivity[actual_position[0] + 1][actual_position[1]] == right_zone and actual_position[1] in [0, grid_height - 1]:
                if actual_position[1] == 0:
                    direction_clean_right_column = "up"
                else:
                    direction_clean_right_column = "down"
                self.knowledge.set_direction_clean_right_column(direction_clean_right_column)

    def update_left_right_column(self):
        list_green_yellow_red_left_columns = self.knowledge.get_list_green_yellow_red_left_columns()
        list_green_yellow_red_right_columns = self.knowledge.get_list_green_yellow_red_right_columns()
        
        for counter in range(len(list_green_yellow_red_left_columns)):
            if counter == 0:
                mode = "green"
            elif counter == 1:
                mode = "yellow"
            else:
                mode = "red"
            # Left zone column
            if list_green_yellow_red_left_columns[counter] is None:
                list_green_yellow_red_left_columns[counter] = self.get_green_yellow_red_left_column(mode)
            # Right zone column
            if list_green_yellow_red_right_columns[counter] is None:
                list_green_yellow_red_right_columns[counter] = self.get_green_yellow_red_right_column(mode)

        self.knowledge.set_list_green_yellow_red_left_columns(list_green_yellow_red_left_columns)
        self.knowledge.set_list_green_yellow_red_right_columns(list_green_yellow_red_right_columns)

    def update_chief_information_knowledge(self):
        grid_knowledge, grid_radioactivity = self.knowledge.get_grids()
        for information in self.list_information_chief:
            information_chief = information["information"] # position of the dropped waste
            _, type_waste, left_zone, _ = self.get_specificities_type_agent()

            grid_knowledge[information_chief[0]][information_chief[1]] = type_waste
            grid_radioactivity[information_chief[0]][information_chief[1]] = left_zone # dropped cell is the left zone
        self.knowledge.set_grids(grid_knowledge, grid_radioactivity)

    def get_green_yellow_red_left_column(self, mode: Literal["green", "yellow", "red"]):
        """
        Get the first column for zones 1, 2 and 3.
        
        Parameters
        ----------
        mode : Literal["green", "yellow", "red"]
            Depending if we are in zone 1, 2 or 3.
        
        Returns
        -------
        int
            Id of the column.
        """
        if mode == "green":
            return 0
        _, grid_radioactivity = self.knowledge.get_grids()
        zone_to_detect = 1 if mode == "yellow" else 2
        for counter_column in range(grid_radioactivity.shape[0]-1, -1, -1):
            current_column = grid_radioactivity[counter_column]
            if True in [int(row) == zone_to_detect for row in current_column]:
                return counter_column + 1
            
    def get_green_yellow_red_right_column(self, mode: Literal["green", "yellow", "red"]):
        """
        Get the first column for zones 1, 2 and 3.
        
        Parameters
        ----------
        mode : Literal["green", "yellow", "red"]
            Depending if we are in zone 1, 2 or 3.
        
        Returns
        -------
        int
            Id of the column.
        """
        _, grid_radioactivity = self.knowledge.get_grids()
        if mode == "red":
            return grid_radioactivity.shape[0] - 1

        zone_to_detect = 2 if mode == "green" else 3
        counter = 0
        for column in grid_radioactivity:
            if True in [int(row) == zone_to_detect for row in column]:
                return counter - 1
            counter += 1

    def send_information_chief(self):
        dict_chiefs = self.knowledge.get_dict_chiefs()
        dict_knowledge_agents = self.knowledge.get_dict_agents_knowledge()
        dict_knowledge_agents[self.get_name()] = {
            "action": self.percepts["action_done"]["action"],
            "position": self.pos
        }

        for agent_name in dict_knowledge_agents:
            dict_knowledge = dict_knowledge_agents[agent_name]
            # Inform the other chief that a transformed waste has been dropped on the border
            if dict_knowledge["action"] == ACT_DROP_TRANSFORMED_WASTE:
                agent_position = dict_knowledge["position"]
                chief: Chief = dict_chiefs["yellow"] if type(self) == ChiefGreenAgent else dict_chiefs["red"]
                self.send_message(Message(self.get_name(), chief.get_name(), MessagePerformative.SEND_INFORMATION_CHIEF_DROP, agent_position))

    def update_chief_with_agents_knowledge(self):
        """
        Updates the chief agent's knowledge based on its percepts

        Parameters
        ----------
        None

        Returns
        -------
        None 
        """
        grid_knowledge, grid_radioactivity = self.knowledge.get_grids()
        dict_agents_knowledge = self.knowledge.get_dict_agents_knowledge()

        # Update the knowledge with the percepts received from the other agents
        for element in self.list_received_percepts_and_data:
            agent = element["agent"]
            percepts_and_data = element["percepts"]

            # Update the grid with the waste position knowledge of the other agents
            for key in percepts_and_data["positions"]:
                list_objects_tile = percepts_and_data["positions"][key]
                if not list_objects_tile is None: # If the tile is the grid 

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

                        if type(element) == Radioactivity:
                            if element.zone == "z1":
                                grid_radioactivity[key[0]][key[1]] = 1
                            elif element.zone == "z2":
                                grid_radioactivity[key[0]][key[1]] = 2
                            elif element.zone == "z3":
                                grid_radioactivity[key[0]][key[1]] = 3
                
            # Update the knowledge of the chief with the number of wastes and the transformed waste
            dict_agents_knowledge[agent] = {
                "nb_wastes" : percepts_and_data["nb_wastes"],
                "transformed_waste" : percepts_and_data["transformed_waste"],
                "position": percepts_and_data["position"],
                "bool_covering": percepts_and_data["bool_covering"],
                "direction_covering": percepts_and_data["direction_covering"],
                "target_position": percepts_and_data["target_position"],
                "action": percepts_and_data["action"]}
        
        # Set the updated knowledge
        self.knowledge.set_dict_agents_knowledge(dict_agents_knowledge=dict_agents_knowledge)
        self.knowledge.set_grids(grid_knowledge=grid_knowledge, grid_radioactivity=grid_radioactivity)
        self.update_left_right_column()

    def deliberate_cover_last_column(self):
        # Get data from knowledge
        direction_clean_right_column = self.knowledge.get_direction_clean_right_column()
        grid_knowledge, _ = self.knowledge.get_grids()
        grid_height = grid_knowledge.shape[1]
        actual_position = self.pos
        list_possible_actions = []

        # First the chief goes to upper right or lower right position
        if direction_clean_right_column is None:
            # If the chief is in the upper part of the grid, it goes up
            if actual_position[1] > grid_height // 2:
                # If the chief can go up, it goes up
                if self.can_go_up():
                    list_possible_actions.append(ACT_GO_UP)
                # If the chief can't go up, it goes right (to still move closer to the right column)
                elif self.can_go_right():
                    list_possible_actions.append(ACT_GO_RIGHT)
            # If the chief is in the lower part of the grid, it goes down
            else:
                # If the chief can go down, it goes down
                if self.can_go_down():
                    list_possible_actions.append(ACT_GO_DOWN)
                # If the chief can't go down, it goes right (to still move closer to the right column)
                elif self.can_go_right():
                    list_possible_actions.append(ACT_GO_RIGHT)

            list_possible_actions.append(ACT_WAIT)
        
        # If the chief has started to clean the column and not finished
        else:

            # Check if there is a waste to transform
            if self.can_transform():
                list_possible_actions.append(ACT_TRANSFORM)
            # Check if agent has a transformed waste and drop it
            if self.can_drop_transformed_waste():
                list_possible_actions.append(ACT_DROP_TRANSFORMED_WASTE)
            # Check if there is a waste to pick up and if we can pick up a waste
            if self.can_pick_up():
                list_possible_actions.append(ACT_PICK_UP)

            # Clean the column in the direction from its position
            if direction_clean_right_column == "up":
                if self.can_go_up():
                    list_possible_actions.append(ACT_GO_UP)

            elif direction_clean_right_column == "down":
                if self.can_go_down():
                    list_possible_actions.append(ACT_GO_DOWN)

            list_possible_actions.append(ACT_WAIT)
        
        return list_possible_actions

    def deliberate(self):
        """
        Determines all possible actions based on the current knowledge of the environment.

        Parameters
        ----------
        None

        Returns
        -------
        list_possible_actions : list
            A list of possible actions the agent can take based on its knowledge.
        """
        # Get data from knowledge
        bool_cleaned_right_column = self.knowledge.get_bool_cleaned_right_column()

        if not bool_cleaned_right_column:
            list_possible_actions = self.deliberate_cover_last_column()
        else:
            list_possible_actions = super().deliberate()

        return list_possible_actions

    def find_closest_waste_to_agent(self, agent_name, agent_position):
        """
        Find the closest waste for an agent.
        
        Parameters
        ----------
        agent_name : int
            Unique id of the agent to assign the closest waste.
        
        agent_position : tuple
            Position of the agent.
        
        Returns
        -------
        position_closest_waste : tuple
            Position of the closest waste to the agent
        """
        grid_knowledge, _ = self.knowledge.get_grids()
        dict_target_position_agent = self.knowledge.get_dict_target_position_agent()
        position_closest_waste = None
        closest_distance = grid_knowledge.shape[0] + grid_knowledge.shape[1]
        _, type_waste, _, _ = self.get_specificities_type_agent()

        for counter_column in range(grid_knowledge.shape[0]):
            for counter_row in range(grid_knowledge.shape[1]):
                tile_content = grid_knowledge[counter_column][counter_row]

                # If the waste has not been attributed for now
                if type_waste == tile_content and (counter_column, counter_row) not in dict_target_position_agent:

                    # If the waste is closer
                    distance = abs(counter_column - agent_position[0]) + abs(counter_row - agent_position[1])
                    if distance < closest_distance:
                        closest_distance = distance
                        position_closest_waste = (counter_column, counter_row)

        # Write this waste has been attributed to an agent
        if position_closest_waste is not None:
            dict_target_position_agent[(counter_column, counter_row)] = agent_name
            self.knowledge.set_dict_target_position_agent(dict_target_position_agent=dict_target_position_agent)
        
        return position_closest_waste

    def find_best_rows_to_cover(self, agent_position, rows_being_covered):
        grid_height = len(rows_being_covered)
        # First start to cover the extremities
        if rows_being_covered[1] == 0 and rows_being_covered[grid_height-2] == 0:
            # The agent is in the upper part of the screen
            if agent_position[1] > grid_height//2:
                return grid_height - 2
            # The agent is in the upper part of the screen
            else:
                return 1
        elif rows_being_covered[1] == 0:
            return 1
        elif rows_being_covered[grid_height - 2] == 0:
            return grid_height - 2
        
        # Cover when there are three rows adjacent not covered
        for counter in range(1, grid_height-1):
            if rows_being_covered[counter-1] == 0 and rows_being_covered[counter] == 0 and rows_being_covered[counter+1] == 0:
                return counter
            
        # Cover when there are two rows adjacent not covered
        for counter in range(1, grid_height-1):
            if (rows_being_covered[counter-1] == 0 and rows_being_covered[counter] == 0) or (rows_being_covered[counter+1] == 0 and rows_being_covered[counter] == 0):
                return counter
            
        # Cover the single row not covered
        for counter in range(1, grid_height-1):
            if rows_being_covered[counter] == 0:
                return counter

    def send_orders_covering(self):
        dict_knowledge_agents = self.knowledge.get_dict_agents_knowledge()
        grid_knowledge, _ = self.knowledge.get_grids()
        grid_height = grid_knowledge.shape[1]
        rows_being_covered = self.knowledge.get_rows_being_covered()
        green_left_column, yellow_left_column, red_left_column = self.knowledge.get_list_green_yellow_red_left_columns()
        green_right_column, yellow_right_column, red_right_column = self.knowledge.get_list_green_yellow_red_right_columns()

        # The chief can now send orders to himself
        dict_knowledge_agents[self.get_name()] = {
            "bool_covering": self.knowledge.get_bool_covering(),
            "direction_covering": self.knowledge.get_direction_covering(),
            "position": self.pos,
            "target_position": self.knowledge.get_target_position()
        }

        # Send orders for each agent, depending on their current knowledge
        for agent_name in dict_knowledge_agents:
            dict_knowledge = dict_knowledge_agents[agent_name]
            bool_covering = dict_knowledge["bool_covering"]
            direction_covering = dict_knowledge["direction_covering"]
            agent_position = dict_knowledge["position"]
            target_position = dict_knowledge["target_position"]

            # If the agent is in covering mode
            if bool_covering:
                # If the agent is waiting for an order
                if target_position is None and direction_covering is None:
                    # Send the order to start a new covering (the closest to the agent) if there are still rows to cover
                    if 0 in rows_being_covered:
                        # Choose the best row to cover (which is ideally covering two other rows)
                        id_row_to_go = self.find_best_rows_to_cover(agent_position=agent_position, rows_being_covered=rows_being_covered)

                        # Update the rows being covered
                        rows_being_covered[id_row_to_go] = 1
                        if id_row_to_go != 0:
                            rows_being_covered[id_row_to_go-1] = 1
                        if id_row_to_go != grid_height - 1:
                            rows_being_covered[id_row_to_go+1] = 1
                        
                        # Determine the position to go if the agent is already on the left column of its zone
                        if agent_position[0] in [green_left_column, yellow_left_column, red_left_column]:
                            position_to_go = (agent_position[0], id_row_to_go)
                        else:
                            if type(self) == ChiefGreenAgent:
                                if green_right_column is not None:
                                    green_right_column -= 1
                                position_to_go = (green_right_column, id_row_to_go)
                            elif type(self) == ChiefYellowAgent:
                                if yellow_right_column is not None:
                                    yellow_right_column -= 1
                                position_to_go = (yellow_right_column, id_row_to_go)
                            else:
                                position_to_go = (red_right_column, id_row_to_go)
                        print("Chief is sending the order to cover row", id_row_to_go, "to agent", agent_name)
                        # Send the order to go to this position
                        self.send_message(Message(self.get_name(), agent_name, MessagePerformative.SEND_ORDERS, position_to_go))

                    # Send the order to stop covering when there is nothing more to cover
                    else:
                        self.send_message(Message(self.get_name(), agent_name, MessagePerformative.SEND_ORDERS, STOP_COVERING))
                        print("Chief is sending the order to stop covering to agent", agent_name)
                        
        # Update the knowledge of the chief with the rows being covered
        self.knowledge.set_rows_being_covered(rows_being_covered=rows_being_covered)

    def send_target_orders(self):
        dict_knowledge_agents = self.knowledge.get_dict_agents_knowledge()

        # The chief can now send orders to himself
        dict_knowledge_agents[self.get_name()] = {
            "bool_covering": self.knowledge.get_bool_covering(),
            "position": self.pos,
            "target_position": self.knowledge.get_target_position(),
            "transformed_waste": self.knowledge.get_transformed_waste(),
            "nb_wastes": len(self.knowledge.get_picked_up_wastes())
        }

        # Send orders for each agent, depending on their current knowledge
        for agent_name in dict_knowledge_agents:
            dict_knowledge = dict_knowledge_agents[agent_name]
            agent_position = dict_knowledge["position"]
            bool_covering = dict_knowledge["bool_covering"]
            target_position = dict_knowledge["target_position"]
            transformed_waste = dict_knowledge["transformed_waste"]
            nb_wastes = dict_knowledge["nb_wastes"]

            # If the agent is not in covering mode
            if not bool_covering:
                # If the agent has no target to follow and has no waste to drop
                if target_position is None and transformed_waste is None and (type(self) is not ChiefRedAgent or nb_wastes == 0):
                    # Find the closest waste to the agent
                    closest_waste_position = self.find_closest_waste_to_agent(agent_name, agent_position)
                    if closest_waste_position is not None:
                        # Send the order to go to this closest waste
                        self.send_message(Message(self.get_name(), agent_name, MessagePerformative.SEND_ORDERS, closest_waste_position))
                        print("Chief is sending the order to", agent_name, "to go clean the waste at", closest_waste_position)

    def send_orders(self):
        grid_knowledge, _ = self.knowledge.get_grids()
        
        # If the grid is not finished to be covered, the chief will send orders of coverage if necessary
        if np.any(grid_knowledge == 9):
            self.send_orders_covering()
        # If the grid is covered, the chief will send orders to the agents to clean the nearest waste
        self.send_target_orders()

class ChiefGreenAgent(Chief, GreenAgent):
    def __init__(self, unique_id, model, grid_size, pos_waste_disposal):
        """
        Initializes the Chief Agent with provided parameters.

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

        # The green chief is not covering anything
        self.knowledge.set_bool_covering(False)


class ChiefYellowAgent(Chief, YellowAgent):
    def __init__(self, unique_id, model, grid_size, pos_waste_disposal):
        """
        Initializes the Chief Agent with provided parameters.

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

        # The yellow chief is not covering anything
        self.knowledge.set_bool_covering(False)

    
class ChiefRedAgent(Chief, RedAgent):
    def __init__(self, unique_id, model, grid_size, pos_waste_disposal):
        """
        Initializes the Chief Agent with provided parameters.

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

        # The red chief does not have to clean the last column
        self.knowledge.set_bool_cleaned_right_column(True)


#################
### Constants ###
#################

DICT_CLASS_COLOR = {
    GreenAgent: "green",
    ChiefGreenAgent : "green",
    YellowAgent: "yellow",
    ChiefYellowAgent: "yellow",
    RedAgent: "red",
    ChiefRedAgent: "red"
}
