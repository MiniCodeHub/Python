from datetime import datetime

class Transaction:
    def __init__(self, amount, category, transaction_type):
        self.amount = amount
        self.category = category
        self.transaction_type = transaction_type
        self.date = datetime.now().strftime("%Y-%m-%d")

    def __str__(self):
        return (
            f"{self.date} | "
            f"{self.transaction_type.upper()} | "
            f"{self.category} | "
            f"${self.amount:.2f}"
        )


class FinanceManager:
    def __init__(self):
        self.transactions = []

    def menu(self):
        while True:
            print("\n==============================")
            print(" PERSONAL FINANCE MANAGER")
            print("==============================")
            print("1. Add Income")
            print("2. Add Expense")
            print("3. View Transactions")
            print("4. Monthly Summary")
            print("5. Exit")

            choice = input("\nEnter choice: ")

            if choice == "1":
                print("\n[Add Income - Episode 2]")
            elif choice == "2":
                print("\n[Add Expense - Episode 3]")
            elif choice == "3":
                print("\n[View Transactions - Episode 4]")
            elif choice == "4":
                print("\n[Monthly Summary - Episode 5]")
            elif choice == "5":
                print("\nThank you for using Personal Finance Manager!")
                break
            else:
                print("\nInvalid choice!")


if __name__ == "__main__":
    app = FinanceManager()
    app.menu()