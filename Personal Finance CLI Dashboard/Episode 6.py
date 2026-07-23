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

    def __str__(self):
        sign = "+" if self.transaction_type == "Income" else "-"
        return (
            f"{self.date} | "
            f"{self.transaction_type.upper()} | "
            f"{self.category.title()} | "
            f"{sign}${self.amount:.2f}"
        )


class FinanceManager:

    FILE_NAME = "transactions.json"

    def __init__(self):
        self.transactions = []
        self.load_data()

    def save_data(self):
        with open(self.FILE_NAME, "w") as file:
            json.dump(
                [t.to_dict() for t in self.transactions],
                file,
                indent=4
            )

    def load_data(self):
        if not os.path.exists(self.FILE_NAME):
            return

        with open(self.FILE_NAME, "r") as file:
            data = json.load(file)

        self.transactions = [
            Transaction.from_dict(item)
            for item in data
        ]

    def add_income(self):
        amount = float(input("Income Amount: "))
        category = input("Category: ")

        self.transactions.append(
            Transaction(amount, category, "Income")
        )

        self.save_data()

        print("\nIncome Added Successfully!")

    def add_expense(self):
        amount = float(input("Expense Amount: "))
        category = input("Category: ")

        self.transactions.append(
            Transaction(amount, category, "Expense")
        )

        self.save_data()

        print("\nExpense Added Successfully!")

    def view_transactions(self):

        if not self.transactions:
            print("\nNo Transactions Found!")
            return

        print("\n========== TRANSACTIONS ==========\n")

        for transaction in self.transactions:
            print(transaction)

    def menu(self):

        while True:

            print("\n========== FINANCE MANAGER ==========")
            print("1. Add Income")
            print("2. Add Expense")
            print("3. View Transactions")
            print("4. Exit")

            choice = input("\nEnter Choice: ")

            if choice == "1":
                self.add_income()

            elif choice == "2":
                self.add_expense()

            elif choice == "3":
                self.view_transactions()

            elif choice == "4":
                print("\nData Saved Successfully!")
                break

            else:
                print("\nInvalid Choice!")


if __name__ == "__main__":
    app = FinanceManager()
    app.menu()