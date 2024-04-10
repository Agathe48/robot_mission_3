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
import mesa.visualization

### Local imports ###

from model import (
    RobotMission
)
from objects import (
    Radioactivity,
    Waste,
    WasteDisposalZone
)
from tools.tools_constants import (
    GRID_HEIGHT,
    GRID_WIDTH,
    WASTE_DENSITY
)

from agents import (
    GreenAgent,
    ChiefGreenAgent,
    YellowAgent,
    ChiefYellowAgent,
    RedAgent,
    ChiefRedAgent
)

#################
### Main code ###
#################


def agent_portrayal(agent):
    """
    Defines how agents are visually represented in the visualization.

    Parameters
    ----------
    agent : Agent
        An instance of an agent subclass representing an entity in the simulation.

    Returns
    -------
    portrayal : dict
        A dictionary specifying the portrayal of the agent in the visualization.
    """

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
            "Layer": 1,
            "scale" : 0.95,
            "Shape" : "ressources/waste_disposal_zone.png"}

    # For the wastes objects
    if type(agent) == Waste:
        portrayal = {"Layer": 2}
        
        portrayal["Color"] = agent.type_waste

        if portrayal["Color"] == "green" :
            portrayal["Shape"] = "ressources/green_waste2.png"
            portrayal["scale"] = 0.4

        if portrayal["Color"] == "yellow" :
            portrayal["Shape"] = "ressources/yellow_waste2.png"
            portrayal["scale"] = 0.4

        if portrayal["Color"] == "red" :
            portrayal["Shape"] = "ressources/red_waste2.png"
            portrayal["scale"] = 0.4


    # For the cleaning and chief agents
    if type(agent) in [GreenAgent, ChiefGreenAgent, YellowAgent, ChiefYellowAgent, RedAgent, ChiefRedAgent]:
        portrayal = {"Layer": 3}

        picked_up_wastes = agent.knowledge.get_picked_up_wastes()
        transformed_waste = agent.knowledge.get_transformed_waste()
        if len(picked_up_wastes) >= 1:
            portrayal["text"] = len(picked_up_wastes)
        if not transformed_waste is None:
            portrayal["text"] = "T"

        if type(agent) in [GreenAgent, ChiefGreenAgent]:
            portrayal["Color"] = "#073d00"
            portrayal["text_color"] = "white"

            if type(agent) is GreenAgent:
                portrayal["Shape"] = "ressources/green_agent.png"
                portrayal["scale"] = 0.7

            if type(agent) is ChiefGreenAgent:
                portrayal["Shape"] = "ressources/green_chief.png"
                portrayal["scale"] = 0.9

        elif type(agent) in [YellowAgent, ChiefYellowAgent]:
            portrayal["Color"] = "#ffa800"
            portrayal["text_color"] = "black"

            if type(agent) is YellowAgent:
                portrayal["Shape"] = "ressources/yellow_agent.png"
                portrayal["scale"] = 0.7

            if type(agent) is ChiefYellowAgent:
                portrayal["Shape"] = "ressources/yellow_chief.png"
                portrayal["scale"] = 0.9
            
        elif type(agent) in [RedAgent, ChiefRedAgent]:
            portrayal["Color"] = "#a90000"
            portrayal["text_color"] = "white"
            if type(agent) is RedAgent:
                portrayal["Shape"] = "ressources/red_agent.png"
                portrayal["scale"] = 0.7

            if type(agent) is ChiefRedAgent:
                portrayal["Shape"] = "ressources/red_chief2.png"
                portrayal["scale"] = 0.9

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

model_params = {
    "nb_green_agents": mesa.visualization.Slider("Initial number of green agents", 2, 1, 6, 1),
    "nb_yellow_agents": mesa.visualization.Slider("Initial number of yellow agents", 2, 1, 6, 1) ,
    "nb_red_agents": mesa.visualization.Slider("Initial number of red agents", 2, 1, 6, 1),
    "width": mesa.visualization.Slider("Grid width", GRID_WIDTH, 6, 30, 1),
    "height": mesa.visualization.Slider("Grid height", GRID_HEIGHT, 3, 20, 1),
    "waste_density": mesa.visualization.Slider("Initial waste density", WASTE_DENSITY, 0, 1, 0.1),
}

server = ModularServer(
    model_cls=RobotMission,
    visualization_elements=[grid],
    name="Area",
    model_params=model_params
)

server.port = 8523
server.launch()

             