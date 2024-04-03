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
    - [Our Agents](#our-agents)
        - [The Agent's knowledge](#the-agents-knowledge)
        - [The CleaningAgent](#the-cleaningagent)
            - [The update method](#the-update-method)
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
- `radioactivity_level`, which defines its level of radioactivity. It is a random number comprised between 0 and 0.33 for z1, 0.33 and 0.66 for z2 and 0.66 and 1 pour z3.

The `Radioactivity` object is placed in each cell of the grid to define our different areas. Its `zone` attribute then is used by our agents to determine which zone they are in.

### The Waste 

The `Waste` object represents the waste. It has one attribute: `type_waste` which defines the type of the waste and can only take three values ("green", "yellow", "red"). 

### The WasteDisposalZone

The `WasteDisposalZone` object represents a cell in the last right column of the grid, chosen randomly from the cells in that column.

## Our Agents

TODO

### The agent's knowledge

The `AgentKnowledge` class represents the knowledge and state of an agent in the simulation. This class is defined in `toolst/tools_knowledge.py`. It has the following attributes:

- `grid_knowledge`: Represents the agent's knowledge of the grid. Its values are set to `0` for an empty tile, `1` for a green waste, `2` for a yellow waste, `3` for a red waste and `4` for the waste disposal zone.
- `grid_radioactivity`: Represents the agent's knowledge of the grid's radioactivity. Its values are set to `1`, `2` or `3` according to the zone.
- `picked_up_wastes`: Represents a list of the Waste agent that our cleaning agent has picked up.
- `transformed_waste`: Represents whether the agent has transformed waste. Its values are `None` or the new transformed waste object.
- `left`, `right`, `up`, `down`: Boolean variables representing the possibility for the agent to move is the corresponding direction. It depends on the presence of other agent in the agent's surrounding cells and on the size of the grid.

The class provides methods to get and set these attributes. The __str__ method provides a string representation of the object's state.

### The CleaningAgent

The `CleaningAgent` class inherit from the Mesa `Agent` class and we used it to define common behaviors for the Green, Yellow and Red cleaning agents.

#### The update method

TODO

### The GreenAgent

TODO

#### The deliberate method

TODO

### The YellowAgent

TODO

#### The deliberate method

TODO

### The RedAgent

TODO

#### The deliberate method

TODO


## Our Model

TODO

--> parler de l'init des waste (avec la densité et comment on gère pour qu'il ne reste pas de déchet vert ou jaune unique à la fin dès l'init des wastes)

## The scheduler

TODO

## The visualization

The visualization is defined in the `server.py`. Each agent and object is there represented according to the following codes:
- the `Radioactivity` objects are rectangles in the layer 0 in the corresponding color (light green, light yellow, light red): they map the grid.
- the `WasteDisposalZone` object is a brown rectangle in the layer 1.
- the `Waste` objects are small rectangles in the corresponding color (green, yellow, red), in the layer 2.
- the `CleaningAgent` are represented by circles in the layer 3 in the corresponding colo  (dark green, dark yellow, dark red). When they have one or two wastes on them, the number of wastes is display in the circle. When they have a transformed waste on them, the letter "T" is displayed in the circle.
