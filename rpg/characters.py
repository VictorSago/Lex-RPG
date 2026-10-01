
from __future__ import annotations
from typing import TYPE_CHECKING

from rpg.items import Weapon

if TYPE_CHECKING:
    from rpg.items import Item
    from rpg.locations import Location


class Character:
    def __init__(self, name: str, max_health: int, attack_power: int) -> None:
        self.name = name
        self.max_health = max_health
        self.current_health = self.max_health
        self.attack_power = attack_power
    
    def take_damage(self, amount: int) -> None:
        if amount < 0:
            raise ValueError("damage amount cannot be negative")
        self.current_health = max(0, self.current_health - amount)
    
    def heal(self, amount: int) -> None:
        if amount < 0:
            raise ValueError("heal amount cannot be negative")
        self.current_health = min(self.max_health, self.current_health + amount)
    
    def effective_attack_power(self) -> int:
        return self.attack_power
    
    def attack(self, target: Character) -> None:
        if self.is_alive() and target.is_alive():
            target.take_damage(self.effective_attack_power())
    
    def is_alive(self) -> bool:
        return self.current_health > 0
    
    def equip(self, item: Item) -> None:
        """Equip an item. Does nothing by default - only characters that
        track equipment (currently just Hero) override this."""
        pass
    
    def __str__(self) -> str:
        return f"{self.name} (HP {self.current_health}/{self.max_health})"


class Hero(Character):
    def __init__(self, name: str, max_health: int, attack_power: int) -> None:
        super().__init__(name, max_health, attack_power)
        self.inventory: list[Item] = []
        self.location: Location | None = None  # set once the world is built
        self.equipped_weapon: Weapon | None = None
    
    def effective_attack_power(self) -> int:
        bonus = self.equipped_weapon.damage_bonus if self.equipped_weapon else 0
        return self.attack_power + bonus
    
    def pick_up(self, item: Item) -> None:
        self.inventory.append(item)
    
    def use_item(self, item: Item) -> None:
        if item not in self.inventory:
            raise ValueError(f"{self.name} does not have {item.name} in the inventory")
        item.use(self)
        if item.consumable:
            self.inventory.remove(item)
    
    def equip(self, item: Item) -> None:
        if not isinstance(item, Weapon):
            return
        self.equipped_weapon = item
    
    def move_to(self, location: Location) -> None:
        self.location = location


class Enemy(Character):
    def __init__(self, name: str, max_health: int, attack_power: int, reward: Item | None = None) -> None:
        super().__init__(name, max_health, attack_power)
        self.reward = reward
