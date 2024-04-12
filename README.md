# Robot Mission - Group 3

This project has been created for the course SMA in CentraleSupélec.
The project has been realized by the group 3 composed of:
- Oumaima CHATER
- Laure-Emilie MARTIN
- Agathe PLU
- Agathe POULAIN

## Table of contents

- [Robot Mission - Group 3](#robot-mission---group-3)
    - [Installation](#installation)
        - [Cloning the repository](#cloning-the-repository)
        - [Creation of a virtual environment](#creation-of-a-virtual-environment)
        - [Installation of the necessary librairies](#installation-of-the-necessary-librairies)
        - [Launch the code](#launch-the-code)
    - [Our Objects](#our-objects)
        - [The Radioactivity](#the-radioactivity)
        - [The Waste](#the-waste)
        - [The WasteDisposalZone](#the-wastedisposalzone)
    - [Without Communication](#without-communication)
        - [Our Agents](#our-agents)
            - [The Agent's knowledge](#the-agents-knowledge)
            - [The CleaningAgent](#the-cleaningagent)
            - [The GreenAgent](#the-greenagent)
                - [The deliberate method](#the-deliberate-method)
            - [The YellowAgent](#the-yellowagent)
                - [The deliberate method](#the-deliberate-method)
            - [The RedAgent](#the-redagent)
                - [The deliberate method](#the-deliberate-method)
        - [Our Model](#our-model)
        - [The scheduler](#the-scheduler)
        - [The visualization](#the-visualization)
    - [With Communication](#with-communication)
        - [Our Agents](#our-agents)
            - [The Agent's knowledge](#the-agents-knowledge)
            - [The CleaningAgent](#the-cleaningagent)
            - [The GreenAgent](#the-greenagent)
                - [The deliberate method](#the-deliberate-method)
            - [The YellowAgent](#the-yellowagent)
                - [The deliberate method](#the-deliberate-method)
            - [The RedAgent](#the-redagent)
                - [The deliberate method](#the-deliberate-method)
        - [Our Model](#our-model)
        - [The scheduler](#the-scheduler)
        - [The visualization](#the-visualization)
 

## Installation

### Cloning the repository

To clone the github repository, you have to search the clone button on the main page of the project. Then click on it and select `https` or `ssh` depending on your favorite mode of connexion. Copy the given id and then open a terminal on your computer, go to the folder where you want to install the project and use the following command:

```bash
git clone <your copied content>
```

### Creation of a virtual environment

You might want to use a virtual environment to execute the code. To do so, use the following command:

```bash
python -m virtualenv venv
```

To start it, use the command on *Windows*:

```bash
./venv/Scripts/Activate.ps1
```

Or for *MacOS* and *Linux*:

```bash
source venv/Scripts/activate
```

### Installation of the necessary librairies

To execute this software, you need several *Python* librairies, specified in the `requirements.txt` file. To install them, use the following command:

```bash
pip install -r requirements.txt
```

### Launch the code

The grid size and the waste density are defined and can be modified in `tools/tools_constants.py`.


The main code can be launched by running the following command:

```bash
python run.py
```

It can also be launched with the visualisation by running the following command:

```bash
python server.py
```

## Our Objects

Our objects are agent types without any behaviour, and they are defined in `objects.py`.

### The Radioactivity

The `Radioactivity` object represents the radioactivity of an area. It has two attributes:
- `zone`, which defines the area it belongs to and can only take three values ("z1", "z2", "z3")
- `radioactivity_level`, which defines its level of radioactivity. It is a random number comprised between 0 and 0.33 for z1, 0.33 and 0.66 for z2 and 0.66 and 1 for z3.

The `Radioactivity` object is placed in each cell of the grid to define our different areas. Its `zone` attribute then is used by our agents to determine which zone they are in.

### The Waste 

The `Waste` object represents the waste. It has one attribute: `type_waste` which defines the type of the waste and can only take three values ("green", "yellow", "red"). 

### The WasteDisposalZone

The `WasteDisposalZone` object represents a cell in the last right column of the grid, chosen randomly from the cells in that column.


## Without Communication

### Our Agents

The implementation of our different cleaning agents is in the `agents.py` file.

#### The agent's knowledge

The `AgentKnowledge` class represents the knowledge and state of an agent in the simulation. This class is defined in `tools/tools_knowledge.py`. It has the following attributes:

- `grid_knowledge`: Represents the agent's knowledge of the grid. Its values are set to `0` for an empty tile, `1` for a green waste, `2` for a yellow waste, `3` for a red waste and `4` for the waste disposal zone. It is a numpy array with the same dimensions as the grid.
- `grid_radioactivity`: Represents the agent's knowledge of the grid's radioactivity. Its values are set to `1`, `2` or `3` according to the different zones. It is a numpy array with the same dimensions as the grid.
- `picked_up_wastes`: Represents a list of the Waste agents that our cleaning agent has picked up.
- `transformed_waste`: Represents whether the agent has transformed waste. Its values are `None` or the new transformed waste object.
- `left`, `right`, `up`, `down`: Boolean variables representing the possibility for the agent to move in the corresponding direction. It depends on the presence of an other agent in the agent's surrounding cells and on the limits of the grid.

The class provides methods to get and set these attributes. The __str__ method provides a string representation of the object's state.

#### The CleaningAgent

The `CleaningAgent` class inherits from the Mesa `Agent` class and is used to define common behaviors for the Green, Yellow and Red cleaning agents. These common behaviors are the methods `step`, `convert_pos_to_tile`, `update` and `update_positions_around_agent`.

The `step` method implements the procedural loop of our agent. It begins by updating the agent's knowledge using the `update` method. Next, the `deliberate` method is called to return a list of possible actions. Finally, the `do` method is invoked in the environment to execute the chosen action.

The `convert_pos_to_tile` method takes as input a position and returns a direction (`left`, `right`, `up` or `down`) based on the agent's current location relative to the input position.

The `update` method updates each attributes of the agent's knowledge according to the percept.

The `update_positions_around_agent` method is used in the `update` method to update `left`, `right`, `up` and `down` boolean values of the agent's knowledge.


#### The GreenAgent

The `GreenAgent` is a class inheriting from the class `CleaningAgent` presented above. It permits to code the specific behaviour of the green agent, mainly the `deliberate` method, which is not the same for all types of cleaning agents.

##### The deliberate method

The `deliberate` method returns a list of actions called `list_possible_actions`, in the order of preference for the agent. Only one will be executed by the model, the first of the list which can be executed.

The actions have been defined in `tools_constants` by strings. Here is the full list:
- `ACT_TRANSFORM`, to transform two wastes in a waste from the superior color
- `ACT_PICK_UP`, to pick up a waste
- `ACT_DROP`, to drop a tranformed waste
- `ACT_GO_LEFT`, to go left
- `ACT_GO_RIGHT`, to go right
- `ACT_GO_UP`, to go up
- `ACT_GO_DOWN`, to go down
- `ACT_WAIT`, to wait

If the agent possesses two green wastes, the top priority action is to transform them.

If the agent possesses a yellow transformed waste, it will ask to go right until its right tile is on zone 2, ie the border. When it is on the border, it will ask to drop its waste if the current tile is empty, otherwise it will go up or down randomly, if nothing is blocking its way (thanks to the attributes`up` and `down` from knowledge). 

If the agent is on a tile with a green waste and if it doesn't have two wastes or a transformed waste, it will ask to perform the pick up action. If it can't move or drop its waste, it will wait.

If the agent has less than two picked up wastes, no transformed waste and is on a cell containing a waste, then it will pick up the waste.

Otherwise, we will add moving to differents directions if nothing blocks its way to its list of possible actions. We will favor adjacent cells with waste by adding them first in its list. Otherwise, possible directions are added in a random order.

The last action of the list will be to wait, so the agent always has an action to preform.

#### The YellowAgent

The `YellowAgent` is a class inheriting from the class `CleaningAgent` presented above. It permits to code the specific behaviour of the yellow agent, mainly the `deliberate` method, which is not the same for all types of cleaning agents.

##### The deliberate method

It has the same behavior as the GreenAgent's deliberate method. One of the few differences is that it can move to the green area to pick up yellow waste at the border.

#### The RedAgent

The `RedAgent` is a class inheriting from the class `CleaningAgent` presented above. It permits to code the specific behaviour of the red agent, mainly the `deliberate` method, which is not the same for all types of cleaning agents.

##### The deliberate method

This method's behavior is still quite similar to the tow other agents' deliberate methods. However, the red agents won't transform wastes, they will only pick up one waste and then put it in the waste disposal zone. To do so, it will go right after picking up a waste and then move up or down to join the waste disposal zone whose position is stored in the agent's knowledge.

### Our Model

The implementation of our model is in the `model.py` file. The `RobotMission` class inherits from the Mesa `Model` class and defines the RobotMission model itself, and uses the agents, the scheduler and the environment. 

We begin by defining several methods to set up the grid and all agents: `init_grid`, `init_wastes` and `init_agents`.

In `init_grid` we establish the position of the waste disposal zone and created  `Radioactivity` objects in every cells of the grid except at the waste disposal zone position, where we created a `WasteDisposalZone` object.

In `init_wastes` we create all wastes. To do so, we first define the total number of wastes in the grid (grid height * grid width * waste density, the density is set in `tools/tools_constants.py`) and the number of cells per zone (grid width/3 * grid height). We then randomly place green, yellow and red wastes in their respective zones. However, we do not initially place a red waste in the waste disposal zone.

- The number of green wastes is randomly determined within a range. The upper bound of this range is the minimum between the number of cells in the green area and the total number of wastes. The lower bound is the maximum between 0 and the total number of waste minus the total number of cells in the rest of the grid. This allocation ensures that wastes are placed in the zone if the other two areas do not have sufficient space to accommodate all remaining wastes. Then we check if that number is even so that we can clean the whole map. Otherwise we add or substract one green waste.

- The number of yellow wastes is randomly determined within a range. The upper bound of this range is the maximum between 0 and the minimum between the remaining wastes and the number of cells in the zone. The lower bound is the maximum between 0 and the total number of waste minus the total number of cells in the rest of the grid. This allocation ensures that waste can be placed in the zone if the red area does not have sufficient space to accommodate all remaining wastes. Then we check if that number plus the number of green wastes' pairs is even, otherwise we add or substract one yellow waste.

- The number of red wastes is determined by the number of remaining wastes to place.

In `init_agents` we create and place the cleaning agent according to their colors and respective areas. We choose to initially place cleaning agent in their color zone. We also do not allow two agents to be in the same cell, this will stay true during the simulations.

The `step` method does the scheduler step while there are still wastes to clean up, otherwise the simulation will terminate.

The `run_model` method executes the `step` method for a given number of sSteps.

The `do` method takes as arguments the agent performing the action and the list of all possible actions. It iterates through this list, checking if the current action is feasible. If it is feasible, the method breaks, ensuring that only one action is performed. If the current action is not feasible, the method moves on to the next action in the list. When an action is performed using the `do` method, the method also executes the changes associated with that action:
- `ACT_TRANSFORM`, if the agent is a `GreenAgent` it creates a green waste, if the agent is a `YellowAgent` it creates a red waste. It then set the agent's knowledge (trasnformed_waste to the current waste) and add it to the scheduler. It will also remove from the scheduler the two waste from the agent's knowledge picked_up_waste and the set up the picked_up_waste as an empty list.
- `ACT_PICK_UP`, it removes the waste agent from the grid and updates the agent's knowledge picked_up_waste with the new waste.
- `ACT_DROP`, if the agent is not a `RedAgent` the transformed waste will be placed on the grid and the agent's knowledge transformed_waste will be set back to None. If  the agent is a `RedAgent` it will remove the picked_up_waste from the scheduler and set the agent's knowledge picked_up_waste back to an empty list.
- `ACT_GO_LEFT`, it will check for another agent in the left cell and move the agent if it is empty.
- `ACT_GO_RIGHT`, it will check for another agent in the right cell and move the agent if it is empty.
- `ACT_GO_UP`, it will check for another agent in the upper cell and move the agent if it is empty.
- `ACT_GO_DOWN`, it will check for another agent in the lower cell and move the agent if it is empty.
- `ACT_WAIT`, it waits.

The `do` method returns the percepts. It is a dictionary of four keys (left, right, up and down). It either contains a list of agents (`Waste`, `Radioactivity`, other cleaning agents and `WasteDisposalZone`) in the surrounding cells or `None` if the cell does not exist (grid limits). This percepts is created after an action is performed to take into account the possible new position of the agent. 

### The scheduler

A custom class of random scheduler `CustomRandomScheduler` has been defined in the file `schedule.py`. This new class inherits from the base class of *mesa* `BaseScheduler`, but its `step()` function is slightly modified to activate the cleaning agents in a random order, according to their type. More precisely, the order of activation of the types of agents is random (random between green, yellow and red), and for each type, the order of activation of agents is random.

### The visualization

The visualization is defined in the `server.py`. Each agent and object is there represented according to the following codes:
- the `Radioactivity` objects are rectangles in the layer 0 in the corresponding color (light green, light yellow, light red): they map the grid.
- the `WasteDisposalZone` object is a brown rectangle in the layer 1.
- the `Waste` objects are small rectangles in the corresponding color (green, yellow, red), in the layer 2.
- the `CleaningAgent` are represented by circles in the layer 3 in the corresponding colo  (dark green, dark yellow, dark red). When they have one or two wastes on them, the number of wastes is display in the circle. When they have a transformed waste on them, the letter "T" is displayed in the circle.


## With Communication

### Our Agents

#### The Agent's knowledge

#### The CleaningAgent

#### The GreenAgent
##### The deliberate method

#### The YellowAgent
##### The deliberate method

#### The RedAgent
##### The deliberate method

### Our Model

### The scheduler

### The visualization
