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
from mesa.time import RandomActivation
from mesa.space import MultiGrid

### Local imports ###

from objects import (
    Radioactivity,
    Waste,
    WasteDisposalZone
)
from tools.tools_constants import (
    GRID_HEIGHT,
    GRID_WIDTH
)

#############
### Model ###
#############

class Area(Model):
    """A model with some number of agents."""
   # density is used only for illustration
    def __init__(self, nb_agents, waste_density=0.3, width=GRID_WIDTH, height=GRID_HEIGHT, density=0.8):
        super().__init__()
        self.nb_agents = nb_agents
        self.width = width
        self.height = height
        self.grid = MultiGrid(self.width, self.height, True)
        self.schedule = RandomActivation(self)
        self.waste_density = waste_density

        ### Create the grid with zones ###

        # Define the position of the waste disposal zone (in the right column of the grid)
        pos_waste_disposal = (self.width-1, rd.randint(0, self.height-1))

        # Create the grid with radioactivity zones and the waste disposal zone

        for i in range(self.height):
            for j in range(self.width):
                
                # Green area
                if j < self.width // 3: 
                    rad = Radioactivity(unique_id = [i , j], model=self, zone = "z1", radioactivity_level=rd.random()/3)
                    self.schedule.add(rad)
                    self.grid.place_agent(rad, (j, i))
                
                # Yellow area
                elif self.width // 3 <= j < 2 * self.width // 3: 
                    rad = Radioactivity(unique_id = [i , j], model=self, zone = "z2", radioactivity_level=rd.random()/3)
                    self.schedule.add(rad)
                    self.grid.place_agent(rad, (j, i))
                
                # Red area
                else:
                    if (j, i) != pos_waste_disposal:
                        rad = Radioactivity(unique_id = [i , j], model=self, zone = "z3", radioactivity_level=rd.random()/3)
                        self.schedule.add(rad)
                        self.grid.place_agent(rad, (j, i))
                    else:
                        dis = WasteDisposalZone(unique_id = [i , j], model=self)
                        self.schedule.add(dis)
                        self.grid.place_agent(dis, pos_waste_disposal)

        ### Place wastes on the grid ###

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

        print(self.nb_wastes_green, self.nb_wastes_yellow, self.nb_wastes_red)

        # Create the waste randomly generated in the map
        for element in list_waste_types_colors:
            nb_wastes_types = element[0]
            waste_color = element[1]
            allowed_zone = element[2]
            for waste in range(nb_wastes_types):
                was = Waste(unique_id = waste, model = self, type_waste = waste_color)
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

        # self.datacollector = DataCollector(
        #     model_reporters={"Gini": compute_gini},
        #     agent_reporters={"Wealth": "wealth"})
        
        # self.running = True

    def step(self):
        self.schedule.step()
        # self.datacollector.collect(self)
        
    def run_model(self, step_count=100):
        model = Area(nb_agents = 1)  # 50 agents in our example
        for i in range(step_count):
            self.step()


        
