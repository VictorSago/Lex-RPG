
# Lex-RPG

A small Python fantasy-adventure/RPG system built as the final project for **Python Fundamentals**.

The game follows a hero exploring a small world, fighting enemies, collecting and using items, and completing a quest.

## Features

* Object-oriented design using classes, inheritance, and polymorphism
* A `Character` base class with `Hero` and `Enemy` subclasses
* A small item system with weapons and healing potions
* Hero inventory and weapon equipment
* A location-based world with connected locations and exits
* Turn-based combat with health and attack mechanics
* Enemy rewards that can be collected by the hero
* A quest that is completed when all enemies have been defeated
* Interactive play with player choices
* An automatic demo mode for running the game without input
* Input/output handled by the `Game` class, keeping the other classes independent of user interaction
* Validation of invalid or no-op actions (negative stats rejected at creation, already-equipped weapons and full-health potions filtered from menus, actions on invalid items rejected)

## Project structure

```text
Lex-RPG/
├── main.py
├── PLANNING.md
├── README.md
├── .gitignore
├── rpg/
│   ├── __init__.py
│   ├── characters.py
│   ├── game.py
│   ├── items.py
│   ├── locations.py
│   └── quests.py
└── tests/
    ├── __init__.py
    ├── test_characters.py
    ├── test_items.py
    ├── test_locations.py
    └── test_quests.py
```

### Main modules

* **`characters.py`** — characters, combat, health, inventory, and equipment
* **`items.py`** — items, weapons, and potions
* **`locations.py`** — locations, exits, and enemies
* **`quests.py`** — quest state and completion
* **`game.py`** — game flow, exploration, combat, and interaction
* **`main.py`** — command-line entry point and initial game setup

## Running the game

Run the game interactively:

```bash
python main.py
```

The player can choose whether to attack or use an inventory item during combat, and can choose where to move when multiple exits are available.

To run the automatic demonstration without entering any input:

```bash
python main.py --demo
```

The short form is also available:

```bash
python main.py -d
```

To see the available command-line options:

```bash
python main.py --help
```

## Running the tests

```bash
python -m unittest
```

## Current game

The hero starts at the Village Outskirts and can explore a small branching world: a path north through the Dark Forest leads to a side route (the Old Bridge and the Abandoned Mill) as well as to the Goblin Cave. A Goblin and a Bandit must be defeated; each drops a weapon the hero can equip. A Health Potion is available from the start.

The current quest is "Clear the Wilds" - rid the woods of the goblin and the bandit threatening the village.

## Status

The core game system is implemented and runnable. Further development is focused on edge cases, validation, testing, and final cleanup rather than on adding a large number of new game mechanics.
