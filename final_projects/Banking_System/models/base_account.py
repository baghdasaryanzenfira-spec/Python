from __future__ import annotations

from datetime import datetime

from ..utils.exceptions import (
    BankingError,
    InsufficientFundsError,
    InvalidAmountError,
)
from ..utils.validators import validate_amount


class BankAccount:
    total_accounts: int = 0
    bank_name: str = "Python National Bank"
    interest_rate: float = 0.02

    def __init__(self, account_number: str, holder_name: str, balance: float = 0.0) -> None:
        if not isinstance(balance, (int, float)) or isinstance(balance, bool):
            raise InvalidAmountError("Opening balance must be a number.")

        self.account_number: str = str(account_number)
        self.holder_name: str = holder_name
        self.balance: float = float(balance)
        self.transaction_history: list[str] = []

        BankAccount.total_accounts += 1
        self._record(f"Account opened with balance {self.balance:.2f}")

    @staticmethod
    def validate_amount(amount: float) -> float:
        return validate_amount(amount)

    def _record(self, message: str) -> None:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.transaction_history.append(f"[{timestamp}] {message}")

    def deposit(self, amount: float) -> float:
        amount = self.validate_amount(amount)
        self.balance += amount
        self._record(f"Deposited {amount:.2f} | Balance: {self.balance:.2f}")
        return self.balance

    def withdraw(self, amount: float) -> float:
        amount = self.validate_amount(amount)
        if amount > self.balance:
            raise InsufficientFundsError(
                f"Cannot withdraw {amount:.2f}; balance is {self.balance:.2f}."
            )
        self.balance -= amount
        self._record(f"Withdrew {amount:.2f} | Balance: {self.balance:.2f}")
        return self.balance

    def transfer(self, target: "BankAccount", amount: float) -> None:
        if not isinstance(target, BankAccount):
            raise BankingError("Transfer target must be a bank account.")
        if target is self:
            raise BankingError("Cannot transfer to the same account.")

        amount = self.validate_amount(amount)
        self.withdraw(amount)
        try:
            target.deposit(amount)
        except BankingError:
            self.balance += amount
            self._record(f"Transfer of {amount:.2f} FAILED and was rolled back")
            raise
        self._record(f"Transferred {amount:.2f} to {target.account_number}")
        target._record(f"Received {amount:.2f} from {self.account_number}")

    def get_balance(self) -> float:
        return self.balance

    def account_type(self) -> str:
        return "Bank Account"

    def __str__(self) -> str:
        return (
            f"{self.account_type()} #{self.account_number} | "
            f"{self.holder_name} | Balance: {self.balance:.2f}"
        )

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}(account_number={self.account_number!r}, "
            f"holder_name={self.holder_name!r}, balance={self.balance:.2f})"
        )
