import json
import csv
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

    def to_csv_row(self):
        return [
            self.date,
            self.transaction_type,
            self.category,
            self.amount
        ]


class FinanceManager:

    JSON_FILE = "transactions.json"
    CSV_FILE = "financial_report.csv"

    def __init__(self):
        self.transactions = []
        self.load_data()

    def save_data(self):
        with open(self.JSON_FILE, "w") as file:
            json.dump(
                [t.to_dict() for t in self.transactions],
                file,
                indent=4
            )

    def load_data(self):
        if not os.path.exists(self.JSON_FILE):
            return

        with open(self.JSON_FILE, "r") as file:
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
            print(
                f"{transaction.date} | "
                f"{transaction.transaction_type} | "
                f"{transaction.category} | "
                f"${transaction.amount:.2f}"
            )

    def export_csv(self):

        if not self.transactions:
            print("\nNo Transactions Available!")
            return

        with open(
            self.CSV_FILE,
            "w",
            newline=""
        ) as file:

            writer = csv.writer(file)

            writer.writerow([
                "Date",
                "Type",
                "Category",
                "Amount"
            ])

            for transaction in self.transactions:
                writer.writerow(
                    transaction.to_csv_row()
                )

        print(
            f"\nReport exported successfully to "
            f"'{self.CSV_FILE}'"
        )

    def menu(self):

        while True:

            print("\n========== FINANCE MANAGER ==========")
            print("1. Add Income")
            print("2. Add Expense")
            print("3. View Transactions")
            print("4. Export CSV Report")
            print("5. Exit")

            choice = input("\nEnter Choice: ")

            if choice == "1":
                self.add_income()

            elif choice == "2":
                self.add_expense()

            elif choice == "3":
                self.view_transactions()

            elif choice == "4":
                self.export_csv()

            elif choice == "5":
                print("\nThank You!")
                break

            else:
                print("\nInvalid Choice!")


if __name__ == "__main__":
    app = FinanceManager()
    app.menu()