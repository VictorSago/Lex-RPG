
from __future__ import annotations

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
        self._path: list[Location] = []
        self._enemies_defeated = 0

    def run(self) -> None:
        """Main loop: enter the hero's current location, fight anything
        living there, then choose where to move next. Repeats until the hero
        dies, the quest completes, or exploration stops (player choice in
        interactive mode, or no unexplored paths left in demo mode)."""
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
        """Read one line of input. Exits the program cleanly on EOF or Ctrl-C 
        instead of letting a raw traceback through."""
        try:
            return input(prompt).strip()
        except (EOFError, KeyboardInterrupt):
            self._say("\nExiting the game.")
            raise SystemExit(0)
    
    def _enter_location(self, location: Location) -> None:
        """Describe location and resolve every living enemy there one at a
        time (fight, announce, hand over reward, re-check the quest). Returns
        early if the hero doesn't survive."""
        self._visited.add(location)
        self._path.append(location)
        self._say(f"\n== {location.name} ==")
        self._say(location.description)
        for enemy in list(location.enemies):
            if not enemy.is_alive():
                continue
            self._fight(enemy)
            if not self.hero.is_alive():
                return
            self._say(f"{enemy.name} is defeated!")
            self._enemies_defeated += 1
            self._collect_reward(enemy)
            self._check_quest()
    
    def _fight(self, enemy: Enemy) -> None:
        """Run combat until one side is dead, or MAX_ROUNDS is reached - a
        guard against an unwinnable stalemate (e.g. 0 damage either side)."""
        MAX_ROUNDS = 100  # safety net against a stalemate (e.g. 0 damage on both sides)
        rounds = 0
        self._say(f"\nA fight begins: {self.hero} vs {enemy}")
        while self.hero.is_alive() and enemy.is_alive() and rounds < MAX_ROUNDS:
            rounds += 1
            for combatant in self._turn_order(enemy):
                opponent = enemy if combatant is self.hero else self.hero
                self._take_turn(combatant, opponent)
                self._say(f"  {self.hero} | {enemy}")
                if not self.hero.is_alive() or not enemy.is_alive():
                    break
        if rounds >= MAX_ROUNDS and self.hero.is_alive() and enemy.is_alive():
            self._say(f"The battle against {enemy.name} drags on inconclusively. Retreating!")
    
    def _turn_order(self, enemy: Enemy) -> list[Character]:
        # TODO: initiative/speed, ambush, randomness. 
        # TODO: Also decide how to avoid the hero dying to a first strike before ever acting.
        return [self.hero, enemy]
        
    def _take_turn(self, combatant: Character, opponent: Character) -> None:
        """Resolve one combatant's turn. The hero may use an item instead of
        attacking; every other combatant always attacks."""
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
        inventory = [item for item in self.hero.inventory if not item.is_in_use(self.hero)]
        self._say("Your move:")
        self._say("  0) Attack")
        for number, item in enumerate(inventory, start=1):
            self._say(f"  {number}) Use {item.name}")
        choice = self._prompt_numeric_choice(len(inventory))
        return None if choice == 0 else inventory[choice - 1]
    
    def _prompt_numeric_choice(self, max_choice: int) -> int:
        """Ask for a number from 0 to max_choice, retrying on invalid input."""
        while True:
            answer = self._ask("> ")
            if answer.isdigit() and int(answer) <= max_choice:
                return int(answer)
            self._say("Please enter one of the options listed above.")
    
    def _demo_action(self) -> Item | None:
        # TODO: the demo hero only heals, never proactively equips a stronger weapon it finds
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
        while True:
            self._say("\nWhat next?")
            self._say("  i) Check inventory / use or equip an item")
            for number, (direction, destination) in enumerate(location.exits.items(), start=1):
                self._say(f"  {number}) Go {direction} to {destination.name}")
            self._say("  0) Stop exploring")
            answer = self._ask("> ")
            if answer.lower() == "i":
                self._manage_inventory()
                continue
            if answer.isdigit() and int(answer) <= len(location.exits):
                choice = int(answer)
                if choice == 0:
                    return False
                _, destination = list(location.exits.items())[choice - 1]
                self.hero.move_to(destination)
                return True
            self._say("Please enter one of the options listed above.")
    
    def _manage_inventory(self) -> None:
        inventory = self.hero.inventory
        if not inventory:
            self._say("Your inventory is empty.")
            return
        self._say("Inventory:")
        for number, item in enumerate(inventory, start=1):
            tag = " (no effect right now)" if item.is_in_use(self.hero) else ""
            self._say(f"  {number}) {item.name}{tag}")
        self._say("  0) Back")
        choice = self._prompt_numeric_choice(len(inventory))
        if choice == 0:
            return
        item = inventory[choice - 1]
        if item.is_in_use(self.hero):
            self._say(f"Using {item.name} wouldn't do anything right now.")
            return
        self._say(f"{self.hero.name} uses {item.name}.")
        self.hero.use_item(item)

    def _demo_move(self, location: Location) -> bool:
        """Choose the demo hero's next move: prefer an unvisited exit from
        location. If every exit leads somewhere already visited (a dead end),
        backtrack to the nearest earlier location on the path that still has
        an unvisited exit, and let the next loop iteration try again from
        there. Returns False only once nothing in the whole map is left to
        explore."""
        for destination in location.exits.values():
            if destination not in self._visited:
                self.hero.move_to(destination)
                return True
        # Dead end: backtrack to the nearest earlier location that still has an
        # unexplored exit, and let the next loop iteration try again from there.
        for previous in reversed(self._path[:-1]):
            if any(dest not in self._visited for dest in previous.exits.values()):
                self._say(f"{self.hero.name} heads back to {previous.name} to try another path.")
                self.hero.move_to(previous)
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
        self._say("\n--- Adventure Stats ---")
        self._say(f"Locations explored: {len(self._visited)}")
        self._say(f"Enemies defeated: {self._enemies_defeated}")
        self._say(f"Quest status: {'Complete' if self.quest.is_complete() else 'Incomplete'}")
