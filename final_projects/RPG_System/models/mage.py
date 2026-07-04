from __future__ import annotations

from RPG_System.models.base_character import Character
from RPG_System.models.inventory import Item


class Mage(Character):
    def __init__(self, name: str) -> None:
        super().__init__(name, health=90, attack=24, defense=5)
        self.inventory.add_item(Item("Healing Potion", "Restores 40 HP.", potency=40), 2)
        self.inventory.add_item(Item("Mana Crystal", "Hums with arcane energy."))

    def special_ability(self, target: Character) -> str:
        return self.cast_spell(target)

    def cast_spell(self, target: Character) -> str:
        power: int = self.attack * 2
        dealt: int = target.take_damage(power)
        return f"{self.name} hurls an Arcane Bolt at {target.name} for {dealt} damage!"

    def __repr__(self) -> str:
        return f"Mage(name={self.name!r}, level={self.level!r}, xp={self.xp!r})"
