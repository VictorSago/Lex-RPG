
# Lex-RPG - Planning Notes

Working design notes. This file records design decisions, deferred ideas, and remaining development work. It is not intended to duplicate the complete implementation, which is documented by the code and docstrings.

## Overall concept

A turn-based-ish RPG system: a hero explores, fights enemies, collects/uses items, and completes a quest. The program should run through a full loop from start to a "quest complete" end state.

## Rough repo structure (surface-level, will shift)

```text
Lex-RPG/
├── README.md             # minimal placeholder for now
├── PLANNING.md           # design notes, evolves
├── .gitignore
├── main.py               # entry point - starts/runs the game
├── rpg/                  # the actual package
│   ├── __init__.py
│   ├── characters.py     # Character, Hero, Enemy (+ subclasses)
│   ├── items.py          # Item, Weapon, Potion, etc.
│   ├── quests.py         # Quest
│   └── game.py           # Game/World - ties everything together
└── tests/                # unit tests, one file per rpg/ module
    ├── __init__.py
    ├── test_characters.py
    ├── test_items.py
    ├── test_quests.py
    └── test_game.py      # later - Game does I/O, not a pure unit test
```

## Characters

### Character (base)

shared idea: something with a name and health that can take damage and be checked for whether it's still alive

- attributes: `name`, `max_health`, `current_health`, `attack_power`
- behavior:
  + `take_damage(amount)` reduces health (not below 0)
  + `is_alive()` checks health > 0
  + `attack(target)` deals damage to target based on `self.attack_power`
  + `heal(amount)` (limited at `max_health`)
- add `__str__` (a status line like "Link (HP 12/20)")

### Hero (a kind of Character)

- the player-controlled character
- carries items, can use them
- adds: `inventory` (a list of `Item`s)
- behavior:
  + `use_item(item)` - applies the item's effect to itself, then removes the item from inventory only if `item.consumable`, or keeps it (a weapon we re-use)
  + `pick_up(item)`

### Enemy (a kind of Character)

- something the hero fights
- maybe more than one enemy "type" with different behavior (e.g. different attack strength, or a reward when defeated)
- adds: maybe a reward (an Item or nothing) it drops when defeated
- if we have 2 enemy types, the difference could be as simple as different `attack_power`/`max_health` values passed at creation - doesn't necessarily need real subclass *behavior* differences to justify existing as subclasses, since "different characteristics" is enough here. Worth deciding: do we want at least one enemy with genuinely different behavior (e.g. one that heals itself), rather than just varying stats?

## Items

### Item (base)

- something the hero can carry and use
- different item types should DO different things when used
- attributes: `name`, the `consumable` flag (Weapon: False, Potion: True)
- behavior: `use(target)` - base version does nothing or raises `NotImplementedError`
  + `Weapon.use(user)` -> equips itself, boosting `user.attack_power`
  + `Potion.use(user)` -> heals `user`
- polymorphism: `Hero.use_item(item)` just calls `item.use(...)` without caring which kind it is

#### Item design principle (decided)

When code outside Item needs to ask "what kind of thing is this item" (e.g. "does it heal"), `Item` gains a method with a harmless default (e.g. `healing_value() -> int: return 0`), overridden only by the subclasses it applies to. Never a stored attribute or boolean flag on the base class for data most subclasses don't have.

Considered and rejected for now: a set of boolean flags on `Item` (consumable, healing, magical, equippable, ...) to let one item have several independent qualities (e.g. a magical weapon, a healing gauntlet). More flexible, but flags can contradict each other (equippable vs. consumable) and tracking that consistently would likely need a helper class or enum - real overengineering for a roster of two item types. Revisit only if items genuinely need to combine several independent qualities at once.

## Quests

### Quest

- represents a goal (e.g. "defeat the enemy")
- needs a way to check whether it's been completed
- attributes: `description`, `_is_complete` (bool)
- behavior: something marks it complete - either the `Game` checks a condition (e.g. "target enemy is dead") and calls `quest.complete()`, or the quest itself holds a reference to what it's tracking and has `check_complete()`. Leaning toward the *Game* driving this rather than the `Quest` reaching out to check enemy state itself - keeps `Quest` simple and dumb (just a flag + description).
- add `is_complete()`

## Tying it together

### Game / World

`Game` ties the other objects together and controls the overall game flow.

- attributes:
  + `hero`
  + `locations` - the locations that make up the game world
  + `quest`
  + `interactive` - `True` for player-controlled play, `False` for the automatic demo
  + `_visited` - a set of locations already visited during exploration
- the `Hero` is placed at a `Location` and moves between locations through their exits
- each `Location` can contain enemies and connections to other locations
- enemies belong to locations rather than directly to `Game`
- when the hero enters a location, `Game` handles any living enemies there
- after an enemy is defeated, `Game` collects its reward through `Hero.pick_up()`
- quest completion is checked after enemies are defeated; for the MVP, the quest is complete when no living enemies remain anywhere in the world

`run()` controls the outer exploration loop:

  1. enter the hero's current location
  2. fight any living enemies there
  3. collect rewards and check the quest
  4. if the quest is not complete and the hero is still alive, choose whether and where to move
  5. announce the ending when exploration stops, the hero dies, or the quest is complete

`run()` delegates the details to small private helpers:

- `_enter_location(location)` - describes the location and handles its enemies
- `_fight(enemy)` - runs combat
- `_turn_order(enemy)` - determines who acts first
- `_take_turn(combatant, opponent)` - performs one combatant's turn
- `_choose_hero_action()` - selects the hero's combat action
- `_collect_reward(enemy)` - gives an enemy's reward to the hero
- `_check_quest()` - checks the current MVP quest condition
- `_choose_move(location)` - chooses the next location
- `_announce_ending()` - reports why the game ended

All input and output goes through exactly two methods:

- `_say(text)` for output
- `_ask(prompt)` for input

Only `Game` performs I/O; `Character`, `Item`, `Location`, and `Quest` do not print or read input.

The hero's combat action is decided in `_choose_hero_action()`:

- interactive mode presents a numbered menu
- demo mode automatically uses a healing item when the hero's health is below half; otherwise the hero attacks

The demo's movement policy automatically chooses an unvisited connected location. Interactive mode lets the player choose an available exit or stop exploring.

Rewards are passed to the hero through `Hero.pick_up()` rather than modifying the inventory directly.

The current world is deliberately small: three connected locations and one enemy. More locations, enemies, items, and quests are extensions.

## What "done" looks like for the minimum version

hero exists -> enemy exists -> hero fights enemy -> health changes -> enemy defeated -> item or reward appears -> quest marked complete

Everything beyond this (more enemies, more items, more quests) is an extension, not a requirement for the core loop to work.

## Combat resolution

Simplest version - each "round," hero deals damage equal to `attack_power` (optionally boosted by an equipped weapon), then enemy retaliates if alive. No dice rolls, no randomness needed yet - keep it deterministic for now, add randomness later only if it feels worth it.

- who acts first is decided by `_turn_order(enemy)`, which returns the combatants in the order they act. For now it always returns `[hero, enemy]`. The fight loop walks that list and stops as soon as anyone is dead, so a dead combatant never acts. Later only `_turn_order` needs to change (speed/initiative, ambush, randomness).
- a fight ends when the hero or the enemy is dead

## Running the program

- `python main.py` -> interactive play (the default)
- `python main.py -d` (or `--demo`) -> automatic demo that runs to completion without input
- `-h` / `--help` comes for free with `argparse`
- argument parsing lives in `main.py` only. `Game` receives a plain `interactive` bool and knows nothing about the command line.

## Parked for later (marked in the code with TODO / FIXME)

- the hero dying to an enemy's first strike before it ever acts (matters once enemies can act first): balance the numbers, or add a rule that prevents it
- maybe detect "no change in state for N rounds"
- sub-quests, or several quests with different goals (the completion condition would live on the quest)
- multi-use items, and the demo hero never equipping weapons
- interactive/demo hero policies could become pluggable functions if they grow apart
- `Quest` growth: sub-quests, `is_complete()` logic by subclasses
- `Potion` subtypes (HealthPotion, ManaPotion, etc.) - Potion currently *is* a health potion. Don't split it into a hierarchy until a second potion type is actually needed
- a dict-of-slots on Hero, with each effective_* method summing whatever's equipped in the slots relevant to it, once a second equippable item type actually exists

## Not decided yet, to think about in the next pass

- how many enemy types, how many item types (keep it small)
- should at least one enemy override behavior (not just stats)?

## Approximate Roadmap

| Status | Phase | Description |
| --- | --- | --- |
| **done** | Skeleton, revised | redo the class signatures type-hints; confirm it imports cleanly with no runtime errors. Commit. |
| **done** | `characters.py` bodies | Character, Hero, Enemy, including `super().__init__()`. Everything else depends on this. Commit. |
| **done** | `items.py` bodies | Item, Weapon, Potion, using (`use(self, user)`). Commit. |
| **done** | `quests.py` body | simple flag-and-description class for now. Commit. |
| **done** | `game.py` body | wire hero/enemies/quest together, implement `run()` as the minimal loop. This is where the first real integration bugs will show up. |
| **done** | `main.py` | construct one hero, one enemy, a couple of items, one quest; call `Game.run()`. First point where we'll have something demoable end-to-end. Commit - "core loop works" milestone. Commit. Merge. |
| **done** | unit tests | Start the first wave of tests. Commit. |
| **partial** | tests | More tests. Integration tests for `game.py`. Commit. Merge. |
| **done** | locations | Character movement. Commit. Merge. |
| **now** | Edge cases / invalid actions | using an item not in inventory, attacking a dead enemy, using a potion at full health, etc. Commit per fix. |
| 11 | Design review pass | reread: any duplicated code, could `__str__` help? Refactor. Commit. |
| 12 | README + final cleanup | fill in the `README.md`, prune dead code, final push. |
