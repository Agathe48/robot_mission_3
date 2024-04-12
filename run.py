"""
Main Python file to launch the simulation.

Group 3:
- Oumaima CHATER
- Laure-Emilie MARTIN
- Agathe PLU
- Agathe POULAIN
"""

###############
### Imports ###
###############

### Local imports ###

from model import (
    RobotMission
)

#############
### Model ###
#############

model = RobotMission(
    nb_green_agents=4,
    nb_yellow_agents=0,
    nb_red_agents=0
)

counter_step = 0
while True:
    bool_exit = model.step()
    counter_step += 1
    if counter_step == 2:
        break
    if bool_exit:
        break

print("The simulation has stopped and has lasted for", counter_step, "steps.")
