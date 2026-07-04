"""Bank management service: creates, stores and coordinates accounts."""

from __future__ import annotations

from ..models.base_account import BankAccount
from ..models.checking_account import CheckingAccount
from ..models.loan_account import LoanAccount
from ..models.savings_account import SavingsAccount
from ..utils.exceptions import AccountNotFoundError, BankingError


class Bank:
    """
    Manages a collection of accounts and cross-account operations.

    Accounts are stored in a dict keyed by account number for O(1) lookup.
    """

    def __init__(self, name: str = BankAccount.bank_name) -> None:
        self.name: str = name
        self.accounts: dict[str, BankAccount] = {}
        self._next_number: int = 1000  # auto-incrementing account numbers

    def _generate_account_number(self) -> str:
        """Return a fresh, unused account number."""
        while str(self._next_number) in self.accounts:
            self._next_number += 1
        number = str(self._next_number)
        self._next_number += 1
        return number

    def create_account(
        self, account_type: str, holder_name: str, **kwargs
    ) -> BankAccount:
        """
        Create and register an account.

        Parameters
        ----------
        account_type : {"savings", "checking", "loan"}
        holder_name : str
        **kwargs : forwarded to the specific account constructor
                   (e.g. balance, minimum_balance, overdraft_limit, loan_amount).
        """
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
        """Return the account with ``account_number`` or raise if missing."""
        account = self.accounts.get(str(account_number))
        if account is None:
            raise AccountNotFoundError(f"No account found with number {account_number}.")
        return account

    def transfer(self, from_number: str, to_number: str, amount: float) -> None:
        """Move money between two managed accounts."""
        source = self.find_account(from_number)
        target = self.find_account(to_number)
        source.transfer(target, amount)

    def total_money(self) -> float:
        """Return the sum of all account balances (loans count as negative)."""
        return sum(acc.balance for acc in self.accounts.values())

    def statistics(self) -> dict:
        """Return a dict of aggregate bank statistics."""
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
