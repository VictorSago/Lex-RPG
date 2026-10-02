
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
    
    def is_in_use(self, user: Character) -> bool:
        """Whether using this item right now would have no effect
        (e.g. a weapon that's already equipped). False by default."""
        return False
    
    def healing_value(self) -> int:
        """How much health using this item would restore. 0 if it doesn't heal."""
        return 0


class Weapon(Item):
    def __init__(self, name: str, damage_bonus: int) -> None:
        if damage_bonus < 0:
            raise ValueError("damage_bonus cannot be negative")
        super().__init__(name, consumable=False)
        self.damage_bonus = damage_bonus
    
    def use(self, user: Character) -> None:
        user.equip(self)
    
    def is_in_use(self, user: Character) -> bool:
        return getattr(user, "equipped_weapon", None) is self


class Potion(Item):
    def __init__(self, name: str, heal_amount: int) -> None:
        if heal_amount < 0:
            raise ValueError("heal_amount cannot be negative")
        super().__init__(name, consumable=True)
        self.heal_amount = heal_amount
    
    def use(self, user: Character) -> None:
        user.heal(self.heal_amount)
    
    def is_in_use(self, user: Character) -> bool:
        return user.current_health >= user.max_health
    
    def healing_value(self) -> int:
        return self.heal_amount
