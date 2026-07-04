from __future__ import annotations

from RPG_System.models.base_character import Character
from RPG_System.models.inventory import Item


class Warrior(Character):
    def __init__(self, name: str) -> None:
        super().__init__(name, health=140, attack=18, defense=10)
        self.inventory.add_item(Item("Healing Potion", "Restores 40 HP.", potency=40), 2)
        self.inventory.add_item(Item("Iron Sword", "A sturdy blade forged for war."))

    def special_ability(self, target: Character) -> str:
        return self.shield_bash(target)

    def shield_bash(self, target: Character) -> str:
        power: int = int(self.attack * 1.5) + self.defense
        dealt: int = target.take_damage(power)
        return f"{self.name} slams {target.name} with a Shield Bash for {dealt} damage!"

    def __repr__(self) -> str:
        return f"Warrior(name={self.name!r}, level={self.level!r}, xp={self.xp!r})"
