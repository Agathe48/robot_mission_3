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
    Area
)

#############
### Model ###
#############

model = Area(
    dict_nb_agents={"green": 1, "yellow": 1, "red": 1}
)
model.run_model(step_count = 1000)
