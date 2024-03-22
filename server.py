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

from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule

### Local imports ###

from model import (
    Area
)
from objects import (
    Radioactivity
)
from tools.tools_constants import (
    GRID_HEIGHT,
    GRID_WIDTH
)

#################
### Main code ###
#################


def agent_portrayal(agent):
    if type(agent) == Radioactivity:
        portrayal = {
            "Shape": "rect",
            "Filled": "true",
            "w": 1,
            "h": 1,
            "Layer": 0}

        # Change here the color with the shade of greens
        portrayal["Color"] = "green"

    return portrayal

grid = CanvasGrid(
    portrayal_method = agent_portrayal,
    grid_width = GRID_WIDTH,
    grid_height = GRID_HEIGHT,
    canvas_width = 300, 
    canvas_height = 200
)

# chart = ChartModule([{"Label": "Gini",
#                       "Color": "Black"}],
#                     data_collector_name='datacollector')

server = ModularServer(
    model_cls=Area,
    visualization_elements=[grid],
    name="Area",
    model_params={"nb_agents":1, "width":GRID_WIDTH, "height":GRID_HEIGHT}) #, "density": mesa.visualization.Slider("Agent density", 0.8, 0.1, 1.0, 0.1)})

server.port = 8523
server.launch()
