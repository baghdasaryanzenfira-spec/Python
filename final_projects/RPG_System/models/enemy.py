from __future__ import annotations

import random

from RPG_System.models.base_character import Character


class Enemy(Character):
    templates: list[tuple[str, int, int, int, int]] = [
        ("Goblin", 45, 10, 3, 40),
        ("Orc", 70, 15, 6, 65),
        ("Dark Skeleton", 60, 18, 4, 70),
        ("Cave Troll", 100, 20, 8, 110),
    ]

    def __init__(
        self,
        name: str,
        health: int,
        attack: int,
        defense: int,
        xp_reward: int,
    ) -> None:
        super().__init__(name, health, attack, defense)
        self.xp_reward: int = xp_reward

    @classmethod
    def generate_random(cls, level_scaling: int = 1) -> Enemy:
        name, health, attack, defense, xp = random.choice(cls.templates)
        scale: float = 1.0 + (max(1, level_scaling) - 1) * 0.2
        return cls(
            name=name,
            health=max(1, int(health * scale)),
            attack=max(1, int(attack * scale)),
            defense=int(defense * scale),
            xp_reward=max(1, int(xp * scale)),
        )

    @classmethod
    def spawn_group(cls, size: int, level_scaling: int = 1) -> list[Enemy]:
        return [cls.generate_random(level_scaling) for _ in range(max(1, size))]

    def choose_action(self, target: Character) -> str:
        return self.basic_attack(target)

    def __str__(self) -> str:
        return (
            f"{self.name} [Enemy] HP {self.health}/{self.max_health} | "
            f"ATK {self.attack} | DEF {self.defense} | Reward {self.xp_reward} XP"
        )

    def __repr__(self) -> str:
        return (
            f"Enemy(name={self.name!r}, health={self.max_health!r}, "
            f"attack={self.attack!r}, defense={self.defense!r}, "
            f"xp_reward={self.xp_reward!r})"
        )
