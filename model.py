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
    ACT_PICK_UP,
    ACT_DROP,
    ACT_TRANSFORM,
    ACT_GO_LEFT,
    ACT_GO_RIGHT,
    ACT_GO_UP,
    ACT_GO_DOWN,
    ACT_WAIT
)
from agents import (
    GreenAgent,
    YellowAgent,
    RedAgent,
    CleaningAgent
)
from schedule import CustomRandomScheduler


DICT_CLASS_COLOR = {
    GreenAgent: "green",
    YellowAgent: "yellow",
    RedAgent: "red"
}

#############
### Model ###
#############

class Area(Model):
    """A model with some number of agents."""

    def __init__(self, dict_nb_agents: dict, waste_density=0.3, width=GRID_WIDTH, height=GRID_HEIGHT):
        super().__init__()
        self.dict_nb_agents = dict_nb_agents
        self.width = width
        self.height = height
        self.grid = MultiGrid(self.width, self.height, torus=False)
        self.schedule = CustomRandomScheduler(self)
        self.waste_density = waste_density

        # Initialize the grid with the zones
        self.init_grid()
        print(self.pos_waste_disposal)

        # Initialize the waste on the grid
        self.init_wastes()
        
        # Initialize the agents on the grid
        self.init_agents()

        # self.datacollector = DataCollector(
        #     model_reporters={"Gini": compute_gini},
        #     agent_reporters={"Wealth": "wealth"})
        
        # self.running = True

    def init_grid(self):

        # Define the position of the waste disposal zone (in the right column of the grid)
        self.pos_waste_disposal = (self.width-1, rd.randint(0, self.height-1))

        # Create the grid with radioactivity zones and the waste disposal zone

        for i in range(self.height):
            for j in range(self.width):
                
                # Green area
                if j < self.width // 3: 
                    rad = Radioactivity(unique_id = self.next_id(), model=self, zone = "z1", radioactivity_level=rd.random()/3)
                    self.schedule.add(rad)
                    self.grid.place_agent(rad, (j, i))
                
                # Yellow area
                elif self.width // 3 <= j < 2 * self.width // 3: 
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
        # Place the wastes on the grid
        self.nb_wastes_total = int(self.height*self.width*self.waste_density)
        number_tiles_per_zone = int(self.width/3*self.height)

        wasted_correctly_placed = False
        while not wasted_correctly_placed:
            self.nb_wastes_green = rd.randint(
                max(0, self.nb_wastes_total - 2*number_tiles_per_zone),
                min(self.nb_wastes_total-1, number_tiles_per_zone-1))

            # Check that we have an even number of green wastes
            if self.nb_wastes_green % 2 != 0:
                self.nb_wastes_green += 1
            
            self.nb_wastes_yellow = rd.randint(
                max(0, self.nb_wastes_total - 2*number_tiles_per_zone), 
                min(self.nb_wastes_total - self.nb_wastes_green - 1, number_tiles_per_zone - 1))

            # Check that we have an even number of yellow and green pairs wastes
            if (self.nb_wastes_yellow + self.nb_wastes_green//2) % 2 != 0:
                self.nb_wastes_yellow += 1
            
            self.nb_wastes_red = self.nb_wastes_total - self.nb_wastes_green - self.nb_wastes_yellow
            
            # If there are not too many wastes in one single zone
            if self.nb_wastes_red <= number_tiles_per_zone - 1:
                wasted_correctly_placed = True

        list_waste_types_colors = [
            [self.nb_wastes_green, "green", (0, self.width//3)],
            [self.nb_wastes_yellow, "yellow",  (self.width//3, 2*self.width//3)],
            [self.nb_wastes_red, "red", (2*self.width//3, self.width)],
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
        
        list_agent_types_colors = [
            [self.dict_nb_agents["green"], GreenAgent, (0, self.width//3)],
            [self.dict_nb_agents["yellow"], YellowAgent,  (self.width//3, 2*self.width//3)],
            [self.dict_nb_agents["red"], RedAgent, (2*self.width//3, self.width)],
        ]

        # Create the cleaning agents randomly generated in the map
        for element in list_agent_types_colors:
            nb_agent_types = element[0]
            agent_class = element[1]
            allowed_zone = element[2]
            for agent in range(nb_agent_types):
                ag = agent_class(
                    unique_id = self.next_id(),
                    model = self,
                    grid_size= (self.width, self.height),
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
                        if type(element) == agent_class:
                            bool_contains_agent = True
                    if not bool_contains_agent:
                        correct_position = True
                        self.grid.place_agent(ag, (x, y))

    def step(self):
        self.schedule.step()
        # self.datacollector.collect(self)
        
    def run_model(self, step_count=100):
        for i in range(step_count):
            self.step()

    def do(self, agent: CleaningAgent, list_possible_actions):
        agent_position = agent.pos

        # Get the current cellmates of the agent
        cellmates = self.grid.get_cell_list_contents(agent_position)

        # Get the color of the agent
        color = DICT_CLASS_COLOR[type(agent)]

        transformed_waste = agent.knowledge.get_transformed_waste()
        print("Agent", agent.unique_id, "is in position", agent_position, "and has the transformed waste", transformed_waste)

        for action in list_possible_actions:
            if action == ACT_PICK_UP:
                # Check if the waste is still there
                has_performed_action = False
                counter = 0
                current_waste_count = agent.knowledge.get_nb_wastes()

                while not has_performed_action and counter < len(cellmates):
                    obj = cellmates[counter]
                    if (isinstance(obj, Waste) and obj.type_waste == color) :
                        # Remove the waste from the grid and update the agent knowledge
                        # We keep the waste in the scheduler to keep trace of it
                        self.grid.remove_agent(obj)
                        agent.knowledge.set_nb_wastes(nb_wastes = current_waste_count + 1)
                        has_performed_action = True
                    counter += 1

                if has_performed_action:
                    print("Agent", agent.unique_id, "picked up a waste")
                    break

            elif action == ACT_DROP:
                # Check if there is no waste in the cell
                if not any(isinstance(obj, Waste) for obj in cellmates):
                    # Get the transformed waste object and place it on the grid
                    transformed_waste = agent.knowledge.get_transformed_waste()
                    self.grid.place_agent(transformed_waste, agent_position)
                    # Update agent knowledge with no transformed waste
                    agent.knowledge.set_transformed_waste(object_transform_waste = None)
                    print("Agent", agent.unique_id, "dropped a waste")
                    break

            elif action == ACT_TRANSFORM:
                # If agent is green, transform the waste to yellow
                if color == "green":
                    waste = Waste(unique_id = self.next_id(), model = self, type_waste="yellow")
                # If agent is yellow, transform the waste to red
                elif color == "yellow":
                    waste = Waste(unique_id = self.next_id(), model = self, type_waste="red")
                # Update the agent knowledge with the transformed waste object and create the object in the scheduler
                agent.knowledge.set_transformed_waste(object_transform_waste = waste)
                agent.knowledge.set_nb_wastes(nb_wastes = 0)
                self.schedule.add(waste)
                print("Agent", agent.unique_id, "transformed a waste")
                break

            elif action == ACT_GO_LEFT:
                next_x = agent_position[0] - 1
                next_y = agent_position[1]
                next_cell_contents = self.grid.get_cell_list_contents((next_x, next_y))
                if not any(isinstance(obj, CleaningAgent) for obj in next_cell_contents):
                    self.grid.move_agent(agent, (next_x, next_y))
                    print("Agent", agent.unique_id, "went left")
                    break

            elif action == ACT_GO_RIGHT:
                next_x = agent_position[0] + 1
                next_y = agent_position[1]
                next_cell_contents = self.grid.get_cell_list_contents((next_x, next_y))
                if not any(isinstance(obj, CleaningAgent) for obj in next_cell_contents):
                    self.grid.move_agent(agent, (next_x, next_y))
                    print("Agent", agent.unique_id, "went right")
                    break

            elif action == ACT_GO_UP:
                next_x = agent_position[0]
                next_y = agent_position[1] + 1
                next_cell_contents = self.grid.get_cell_list_contents((next_x, next_y))
                if not any(isinstance(obj, CleaningAgent) for obj in next_cell_contents):
                    self.grid.move_agent(agent, (next_x, next_y))
                    print("Agent", agent.unique_id, "went up")
                    break
            
            elif action == ACT_GO_DOWN:
                next_x = agent_position[0]
                next_y = agent_position[1] - 1
                next_cell_contents = self.grid.get_cell_list_contents((next_x, next_y))
                if not any(isinstance(obj, CleaningAgent) for obj in next_cell_contents):
                    self.grid.move_agent(agent, (next_x, next_y))
                    print("Agent", agent.unique_id, "went down")
                    break

            elif action == ACT_WAIT:
                pass
                print("Agent", agent.unique_id, "waited")   
                break

        agent_position = agent.pos
        # Initialize the percepts
        percepts = {
            agent_position: self.grid.get_cell_list_contents(agent_position)
        }

        if agent_position[0] - 1 >= 0:
            percepts[(agent_position[0] - 1, agent_position[1])] = self.grid.get_cell_list_contents((agent_position[0] - 1, agent_position[1]))
        if agent_position[0] + 1 < self.width:
            percepts[(agent_position[0] + 1, agent_position[1])] = self.grid.get_cell_list_contents((agent_position[0] + 1, agent_position[1]))
        if agent_position[1] - 1 >= 0:
            percepts[(agent_position[0], agent_position[1] - 1)] = self.grid.get_cell_list_contents((agent_position[0], agent_position[1] - 1))
        if agent_position[1] + 1 < self.height:
            percepts[(agent_position[0], agent_position[1] + 1)] = self.grid.get_cell_list_contents((agent_position[0], agent_position[1] + 1))
        
        return percepts