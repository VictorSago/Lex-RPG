
#from __future__ import annotations
from rpg.characters import Character, Hero, Enemy
from rpg.items import Item
from rpg.quests import Quest


class Game:
    def __init__(self, hero: Hero, enemies: list[Enemy], quest: Quest, interactive: bool = True) -> None:
        self.hero = hero
        self.enemies = enemies
        self.quest = quest
        self.interactive = interactive
    
    def _say(self, text: str) -> None:
        print(text)
    
    def _ask(self, prompt: str) -> str:
        # # TODO: handle EOFError (closed input) and KeyboardInterrupt gracefully
        return input(prompt).strip()
    
    def _fight(self, enemy: Enemy) -> None:
        self._say(f"\nA fight begins: {self.hero} vs {enemy}")
        # TODO: round cap / stalemate detection (both sides at 0 attack_power loops forever)
        while self.hero.is_alive() and enemy.is_alive():
            for combatant in self._turn_order(enemy):
                self._take_turn(combatant, enemy)
                self._say(f"  {self.hero} | {enemy}")
                if not (self.hero.is_alive() and enemy.is_alive()):
                    break
    
    def _turn_order(self, enemy: Enemy) -> list[Character]:
            # TODO: initiative/speed, ambush, randomness. 
            # TODO: Also decide how to avoid the hero dying to a first strike before ever acting.
            return [self.hero, enemy]
        
    def _take_turn(self, combatant: Character, enemy: Enemy) -> None:
        if combatant is self.hero:
            self._hero_turn(enemy)
        else:
            self._enemy_turn(enemy)
    
    def _hero_turn(self, enemy: Enemy) -> None:
        item = self._choose_hero_action(enemy)
        if item is None:
            self._say(f"{self.hero.name} attacks {enemy.name}!")
            self.hero.attack(enemy)
        else:
            self._say(f"{self.hero.name} uses {item.name}.")
            self.hero.use_item(item)
    
    def _enemy_turn(self, enemy: Enemy) -> None:
        self._say(f"{enemy.name} attacks {self.hero.name}!")
        enemy.attack(self.hero)
    
    def _choose_hero_action(self, enemy: Enemy) -> Item | None:
        """Return the item the hero uses this turn, or None to attack."""
        if self.interactive:
            return self._prompt_action()
        return self._demo_action()
    
    def _prompt_action(self) -> Item | None:
        inventory = self.hero.inventory
        self._say("Your move:")
        self._say("  0) Attack")
        for number, item in enumerate(inventory):
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
                if item.consumable:
                    return item
        return None
        
    def _collect_reward(self, enemy: Enemy) -> None:
        if enemy.reward is not None:
            self._say(f"{self.hero.name} finds {enemy.reward.name}!")
            self.hero.pick_up(enemy.reward)
    
    def _check_quest(self) -> None:
        # Hardcoded rule for the MVP: done when every enemy is defeated.
        # TODO: replace with a per-quest condition (e.g. a callable stored on Quest).
        if not self.quest.is_comlete() and all(not e.is_alive() for e in self.enemies):
            self._say(f"Quest complete: {self.quest.description}")
            self.quest.complete()
    
    def run(self) -> None:
        self._say(f"Quest: {self.quest.description}")
        for enemy in self.enemies:
            self._fight(enemy)
            if not self.hero.is_alive():
                break
            self._say(f"{enemy.name} is defeated!")
            self._collect_reward(enemy)
            self._check_quest()
        
        if self.hero.is_alive():
            self._say(f"{self.hero.name} survives the adventure.")
        else:
            self._say(f"{self.hero.name} has fallen! Game over!")
