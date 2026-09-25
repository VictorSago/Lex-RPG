
# Lex-RPG - Planning Notes

Working design notes. This file will change and grow as decisions get made,
and will eventually be superseded by the actual code and docstrings (and a proper `README.md`).

## Overall concept

A turn-based-ish RPG system: a hero explores, fights enemies, collects/uses
items, and completes a quest. The program should run through a full loop from
start to a "quest complete" end state.

## Rough repo structure (surface-level, will shift)

Lex-RPG/
├── README.md           # minimal placeholder for now
├── PLANNING.md         # today's outline lives here, evolves
├── .gitignore
├── main.py             # entry point - starts/runs the game
└── rpg/                # the actual package
    ├── __init__.py
    ├── characters.py   # Character, Hero, Enemy (+ subclasses)
    ├── items.py        # Item, Weapon, Potion, etc.
    ├── quest.py        # Quest
    └── game.py         # Game/World - ties everything together

## Characters

### Character (base)

shared idea: something with a name and health that can take damage and be checked for whether it's still alive

- attributes: `name`, `max_health`, `current_health`, `attack_power`
- behavior:
  + `take_damage(amount)` reduces health (not below 0)
  + `is_alive()` checks health > 0
  + `attack(target)` deals damage to target based on `self.attack_power`

### Hero (a kind of Character)

- the player-controlled character
- carries items, can use them
- adds: `inventory` (a list of `Item`s)
- behavior: `use_item(item)` - applies the item's effect to itself, then likely removes it from inventory (consumables) or keeps it (a weapon we re-use)

### Enemy (a kind of Character)

- something the hero fights
- maybe more than one enemy "type" with different behavior (e.g. different attack strength, or a reward when defeated)
- adds: maybe a reward (an Item or nothing) it drops when defeated
- if we have 2 enemy types, the difference could be as simple as different `attack_power`/`max_health` values passed at creation - doesn't necessarily need real subclass *behavior* differences to justify existing as subclasses, since "different characteristics" is enough here. Worth deciding: do we want at least one enemy with genuinely different behavior (e.g. one that heals itself), rather than just varying stats?

## Items

### Item (base)

- something the hero can carry and use
- different item types should DO different things when used
- attributes: `name`
- behavior: `use(target)` - base version does nothing or raises `NotImplementedError`
  + `Weapon.use(user)` -> equips itself, boosting `user.attack_power`
  + `Potion.use(user)` -> heals `user`
- polymorphism: `Hero.use_item(item)` just calls `item.use(...)` without caring which kind it is

## Quests

### Quest

- represents a goal (e.g. "defeat the enemy")
- needs a way to check whether it's been completed
- attributes: `description`, `is_complete` (bool)
- behavior: something marks it complete - either the `Game` checks a condition (e.g. "target enemy is dead") and calls `quest.complete()`, or the quest itself holds a reference to what it's tracking and has `check_complete()`. Leaning toward the *Game* driving this rather than the `Quest` reaching out to check enemy state itself - keeps `Quest` simple and dumb (just a flag + description).

## Tying it together

### Game / World

- owns the hero, the current enemy/enemies, the quest
- this is where the actual "run" happens: hero acts, state changes, consequences ripple (enemy takes damage, hero takes damage, quest gets checked, etc.)
- attributes: `hero`, `enemies` (list, even if we start with one), `quest`
- behavior: `run()` - the orchestration: hero attacks enemy, enemy attacks back if still alive, repeat until someone dies; on enemy death, hand over reward, check/complete quest

## What "done" looks like for the minimum version

hero exists -> enemy exists -> hero fights enemy -> health changes -> enemy defeated -> item or reward appears -> quest marked complete

Everything beyond this (more enemies, more items, more quests) is an extension, not a requirement for the core loop to work.

## Combat resolution

Simplest version - each "round," hero deals damage equal to `attack_power` (optionally boosted by an equipped weapon), then enemy retaliates if alive. No dice rolls, no randomness needed yet - keep it deterministic for now, add randomness later only if it feels worth it.

## Not decided yet, to think about in the next pass

- how many enemy types, how many item types (keep it small)
- should at least one enemy override behavior (not just stats)?
- does an unarmed `Hero` have some baseline `attack_power`, or does `attack()` do nothing meaningful until a weapon is equipped?
- file/module split (characters, items, quest, game runner, etc.)
