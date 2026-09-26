
from rpg.characters import Hero, Enemy
from rpg.quests import Quest


class Game:
    def __init__(self, hero: Hero, enemies: list[Enemy], quest: Quest) -> None:
        self.hero = hero
        self.enemies = enemies
        self.quest = quest

    def run(self) -> None:
        pass
