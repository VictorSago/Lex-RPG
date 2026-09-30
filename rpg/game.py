
#from __future__ import annotations

from rpg.characters import Character, Hero, Enemy
from rpg.items import Item
from rpg.quests import Quest
from rpg.locations import Location


class Game:
    def __init__(self, hero: Hero, locations: list[Location], quest: Quest, interactive: bool = True) -> None:
        self.hero = hero
        self.locations = locations
        self.quest = quest
        self.interactive = interactive
        self._visited: set[Location] = set()

    def run(self) -> None:
        self._say(f"Quest: {self.quest.name} - {self.quest.description}")
        while self.hero.is_alive():
            location = self.hero.location
            assert location is not None, "Hero must be placed at a location before exploring"
            self._enter_location(location)
            if not self.hero.is_alive() or self.quest.is_complete():
                break
            if not self._choose_move(location):
                break
        self._announce_ending()
    
    def _say(self, text: str) -> None:
        print(text)
    
    def _ask(self, prompt: str) -> str:
        # # TODO: handle EOFError (closed input) and KeyboardInterrupt gracefully
        return input(prompt).strip()
    
    def _enter_location(self, location: Location) -> None:
        self._visited.add(location)
        self._say(f"\n== {location.name} ==")
        self._say(location.description)
        for enemy in list(location.enemies):
            if not enemy.is_alive():
                continue
            self._fight(enemy)
            if not self.hero.is_alive():
                return
            self._say(f"{enemy.name} is defeated!")
            self._collect_reward(enemy)
            self._check_quest()
    
    def _fight(self, enemy: Enemy) -> None:
        self._say(f"\nA fight begins: {self.hero} vs {enemy}")
        # TODO: round cap / stalemate detection (both sides at 0 attack_power loops forever)
        while self.hero.is_alive() and enemy.is_alive():
            for combatant in self._turn_order(enemy):
                opponent = enemy if combatant is self.hero else self.hero
                self._take_turn(combatant, opponent)
                self._say(f"  {self.hero} | {enemy}")
                if not self.hero.is_alive() or not enemy.is_alive():
                    break
    
    def _turn_order(self, enemy: Enemy) -> list[Character]:
            # TODO: initiative/speed, ambush, randomness. 
            # TODO: Also decide how to avoid the hero dying to a first strike before ever acting.
            return [self.hero, enemy]
        
    def _take_turn(self, combatant: Character, opponent: Character) -> None:
        if isinstance(combatant, Hero):
            item = self._choose_hero_action()
            if item is not None:
                self._say(f"{combatant.name} uses {item.name}.")
                combatant.use_item(item)
                return
        self._say(f"{combatant.name} attacks {opponent.name}!")
        combatant.attack(opponent)
    
    def _choose_hero_action(self) -> Item | None:
        """Return the item the hero uses this turn, or None to attack."""
        if self.interactive:
            return self._prompt_action()
        return self._demo_action()
    
    def _prompt_action(self) -> Item | None:
        inventory = self.hero.inventory
        self._say("Your move:")
        self._say("  0) Attack")
        for number, item in enumerate(inventory, start=1):
            self._say(f"  {number}) Use {item.name}")
        while True:
            answer = self._ask("> ")
            if answer.isdigit() and int(answer) <= len(inventory):
                choice = int(answer)
                return None if choice == 0 else inventory[choice - 1]
            self._say("Please enter one of the numbers listed above.")
    
    def _demo_action(self) -> Item | None:
        # TODO: the demo hero only heals; equipping weapons waits for an `equipped` flag
        if self.hero.current_health < self.hero.max_health // 2:
            for item in self.hero.inventory:
                if item.healing_value() > 0:
                    return item
        return None
        
    def _collect_reward(self, enemy: Enemy) -> None:
        if enemy.reward is not None:
            self._say(f"{self.hero.name} finds {enemy.reward.name}!")
            self.hero.pick_up(enemy.reward)
    
    def _check_quest(self) -> None:
        # Hardcoded rule for the MVP: done when every enemy is defeated.
        # TODO: replace with a per-quest condition (e.g. a callable stored on Quest).
        if not self.quest.is_complete() and not any(loc.has_living_enemies() for loc in self.locations):
            self._say(f"Quest complete: {self.quest.name} - {self.quest.description}")
            self.quest.complete()

    def _choose_move(self, location: Location) -> bool:
        if not location.exits:
            return False
        if self.interactive:
            return self._prompt_move(location)
        return self._demo_move(location)
    
    def _prompt_move(self, location: Location) -> bool:
        self._say("\nWhere to?")
        options = list(location.exits.items())
        for number, (direction, destination) in enumerate(options, start=1):
            self._say(f"  {number}) Go {direction} to {destination.name}")
        self._say("  0) Stop exploring")
        while True:
            answer = self._ask("> ")
            if answer.isdigit() and int(answer) <= len(options):
                choice = int(answer)
                if choice == 0:
                    return False
                _, destination = options[choice - 1]
                self.hero.move_to(destination)
                return True
            self._say("Please enter one of the numbers listed above.")

    def _demo_move(self, location: Location) -> bool:
        for direction, destination in location.exits.items():
            if destination not in self._visited:
                self.hero.move_to(destination)
                return True
        return False
    
    def _announce_ending(self) -> None:
        if not self.hero.is_alive():
            self._say(f"\n{self.hero.name} has fallen. Game over.")
        elif self.quest.is_complete():
            self._say(f"\nQuest complete: {self.quest.description}")
            self._say(f"{self.hero.name} can rest, for now.")
        else:
            self._say(f"\n{self.hero.name} stops exploring. The quest remains unfinished.")
