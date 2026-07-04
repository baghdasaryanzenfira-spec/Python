from __future__ import annotations
from .exceptions import InvalidAmountError

def validate_amount(amount: float) -> float:
    if isinstance(amount, bool) or not isinstance(amount, (int, float)):
        raise InvalidAmountError("Amount must be a number.")
    amount = float(amount)
    if amount != amount or amount in (float("inf"), float("-inf")):  # NaN / inf
        raise InvalidAmountError("Amount must be a finite number.")
    if amount <= 0:
        raise InvalidAmountError("Amount must be greater than zero.")
    return amount


def validate_rate(rate: float) -> float:
    if isinstance(rate, bool) or not isinstance(rate, (int, float)):
        raise InvalidAmountError("Interest rate must be a number.")
    if rate < 0:
        raise InvalidAmountError("Interest rate cannot be negative.")
    return float(rate)
