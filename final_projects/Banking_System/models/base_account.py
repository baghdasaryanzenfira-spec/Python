"""Base account class shared by every account type."""

from __future__ import annotations

from datetime import datetime

from ..utils.exceptions import (
    BankingError,
    InsufficientFundsError,
    InvalidAmountError,
)
from ..utils.validators import validate_amount


class BankAccount:
    """
    Base class for all bank accounts.

    Class attributes
    ----------------
    total_accounts : int
        Running count of every account ever created (across all subclasses).
    bank_name : str
        Name of the bank all accounts belong to.
    interest_rate : float
        Default annual interest rate (as a fraction, e.g. 0.02 == 2%).

    Instance attributes
    -------------------
    account_number : str
    holder_name : str
    balance : float
    transaction_history : list[str]
    """

    total_accounts: int = 0
    bank_name: str = "Python National Bank"
    interest_rate: float = 0.02

    def __init__(self, account_number: str, holder_name: str, balance: float = 0.0) -> None:
        """Initialize an account, validating the opening balance."""
        # Opening balance may legitimately be 0; only reject invalid numbers.
        if not isinstance(balance, (int, float)) or isinstance(balance, bool):
            raise InvalidAmountError("Opening balance must be a number.")

        self.account_number: str = str(account_number)
        self.holder_name: str = holder_name
        self.balance: float = float(balance)
        self.transaction_history: list[str] = []

        BankAccount.total_accounts += 1
        self._record(f"Account opened with balance {self.balance:.2f}")

    # ----------------------------- helpers -------------------------------- #
    @staticmethod
    def validate_amount(amount: float) -> float:
        """
        Ensure ``amount`` is a positive, finite number and return it as float.

        Delegates to the shared validator so validation lives in one place,
        while remaining available as ``BankAccount.validate_amount(...)``.
        """
        return validate_amount(amount)

    def _record(self, message: str) -> None:
        """Append a timestamped entry to the transaction history."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.transaction_history.append(f"[{timestamp}] {message}")

    # ----------------------------- core API ------------------------------- #
    def deposit(self, amount: float) -> float:
        """Deposit a positive amount and return the new balance."""
        amount = self.validate_amount(amount)
        self.balance += amount
        self._record(f"Deposited {amount:.2f} | Balance: {self.balance:.2f}")
        return self.balance

    def withdraw(self, amount: float) -> float:
        """
        Withdraw a positive amount and return the new balance.

        Base rule: balance may not go below zero. Subclasses override this
        to implement their own constraints (minimum balance, overdraft, etc.).
        """
        amount = self.validate_amount(amount)
        if amount > self.balance:
            raise InsufficientFundsError(
                f"Cannot withdraw {amount:.2f}; balance is {self.balance:.2f}."
            )
        self.balance -= amount
        self._record(f"Withdrew {amount:.2f} | Balance: {self.balance:.2f}")
        return self.balance

    def transfer(self, target: "BankAccount", amount: float) -> None:
        """
        Transfer ``amount`` from this account to ``target``.

        Implemented in terms of withdraw()/deposit() so every subclass's rules
        are honored automatically (polymorphism). Rolls back on failure.
        """
        if not isinstance(target, BankAccount):
            raise BankingError("Transfer target must be a bank account.")
        if target is self:
            raise BankingError("Cannot transfer to the same account.")

        amount = self.validate_amount(amount)
        self.withdraw(amount)  # may raise; nothing has changed on target yet
        try:
            target.deposit(amount)
        except BankingError:
            # Roll back the withdrawal so money is never lost.
            self.balance += amount
            self._record(f"Transfer of {amount:.2f} FAILED and was rolled back")
            raise
        self._record(f"Transferred {amount:.2f} to {target.account_number}")
        target._record(f"Received {amount:.2f} from {self.account_number}")

    def get_balance(self) -> float:
        """Return the current balance."""
        return self.balance

    # --------------------------- representation --------------------------- #
    def account_type(self) -> str:
        """Return a human-readable label for the account type (overridable)."""
        return "Bank Account"

    def __str__(self) -> str:
        """User-friendly one-line summary."""
        return (
            f"{self.account_type()} #{self.account_number} | "
            f"{self.holder_name} | Balance: {self.balance:.2f}"
        )

    def __repr__(self) -> str:
        """Unambiguous developer representation."""
        return (
            f"{type(self).__name__}(account_number={self.account_number!r}, "
            f"holder_name={self.holder_name!r}, balance={self.balance:.2f})"
        )
