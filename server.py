"""
Python file for the Visualization.

Group 3:
- Oumaima CHATER
- Laure-Emilie MARTIN
- Agathe PLU
- Agathe POULAIN
"""

###############
### Imports ###
###############

### Mesa imports ###

import mesa
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule

### Local imports ###

from model import Area
from tools.tools_constants import (
    GRID_HEIGHT,
    GRID_WIDTH
)

#################
### Main code ###
#################


def agent_portrayal(agent):
    portrayal = {"Shape": "square",
                 "Filled": "true",
                 "r": 0.5}

    portrayal["Color"] = "red"
    portrayal["Layer"] = 0

    # if agent.wealth > 0:
    #     portrayal["Color"] = "red"
    #     portrayal["Layer"] = 0
    # else:
    #     portrayal["Color"] = "grey"
    #     portrayal["Layer"] = 1
    #     portrayal["r"] = 0.2
    return portrayal

grid = CanvasGrid(portrayal_method = agent_portrayal, 
                  grid_width = GRID_WIDTH, 
                  grid_height = GRID_HEIGHT, 
                  canvas_width = 300, 
                  canvas_height = 200)

# chart = ChartModule([{"Label": "Gini",
#                       "Color": "Black"}],
#                     data_collector_name='datacollector')

server = ModularServer(Area,
                #    [grid, chart],
                    [grid],
                   "Area",
                   {"nb_agents":1, "width":GRID_WIDTH, "height":GRID_HEIGHT}) #, "density": mesa.visualization.Slider("Agent density", 0.8, 0.1, 1.0, 0.1)})


server.port = 8523 # The default
server.launch()