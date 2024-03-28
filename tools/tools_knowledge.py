"""
Python tools file for the knowledge class.

Group 3:
- Oumaima CHATER
- Laure-Emilie MARTIN
- Agathe PLU
- Agathe POULAIN
"""

class AgentKnowledge:

    def __init__(self, grid, nb_wastes=0):
        self.grid = grid
        self.nb_wastes = nb_wastes
        self.transformed_waste = False

    def set_transformed_waste(self, boolean_transform_waste):
        self.transformed_waste = boolean_transform_waste

    def increase_nb_waste(self):
        # Increase the number of wastes
        self.nb_wastes += 1
    
    
    def update_grid(self):
        pass
