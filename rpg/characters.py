
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
        pass
    
    def attack(self, target: Character) -> None:
        pass
    
    def is_alive(self) -> bool:
        return True


class Hero(Character):
    def __init__(self, name: str, max_health: int, attack_power: int) -> None:
        super().__init__(name, max_health, attack_power)
    
    def use_item(self, item: Item) -> None:
        pass


class Enemy(Character):
    def __init__(self, name: str, max_health: int, attack_power: int, reward: Item | None = None) -> None:
        super().__init__(name, max_health, attack_power)
        self.reward = reward
