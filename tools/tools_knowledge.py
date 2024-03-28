"""
Python tools file for the knowledge class.

Group 3:
- Oumaima CHATER
- Laure-Emilie MARTIN
- Agathe PLU
- Agathe POULAIN
"""

###############
### Imports ###
###############

### Python imports ###

import numpy as np

#############
### Class ###
#############

class AgentKnowledge:

    def __init__(self, grid, nb_wastes=0):
        self.grid_knowledge = grid
        self.grid_radioactivity = np.copy(grid)
        self.nb_wastes = nb_wastes
        self.transformed_waste = False
        self.left = False
        self.right = False
        self.up = False
        self.down = False

    def get_transformed_waste(self):
        return self.transformed_waste

    def get_nb_wastes(self):
        return self.nb_wastes

    def get_grids(self):
        return self.grid_knowledge, self.grid_radioactivity
    
    def get_left(self):
        return self.left
    
    def get_right(self):
        return self.right
    
    def get_up(self):
        return self.up
    
    def get_down(self):
        return self.down

    def set_transformed_waste(self, boolean_transform_waste):
        self.transformed_waste = boolean_transform_waste

    def set_nb_wastes(self, nb_wastes):
        self.nb_wastes  = nb_wastes
    
    def set_grids(self, grid_knowledge, grid_radioactivity):
        self.grid_knowledge = grid_knowledge
        self.grid_radioactivity = grid_radioactivity

    def set_left(self, boolean_left):
        self.left = boolean_left

    def set_right(self, boolean_right):
        self.right = boolean_right
    
    def set_up(self, boolean_up):
        self.up = boolean_up

    def set_down(self, boolean_down):
        self.down = boolean_down

    def __str__(self) -> str:
        return f"AgentKnowledge(grid_knowledge={self.grid_knowledge}, grid_radioactivity={self.grid_radioactivity}, nb_wastes={self.nb_wastes}, transformed_waste={self.transformed_waste}, left={self.left}, right={self.right}, up={self.up}, down={self.down})"
        
