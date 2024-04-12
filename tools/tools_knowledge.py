"""
Python tools file for the knowledge class.

Group 3:
- Oumaima CHATER
- Laure-Emilie MARTIN
- Agathe PLU
- Agathe POULAIN
"""

import numpy as np

#############
### Class ###
#############

class AgentKnowledge:

    def __init__(self, grid_knowledge, grid_radioactivity):
        """
        Initialization of the agent's knowledge.

        Parameters
        ----------
        grid_knowledge : np.ndarray
            Represents the agent's knowledge of the grid.

        grid_radioactivity : np.ndarray
            Represents the agent's knowledge of the grid's radioactivity. 

        Returns
        -------
        None
        """
        self.grid_knowledge = grid_knowledge
        self.grid_radioactivity = grid_radioactivity
        self.picked_up_wastes = []
        self.transformed_waste = None
        self.left = True
        self.right = True
        self.up = True
        self.down = True
        self.dict_chiefs = {
            "green": [],
            "yellow": [],
            "red": []
        }

    def get_transformed_waste(self):
        """
        Return the transformed wastes if it is possible.

        Parameters
        ----------
        None

        Returns
        -------
        Waste | None
        """
        return self.transformed_waste

    def get_picked_up_wastes(self):
        """
        Return the list of the picked up wastes.

        Parameters
        ----------
        None

        Returns
        -------
        list[Waste]
        """
        return self.picked_up_wastes

    def get_grids(self):
        """
        Return the grid_knowledge and the grid_radioactivity.

        Parameters
        ----------
        None

        Returns
        -------
        np.ndarray, np.ndarray
        """
        return self.grid_knowledge, self.grid_radioactivity
    
    def get_left(self):
        """
        Return the boolean according if the agent can go left.

        Parameters
        ----------
        None

        Returns
        -------
        bool
        """
        return self.left
    
    def get_right(self):
        """
        Return the boolean according if the agent can go right.

        Parameters
        ----------
        None

        Returns
        -------
        bool
        """
        return self.right
    
    def get_up(self):
        """
        Return the boolean according if the agent can go up.

        Parameters
        ----------
        None

        Returns
        -------
        bool
        """
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
    
    def get_dict_chiefs(self):
        """
        Return the dictionary of chiefs.

        Parameters
        ----------
        None

        Returns
        -------
        dict
        """
        return self.dict_chiefs

    def set_transformed_waste(self, transformed_waste):
        """
        Set transformed waste in knowledge.

        Parameters
        ----------
        transformed_waste : Waste | None
            The transformed waste.

        Returns
        -------
        None
        """
        self.transformed_waste = transformed_waste

    def set_picked_up_wastes(self, picked_up_wastes):
        """
        Set picked up waste in knowledge.

        Parameters
        ----------
        picked_up_wastes: Waste
            The picked up waste.

        Returns
        -------
        None
        """
        self.picked_up_wastes = picked_up_wastes
    
    def set_grids(self, grid_knowledge, grid_radioactivity):
        """
        Set grid_knowledge and grid_radioactivity in knowledge.

        Parameters
        ----------
        grid_knowledge : np.ndarray
            Represents the agent's knowledge of the grid.

        grid_radioactivity : np.ndarray
            Represents the agent's knowledge of the grid's radioactivity.

        Returns
        -------
        None
        """
        self.grid_knowledge = grid_knowledge
        self.grid_radioactivity = grid_radioactivity

    def set_left(self, boolean_left):
        """
        Set boolean regarding the left action in knowledge.

        Parameters
        ----------
        boolean_left : bool
            Boolean according if the agent can go left.

        Returns
        -------
        None
        """
        self.left = boolean_left

    def set_right(self, boolean_right):
        """
        Set boolean regarding the right action in knowledge.

        Parameters
        ----------
        boolean_right : bool
            Boolean according if the agent can go right.

        Returns
        -------
        None
        """
        self.right = boolean_right
    
    def set_up(self, boolean_up):
        """
        Set boolean regarding the up action in knowledge.

        Parameters
        ----------
        boolean_up : bool
            Boolean according if the agent can go up.

        Returns
        -------
        None
        """
        self.up = boolean_up

    def set_down(self, boolean_down):
        """
        Set boolean regarding the down action in knowledge.

        Parameters
        ----------
        boolean_down : bool
            Boolean according if the agent can go down.

        Returns
        -------
        None
        """
        self.down = boolean_down

    def set_dict_chiefs(self, dict_chiefs):
        """
        Set dictionary of chiefs in knowledge.

        Parameters
        ----------
        dict_chiefs : dict
            Dictionary of chiefs.

        Returns
        -------
        None
        """
        self.dict_chiefs = dict_chiefs

    def __str__(self) -> str:
        return f"AgentKnowledge(grid_knowledge={np.flip(self.grid_knowledge.T,0)}, grid_radioactivity={np.flip(self.grid_radioactivity.T,0)}, picked_up_wastes={self.picked_up_wastes}, transformed_waste={self.transformed_waste}, left={self.left}, right={self.right}, up={self.up}, down={self.down}, dict_chiefs={self.dict_chiefs})"
        

class ChiefAgentKnowledge(AgentKnowledge):
    def __init__(self, grid_knowledge, grid_radioactivity):
        super().__init__(grid_knowledge, grid_radioactivity)

        self.dict_agents_knowledge = {}

    def get_dict_agents_knowledge(self):
        """"
        Return the dictionary of agents knowledge.

        Parameters
        ----------
        None

        Returns
        -------
        dict
        """
        return self.dict_agents_knowledge
    
    def set_dict_agents_knowledge(self, dict_agents_knowledge):
        """
        Set the dictionary of agents knowledge.

        Parameters
        ----------
        dict_agents_knowledge : dict
            Dictionary of agents knowledge.

        Returns
        -------
        None
        """
        self.dict_agents_knowledge = dict_agents_knowledge

    def __str__(self) -> str:
        return f"ChiefAgentKnowledge(grid_knowledge={np.flip(self.grid_knowledge.T,0)}, grid_radioactivity={np.flip(self.grid_radioactivity.T,0)}, picked_up_wastes={self.picked_up_wastes}, transformed_waste={self.transformed_waste}, left={self.left}, right={self.right}, up={self.up}, down={self.down}, dict_chiefs={self.dict_chiefs}, dict_agents_knowledge={self.dict_agents_knowledge})"
