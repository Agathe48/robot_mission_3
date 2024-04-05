"""
Python tools file for the constants of the program.

Group 3:
- Oumaima CHATER
- Laure-Emilie MARTIN
- Agathe PLU
- Agathe POULAIN
"""

GRID_SIZE = (9, 18)
GRID_HEIGHT = GRID_SIZE[0]
GRID_WIDTH = GRID_SIZE[1]
WASTE_DENSITY = 0.3

DICT_NUMBER_TYPE_CONTENT = {
    0: "Empty tile",
    1: "Waste Green",
    2: "Waste Yellow",
    3: "Waste Red",
    4: "Waste disposal zone"
}

###############
### ACTIONS ###
###############

ACT_PICK_UP = "pick_up"
ACT_DROP_TRANSFORMED_WASTE = "drop_transformed_waste"
ACT_DROP_ONE_WASTE = "drop_one_waste"
ACT_TRANSFORM = "transform"
ACT_GO_LEFT = "go_left"
ACT_GO_RIGHT = "go_right"
ACT_GO_UP = "go_up"
ACT_GO_DOWN = "go_down"
ACT_WAIT = "wait"

