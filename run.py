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
    dict_nb_agents={"green": 2, "yellow": 2, "red": 2}
)

counter_step = 0
while True:
    bool_exit = model.step()
    counter_step += 1
    if bool_exit:
        break

print("The simulation has stopped and has lasted for", counter_step, "steps.")
