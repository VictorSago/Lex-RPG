# Lex-RPG - Planning Notes

Working design notes. This file will change and grow as decisions get
made, and will eventually be superseded by the actual code and
docstrings (and a proper `README.md`).

## Overall concept

A turn-based-ish RPG system: a hero explores, fights enemies,
collects/uses items, and completes a quest. The program should run
through a full loop from start to a "quest complete" end state.

## Characters

**Character (base)**

- shared idea: something with a name and health that can take damage
  and be checked for whether it's still alive

**Hero (a kind of Character)**

- the player-controlled character
- carries items, can use them

**Enemy (a kind of Character)**

- something the hero fights
- maybe more than one enemy "type" with different behavior
  (e.g. different attack strength, or a reward when defeated)

## Items

**Item (base)**

- something the hero can carry and use
- different item types should DO different things when used

## Quest

**Quest**

- represents a goal (e.g. "defeat the enemy")
- needs a way to check whether it's been completed

## Tying it together

**Game / World**

- owns the hero, the current enemy/enemies, the quest
- this is where the actual "run" happens: hero acts, state changes,
  consequences ripple (enemy takes damage, hero takes damage, quest
  gets checked, etc.)

## What "done" looks like for the minimum version

hero exists -> enemy exists -> hero fights enemy -> health changes ->
enemy defeated -> item or reward appears -> quest marked complete

Everything beyond this (more enemies, more items, more quests) is an
extension, not a requirement for the core loop to work.

## Not decided yet, to think about in the next pass

- how many enemy types, how many item types (keep it small)
- how combat actually works (simple stat subtraction vs. something
  with more nuance)
- whether Quest needs its own class at all, or could start as
  something simpler and grow into a class if needed
- file/module split (characters, items, quest, game runner, etc.)
