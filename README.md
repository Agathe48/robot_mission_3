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
            - [The deliberate method](#the-deliberate-method)
        - [The GreenAgent](#the-greenagent)
        - [The YellowAgent](#the-yellowagent)
        - [The RedAgent](#the-redagent)

    - [Our Model](#our-model)
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

TODO : PARTIE SERVER.PY>V


## Our Objects

Our objects are agent types without any behaviour, they are defined in `objects.py` .

### The Radioactivity

The `Radioactivity` object represents the radioactivity of an area. It has two attributes: `zone`, which defines the area it belongs to and can only take three values ("z1", "z2", "z3"), and `radioactivity_level`, which defines its level of radioactivity. The `Radioactivity` object is placed in each cell of the grid to define our different areas. Its `radioactivity_level` attribute then is used by our agents to determine which zone they are in.

### The Waste 

The `Waste` object represents the waste. It has one attribute: `type_waste` which defines the type of the waste and can only take three values ("green", "yellow", "red"). 

### The WasteDisposalZone

The `WasteDisposalZone` object represents a cell in the last right column of the grid, chosen randomly from the cells in that column.

## Our Agents

TODO

### The agent's knowledge

The `AgentKnowledge` class represents the knowledge and state of an agent in the simulation. It has the following attributes:

- `grid_knowledge`: Represents the agent's knowledge of the grid.
- `grid_radioactivity`: Represents the agent's knowledge of the grid's radioactivity.
- `nb_wastes`: Represents the number of wastes the agent has.
- `transformed_waste`: Represents whether the agent has transformed waste.
- `left`, `right`, `up`, `down`: Boolean variable representing the presence of other agent in the agent's surrounding cells.

The class provides methods to __get__ and __set__ these attributes. The __str__ method provides a string representation of the object's state.

TODO : ADD THE WDZ ATTRIBUTES

### The CleaningAgent

TODO

#### The update method

TODO

#### The deliberate method

TODO

### The GreenAgent

TODO

### The YellowAgent

TODO

### The RedAgent

TODO


## Our Model

TODO

--> parler de l'init des waste (avec la densité et comment on gère pour qu'il ne reste pas de déchet vert ou jaune unique à la fin dès l'init des wastes)


## The visualization

TODO
