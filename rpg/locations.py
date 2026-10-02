
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from rpg.characters import Enemy


class Location:
    def __init__(self, name: str, description: str) -> None:
        self.name = name
        self.description = description
        self.exits: dict[str, Location] = {}
        self.enemies: list[Enemy] = []

    def add_enemy(self, enemy: Enemy) -> None:
        self.enemies.append(enemy)

    def add_exit(self, direction: str, destination: Location, *, reciprocal: str | None = None) -> None:
        """Add a one-way exit from this location to destination. If reciprocal 
        is given, also adds the return exit back to this location under that 
        direction - pass it for a two-way passage, leave it None for a 
        one-way passage."""
        self.exits[direction] = destination
        if reciprocal is not None:
            destination.exits[reciprocal] = self

    def has_living_enemies(self) -> bool:
        return any(e.is_alive() for e in self.enemies)
