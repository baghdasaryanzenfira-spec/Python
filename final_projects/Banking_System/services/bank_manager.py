from __future__ import annotations
from ..models.base_account import BankAccount
from ..models.checking_account import CheckingAccount
from ..models.loan_account import LoanAccount
from ..models.savings_account import SavingsAccount
from ..utils.exceptions import AccountNotFoundError, BankingError


class Bank:
    def __init__(self, name: str = BankAccount.bank_name) -> None:
        self.name: str = name
        self.accounts: dict[str, BankAccount] = {}
        self._next_number: int = 1000  

    def _generate_account_number(self) -> str:
        while str(self._next_number) in self.accounts:
            self._next_number += 1
        number = str(self._next_number)
        self._next_number += 1
        return number

    def create_account(
        self, account_type: str, holder_name: str, **kwargs
    ) -> BankAccount:
        if not holder_name or not str(holder_name).strip():
            raise BankingError("Holder name cannot be empty.")

        number = self._generate_account_number()
        key = account_type.strip().lower()

        factory = {
            "savings": SavingsAccount,
            "checking": CheckingAccount,
            "loan": LoanAccount,
        }
        if key not in factory:
            raise BankingError(f"Unknown account type: {account_type!r}")

        account = factory[key](number, holder_name, **kwargs)
        self.accounts[number] = account
        return account

    def find_account(self, account_number: str) -> BankAccount:
        account = self.accounts.get(str(account_number))
        if account is None:
            raise AccountNotFoundError(f"No account found with number {account_number}.")
        return account

    def transfer(self, from_number: str, to_number: str, amount: float) -> None:
        source = self.find_account(from_number)
        target = self.find_account(to_number)
        source.transfer(target, amount)

    def total_money(self) -> float:
        return sum(acc.balance for acc in self.accounts.values())

    def statistics(self) -> dict:
        by_type: dict[str, int] = {}
        for acc in self.accounts.values():
            by_type[acc.account_type()] = by_type.get(acc.account_type(), 0) + 1
        return {
            "bank_name": self.name,
            "num_accounts": len(self.accounts),
            "total_money": self.total_money(),
            "by_type": by_type,
            "lifetime_accounts": BankAccount.total_accounts,
        }

    def __str__(self) -> str:
        return f"{self.name} — {len(self.accounts)} account(s)"

    def __repr__(self) -> str:
        return f"Bank(name={self.name!r}, accounts={len(self.accounts)})"
