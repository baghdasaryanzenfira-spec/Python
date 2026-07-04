"""Domain-specific exceptions for the banking system."""


class BankingError(Exception):
    """Base class for all domain-specific banking errors."""


class InvalidAmountError(BankingError):
    """Raised when an amount is not a positive, finite number."""


class InsufficientFundsError(BankingError):
    """Raised when an operation would violate an account's balance rules."""


class AccountNotFoundError(BankingError):
    """Raised when a requested account number does not exist."""
