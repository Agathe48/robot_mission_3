"""
Python tools file for the knowledge class.

Group 3:
- Oumaima CHATER
- Laure-Emilie MARTIN
- Agathe PLU
- Agathe POULAIN
"""

#############
### Class ###
#############

class AgentKnowledge:

    def __init__(self, grid_knowledge, grid_radioactivity):
        self.grid_knowledge = grid_knowledge
        self.grid_radioactivity = grid_radioactivity
        self.picked_up_wastes = []
        self.transformed_waste = None
        self.left = True
        self.right = True
        self.up = True
        self.down = True

    def get_transformed_waste(self):
        return self.transformed_waste

    def get_picked_up_wastes(self):
        return self.picked_up_wastes

    def get_grids(self):
        return self.grid_knowledge, self.grid_radioactivity
    
    def get_left(self):
        return self.left
    
    def get_right(self):
        return self.right
    
    def get_up(self):
        return self.up
    
    def get_down(self):
        """
        Return the boolean according if the agent can go down.

        Parameters
        ----------
        None

        Returns
        -------
        bool
        """
        return self.down

    def set_transformed_waste(self, object_transform_waste):
        """
        Set transformed waste in knowledge.

        Parameters
        ----------
        object_transform_waste: Waste
            The transformed waste.

        Returns
        -------
        None
        """
        self.transformed_waste = object_transform_waste

    def set_picked_up_wastes(self, picked_up_wastes):
        self.picked_up_wastes = picked_up_wastes
    
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
        return f"AgentKnowledge(grid_knowledge={self.grid_knowledge}, grid_radioactivity={self.grid_radioactivity}, picked_up_wastes={self.picked_up_wastes}, transformed_waste={self.transformed_waste}, left={self.left}, right={self.right}, up={self.up}, down={self.down})"
        
