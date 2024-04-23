"""
Python file for the Objects.

Group 3:
- Oumaima CHATER
- Laure-Emilie MARTIN
- Agathe PLU
- Agathe POULAIN
"""

###############
### Imports ###
###############

from typing import Literal

### Mesa imports ###
from mesa import Agent
from mesa.time import RandomActivation
from mesa.space import MultiGrid


###############
### Objects ###
###############

class Radioactivity(Agent): # un par case avec un niveau de radioactivité
    """ An objet for the radioactivity of the area."""
    def __init__(self, unique_id, model, zone : Literal["z1", "z2", "z3"], radioactivity_level):
        """
        Initialization of the radioactivity agent.

        Parameters
        ----------
        unique_id : int
            Represents the object's identifier.

        model : Model
            Represents the model the radioactivity agent belongs to.

        zone : Literal["z1", "z2", "z3"]
            Defines the area the object belongs to.

        radioactivity_level :
            Defines the level of radioactivity of the object.

        Returns
        -------
        None
        """
        super().__init__(unique_id, model)
        self.zone = zone
        self.radioactivity_level = radioactivity_level

    def step(self):
        pass

class Waste(Agent):
    def __init__(self, unique_id, model, type_waste : Literal["green", "yellow", "red"]):
        """
        Initialization of the waste agent.

        Parameters
        ----------
        unique_id : int
            Represents the object's identifier.

        model : Model
            Represents the model the waste agent belongs to. 

        type_waste : Literal["green", "yellow", "red"]
            Defines the type of waste corresponding to the object.

        Returns
        -------
        None
        """
        super().__init__(unique_id, model)
        self.type_waste = type_waste

    def step(self):
        pass

class WasteDisposalZone(Agent):
    def __init__(self, unique_id, model):
        """
        Initialization of the waste disposal zone agent.

        Parameters
        ----------
        unique_id : int
            Represents the object's identifier.

        model : Model
            Represents the model the waste disposal zone agent belongs to.  

        Returns
        -------
        None
        """
        super().__init__(unique_id, model)

    def step(self):
        pass
