
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from rpg.characters import Character


class Item:
    def __init__(self, name: str, consumable: bool) -> None:
        self.name = name
        self.consumable = consumable
    
    def use(self, user: Character) -> None:
        raise NotImplementedError


class Weapon(Item):
    def __init__(self, name: str, damage_bonus: int):
        super().__init__(name, consumable=False)
        self.damage_bonus = damage_bonus
    
    def use(self, user: Character) -> None:
        user.attack_power += self.damage_bonus


class Potion(Item):
    def __init__(self, name: str, heal_amount: int) -> None:
        super().__init__(name, consumable=True)
        self.heal_amount = heal_amount
    
    def use(self, user: Character) -> None:
        user.heal(self.heal_amount)
