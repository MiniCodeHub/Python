import json
import os
from datetime import datetime


class Transaction:
    def __init__(self, amount, category, transaction_type, date=None):
        self.amount = amount
        self.category = category
        self.transaction_type = transaction_type
        self.date = date or datetime.now().strftime("%Y-%m-%d")

    def to_dict(self):
        return {
            "amount": self.amount,
            "category": self.category,
            "transaction_type": self.transaction_type,
            "date": self.date
        }

    @staticmethod
    def from_dict(data):
        return Transaction(
            data["amount"],
            data["category"],
            data["transaction_type"],
            data["date"]
        )


class FinanceManager:

    FILE_NAME = "transactions.json"
    BUDGET_FILE = "budgets.json"

    def __init__(self):
        self.transactions = []
        self.budgets = {}

        self.load_transactions()
        self.load_budgets()

    # -------------------------
    # Transaction Storage
    # -------------------------

    def save_transactions(self):

        with open(self.FILE_NAME, "w") as file:

            json.dump(
                [t.to_dict() for t in self.transactions],
                file,
                indent=4
            )

    def load_transactions(self):

        if not os.path.exists(self.FILE_NAME):
            return

        with open(self.FILE_NAME, "r") as file:

            data = json.load(file)

        self.transactions = [
            Transaction.from_dict(item)
            for item in data
        ]

    # -------------------------
    # Budget Storage
    # -------------------------

    def save_budgets(self):

        with open(self.BUDGET_FILE, "w") as file:

            json.dump(
                self.budgets,
                file,
                indent=4
            )

    def load_budgets(self):

        if not os.path.exists(self.BUDGET_FILE):
            return

        with open(self.BUDGET_FILE, "r") as file:

            self.budgets = json.load(file)

    # -------------------------
    # Budget Functions
    # -------------------------

    def set_budget(self):

        category = input("Category: ").title()

        amount = float(
            input("Monthly Budget: ")
        )

        self.budgets[category] = amount

        self.save_budgets()

        print("\nBudget Saved!")

    def show_budgets(self):

        if not self.budgets:
            print("\nNo Budgets Set.")
            return

        print("\n========== BUDGETS ==========")

        for category, amount in self.budgets.items():

            spent = self.get_spent(category)

            remaining = amount - spent

            print(
                f"{category:<15}"
                f" Budget: ${amount:.2f}"
                f" | Spent: ${spent:.2f}"
                f" | Remaining: ${remaining:.2f}"
            )

    # -------------------------
    # Expense Tracking
    # -------------------------

    def get_spent(self, category):

        total = 0

        for t in self.transactions:

            if (
                t.transaction_type == "Expense"
                and
                t.category.title() == category
            ):
                total += t.amount

        return total

    def check_budget(self, category):

        if category not in self.budgets:
            return

        spent = self.get_spent(category)

        limit = self.budgets[category]

        if spent > limit:

            print("\n🚨 Budget Exceeded!")
            print(
                f"{category}: "
                f"${spent:.2f} / ${limit:.2f}"
            )

        elif spent >= limit * 0.9:

            print("\n⚠ Warning!")
            print(
                f"You have used "
                f"{spent/limit*100:.0f}% "
                f"of your {category} budget."
            )

    # -------------------------
    # Add Transaction
    # -------------------------

    def add_transaction(self, transaction_type):

        amount = float(
            input("Amount: ")
        )

        category = input(
            "Category: "
        ).title()

        self.transactions.append(
            Transaction(
                amount,
                category,
                transaction_type
            )
        )

        self.save_transactions()

        if transaction_type == "Expense":
            self.check_budget(category)

        print("\nTransaction Saved!")

    # -------------------------
    # Menu
    # -------------------------

    def menu(self):

        while True:

            print("\n========== FINANCE MANAGER ==========")
            print("1. Add Income")
            print("2. Add Expense")
            print("3. Set Budget")
            print("4. View Budgets")
            print("5. Exit")

            choice = input("\nChoice: ")

            if choice == "1":
                self.add_transaction("Income")

            elif choice == "2":
                self.add_transaction("Expense")

            elif choice == "3":
                self.set_budget()

            elif choice == "4":
                self.show_budgets()

            elif choice == "5":
                print("\nGoodbye!")
                break

            else:
                print("\nInvalid Choice!")


if __name__ == "__main__":
    app = FinanceManager()
    app.menu()