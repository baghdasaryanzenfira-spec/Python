#!/usr/bin/python3
from __future__ import annotations

try:
    from .models import CheckingAccount, LoanAccount, SavingsAccount
    from .services import Bank
    from .utils import BankingError
except ImportError: 
    import os
    import sys

    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from Banking_System.models import CheckingAccount, LoanAccount, SavingsAccount
    from Banking_System.services import Bank
    from Banking_System.utils import BankingError


def _prompt_float(message: str) -> float:
    while True:
        raw = input(message).strip()
        try:
            return float(raw)
        except ValueError:
            print("  ! Please enter a valid number.")


MENU = """
========================================
      {bank}
========================================
 1. Create account
 2. Deposit
 3. Withdraw
 4. Transfer money
 5. View account / balance
 6. View transaction history
 7. Change savings interest rate
 8. Apply interest (savings/loan)
 9. Show bank statistics
10. List all accounts
 0. Exit
----------------------------------------"""


def run_cli() -> None:
    bank = Bank()
    try:
        bank.create_account("savings", "Alice", balance=500, minimum_balance=100)
        bank.create_account("checking", "Bob", balance=200)
    except BankingError as exc:  
        print(f"Could not seed demo accounts: {exc}")

    while True:
        print(MENU.format(bank=bank.name))
        choice = input("Select an option: ").strip()

        try:
            if choice == "1":
                print("Types: savings | checking | loan")
                acc_type = input("  Account type: ").strip().lower()
                name = input("  Holder name: ").strip()
                kwargs: dict = {}
                if acc_type == "savings":
                    kwargs["balance"] = _prompt_float("  Opening balance: ")
                    kwargs["minimum_balance"] = _prompt_float("  Minimum balance: ")
                elif acc_type == "checking":
                    kwargs["balance"] = _prompt_float("  Opening balance: ")
                    kwargs["overdraft_limit"] = _prompt_float("  Overdraft limit: ")
                elif acc_type == "loan":
                    kwargs["loan_amount"] = _prompt_float("  Loan amount: ")
                account = bank.create_account(acc_type, name, **kwargs)
                print(f"  Created: {account}")

            elif choice == "2": 
                num = input("  Account number: ").strip()
                acc = bank.find_account(num)
                amount = _prompt_float("  Amount to deposit: ")
                acc.deposit(amount)
                print(f"  New balance: {acc.get_balance():.2f}")

            elif choice == "3":  
                num = input("  Account number: ").strip()
                acc = bank.find_account(num)
                amount = _prompt_float("  Amount to withdraw: ")
                acc.withdraw(amount)
                print(f"  New balance: {acc.get_balance():.2f}")

            elif choice == "4":  
                src = input("  From account number: ").strip()
                dst = input("  To account number: ").strip()
                amount = _prompt_float("  Amount to transfer: ")
                bank.transfer(src, dst, amount)
                print("  Transfer complete.")

            elif choice == "5": 
                num = input("  Account number: ").strip()
                print(f"  {bank.find_account(num)}")

            elif choice == "6": 
                num = input("  Account number: ").strip()
                acc = bank.find_account(num)
                if not acc.transaction_history:
                    print("  (No transactions yet.)")
                for entry in acc.transaction_history:
                    print(f"  {entry}")

            elif choice == "7": 
                rate = _prompt_float("  New savings interest rate (e.g. 0.05 for 5%): ")
                SavingsAccount.set_interest_rate(rate)
                print(f"All savings accounts now earn {rate:.2%}.")

            elif choice == "8": 
                num = input("  Account number: ").strip()
                acc = bank.find_account(num)
                if isinstance(acc, (SavingsAccount, LoanAccount)):
                    acc.apply_interest()
                    print(f"Interest applied. {acc}")
                else:
                    print("Interest only applies to savings or loan accounts.")

            elif choice == "9":  
                stats = bank.statistics()
                print(f"  Bank: {stats['bank_name']}")
                print(f"  Accounts: {stats['num_accounts']}")
                print(f"  Total money in bank: {stats['total_money']:.2f}")
                print(f"  Lifetime accounts opened: {stats['lifetime_accounts']}")
                print(f"  Breakdown: {stats['by_type']}")

            elif choice == "10":  
                if not bank.accounts:
                    print("  (No accounts yet.)")
                for acc in bank.accounts.values():
                    print(f"  {acc}")

            elif choice == "0":  # Exit
                print("Goodbye!")
                break

            else:
                print("Invalid option, please try again.")

        except BankingError as exc:
            print(f"Error: {exc}")
        except EOFError:
            print("\nGoodbye!")
            break
        except Exception as exc:  
            print(f"Unexpected error: {exc}")


if __name__ == "__main__":
    try:
        run_cli()
    except KeyboardInterrupt:
        print("\nInterrupted. Goodbye!")
