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

from mesa import Model, DataCollector
from mesa.space import MultiGrid

### Local imports ###

from objects import (
    Radioactivity,
    Waste,
    WasteDisposalZone
)
from tools.tools_constants import (
    GRID_HEIGHT,
    GRID_WIDTH,
    WASTE_DENSITY,
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
from agents import (
    ChiefGreenAgent,
    ChiefYellowAgent,
    ChiefRedAgent,
    GreenAgent,
    YellowAgent,
    RedAgent,
    CleaningAgent,
    DICT_CLASS_COLOR
)
from schedule import (
    CustomRandomScheduler
)
from communication.message.MessageService import (
    MessageService
)

#############
### Model ###
#############

class RobotMission(Model):
    
    def __init__(self, nb_green_agents: int, nb_yellow_agents: int, nb_red_agents: int, waste_density=WASTE_DENSITY, width=GRID_WIDTH, height=GRID_HEIGHT):
        """
        Initializes the Environment object with provided parameters.

        Parameters
        ----------
        nb_green_agents : int
            The number of green agents
        nb_yellow_agents : int
            The number of yellow agents
        nb_red_agents : int
            The number of red agents
        waste_density : float
            The density of waste in the environment.
        width : int
            The width of the grid.
        height : int
            The height of the grid.

        Returns
        -------
        None 
        """
        super().__init__()

        self.dict_nb_agents = {
            "green": nb_green_agents,
            "yellow": nb_yellow_agents,
            "red": nb_red_agents
        }
        self.width = width
        self.height = height
        self.grid = MultiGrid(self.width, self.height, torus=False)
        self.schedule = CustomRandomScheduler(self)
        self.__messages_service = MessageService(self.schedule)
        self.waste_density = waste_density

        # Initialize the grid with the zones
        self.init_grid()

        # Initialize the waste on the grid
        self.init_wastes()
        
        # Initialize the agents on the grid
        self.init_agents()

        self.datacollector = DataCollector(
            {
                "nb_green_waste": lambda m: sum(1 for agent in m.schedule.agents if isinstance(agent, Waste) and agent.type_waste == "green"),
                "nb_yellow_waste": lambda m: sum(1 for agent in m.schedule.agents if isinstance(agent, Waste) and agent.type_waste == "yellow"),
                "nb_red_waste": lambda m: sum(1 for agent in m.schedule.agents if isinstance(agent, Waste) and agent.type_waste == "red"),
                "nb_messages_chief_to_agent": lambda m: m.__messages_service.nb_messages_chief_to_agent,
                "nb_messages_agent_to_chief": lambda m: m.__messages_service.nb_messages_agent_to_chief,
                "nb_messages_chief_to_chief": lambda m: m.__messages_service.nb_messages_chief_to_chief
            }
        )

    def init_grid(self):
        """
        Initializes the grid environment with radioactivity zones and a waste disposal zone.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """

        # Define the position of the waste disposal zone (in the right column of the grid)
        self.pos_waste_disposal = (self.width-1, rd.randint(0, self.height-1))

        # Create the grid with radioactivity zones and the waste disposal zone
        zone_width = self.width // 3
        remaining_width = self.width % 3

        extra_width_distribution = [zone_width] * 3

        # If there are 2 extra columns, we need to ensure they aren't added to the same zone
        if remaining_width == 2:
            # Choose two different zones randomly
            zone_indices = [0, 1, 2]
            rd.shuffle(zone_indices)
            extra_width_distribution[zone_indices[0]] += 1
            extra_width_distribution[zone_indices[1]] += 1
        elif remaining_width == 1:
            # Distribute the remaining width randomly among the zones
            zone_index = rd.randint(0, 2)
            extra_width_distribution[zone_index] += 1
        # Store the dimensions of each zone
        self.zone_dimensions = [
            (0, extra_width_distribution[0]),  # Green zone
            (extra_width_distribution[0], extra_width_distribution[0] + extra_width_distribution[1]),  # Yellow zone
            (extra_width_distribution[0] + extra_width_distribution[1], self.width)  # Red zone
        ]
                
        for i in range(self.height):
            for j in range(self.width):
                
                # Green area
                if j < extra_width_distribution[0]: 
                    rad = Radioactivity(unique_id = self.next_id(), model=self, zone = "z1", radioactivity_level=rd.random()/3)
                    self.schedule.add(rad)
                    self.grid.place_agent(rad, (j, i))
                
                # Yellow area
                elif extra_width_distribution[0] <= j < extra_width_distribution[0]+ extra_width_distribution[1]: 
                    rad = Radioactivity(unique_id = self.next_id(), model=self, zone = "z2", radioactivity_level=(rd.random()/3) + 0.33)
                    self.schedule.add(rad)
                    self.grid.place_agent(rad, (j, i))
                
                # Red area
                else:
                    if (j, i) != self.pos_waste_disposal:
                        rad = Radioactivity(unique_id = self.next_id(), model=self, zone = "z3", radioactivity_level=(rd.random()/3) + 0.66)
                        self.schedule.add(rad)
                        self.grid.place_agent(rad, (j, i))
                    else:
                        dis = WasteDisposalZone(unique_id = self.next_id(), model=self)
                        self.schedule.add(dis)
                        self.grid.place_agent(dis, self.pos_waste_disposal)

    def init_wastes(self):
        """
        Initializes waste objects on the grid environment.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        # Place the wastes on the grid
        self.nb_wastes_total = int(self.height*self.width*self.waste_density)
        # Get the dimensions of each zone
        green_zone, yellow_zone, red_zone = self.zone_dimensions
        number_green_tiles = (green_zone[1] - green_zone[0]) * self.height
        number_yellow_tiles = (yellow_zone[1] - yellow_zone[0]) * self.height
        number_red_tiles = (red_zone[1] - red_zone[0]) * self.height

        # Treat the edge case of waste density equal to 1
        if self.waste_density == 1:
            self.nb_wastes_green = number_green_tiles
            if self.nb_wastes_green % 2 != 0:
                self.nb_wastes_green -= 1
            self.nb_wastes_yellow = number_yellow_tiles
            if (self.nb_wastes_yellow + self.nb_wastes_green//2) % 2 != 0:
                self.nb_wastes_yellow -= 1
            self.nb_wastes_red = number_red_tiles - 1
        else:
            wasted_correctly_placed = False
            while not wasted_correctly_placed:
                self.nb_wastes_green = rd.randint(
                    max(0, self.nb_wastes_total - 2*number_green_tiles + 1),
                    min(self.nb_wastes_total, number_green_tiles))

                # Check that we have an even number of green wastes
                if self.nb_wastes_green % 2 != 0:
                    if self.nb_wastes_green == min(self.nb_wastes_total, number_yellow_tiles):
                        self.nb_wastes_green -= 1
                    else:
                        self.nb_wastes_green += 1
                
                self.nb_wastes_yellow = rd.randint(
                    max(0, self.nb_wastes_total - 2*number_red_tiles + 1), 
                    max(0, min(self.nb_wastes_total - self.nb_wastes_green, number_yellow_tiles)))

                # Check that we have an even number of yellow and green pairs wastes
                if (self.nb_wastes_yellow + self.nb_wastes_green//2) % 2 != 0:
                    if self.nb_wastes_yellow == min(self.nb_wastes_total - self.nb_wastes_green, number_yellow_tiles):
                        self.nb_wastes_yellow -= 1
                    else:
                        self.nb_wastes_yellow += 1
                
                self.nb_wastes_red = max(0, self.nb_wastes_total - self.nb_wastes_green - self.nb_wastes_yellow)
                
                # If there are not too many wastes in one single zone
                if self.nb_wastes_red <= number_red_tiles - 1:
                    wasted_correctly_placed = True

        print("nb initial green waste : ", self.nb_wastes_green)
        print("nb initial yellow waste : ", self.nb_wastes_yellow)
        print("nb initial red waste : ", self.nb_wastes_red)

        list_waste_types_colors = [
            [self.nb_wastes_green, "green", green_zone],
            [self.nb_wastes_yellow, "yellow",  yellow_zone],
            [self.nb_wastes_red, "red", red_zone],
        ]

        # Create the waste randomly generated in the map
        for element in list_waste_types_colors:
            nb_wastes_types = element[0]
            waste_color = element[1]
            allowed_zone = element[2]
            for waste in range(nb_wastes_types):
                was = Waste(unique_id = self.next_id(), model = self, type_waste = waste_color)
                self.schedule.add(was)
                correct_position = False
                while not correct_position:
                    # Randomly place the waste objects on the grid
                    x = self.random.randrange(allowed_zone[0], allowed_zone[1])
                    y = self.random.randrange(self.height)
                    cellmates = self.grid.get_cell_list_contents((x,y))

                    # We check to see if there is already a waste object in the cell
                    bool_contains_waste = False
                    for element in cellmates: 
                        if type(element) in [Waste, WasteDisposalZone]:
                            bool_contains_waste = True
                    if not bool_contains_waste:
                        correct_position = True
                        self.grid.place_agent(was, (x, y))
                        
    def init_agents(self):
        """
        Initializes cleaning agents on the grid environment.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        # Get the dimensions of each zone
        green_zone, yellow_zone, red_zone = self.zone_dimensions
        list_agent_types_colors = [
            [self.dict_nb_agents["green"], GreenAgent, ChiefGreenAgent, green_zone],
            [self.dict_nb_agents["yellow"], YellowAgent, ChiefYellowAgent, yellow_zone],
            [self.dict_nb_agents["red"], RedAgent, ChiefRedAgent, red_zone],
        ]
        dict_chiefs = {
            "green": None,
            "yellow": None,
            "red": None
        }

        # Create the cleaning agents randomly generated in the map
        for element in list_agent_types_colors:
            nb_agent_types = element[0]
            agent_class = element[1]
            chief_agent_class = element[2]
            allowed_zone = element[3]
            chief_agent = True
            for agent in range(nb_agent_types):
                
                # Add the chief : the first agent
                if chief_agent:
                    ag = chief_agent_class(
                        unique_id = self.next_id(),
                        model = self,
                        grid_size = (self.width, self.height),
                        pos_waste_disposal = self.pos_waste_disposal 
                        )
                    chief_agent = False
                    dict_chiefs[DICT_CLASS_COLOR[chief_agent_class]] = ag

                else:
                    ag = agent_class(
                        unique_id = self.next_id(),
                        model = self,
                        grid_size = (self.width, self.height),
                        pos_waste_disposal = self.pos_waste_disposal 
                        )

                self.schedule.add(ag)
                correct_position = False
                while not correct_position:
                    # Randomly place the waste objects on the grid
                    x = self.random.randrange(allowed_zone[0], allowed_zone[1])
                    y = self.random.randrange(self.height)
                    cellmates = self.grid.get_cell_list_contents((x,y))

                    # We check to see if there is already an agent in the cell
                    bool_contains_agent = False
                    for element in cellmates: 
                        if type(element) == agent_class or type(element) == chief_agent_class:
                            bool_contains_agent = True
                    if not bool_contains_agent:
                        correct_position = True
                        self.grid.place_agent(ag, (x, y))

                ag.percepts = self.do(
                    ag, list_possible_actions=[ACT_WAIT])
                ag.update()

        for agent in self.schedule.agents:
            # Update the knowledge of all agents with the chiefs
            if type(agent) in list(DICT_CLASS_COLOR.keys()):
                agent.knowledge.set_dict_chiefs(dict_chiefs)
            # Update the knowledge of the chiefs with their colored agent
            if type(agent) in [GreenAgent, YellowAgent, RedAgent]:
                agent.send_percepts_and_data()

    def step(self):
        """
        Executes a step in the simulation.

        Parameters
        ----------
        None

        Returns
        -------
        bool: 
            True if this is the end of the simulation.
        """
        self.__messages_service.dispatch_messages()
        # If all red agents are in bool_stop_acting, stop the simulation
        if any(type(agent) in [RedAgent, ChiefRedAgent] and not agent.knowledge.get_bool_stop_acting() for agent in self.schedule.agents):
        # if any(type(agent) == Waste for agent in self.schedule.agents):
            self.schedule.step()
            self.datacollector.collect(self)
        else:
            print("END OF THE SIMULATION <3")
            self.running = False
            return True
        
    def run_model(self, step_count=100):
        """
        Runs the simulation for a specified number of steps.

        Parameters
        ----------
        step_count : int (optional)
            The number of steps to run the simulation. Defaults to 100.

        Returns
        -------
        None
        """
        for i in range(step_count):
            self.step()

    def do(self, agent: CleaningAgent, list_possible_actions):
        """
        Performs an action for the given agent based on the list of possible actions and updates the percepts.

        Parameters
        ----------
        agent : CleaningAgent
            The cleaning agent performing the action.
        list_possible_actions : list
            A list of possible actions for the agent.

        Returns
        -------
        percepts: dict
            A dictionary representing the updated percepts after the action is performed.
        """
        agent_position = agent.pos
        action_done = {
            "action": "",
            "object": None
        }

        # Get the current cellmates of the agent
        cellmates = self.grid.get_cell_list_contents(agent_position)

        # Get the color of the agent
        color = DICT_CLASS_COLOR[type(agent)]

        transformed_waste = agent.knowledge.get_transformed_waste()
        picked_up_wastes = agent.knowledge.get_picked_up_wastes()
        agent.print_custom(f"I am in position {agent_position}, I have the transformed waste {transformed_waste} and have the picked up wastes {picked_up_wastes}.")

        for action in list_possible_actions:
            if action == ACT_PICK_UP:
                # Check if the waste is still there
                has_performed_action = False
                counter = 0

                while not has_performed_action and counter < len(cellmates):
                    obj = cellmates[counter]
                    if (isinstance(obj, Waste) and obj.type_waste == color) :
                        # Remove the waste from the grid and we keep the waste in the scheduler to keep trace of it
                        self.grid.remove_agent(obj)
                        has_performed_action = True
                    counter += 1

                if has_performed_action:
                    agent.print_custom("I picked up the waste", obj)
                    action_done["object"] = obj
                    break

            elif action == ACT_DROP_TRANSFORMED_WASTE:
                # Check if there is no waste in the cell
                if not any(isinstance(obj, Waste) for obj in cellmates):
                    if color != "red":
                        # Get the transformed waste object and place it on the grid
                        self.grid.place_agent(transformed_waste, agent_position)
                        agent.print_custom("I dropped a waste.")
                    break

            elif action == ACT_DROP_ONE_WASTE:
                # Check if there is no waste in the cell
                if not any(isinstance(obj, Waste) for obj in cellmates):
                    if color!= "red":
                        # Get the picked up waste and place it on the grid 
                        self.grid.place_agent(picked_up_wastes[0], agent_position)
                        agent.print_custom(f"I dropped a {color} waste.")
                    else:
                        self.schedule.remove(picked_up_wastes[0])
                        agent.print_custom("I destroyed a waste in the waste disposal zone.")
                    break


            elif action == ACT_TRANSFORM:
                # If agent is green, transform the waste to yellow
                if color == "green":
                    waste = Waste(unique_id = self.next_id(), model = self, type_waste="yellow")
                # If agent is yellow, transform the waste to red
                elif color == "yellow":
                    waste = Waste(unique_id = self.next_id(), model = self, type_waste="red")

                self.schedule.add(waste)
                action_done["object"] = waste

                # Remove the former wastes from the scheduler
                for waste in picked_up_wastes:
                    self.schedule.remove(waste)

                agent.print_custom("I transformed a waste.")
                break

            elif action == ACT_GO_LEFT:
                next_x = agent_position[0] - 1
                next_y = agent_position[1]
                next_cell_contents = self.grid.get_cell_list_contents((next_x, next_y))
                if not any(isinstance(obj, CleaningAgent) for obj in next_cell_contents):
                    self.grid.move_agent(agent, (next_x, next_y))
                    agent.print_custom("I went left.")
                    break

            elif action == ACT_GO_RIGHT:
                next_x = agent_position[0] + 1
                next_y = agent_position[1]
                next_cell_contents = self.grid.get_cell_list_contents((next_x, next_y))
                if not any(isinstance(obj, CleaningAgent) for obj in next_cell_contents):
                    self.grid.move_agent(agent, (next_x, next_y))
                    agent.print_custom("I went right.")
                    break

            elif action == ACT_GO_UP:
                next_x = agent_position[0]
                next_y = agent_position[1] + 1
                next_cell_contents = self.grid.get_cell_list_contents((next_x, next_y))
                if not any(isinstance(obj, CleaningAgent) for obj in next_cell_contents):
                    self.grid.move_agent(agent, (next_x, next_y))
                    agent.print_custom("I went up.")
                    break
            
            elif action == ACT_GO_DOWN:
                next_x = agent_position[0]
                next_y = agent_position[1] - 1
                next_cell_contents = self.grid.get_cell_list_contents((next_x, next_y))
                if not any(isinstance(obj, CleaningAgent) for obj in next_cell_contents):
                    self.grid.move_agent(agent, (next_x, next_y))
                    agent.print_custom("I went down.")
                    break

            elif action == ACT_WAIT:
                agent.print_custom("I waited.")
                break

        action_done["action"] = action
        agent_position = agent.pos

        # Initialize the percepts
        percepts = {
            "positions": {
                agent_position: self.grid.get_cell_list_contents(agent_position)
            },
            "action_done": action_done
        }

        if agent_position[0] - 1 >= 0:
            percepts["positions"][(agent_position[0] - 1, agent_position[1])] = self.grid.get_cell_list_contents((agent_position[0] - 1, agent_position[1]))
        else:
            percepts["positions"][(agent_position[0] - 1, agent_position[1])] = None
        if agent_position[0] + 1 < self.width:
            percepts["positions"][(agent_position[0] + 1, agent_position[1])] = self.grid.get_cell_list_contents((agent_position[0] + 1, agent_position[1]))
        else:
            percepts["positions"][(agent_position[0] + 1, agent_position[1])] = None
        if agent_position[1] - 1 >= 0:
            percepts["positions"][(agent_position[0], agent_position[1] - 1)] = self.grid.get_cell_list_contents((agent_position[0], agent_position[1] - 1))
        else:
            percepts["positions"][(agent_position[0], agent_position[1] - 1)] = None
        if agent_position[1] + 1 < self.height:
            percepts["positions"][(agent_position[0], agent_position[1] + 1)] = self.grid.get_cell_list_contents((agent_position[0], agent_position[1] + 1))
        else :
            percepts["positions"][(agent_position[0], agent_position[1] + 1)] = None
            
        return percepts