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
        self.target_position = None
        self.bool_covering = True
        self.direction_covering = None

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

    def get_target_position(self):
        """
        Return the target position.

        Parameters
        ----------
        None

        Returns
        -------
        tuple
        """
        return self.target_position

    def get_bool_covering(self):
        """
        Return the covering mode.

        Parameters
        ----------
        None

        Returns
        -------
        bool
        """
        return self.bool_covering
    
    def get_direction_covering(self):
        """
        Return the covering direction.

        Parameters
        ----------
        None

        Returns
        -------
        None, "right" or "left"
        """
        return self.direction_covering

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

    def set_target_position(self, target_position):
        """
        Set target position in knowledge.

        Parameters
        ----------
        target_position : tuple
            The target position.

        Returns
        -------
        None
        """
        self.target_position = target_position

    def set_bool_covering(self, bool_covering):
        """
        Set covering mode.

        Parameters
        ----------
        bool_covering : bool
            covering mode.

        Returns
        -------
        None
        """
        self.bool_covering = bool_covering

    def set_direction_covering(self, direction_covering):
        """
        Set covering direction.

        Parameters
        ----------
        bool_covering : None, "right" or "left"
            covering direction.

        Returns
        -------
        None
        """
        self.direction_covering = direction_covering

    def __str__(self) -> str:
        return f"AgentKnowledge(grid_knowledge={np.flip(self.grid_knowledge.T,0)}, grid_radioactivity={np.flip(self.grid_radioactivity.T,0)}, picked_up_wastes={self.picked_up_wastes}, transformed_waste={self.transformed_waste}, left={self.left}, right={self.right}, up={self.up}, down={self.down}, dict_chiefs={self.dict_chiefs}, target_position={self.target_position}, direction_covering={self.direction_covering}, bool_covering={self.bool_covering})"
        

class ChiefAgentKnowledge(AgentKnowledge):
    def __init__(self, grid_knowledge, grid_radioactivity):
        super().__init__(grid_knowledge, grid_radioactivity)

        self.dict_agents_knowledge = {}
        self.bool_cleaned_right_column = False
        self.direction_clean_right_column = None # can take as values None when the agent has not started cleaning the right column, "up", "down"
        self.rows_being_covered = [0] * grid_knowledge.shape[1] # 0 if the row is being covered or has been covered, 1 elsewhere

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
    
    def get_bool_cleaned_right_column(self):
        """
        Return the boolean regarding if the right column is cleaned.

        Parameters
        ----------
        None

        Returns
        -------
        bool
        """
        return self.bool_cleaned_right_column
    
    def get_direction_clean_right_column(self):
        """
        Return the direction of the right column cleaning.

        Parameters
        ----------
        None

        Returns
        -------
        str
        """
        return self.direction_clean_right_column
    
    def get_rows_being_covered(self):
        """
        Return the list of rows being covered.

        Parameters
        ----------
        None

        Returns
        -------
        list
        """
        return self.rows_being_covered

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

    def set_bool_cleaned_right_column(self, bool_cleaned_right_column):
        """
        Set the boolean regarding if the right column is cleaned.

        Parameters
        ----------
        bool_cleaned_right_column : bool
            Boolean regarding if the right column is cleaned.

        Returns
        -------
        None
        """
        self.bool_cleaned_right_column = bool_cleaned_right_column
    
    def set_direction_clean_right_column(self, direction_clean_right_column):
        """
        Set the direction of the right column cleaning.

        Parameters
        ----------
        direction_clean_right_column : str
            The direction of the right column cleaning.

        Returns
        -------
        None
        """
        self.direction_clean_right_column = direction_clean_right_column

    def set_rows_being_covered(self, rows_being_covered):
        """
        Set the list of rows being covered.

        Parameters
        ----------
        rows_being_covered : list
            The list of rows being covered.

        Returns
        -------
        None
        """
        self.rows_being_covered = rows_being_covered

    def __str__(self) -> str:
        return f"ChiefAgentKnowledge(grid_knowledge={np.flip(self.grid_knowledge.T,0)}, grid_radioactivity={np.flip(self.grid_radioactivity.T,0)}, picked_up_wastes={self.picked_up_wastes}, transformed_waste={self.transformed_waste}, left={self.left}, right={self.right}, up={self.up}, down={self.down}, dict_chiefs={self.dict_chiefs}, dict_agents_knowledge={self.dict_agents_knowledge}, target_position={self.target_position}), bool_cleaned_right_column={self.bool_cleaned_right_column}, direction_clean_right_column={self.direction_clean_right_column})"
