# Robot Mission - Group 3

This project has been created for the course SMA in CentraleSupélec.
The project has been realized by the group 3 composed of:
- Oumaima CHATER
- Laure-Emilie MARTIN
- Agathe PLU
- Agathe POULAIN

This `README` is composed of four main parts, the [first one](#installation) describing the steps to follow to install and run our code. The [second one](#without-communication) describes our implementation choices for non-communicating agent, whereas the [third one](#with-communication-and-improved-movement) deals with our implementation choices with communication between agents. The [fourth part](#simulations-results-interpretation) presents the results obtained for both approaches.

## PISTES D'AMELIORATION A REDIGER
- envoi de la part du chef d'un ordre pour indiquer l'endroit où drop un waste (le plus proche de l'agent) en se servant de sa knowledge et des communications du chef supérieur qui lui indique quand un déchet n'est plus là. Mettre dans knowledge un attribut drop_target_position et renommer target_position en pick_up_target_position.

## PERSPECTIVES FUTURES A REDIGER
- chef qui se casse => élection d'un nouveau chef (quand par exemple il ne répond plus aux messages envoyés par ses sous-fifres => message de confirmation à envoyer de la part du chef à chaque fois qu'il reçoit les percepts de ses sous-fifres)

## Table of contents

- [Robot Mission - Group 3](#robot-mission---group-3)
  - [PISTES D'AMELIORATION A REDIGER](#pistes-damelioration-a-rediger)
  - [PERSPECTIVES FUTURES A REDIGER](#perspectives-futures-a-rediger)
  - [Table of contents](#table-of-contents)
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
      - [The agent's knowledge](#the-agents-knowledge)
      - [The CleaningAgent](#the-cleaningagent)
      - [The GreenAgent](#the-greenagent)
        - [The deliberate method](#the-deliberate-method)
      - [The YellowAgent](#the-yellowagent)
        - [The deliberate method](#the-deliberate-method-1)
      - [The RedAgent](#the-redagent)
        - [The deliberate method](#the-deliberate-method-2)
    - [Our Model](#our-model)
    - [The scheduler](#the-scheduler)
    - [The visualization](#the-visualization)
  - [With Communication and improved movement](#with-communication-and-improved-movement)
    - [The knowledge](#the-knowledge)
      - [The Agent's knowledge](#the-agents-knowledge-1)
      - [The Chief's knowledge](#the-chiefs-knowledge)
    - [The agents](#the-agents)
      - [The CleaningAgent](#the-cleaningagent-1)
      - [The GreenAgent](#the-greenagent-1)
        - [The deliberate method](#the-deliberate-method-3)
      - [The YellowAgent](#the-yellowagent-1)
        - [The deliberate method](#the-deliberate-method-4)
      - [The RedAgent](#the-redagent-1)
        - [The deliberate method](#the-deliberate-method-5)
      - [The Chief](#the-chief)
      - [The ChiefGreenAgent](#the-chiefgreenagent)
      - [The ChiefYellowAgent](#the-chiefyellowagent)
      - [The ChiefRedAgent](#the-chiefredagent)
    - [Our Model](#our-model-1)
    - [The scheduler](#the-scheduler-1)
    - [The visualization](#the-visualization-1)
  - [Simulation's results interpretation](#simulations-results-interpretation)
    - [Without communication](#without-communication-1)
    - [With communication and improved movement](#with-communication-and-improved-movement-1)


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

The `CleaningAgent` class inherits from the Mesa `Agent` class and is used to define common behaviors for the Green, Yellow and Red cleaning agents. These common behaviors are the methods `step`, `convert_pos_to_tile`, `update`, `update_positions_around_agent` and `update_knowledge_with_action`.

The `step` method implements the procedural loop of our agent. It begins by updating the agent's knowledge using the `update` method. Next, the `deliberate` method is called to return a list of possible actions. Finally, the `do` method is invoked in the environment to execute the chosen action.

The `convert_pos_to_tile` method takes as input a position and returns a direction (`left`, `right`, `up` or `down`) based on the agent's current location relative to the input position.

The `update` method updates each attributes of the agent's knowledge according to the percept.

The `update_positions_around_agent` method is used in the `update` method to update `left`, `right`, `up` and `down` boolean values of the agent's knowledge.

The `update_knowledge_with_action` method is used in the `update` method to update the knowledge of the agent given the action it has performed on the previous step. For instance, if the agent has transformed a waste, `transformed_waste` will be set to the transformed created waste contained the `percepts` returned by the model.

#### The GreenAgent

The `GreenAgent` is a class inheriting from the class `CleaningAgent` presented above. It permits to code the specific behavior of the green agent, mainly the `deliberate` method, which is not the same for all types of cleaning agents.

##### The deliberate method

The `deliberate` method returns a list of actions called `list_possible_actions`, in the order of preference for the agent. Only one will be executed by the model, the first of the list which can be executed.

The actions have been defined in `tools_constants` by strings. Here is the full list:
- `ACT_TRANSFORM`, to transform two wastes in a waste from the superior color
- `ACT_PICK_UP`, to pick up a waste
- `ACT_DROP`, to drop a transformed waste
- `ACT_GO_LEFT`, to go left
- `ACT_GO_RIGHT`, to go right
- `ACT_GO_UP`, to go up
- `ACT_GO_DOWN`, to go down
- `ACT_WAIT`, to wait

If the agent possesses two green wastes, the top priority action is to transform them.

If the agent possesses a yellow transformed waste, it will ask to go right until its right tile is on zone 2, ie the border. When it is on the border, it will ask to drop its waste if the current tile is empty, otherwise it will go up or down randomly, if nothing is blocking its way (thanks to the attributes `up` and `down` from knowledge). 

If the agent is on a tile with a green waste and if it doesn't have two wastes or a transformed waste, it will ask to perform the pick up action. If it can't move or drop its waste, it will wait.

If the agent has less than two picked up wastes, no transformed waste and is on a cell containing a waste, then it will pick up the waste.

Otherwise, we will add moving to different directions if nothing blocks its way to its list of possible actions. We will favor adjacent cells with waste by adding them first in its list. Otherwise, possible directions are added in a random order.

The last action of the list will be to wait, so the agent always has an action to preform.

#### The YellowAgent

The `YellowAgent` is a class inheriting from the class `CleaningAgent` presented above. It permits to code the specific behavior of the yellow agent, mainly the `deliberate` method, which is not the same for all types of cleaning agents.

##### The deliberate method

It has the same behavior as the GreenAgent's deliberate method. One of the few differences is that it can move to the green area to pick up yellow waste at the border.

#### The RedAgent

The `RedAgent` is a class inheriting from the class `CleaningAgent` presented above. It permits to code the specific behavior of the red agent, mainly the `deliberate` method, which is not the same for all types of cleaning agents.

##### The deliberate method

This method's behavior is still quite similar to the tow other agents' deliberate methods. However, the red agents won't transform wastes, they will only pick up one waste and then put it in the waste disposal zone. To do so, it will go right after picking up a waste and then move up or down to join the waste disposal zone whose position is stored in the agent's knowledge.

### Our Model

The implementation of our model is in the `model.py` file. The `RobotMission` class inherits from the Mesa `Model` class and defines the RobotMission model itself, and uses the agents, the scheduler and the environment. 

We begin by defining several methods to set up the grid and all agents: `init_grid`, `init_wastes` and `init_agents`.

TODO - Agathe Poulain => expliquer le datacollector

In `init_grid` we establish the position of the waste disposal zone and created  `Radioactivity` objects in every cells of the grid except at the waste disposal zone position, where we created a `WasteDisposalZone` object.

In `init_wastes` we create all wastes. To do so, we first define the total number of wastes in the grid (grid height * grid width * waste density, the density is set in `tools/tools_constants.py`) and the number of cells per zone (grid width/3 * grid height). We then randomly place green, yellow and red wastes in their respective zones. However, we do not initially place a red waste in the waste disposal zone.

- The number of green wastes is randomly determined within a range. The upper bound of this range is the minimum between the number of cells in the green area and the total number of wastes. The lower bound is the maximum between 0 and the total number of waste minus the total number of cells in the rest of the grid. This allocation ensures that wastes are placed in the zone if the other two areas do not have sufficient space to accommodate all remaining wastes. Then we check if that number is even so that we can clean the whole map. Otherwise we add or subtract one green waste.

- The number of yellow wastes is randomly determined within a range. The upper bound of this range is the maximum between 0 and the minimum between the remaining wastes and the number of cells in the zone. The lower bound is the maximum between 0 and the total number of waste minus the total number of cells in the rest of the grid. This allocation ensures that waste can be placed in the zone if the red area does not have sufficient space to accommodate all remaining wastes. Then we check if that number plus the number of green wastes' pairs is even, otherwise we add or subtract one yellow waste.

- The number of red wastes is determined by the number of remaining wastes to place.

In `init_agents` we create and place the cleaning agent according to their colors and respective areas. We choose to initially place cleaning agent in their color zone. We also do not allow two agents to be in the same cell, this will stay true during the simulations.

The `step` method does the scheduler step while there are still wastes to clean up, otherwise the simulation will terminate.

The `run_model` method executes the `step` method for a given number of sSteps.

The `do` method takes as arguments the agent performing the action and the list of all possible actions. It iterates through this list, checking if the current action is feasible. If it is feasible, the method breaks, ensuring that only one action is performed. If the current action is not feasible, the method moves on to the next action in the list. When an action is performed using the `do` method, the method also executes the changes associated with that action:
- `ACT_TRANSFORM`, if the agent is a `GreenAgent` it creates a green waste, if the agent is a `YellowAgent` it creates a red waste. It then adds the transformed created waste to the scheduler. It also removes from the scheduler the two wastes from the agent's knowledge `picked_up_waste`.
- `ACT_PICK_UP`, it removes the waste agent from the grid.
- `ACT_DROP`, if the agent is not a `RedAgent` the transformed waste will be placed on the grid. If the agent is a `RedAgent` it will remove the picked_up_waste from the scheduler.
- `ACT_GO_LEFT`, it will check for another agent in the left cell and move the agent if it is empty.
- `ACT_GO_RIGHT`, it will check for another agent in the right cell and move the agent if it is empty.
- `ACT_GO_UP`, it will check for another agent in the upper cell and move the agent if it is empty.
- `ACT_GO_DOWN`, it will check for another agent in the lower cell and move the agent if it is empty.
- `ACT_WAIT`, it waits.

The `do` method returns the percepts. It is a dictionary of two mains keys: `action_done` and `positions`. The first key is associated with a dictionary containing the key `action` associated to the constant representing the action executed and `object` if the agent has picked up a waste or transformed it. The second key is a dictionary with four keys: left, right, up and down. It either contains a list of agents (`Waste`, `Radioactivity`, other cleaning agents and `WasteDisposalZone`) in the surrounding cells or `None` if the cell does not exist (grid limits). This percepts is created after the action is performed to take into account the possible new position of the agent.

### The scheduler

A custom class of random scheduler `CustomRandomScheduler` has been defined in the file `schedule.py`. This new class inherits from the base class of *mesa* `BaseScheduler`, but its `step()` function is slightly modified to activate the cleaning agents in a random order, according to their type. More precisely, the order of activation of the types of agents is random (random between green, yellow and red), and for each type, the order of activation of agents is random.

### The visualization

The visualization is defined in the `server.py`. Each agent and object is there represented according to the following codes:
- the `Radioactivity` objects are rectangles in the layer 0 in the corresponding color (light green, light yellow, light red): they map the grid.
- the `WasteDisposalZone` object is a brown rectangle in the layer 1.
- the `Waste` objects are small rectangles in the corresponding color (green, yellow, red), in the layer 2.
- the `CleaningAgent` are represented by circles in the layer 3 in the corresponding colo  (dark green, dark yellow, dark red). When they have one or two wastes on them, the number of wastes is display in the circle. When they have a transformed waste on them, the letter "T" is displayed in the circle.

## With Communication and improved movement

We worked from the previous part to add communication between our agent and we improved their movement. In this new part, we will develop all implemented changes and enhancements.

The key points are the covering mode at the beginning of the cleaning to identify all wastes in the map, and the creation of a Chief for each color agents. This Chief is in charge of centering the knowledge (for each color agents), managing its agents for the new covering phase and sending appropriate orders. For this purpose, we create a new super class `Chief` and we create a dedicated `ChiefKnowledge` class in `tools/tools_knowledge.py`. We will now delve into our implemented improvements: the code is based on the previous part, hence, we will only mention deleted, changed and/or added behaviors in this part.

### The knowledge

For our communication, we choose to extend our agents' knowledge by incorporating additional elements. We also created a dedicated `ChiefAgentKnowledge` class inheriting from our `AgentKnowledge` class.

#### The Agent's knowledge

We added several attributes to our inital `AgentKnowledge` class, including:

- `dict_chiefs` : A dictionary containing the chief agents for each color.
- `target_position` : Represents the target position to reach, which can be None or a position tuple.
- `bool_covering` : Boolean variable representing whether the agent is in covering mode or not, initialized at `True`.
- `direction_covering` : Represents the direction to cover, initialized at `None` and can take values `right` or `left`.

#### The Chief's knowledge

The `ChiefAgentKnowledge` class inherits from the `AgentKnowledge` class and includes additional attributes:

- `dict_agents_knowledge` : A dictionary containing the agents' knowledge.
- `bool_cleaned_right_column` : Boolean variable representing whether the Chief's zone's rightmost column has been cleaned. Indeed, the green and yellow chiefs will start cleaning the rightmost column of their zone, in order to allow easier drop of transformed waste on the border.
- `direction_clean_right_column` : Represents the direction to clean, initialized at `None` and can take values `up` or `down`.
- `rows_being_covered` : A list of size equal to the grid height, containing 0 if the row is being covered or has been covered, and 1 otherwise.
- `list_green_yellow_red_left_columns` : A list of three values, initialized at `None`, representing the columns of the leftmost columns in the green, yellow, and red zones.
- `list_green_yellow_red_right_columns` :  A list of three values, initialized at `None`, representing the columns of the rightmost columns in the green, yellow, and red zones.
- `dict_target_position_agent` : A dictionary containing the target positions given to each agent.

The class provides methods to get and set these attributes. The __str__ method provides a string representation of the object's state.

### The agents

The principle beyond the behavior of each agent given its type (chief or not) and its color is the following:
- at the beginning of the simulation, the green and yellow chiefs are on the rightmost column of their zone to clean it, to allow easier drop of the transformed wastes. The other agents (the red chief including) will start cover their own zone, so each tile of their zone has been seen at least once. It will been done accordingly to the following image.
![explanation_covering](images/explanations_covering.png)
Each agent will place himself to the target position indicated by the chief to perform the coverage of the row (and the two adjacent rows at the same time); this row is chosen to be the closest non covered row to the agent. The agents performing the coverage can pick up wastes during their covering if the waste is on their way. Nevertheless, they cannot derive from their row and their target position to pick a close waste or drop a transformed waste (they can drop it only if their way to go to their cover target is on the last column, which is not always the case). 
- after all rows being covered, the agents will receive new orders from the chief, indicating the position of the closest waste to the agent (the chief will also receive this kind of orders from himself). The agent will thus go to this target; if he finds a waste on his way, he can pick it and warn the chief of this action. When the agent has a transformed waste, he goes right (and indicates the chief he cancels his target if he had still one) to drop it on the last column. This principle is the same for red agents with the waste disposal zone.
- at the end of the cleaning of the green or yellow zone, some blocking situations can exist. For instance, if the two last green wastes have been picked up by different agents. To overcome this dead-end, we added a special action `ACT_DROP_ONE_WASTE` and we used communication; the chief will a message to one of the agents to drop its waste and let the other agent pick it.

#### The CleaningAgent

The `CleaningAgent` class inherits from the `CommunicatingAgent` class defined in `communication/agent/CommunicatingAgent.py` and is used to define common behaviors for the Green, Yellow and Red cleaning agents and their chiefs. These common behaviors are the methods `step`, `convert_pos_to_tile` (same as part 1), `treat_order`, `receive_orders`, `get_specificities_type_agent`, `can_drop_transformed_waste`, `can_drop_one_waste`, `can_transform`, `can_pick_up`, `can_go_up`, `can_go_down`, `can_go_right`, `can_go_left`, `deliberate_go_to_pick_close_waste`, `deliberate_go_to_target`, `send_message_disable_target_position`, `update_knowledge_target_position`, `update_knowledge_with_action`, `update` and `send_percepts_and_data`.

In the `step` method, we implement the improved procedural loop of our agent. We start by receiving orders from the chief with `receive_orders`. We then call the `deliberate` and `do` methods, followed by the `update` method. Finally, the step is finished by the agent sending its percept and data to the chief using `send_percepts_and_data`. We chose to move the `update` method after the `deliberate` and `do` methods as this new order best fits our implementation and our needs.

The `treat_order` method defines the agent's action corresponding to received orders from its chief. The message reception of the agent is defined in the `receive_orders` method.

The `get_specificities_type_agent` method is widely used in our code as it returns specific values depending on the agent's type (i.e., its color). It returns the maximum number of waste items that can be picked up (2 for green and yellow, 1 for red agents), the type of waste that can be picked up (1 for green, 2 for yellow, 3 for red agents), and the type of the right (2 for green, 3 for yellow and None for red agents) and left (None for green, 1 for yellow and 2 for red agents) zones for the agent.

The methods `can_drop_transformed_waste`, `can_drop_one_waste`, `can_transform`, `can_pick_up`, `can_go_up`, `can_go_down`, `can_go_right`, `can_go_left` each return a boolean value indicating whether the agent can perform the corresponding action. We verify all conditions in these functions and define them to simplify and clean our code.  We use them in various ♠`deliberate` functions in our program.

TODO :
deliberate go to pick close waste
deliberate go to target

The `send_message_disable_target_position` methods is defined to allow the agent to notify its chief when it decides to not pursue its assigned target position. This can append in normal mode if the agent now has a transformed waste to drop, for instance.

TODO:
update knowledge target position

The `update_knowledge_with_action` method defines which attributes to update in the agent's knowledge depending on the action it has performed. The `update` method update the agent's knowledge based on the agent's percepts after performing its action. At the end of the step, the `send_percepts_and_data` method is used by the agent to send its latest percepts and knowledge to its chief

#### The GreenAgent
As presented for the part without communication,the `GreenAgent` is a class inheriting from the class `CleaningAgent` presented above. It permits to code the specific behavior of the green agent, mainly the `deliberate` method, which is not the same for all types of cleaning agents.
##### The deliberate method
The `deliberate` method returns a list of actions called `list_possible_actions`, in the order of preference for the agent. Only one will be executed by the model, the first of the list which can be executed.

The actions have been defined in `tools_constants` by strings. Here is the full list:

- `ACT_TRANSFORM`, to transform two wastes in a waste from the superior color
- `ACT_PICK_UP`, to pick up a waste
- `ACT_DROP`, to drop a transformed waste
- `ACT_GO_LEFT`, to go left
- `ACT_GO_RIGHT`, to go right
- `ACT_GO_UP`, to go up
- `ACT_GO_DOWN`, to go down
- `ACT_WAIT`, to wait

If the agent possesses two green wastes, the top priority action is to transform them.

If the agent possesses a yellow transformed waste, it will ask to go right until its right tile is on zone 2, i.e. the border. When it is on the border, it will ask to drop its waste if the current tile is empty, otherwise it will go up or down randomly, if nothing is blocking its way (thanks to the attributes `up` and `down` from knowledge).

If the agent is on a tile with a green waste and if it doesn't have two wastes or a transformed waste, it will ask to perform the pick-up action. If it can't move or drop its waste, it will wait.

If the agent has less than two picked up wastes, no transformed waste and is on a cell containing a waste, then it will pick up the waste.

Otherwise, we will add moving to different directions if nothing blocks its way to its list of possible actions. We will favor adjacent cells with waste by adding them first in its list. Otherwise, possible directions are added in a random order.

The last action of the list will be to wait, so the agent always has an action to perform.

#### The YellowAgent
##### The deliberate method

#### The RedAgent
##### The deliberate method

#### The Chief

#### The ChiefGreenAgent

#### The ChiefYellowAgent

#### The ChiefRedAgent

### Our Model

We improved a few things in the model class. 

First of all, we took into account the configurations where the grid width is not divisible by 3. In these cases, we attributed the one or two columns remaining to one or two zones randomly. For instance, for a grid width of 20, the green zone can have 7 columns, the yellow 6 and the red 7, at random.

Moreover, we implemented the `MessageService` class to enable the communication between agents.

### The scheduler

We improved the class `CustomRandomScheduler` by adding the chiefs in the `step` method. We choose to call the chiefs before the agents of their respecting colors, to allow them to distribute orders always at the beginning of the step.

### The visualization

We improved the visualization by adding *mesa* sliders to enable the user to configure the simulation directly on the interface. The user can choose the number of green, yellow and red agents, and also the waste density.

We also added clearer images for each type of object. We distinguished chiefs from agent for each color with specific images, and we also chose an image for the wastes and the waste disposal zone. All of these images are located in the folder `resources/`.

## Simulation's results interpretation

To compare both approaches presented above, mostly to analyse the improvements made in the second method, we decided to run many simulations for both cases and compare the terminating rate of simulations (for non communication approaches, the simulation may not terminate), and the average number of steps needed to clean the entire map. For each test, we use (9, 18) as grid size and 0.3 for the waste density.

Only the number of agents per zone evolves across simulations, and for each case we have launched 10 simulations to be able to compute a correct average. Without communication, we launched simulations for 1 agent per zone, 2 and 3 agents per zone. With communication, we launched for 1, 2, 3 and 4 agents per zone. Doing it for 4 agents per zone without communication was useless as the simulation is almost never terminating in this case.

### Without communication

To analyse the performance of the model without communication, we launched 30 simulations corresponding to:
- Simulations 1 to 10 : 1 agent per zone
- Simulations 11 to 20 : 2 agents per zone
- Simulations 21 to 30 : 3 agents per zone

Here is the table with all the results:

![alt text](results/results_without_communication.png)

When there is only one agent per zone (blue cells on the previous picture), the average number of steps to complete the cleaning of the map is 1346.

When there are two agents per zone (green cells on the previous picture), the average number of steps to complete the cleaning of the map is 713. It is almost two times less than the average number of steps needed with one agent per zone. However, half of the simulations launched with two agents did not end because two agents of the same zone picked up one waste left at the end of their zone cleaning and blocked themselves from transforming the waste into a new one.

When there are three agents per zone (purple cells on the previous picture), the average number of steps to complete the cleaning of the map is 404. It is almost three times less than the average number of steps needed with one agent per zone. However, 6 out of 10 simulations launched did not end because two agents of the same zone picked up one waste left at the end of their zone cleaning and blocked themselves from transforming the waste into a new one.

According to these results, we can conclude that, on one hand, the higher the number of agents per zone, the fewer steps needed to clean the map. On the other hand, the higher the number of agents per zone, the higher the number of simulations that could not be terminated because of a conflict between two agents at the end of their zone cleaning. Therefore, we want to add communication between the agents to optimize the cleaning of the map and avoid non-terminated simulations.

You can see in appendix in `results/graphics_without_communication` the graphs obtained at the end of each of the simulations previously studied and indicating the number of waste remaining per zone at the end of the simulation. 

### With communication and improved movement

To analyse the performance of the model with communication, we launched 40 simulations corresponding to:
- Simulations 1 to 10 : 1 agent per zone
- Simulations 11 to 20 : 2 agents per zone
- Simulations 21 to 30 : 3 agents per zone
- Simulations 31 to 40 : 4 agents per zone

Here is the table with all the results:
