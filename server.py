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
    Radioactivity,
    Waste
)
from tools.tools_constants import (
    GRID_HEIGHT,
    GRID_WIDTH
)

#################
### Main code ###
#################


def agent_portrayal(agent):

    # For the radioactivity objects
    if type(agent) == Radioactivity:
        portrayal = {
            "Shape": "rect",
            "Filled": "true",
            "w": 1,
            "h": 1,
            "Layer": 0}

        # Set the color with the shade of greens
        portrayal["Color"] = "#4fae50"

    # For the cleaning agents
    if type(agent) == Waste:
        portrayal = {
            "Shape": "circle",
            "Filled": "true",
            "r": 0.5,
            "Layer": 1}

        # Set the color of the agent according to its type
        portrayal["Color"] = "red"

    # For the wastes objects
    if type(agent) == Waste:
        portrayal = {
            "Shape": "rect",
            "Filled": "true",
            "w": 0.25,
            "h": 0.25,
            "Layer": 2}

        # Set the color of the waste according to its type
        portrayal["Color"] = agent.type_waste

    return portrayal

grid = CanvasGrid(
    portrayal_method = agent_portrayal,
    grid_width = GRID_WIDTH,
    grid_height = GRID_HEIGHT,
    canvas_width = 300,
    canvas_height = 300 * GRID_HEIGHT / GRID_WIDTH
)

# chart = ChartModule([{"Label": "Gini",
#                       "Color": "Black"}],
#                     data_collector_name='datacollector')

server = ModularServer(
    model_cls=Area,
    visualization_elements=[grid],
    name="Area",
    model_params={
        "nb_agents":1,
        "width":GRID_WIDTH,
        "height":GRID_HEIGHT}) #, "density": mesa.visualization.Slider("Agent density", 0.8, 0.1, 1.0, 0.1)})

server.port = 8523
server.launch()
