"""
Python file for the Agents.

Group 3:
- Oumaima CHATER
- Laure-Emilie MARTIN
- Agathe PLU
- Agathe POULAIN
"""

### Mesa imports ###
from mesa import Agent
from mesa.time import RandomActivation
from mesa.space import MultiGrid

class CleaningAgent(Agent):

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def random_movement(self):
        pass

    def go_left(self):
        x, y = self.pos
        self.model.grid.move_agent(self, (x - 1, y))

    def go_right(self):
        x, y = self.pos
        self.model.grid.move_agent(self, (x + 1, y))

    def go_down(self):
        x, y = self.pos
        self.model.grid.move_agent(self, (x, y + 1))

    def go_up(self):
        x, y = self.pos
        self.model.grid.move_agent(self, (x, y - 1))


    

    
    

class GreenAgent(CleaningAgent):

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        # update(self.knowledge,percepts)
        # action = deliberate(self.knowledge)
        # percepts = self.model.do(self)
        pass

    

class YellowAgent(CleaningAgent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        pass

class RedAgent(CleaningAgent):

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        pass