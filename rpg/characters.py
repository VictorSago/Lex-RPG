
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from rpg.items import Item


class Character:
    def __init__(self, name: str, max_health: int, attack_power: int) -> None:
        self.name = name
        self.max_health = max_health
        self.current_health = self.max_health
        self.attack_power = attack_power
    
    def take_damage(self, amount: int) -> None:
        self.current_health = max(0, self.current_health - amount)
    
    def heal(self, amount: int) -> None:
        self.current_health = min(self.max_health, self.current_health + amount)
    
    def attack(self, target: Character) -> None:
        target.take_damage(self.attack_power)
    
    def is_alive(self) -> bool:
        return self.current_health > 0
    
    def __str__(self) -> str:
        return f"{self.name} (HP {self.current_health}/{self.max_health})"


class Hero(Character):
    def __init__(self, name: str, max_health: int, attack_power: int) -> None:
        super().__init__(name, max_health, attack_power)
        self.inventory: list[Item] = []
    
    def pick_up(self, item: Item) -> None:
        self.inventory.append(item)
    
    def use_item(self, item: Item) -> None:
        if item not in self.inventory:
            raise ValueError(f"{self.name} does not {item.name} in the inventory")
        item.use(self)
        if item.consumable:
            self.inventory.remove(item)


class Enemy(Character):
    def __init__(self, name: str, max_health: int, attack_power: int, reward: Item | None = None) -> None:
        super().__init__(name, max_health, attack_power)
        self.reward = reward
