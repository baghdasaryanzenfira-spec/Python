from __future__ import annotations

import random
from typing import Callable

from RPG_System.models.base_character import Character
from RPG_System.models.enemy import Enemy
from RPG_System.models.inventory import Item

PromptChoice = Callable[[str, int, int], int]
PromptText = Callable[[str], str]
Announce = Callable[[str], None]


class CombatManager:
    def __init__(
        self,
        prompt_choice: PromptChoice,
        prompt_text: PromptText,
        announce: Announce,
    ) -> None:
        self.prompt_choice: PromptChoice = prompt_choice
        self.prompt_text: PromptText = prompt_text
        self.announce: Announce = announce

    def start_battle(self, hero: Character, enemies: list[Enemy]) -> bool:
        living: list[Enemy] = self._living_enemies(enemies)
        if not hero.is_alive or not living:
            return self._resolve(hero, enemies)

        self.announce(f"\nA battle begins against {len(living)} enemy(ies)!")
        for enemy in living:
            self.announce(f"  - {enemy}")

        while hero.is_alive and any(enemy.is_alive for enemy in enemies):
            saved_defense: int = self._run_hero_turn(hero, enemies)
            self._run_enemy_turn(hero, enemies)
            hero.defense = saved_defense

        return self._resolve(hero, enemies)

    def _living_enemies(self, enemies: list[Enemy]) -> list[Enemy]:
        return [enemy for enemy in enemies if enemy.is_alive]

    def _run_hero_turn(self, hero: Character, enemies: list[Enemy]) -> int:
        living: list[Enemy] = self._living_enemies(enemies)
        saved_defense: int = hero.defense
        self.announce("\n" + "-" * 55)
        self.announce(str(hero))
        for index, enemy in enumerate(living, start=1):
            self.announce(f"  {index}. {enemy.name} (HP {enemy.health}/{enemy.max_health})")

        self.announce("Actions:  1) Attack  2) Defend  3) Ability  4) Use Item")
        action: int = self.prompt_choice("Your action: ", 1, 4)

        if action in (1, 3):
            target: Enemy = self._select_target(living)
            if action == 1:
                self.announce(hero.basic_attack(target))
            else:
                self.announce(hero.special_ability(target))
        elif action == 2:
            hero.defense *= 2
            self.announce(f"{hero.name} raises a guard, doubling defense this turn.")
        elif action == 4:
            self._handle_item(hero)

        return saved_defense

    def _select_target(self, living: list[Enemy]) -> Enemy:
        if len(living) == 1:
            return living[0]
        self.announce("Choose a target:")
        for index, enemy in enumerate(living, start=1):
            self.announce(f"  {index}. {enemy.name}")
        choice: int = self.prompt_choice("Target: ", 1, len(living))
        return living[choice - 1]

    def _handle_item(self, hero: Character) -> None:
        if hero.inventory.is_empty():
            self.announce("Inventory is empty.")
            return
        self.announce(str(hero.inventory))
        item_name: str = self.prompt_text("Enter item name to use: ")
        if not item_name:
            self.announce("No item selected.")
            return
        self.announce(hero.use_item(item_name))

    def _run_enemy_turn(self, hero: Character, enemies: list[Enemy]) -> None:
        for enemy in enemies:
            if enemy.is_alive and hero.is_alive:
                self.announce(enemy.choose_action(hero))

    def _resolve(self, hero: Character, enemies: list[Enemy]) -> bool:
        if not hero.is_alive:
            self.announce("\nDefeat... your hero has fallen in battle.")
            return False
        total_xp: int = sum(enemy.xp_reward for enemy in enemies)
        self.announce("\nVictory! Every enemy has been defeated.")
        for line in hero.gain_xp(total_xp):
            self.announce(line)
        if random.random() < 0.5:
            hero.inventory.add_item(Item("Healing Potion", "Restores 40 HP.", potency=40))
            self.announce("You loot a Healing Potion from the fallen foes!")
        return True
