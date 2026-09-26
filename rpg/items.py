
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from rpg.characters import Character


class Item:
    def __init__(self, name: str) -> None:
        self.name = name
    
    def use(self, user: Character) -> None:
        pass


class Weapon(Item):
    def __init__(self, name: str, damage_bonus: int):
        super().__init__(name)
        self.damage_bonus = damage_bonus
    
    def use(self, user: Character) -> None:
        pass


class Potion(Item):
    def __init__(self, name: str, heal_amount: int) -> None:
        super().__init__(name)
        self.heal_amount = heal_amount
    
    def use(self, user: Character) -> None:
        pass
