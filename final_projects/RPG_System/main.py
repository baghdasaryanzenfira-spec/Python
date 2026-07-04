#!/usr/bin/python3
from __future__ import annotations

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import random
from typing import Optional

from RPG_System.models.archer import Archer
from RPG_System.models.base_character import Character
from RPG_System.models.enemy import Enemy
from RPG_System.models.mage import Mage
from RPG_System.models.warrior import Warrior
from RPG_System.services.combat_manager import CombatManager
from RPG_System.utils.validators import Validators


class SessionExit(Exception):
    pass


class Application:
    def __init__(self) -> None:
        self.hero: Optional[Character] = None
        self.running: bool = True
        self.combat: CombatManager = CombatManager(
            prompt_choice=self.prompt_choice,
            prompt_text=self.prompt_text,
            announce=print,
        )

    def prompt_choice(self, message: str, minimum: int, maximum: int) -> int:
        while True:
            try:
                return Validators.parse_menu_choice(input(message), minimum, maximum)
            except ValueError:
                print(f"Invalid input. Enter a number between {minimum} and {maximum}.")
            except (KeyboardInterrupt, EOFError):
                raise SessionExit

    def prompt_text(self, message: str) -> str:
        try:
            return input(message).strip()
        except (KeyboardInterrupt, EOFError):
            raise SessionExit

    def create_hero(self) -> None:
        name: str = self.prompt_text("Enter your hero's name: ")
        if not Validators.validate_name(name):
            print("Invalid name. Use up to 20 alphanumeric characters.")
            return
        print("Choose a class:  1) Warrior  2) Mage  3) Archer")
        choice: int = self.prompt_choice("Class: ", 1, 3)
        try:
            if choice == 1:
                self.hero = Warrior(name)
            elif choice == 2:
                self.hero = Mage(name)
            else:
                self.hero = Archer(name)
        except ValueError as error:
            print(f"Failed to create hero: {error}")
            return
        print(f"\n{self.hero.name} the {type(self.hero).__name__} enters the realm!")

    def view_profile(self) -> None:
        if self.hero is None:
            print("No hero exists yet. Create one with option 1.")
            return
        print("\n" + "=" * 55)
        print(self.hero)
        print(self.hero.inventory)
        print(repr(self.hero))
        print("=" * 55)

    def enter_battle(self) -> None:
        if self.hero is None:
            print("Create a hero before entering battle.")
            return
        if not self.hero.is_alive:
            print("Your hero has fallen and cannot fight. Create a new hero.")
            return
        group_size: int = random.randint(1, 3)
        enemies: list[Enemy] = Enemy.spawn_group(group_size, self.hero.level)
        self.combat.start_battle(self.hero, enemies)

    def exit_game(self) -> None:
        self.running = False
        print(f"\nTotal characters created this session: {Character.total_characters_created}")
        print("Thank you for playing. Farewell, hero!")

    def run(self) -> None:
        print("=" * 55)
        print("            WELCOME TO THE RPG_SYSTEM ARENA")
        print("=" * 55)
        while self.running:
            print("\nMain Menu:")
            print("  1) Create a Hero")
            print("  2) View Hero Profile")
            print("  3) Enter Battle")
            print("  4) Exit Game")
            try:
                choice: int = self.prompt_choice("Select an option: ", 1, 4)
                if choice == 1:
                    self.create_hero()
                elif choice == 2:
                    self.view_profile()
                elif choice == 3:
                    self.enter_battle()
                elif choice == 4:
                    self.exit_game()
            except SessionExit:
                self.exit_game()


def main() -> None:
    Application().run()


if __name__ == "__main__":
    main()
