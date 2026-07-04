"""Savings account: no negative balance, enforced minimum, earns interest."""

from __future__ import annotations

from ..utils.exceptions import InsufficientFundsError, InvalidAmountError
from ..utils.validators import validate_rate
from .base_account import BankAccount


class SavingsAccount(BankAccount):
    """
    Savings account: cannot go negative and must keep a minimum balance.

    Overrides withdraw() to enforce the minimum-balance constraint, adds
    interest application, and exposes a classmethod to change the interest
    rate for *all* savings accounts at once.
    """

    interest_rate: float = 0.04  # savings earns more than the base rate

    def __init__(
        self,
        account_number: str,
        holder_name: str,
        balance: float = 0.0,
        minimum_balance: float = 100.0,
    ) -> None:
        """Create a savings account with an enforced minimum balance."""
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
        """Withdraw while keeping the balance at or above the minimum."""
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
        """Add interest (using this class's rate) to the balance."""
        interest = self.balance * self.interest_rate
        self.balance += interest
        self._record(
            f"Interest {interest:.2f} @ {self.interest_rate:.2%} | "
            f"Balance: {self.balance:.2f}"
        )
        return self.balance

    @classmethod
    def set_interest_rate(cls, new_rate: float) -> None:
        """
        Update the interest rate for every savings account simultaneously.

        Because the rate lives on the class, changing it here affects all
        existing and future SavingsAccount instances at once.
        """
        cls.interest_rate = validate_rate(new_rate)

    def account_type(self) -> str:
        return "Savings Account"
