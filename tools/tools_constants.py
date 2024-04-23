"""
Python tools file for the constants of the program.

Group 3:
- Oumaima CHATER
- Laure-Emilie MARTIN
- Agathe PLU
- Agathe POULAIN
"""
###############
### Imports ###
###############

from colorama import Fore

#############
### Paths ###
#############

PATH_RESOURCES = "resources/"

#######################
### Parametrization ###
#######################

GRID_SIZE = (9, 18)
GRID_HEIGHT = GRID_SIZE[0]
GRID_WIDTH = GRID_SIZE[1]
WASTE_DENSITY = 0.3

DICT_NUMBER_TYPE_CONTENT = {
    9: "Unknown content",
    0: "Empty tile",
    1: "Waste Green",
    2: "Waste Yellow",
    3: "Waste Red",
    4: "Waste disposal zone"
}

###############
### Actions ###
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

##############
### Orders ###
##############

ORDER_STOP_COVERING = "stop_covering"
ORDER_STOP_ACTING = "stop_acting"

##############
### Prints ###
##############

# To display the prints or not
DEBUG_MODE = True

def print_green_agent(agent_id, *args, **kwargs):
    print("[" + Fore.GREEN + str(agent_id) + Fore.RESET + "] ", *args, **kwargs)

def print_yellow_agent(agent_id, *args, **kwargs):
    print("[" + Fore.YELLOW + str(agent_id) + Fore.RESET + "] ", *args, **kwargs)

def print_red_agent(agent_id, *args, **kwargs):
    print("[" + Fore.RED + str(agent_id) + Fore.RESET + "] ", *args, **kwargs)

def print_green_chief(agent_id, *args, **kwargs):
    print("[" + Fore.GREEN + "Chief " + str(agent_id) + Fore.RESET + "] ", *args, **kwargs)

def print_yellow_chief(agent_id, *args, **kwargs):
    print("[" + Fore.YELLOW + "Chief " + str(agent_id) + Fore.RESET + "] ", *args, **kwargs)

def print_red_chief(agent_id, *args, **kwargs):
    print("[" + Fore.RED + "Chief " + str(agent_id) + Fore.RESET + "] ", *args, **kwargs)
