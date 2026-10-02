
from __future__ import annotations
from typing import TYPE_CHECKING

from rpg.items import Weapon

if TYPE_CHECKING:
    from rpg.items import Item
    from rpg.locations import Location


class Character:
    def __init__(self, name: str, max_health: int, attack_power: int) -> None:
        if max_health <= 0:
            raise ValueError("max_health must be positive")
        if attack_power < 0:
            raise ValueError("attack_power cannot be negative")
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
        """Attack power actually used in combat. Equal to attack_power by
        default; Hero overrides this to include any equipment bonus."""
        return self.attack_power
    
    def attack(self, target: Character) -> None:
        """Deal damage to target equal to effective_attack_power(). No-op if
        either self or target is already dead."""
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
        """attack_power plus the equipped weapon's bonus, if any. Computed
        fresh each call rather than stored, so it can't drift out of sync if
        attack_power or the equipped weapon ever changes."""
        bonus = self.equipped_weapon.damage_bonus if self.equipped_weapon else 0
        return self.attack_power + bonus
    
    def pick_up(self, item: Item) -> None:
        self.inventory.append(item)
    
    def use_item(self, item: Item) -> None:
        """Apply item's effect to this hero. Removes it from inventory
        afterward only if item.consumable is True.

        Raises:
            ValueError: if item is not in this hero's inventory.
        """
        if item not in self.inventory:
            raise ValueError(f"{self.name} does not have {item.name} in the inventory")
        item.use(self)
        if item.consumable:
            self.inventory.remove(item)
    
    def equip(self, item: Item) -> None:
        """Equip item as the current weapon. Silently does nothing if item
        isn't a Weapon - called polymorphically via Item.use()."""
        if not isinstance(item, Weapon):
            return
        self.equipped_weapon = item
    
    def move_to(self, location: Location) -> None:
        self.location = location


class Enemy(Character):
    def __init__(self, name: str, max_health: int, attack_power: int, reward: Item | None = None) -> None:
        super().__init__(name, max_health, attack_power)
        self.reward = reward
