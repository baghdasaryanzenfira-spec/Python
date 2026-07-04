from __future__ import annotations
from ..utils.exceptions import BankingError, InvalidAmountError
from .base_account import BankAccount


class LoanAccount(BankAccount):
    interest_rate: float = 0.09  # loans accrue the highest rate

    def __init__(
        self,
        account_number: str,
        holder_name: str,
        loan_amount: float = 0.0,
    ) -> None:
        if loan_amount < 0:
            raise InvalidAmountError("Loan amount cannot be negative.")
        super().__init__(account_number, holder_name, -float(loan_amount))

    def deposit(self, amount: float) -> float:
        return self.make_payment(amount)

    def make_payment(self, amount: float) -> float:
        amount = self.validate_amount(amount)
        if self.balance >= 0:
            raise BankingError("Loan is already fully paid off.")
        if amount > -self.balance:
            raise InvalidAmountError(
                f"Payment {amount:.2f} exceeds remaining debt of "
                f"{-self.balance:.2f}."
            )
        self.balance += amount
        self._record(
            f"Payment {amount:.2f} | Remaining debt: {-self.balance:.2f}"
        )
        return self.balance

    def withdraw(self, amount: float) -> float:
        raise BankingError("Cannot withdraw from a loan account.")

    def apply_interest(self) -> float:
        interest = -self.balance * self.interest_rate
        self.balance -= interest
        self._record(
            f"Interest {interest:.2f} accrued | Debt: {-self.balance:.2f}"
        )
        return self.balance

    def account_type(self) -> str:
        return "Loan Account"

    def __str__(self) -> str:
        debt = max(0.0, -self.balance)
        return (
            f"{self.account_type()} #{self.account_number} | "
            f"{self.holder_name} | Outstanding debt: {debt:.2f}"
        )
