from __future__ import annotations
from ..utils.exceptions import InsufficientFundsError, InvalidAmountError
from .base_account import BankAccount


class CheckingAccount(BankAccount):
    interest_rate: float = 0.0  

    def __init__(
        self,
        account_number: str,
        holder_name: str,
        balance: float = 0.0,
        overdraft_limit: float = 500.0,
        overdraft_fee: float = 35.0,
    ) -> None:
        if overdraft_limit < 0 or overdraft_fee < 0:
            raise InvalidAmountError("Overdraft limit and fee must be non-negative.")
        super().__init__(account_number, holder_name, balance)
        self.overdraft_limit: float = float(overdraft_limit)
        self.overdraft_fee: float = float(overdraft_fee)

    def withdraw(self, amount: float) -> float:
        amount = self.validate_amount(amount)
        projected = self.balance - amount
        fee = self.overdraft_fee if projected < 0 else 0.0

        if projected - fee < -self.overdraft_limit:
            raise InsufficientFundsError(
                f"Withdrawal denied: exceeds overdraft limit of "
                f"{self.overdraft_limit:.2f}."
            )

        self.balance = projected - fee
        self._record(f"Withdrew {amount:.2f} | Balance: {self.balance:.2f}")
        if fee:
            self._record(f"Overdraft fee {fee:.2f} | Balance: {self.balance:.2f}")
        return self.balance

    def account_type(self) -> str:
        return "Checking Account"
