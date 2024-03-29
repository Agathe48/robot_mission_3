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
    Waste,
    WasteDisposalZone
)
from tools.tools_constants import (
    GRID_HEIGHT,
    GRID_WIDTH
)

from agents import (
    GreenAgent,
    YellowAgent,
    RedAgent
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
        if agent.zone == "z1":
            portrayal["Color"] = "#b4deb8"
        elif agent.zone == "z2":
            portrayal["Color"] = "#fdec82"
        else:
            portrayal["Color"] = "#ff9688"

    # For the radioactivity objects
    if type(agent) == WasteDisposalZone:
        portrayal = {
            "Shape": "rect",
            "Filled": "true",
            "w": 1,
            "h": 1,
            "Layer": 1}

        # Set the color with the shade of greens
        portrayal["Color"] = "brown"

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

    # For the cleaning agents
    if type(agent) in [GreenAgent, YellowAgent, RedAgent]:
        portrayal = {
            "Shape": "circle",
            "Filled": "true",
            "r": 0.5,
            "Layer": 3
        }
        if type(agent) == GreenAgent:
            portrayal["Color"] = "#073d00"
        elif type(agent) == YellowAgent:
            portrayal["Color"] = "#ffa800"
        elif type(agent) == RedAgent:
            portrayal["Color"] = "#a90000"

    return portrayal

grid = CanvasGrid(
    portrayal_method = agent_portrayal,
    grid_width = GRID_WIDTH,
    grid_height = GRID_HEIGHT,
    canvas_width = 600,
    canvas_height = 600 * GRID_HEIGHT / GRID_WIDTH
)

# chart = ChartModule([{"Label": "Gini",
#                       "Color": "Black"}],
#                     data_collector_name='datacollector')

server = ModularServer(
    model_cls=Area,
    visualization_elements=[grid],
    name="Area",
    model_params={
        "dict_nb_agents": {"green": 3, "yellow": 2, "red": 2},
        "width":GRID_WIDTH,
        "height":GRID_HEIGHT
    }
)

server.port = 8523
server.launch()

             