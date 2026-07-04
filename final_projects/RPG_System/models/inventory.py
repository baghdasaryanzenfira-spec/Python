from __future__ import annotations


class Item:
    def __init__(self, name: str, description: str, potency: int = 0) -> None:
        self.name: str = name
        self.description: str = description
        self.potency: int = potency

    def __str__(self) -> str:
        if self.potency > 0:
            return f"{self.name} (+{self.potency}) - {self.description}"
        return f"{self.name} - {self.description}"

    def __repr__(self) -> str:
        return (
            f"Item(name={self.name!r}, description={self.description!r}, "
            f"potency={self.potency!r})"
        )


class Inventory:
    def __init__(self) -> None:
        self.slots: dict[str, list[Item]] = {}

    def add_item(self, item: Item, quantity: int = 1) -> None:
        if quantity <= 0:
            raise ValueError("Quantity must be a positive integer.")
        self.slots.setdefault(item.name, [])
        for _ in range(quantity):
            self.slots[item.name].append(item)

    def remove_item(self, item_name: str) -> Item | None:
        stack: list[Item] = self.slots.get(item_name, [])
        if not stack:
            return None
        removed: Item = stack.pop()
        if not stack:
            del self.slots[item_name]
        return removed

    def peek(self, item_name: str) -> Item | None:
        stack: list[Item] = self.slots.get(item_name, [])
        return stack[-1] if stack else None

    def has_item(self, item_name: str) -> bool:
        return len(self.slots.get(item_name, [])) > 0

    def count(self, item_name: str) -> int:
        return len(self.slots.get(item_name, []))

    def is_empty(self) -> bool:
        return len(self.slots) == 0

    def item_names(self) -> list[str]:
        return list(self.slots.keys())

    def __str__(self) -> str:
        if self.is_empty():
            return "Inventory: (empty)"
        lines: list[str] = [
            f"  - {name} x{len(stack)}" for name, stack in self.slots.items()
        ]
        return "Inventory:\n" + "\n".join(lines)

    def __repr__(self) -> str:
        summary: dict[str, int] = {
            name: len(stack) for name, stack in self.slots.items()
        }
        return f"Inventory(slots={summary!r})"
