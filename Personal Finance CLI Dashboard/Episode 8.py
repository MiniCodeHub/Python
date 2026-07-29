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

    def add_transaction(self, transaction_type):
        amount = float(input("Amount: "))
        category = input("Category: ")

        self.transactions.append(
            Transaction(amount, category, transaction_type)
        )

        self.save_data()

        print("\nTransaction Added Successfully!")

    def monthly_report(self):

        month = input("Enter Month (YYYY-MM): ")

        income = 0
        expense = 0

        for t in self.transactions:

            if t.date.startswith(month):

                if t.transaction_type == "Income":
                    income += t.amount
                else:
                    expense += t.amount

        print("\n========== MONTHLY REPORT ==========")
        print(f"Month         : {month}")
        print(f"Income        : ${income:.2f}")
        print(f"Expense       : ${expense:.2f}")
        print(f"Net Savings   : ${income-expense:.2f}")

    def yearly_report(self):

        year = input("Enter Year (YYYY): ")

        income = 0
        expense = 0

        for t in self.transactions:

            if t.date.startswith(year):

                if t.transaction_type == "Income":
                    income += t.amount
                else:
                    expense += t.amount

        print("\n========== YEARLY REPORT ==========")
        print(f"Year          : {year}")
        print(f"Income        : ${income:.2f}")
        print(f"Expense       : ${expense:.2f}")
        print(f"Net Savings   : ${income-expense:.2f}")

    def menu(self):

        while True:

            print("\n========== FINANCE MANAGER ==========")
            print("1. Add Income")
            print("2. Add Expense")
            print("3. Monthly Report")
            print("4. Yearly Report")
            print("5. Exit")

            choice = input("\nEnter Choice: ")

            if choice == "1":
                self.add_transaction("Income")

            elif choice == "2":
                self.add_transaction("Expense")

            elif choice == "3":
                self.monthly_report()

            elif choice == "4":
                self.yearly_report()

            elif choice == "5":
                print("\nThank You!")
                break

            else:
                print("\nInvalid Choice!")


if __name__ == "__main__":
    app = FinanceManager()
    app.menu()