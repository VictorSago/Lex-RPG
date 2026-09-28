
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
        pass
    
    def _collect_reward(self, enemy: Enemy) -> None:
        pass
    
    def _check_quest(self) -> None:
        pass
    
    def hero_is_alive(self) -> bool:
        return True

    def run(self) -> None:
        self._say(f"Quest: {self.quest.description}")
        for enemy in self.enemies:
            self._fight(enemy)
            if not self.hero_is_alive():
                break
            self._say(f"{enemy.name} is defeated!")
            self._collect_reward(enemy)
            self._check_quest()
        
        if self.hero_is_alive():
            self._say(f"{self.hero.name} survives the adventure.")
        else:
            self._say(f"{self.hero.name} has fallen! Game over!")
