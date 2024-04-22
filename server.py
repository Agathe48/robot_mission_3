"""
Python file for the Visualization of the simulation.

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
from mesa.visualization.modules import CanvasGrid
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
    WASTE_DENSITY,
    PATH_RESOURCES
)

from agents import (
    GreenAgent,
    ChiefGreenAgent,
    YellowAgent,
    ChiefYellowAgent,
    RedAgent,
    ChiefRedAgent,
    DICT_CLASS_COLOR
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
            "scale": 0.95,
            "Shape": PATH_RESOURCES + "waste_disposal_zone_illustration.png"}

    # For the wastes objects
    if type(agent) == Waste:
        portrayal = {"Layer": 2}
        
        portrayal["Color"] = agent.type_waste
        path_image = PATH_RESOURCES + agent.type_waste + "_waste.png"
        portrayal["Shape"] = path_image
        portrayal["scale"] = 0.4

    # For the cleaning and chief agents
    if type(agent) in list(DICT_CLASS_COLOR.keys()):
        portrayal = {"Layer": 3}

        picked_up_wastes = agent.knowledge.get_picked_up_wastes()
        transformed_waste = agent.knowledge.get_transformed_waste()

        path_image = PATH_RESOURCES
        
        # Change the name of the image according to the agent's color
        if type(agent) in [GreenAgent, ChiefGreenAgent]:
            path_image += "green"
        elif type(agent) in [YellowAgent, ChiefYellowAgent]:
            path_image += "yellow" 
        elif type(agent) in [RedAgent, ChiefRedAgent]:
            path_image += "red"

        # Change the name of the image according to the agent's type
        if type(agent) in [ChiefGreenAgent, ChiefYellowAgent, ChiefRedAgent]:
            path_image += "_chief"
            scale = 0.9
        else:
            path_image += "_agent"
            scale = 0.7
        
        # Change the name of the image according to the wastes it possesses
        if len(picked_up_wastes) == 1:
            path_image += "_1_waste"
        elif len(picked_up_wastes) == 2:
            path_image += "_2_waste"
        if transformed_waste is not None:
            path_image += "_transformed_waste"

        path_image += ".png"

        portrayal["Shape"] = path_image
        portrayal["scale"] = scale

    return portrayal

grid = CanvasGrid(
    portrayal_method = agent_portrayal,
    grid_width = GRID_WIDTH,
    grid_height = GRID_HEIGHT,
    canvas_width = 600,
    canvas_height = 600 * GRID_HEIGHT / GRID_WIDTH
)
chart_element = mesa.visualization.ChartModule(
    [
        {"Label": "nb_green_waste", "Color": "#b4deb8"},
        {"Label": "nb_yellow_waste", "Color": "#fdec82"},
        {"Label": "nb_red_waste", "Color": "#ff9688"},
    ],
    data_collector_name='datacollector'
)

model_params = {
    "nb_green_agents": mesa.visualization.Slider("Initial number of green agents", 0, 1, 6, 1),
    "nb_yellow_agents": mesa.visualization.Slider("Initial number of yellow agents", 0, 1, 6, 1) ,
    "nb_red_agents": mesa.visualization.Slider("Initial number of red agents", 3, 1, 6, 1),
    "waste_density": mesa.visualization.Slider("Initial waste density", WASTE_DENSITY, 0, 1, 0.1)
}

server = ModularServer(
    model_cls=RobotMission,
    visualization_elements=[grid, chart_element],
    name="Area",
    model_params=model_params
)

server.port = 8523
server.launch()
             