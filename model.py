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
        self.nb_wastes = int(self.height*self.width*self.waste_density)
        # self.density= width/height #used only for illustration for the slider density
        
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

        # Create the waste randomly generated in the map
        for waste in range(self.nb_wastes):
            was = Waste(unique_id = waste, model = self, type_waste = "green")
            self.schedule.add(was)
            correct_position = False
            while not correct_position:
                # Randomly place the waste objects on the grid
                x = self.random.randrange(self.width)
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


        
