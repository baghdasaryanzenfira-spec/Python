"""
Banking_System
==============

A modular, object-oriented banking system demonstrating inheritance,
method overriding, polymorphism, and clean package structure.

Public API
----------
    from Banking_System import Bank, SavingsAccount, CheckingAccount, LoanAccount

Run the interactive CLI with:

    python -m Banking_System.main
"""

from .models import BankAccount, CheckingAccount, LoanAccount, SavingsAccount
from .services import Bank
from .utils import (
    AccountNotFoundError,
    BankingError,
    InsufficientFundsError,
    InvalidAmountError,
)

__version__ = "1.0.0"

__all__ = [
    "BankAccount",
    "SavingsAccount",
    "CheckingAccount",
    "LoanAccount",
    "Bank",
    "BankingError",
    "InvalidAmountError",
    "InsufficientFundsError",
    "AccountNotFoundError",
]
