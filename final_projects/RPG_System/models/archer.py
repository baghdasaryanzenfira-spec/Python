from __future__ import annotations

import random

from RPG_System.models.base_character import Character
from RPG_System.models.inventory import Item


class Archer(Character):
    def __init__(self, name: str) -> None:
        super().__init__(name, health=110, attack=20, defense=7)
        self.inventory.add_item(Item("Healing Potion", "Restores 40 HP.", potency=40), 2)
        self.inventory.add_item(Item("Quiver", "Holds a bundle of sharp arrows."))

    def special_ability(self, target: Character) -> str:
        return self.arrow_shower(target)

    def arrow_shower(self, target: Character) -> str:
        arrows: int = random.randint(3, 5)
        fired: int = 0
        total: int = 0
        for _ in range(arrows):
            if not target.is_alive:
                break
            total += target.take_damage(max(1, self.attack // 2))
            fired += 1
        return (
            f"{self.name} rains an Arrow Shower of {fired} arrows on "
            f"{target.name} for {total} damage!"
        )

    def __repr__(self) -> str:
        return f"Archer(name={self.name!r}, level={self.level!r}, xp={self.xp!r})"
