from __future__ import annotations


class Validators:
    @staticmethod
    def validate_stats(health: int, attack: int, defense: int) -> bool:
        return health > 0 and attack >= 0 and defense >= 0

    @staticmethod
    def validate_name(name: str) -> bool:
        cleaned: str = name.strip()
        return 0 < len(cleaned) <= 20 and cleaned.replace(" ", "").isalnum()

    @staticmethod
    def parse_menu_choice(raw: str, minimum: int, maximum: int) -> int:
        value: int = int(raw.strip())
        if value < minimum or value > maximum:
            raise ValueError(f"Choice must be between {minimum} and {maximum}.")
        return value

    @staticmethod
    def clamp(value: int, minimum: int, maximum: int) -> int:
        return max(minimum, min(maximum, value))
