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
            "scale" :0.95,
            "Shape" : "ressources/waste_disposal_zone_illustration.png"}

    # For the wastes objects
    if type(agent) == Waste:
        portrayal = {"Layer": 2}
        
        portrayal["Color"] = agent.type_waste

        if portrayal["Color"] == "green" :
            portrayal["Shape"] = "ressources/green_waste3.png"
            portrayal["scale"] = 0.4

        if portrayal["Color"] == "yellow" :
            portrayal["Shape"] = "ressources/yellow_waste3.png"
            portrayal["scale"] = 0.4

        if portrayal["Color"] == "red" :
            portrayal["Shape"] = "ressources/red_waste3.png"
            portrayal["scale"] = 0.4


    # For the cleaning and chief agents
    if type(agent) in [GreenAgent, ChiefGreenAgent, YellowAgent, ChiefYellowAgent, RedAgent, ChiefRedAgent]:
        portrayal = {"Layer": 3}

        picked_up_wastes = agent.knowledge.get_picked_up_wastes()
        transformed_waste = agent.knowledge.get_transformed_waste()


        if type(agent) in [GreenAgent, ChiefGreenAgent]:

            if type(agent) is GreenAgent:
                portrayal["Shape"] = "ressources/green_agent.png"
                portrayal["scale"] = 0.7
                if len(picked_up_wastes) == 1:
                    portrayal["Shape"] = "ressources/green_agent_1_green_waste.png"
                    portrayal["scale"] = 0.7
                if len(picked_up_wastes) == 2:
                    portrayal["Shape"] = "ressources/green_agent_2_green_waste.png"
                    portrayal["scale"] = 0.7
                if not transformed_waste is None:
                    portrayal["Shape"] = "ressources/green_agent_yellow_waste.png"
                    portrayal["scale"] = 0.7

            if type(agent) is ChiefGreenAgent:
                portrayal["Shape"] = "ressources/green_chief.png"
                portrayal["scale"] = 0.9
                if len(picked_up_wastes) == 1:
                    portrayal["Shape"] = "ressources/green_chief_1_green_waste.png"
                    portrayal["scale"] = 0.9
                if len(picked_up_wastes) == 2:
                    portrayal["Shape"] = "ressources/green_chief_2_green_waste.png"
                    portrayal["scale"] = 0.9
                if not transformed_waste is None:
                    portrayal["Shape"] = "ressources/green_chief_yellow_waste.png"
                    portrayal["scale"] = 0.9

        elif type(agent) in [YellowAgent, ChiefYellowAgent]:

            if type(agent) is YellowAgent:
                portrayal["Shape"] = "ressources/yellow_agent.png"
                portrayal["scale"] = 0.7
                if len(picked_up_wastes) == 1:
                    portrayal["Shape"] = "ressources/yellow_agent_1_yellow_waste.png"
                    portrayal["scale"] = 0.7
                if len(picked_up_wastes) == 2:
                    portrayal["Shape"] = "ressources/yellow_agent_2_yellow_waste.png"
                    portrayal["scale"] = 0.7
                if not transformed_waste is None:
                    portrayal["Shape"] = "ressources/yellow_agent_1_red_waste.png"
                    portrayal["scale"] = 0.7

            if type(agent) is ChiefYellowAgent:
                portrayal["Shape"] = "ressources/yellow_chief.png"
                portrayal["scale"] = 0.9
                if len(picked_up_wastes) == 1:
                    portrayal["Shape"] = "ressources/yellow_chief_1_yellow_waste.png"
                    portrayal["scale"] = 0.9
                if len(picked_up_wastes) == 2:
                    portrayal["Shape"] = "ressources/yellow_chief_2_yellow_waste.png"
                    portrayal["scale"] = 0.9
                if not transformed_waste is None:
                    portrayal["Shape"] = "ressources/yellow_chief_1_red_waste.png"
                    portrayal["scale"] = 0.9
            
        elif type(agent) in [RedAgent, ChiefRedAgent]:
            portrayal["Color"] = "#a90000"
            # portrayal["text_color"] = "white"
            if type(agent) is RedAgent:
                portrayal["Shape"] = "ressources/red_agent.png"
                portrayal["scale"] = 0.7
                if len(picked_up_wastes) == 1:
                    portrayal["Shape"] = "ressources/red_agent_1_red_waste.png"
                    portrayal["scale"] = 0.7

            if type(agent) is ChiefRedAgent:
                portrayal["Shape"] = "ressources/red_chief2.png"
                portrayal["scale"] = 0.9
                if len(picked_up_wastes) == 1:
                    portrayal["Shape"] = "ressources/red_chief_1_red_waste.png"
                    portrayal["scale"] = 0.9

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
# chart = ChartModule([{"Label": "Gini",
#                       "Color": "Black"}],
#                     )

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
    visualization_elements=[grid, chart_element],
    name="Area",
    model_params=model_params
)

server.port = 8523
server.launch()

             