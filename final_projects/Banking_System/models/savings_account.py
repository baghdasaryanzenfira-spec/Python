from __future__ import annotations
from ..utils.exceptions import InsufficientFundsError, InvalidAmountError
from ..utils.validators import validate_rate
from .base_account import BankAccount

class SavingsAccount(BankAccount):
    interest_rate: float = 0.04  # savings earns more than the base rate

    def __init__(
        self,
        account_number: str,
        holder_name: str,
        balance: float = 0.0,
        minimum_balance: float = 100.0,
    ) -> None:
        if minimum_balance < 0:
            raise InvalidAmountError("Minimum balance cannot be negative.")
        if balance < minimum_balance:
            raise InsufficientFundsError(
                f"Opening balance {balance:.2f} is below the required "
                f"minimum of {minimum_balance:.2f}."
            )
        super().__init__(account_number, holder_name, balance)
        self.minimum_balance: float = float(minimum_balance)

    def withdraw(self, amount: float) -> float:
        amount = self.validate_amount(amount)
        if self.balance - amount < self.minimum_balance:
            raise InsufficientFundsError(
                f"Withdrawal denied: balance would fall below the minimum "
                f"of {self.minimum_balance:.2f}."
            )
        self.balance -= amount
        self._record(f"Withdrew {amount:.2f} | Balance: {self.balance:.2f}")
        return self.balance

    def apply_interest(self) -> float:
        interest = self.balance * self.interest_rate
        self.balance += interest
        self._record(
            f"Interest {interest:.2f} @ {self.interest_rate:.2%} | "
            f"Balance: {self.balance:.2f}"
        )
        return self.balance

    @classmethod
    def set_interest_rate(cls, new_rate: float) -> None:
        cls.interest_rate = validate_rate(new_rate)

    def account_type(self) -> str:
        return "Savings Account"
