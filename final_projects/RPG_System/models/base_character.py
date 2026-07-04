from __future__ import annotations

import random

from RPG_System.models.inventory import Inventory, Item
from RPG_System.utils.validators import Validators


class Character:
    total_characters_created: int = 0
    xp_per_level: int = 100

    def __init__(
        self,
        name: str,
        health: int,
        attack: int,
        defense: int,
        level: int = 1,
        xp: int = 0,
    ) -> None:
        if not Validators.validate_stats(health, attack, defense):
            raise ValueError(f"Invalid stats for character '{name}'.")
        self.name: str = name
        self.max_health: int = health
        self.health: int = health
        self.attack: int = attack
        self.defense: int = defense
        self.level: int = level
        self.xp: int = xp
        self.inventory: Inventory = Inventory()
        Character.total_characters_created += 1

    @property
    def is_alive(self) -> bool:
        return self.health > 0

    def take_damage(self, incoming: int) -> int:
        mitigated: int = max(1, incoming - self.defense)
        self.health = max(0, self.health - mitigated)
        return mitigated

    def heal(self, amount: int) -> int:
        restored: int = min(amount, self.max_health - self.health)
        self.health += restored
        return restored

    def basic_attack(self, target: Character) -> str:
        power: int = self.attack + random.randint(-2, 2)
        dealt: int = target.take_damage(max(1, power))
        return f"{self.name} attacks {target.name} for {dealt} damage."

    def special_ability(self, target: Character) -> str:
        return self.basic_attack(target)

    def gain_xp(self, amount: int) -> list[str]:
        messages: list[str] = [f"{self.name} gains {amount} XP."]
        self.xp += amount
        while self.xp >= self.xp_per_level:
            self.xp -= self.xp_per_level
            messages.extend(self.level_up())
        return messages

    def level_up(self) -> list[str]:
        self.level += 1
        self.max_health += 15
        self.health = self.max_health
        self.attack += 4
        self.defense += 2
        return [f"{self.name} advances to level {self.level}! Stats grow and health is restored."]

    def use_item(self, item_name: str) -> str:
        item: Item | None = self.inventory.peek(item_name)
        if item is None:
            return f"{self.name} has no {item_name} to use."
        if item.potency <= 0:
            return f"{item.name} cannot be consumed and stays in the inventory."
        if self.health >= self.max_health:
            return f"{self.name} is already at full health and saves the {item.name}."
        self.inventory.remove_item(item_name)
        restored: int = self.heal(item.potency)
        return f"{self.name} uses {item.name} and restores {restored} HP."

    def __str__(self) -> str:
        return (
            f"{self.name} [{type(self).__name__}] "
            f"Lv.{self.level} | HP {self.health}/{self.max_health} | "
            f"ATK {self.attack} | DEF {self.defense} | XP {self.xp}/{self.xp_per_level}"
        )

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}(name={self.name!r}, health={self.max_health!r}, "
            f"attack={self.attack!r}, defense={self.defense!r}, "
            f"level={self.level!r}, xp={self.xp!r})"
        )
