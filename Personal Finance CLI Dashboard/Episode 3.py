from datetime import datetime


class Transaction:
    def __init__(self, amount, category, transaction_type):
        self.amount = amount
        self.category = category
        self.transaction_type = transaction_type
        self.date = datetime.now().strftime("%Y-%m-%d")

    def __str__(self):
        sign = "+" if self.transaction_type == "Income" else "-"
        return (
            f"{self.date} | "
            f"{self.transaction_type.upper()} | "
            f"{self.category} | "
            f"{sign}${self.amount:.2f}"
        )


class FinanceManager:
    def __init__(self):
        self.transactions = []

    def add_income(self):
        amount = float(input("Enter Income Amount: "))
        category = input("Enter Income Category: ")

        self.transactions.append(
            Transaction(
                amount,
                category,
                "Income"
            )
        )

        print("\nIncome Added Successfully!")

    def add_expense(self):
        amount = float(input("Enter Expense Amount: "))
        category = input("Enter Expense Category: ")

        self.transactions.append(
            Transaction(
                amount,
                category,
                "Expense"
            )
        )

        print("\nExpense Added Successfully!")

    def view_transactions(self):
        if not self.transactions:
            print("\nNo Transactions Found!")
            return

        balance = 0

        print("\nTransaction History\n")

        for transaction in self.transactions:
            print(transaction)

            if transaction.transaction_type == "Income":
                balance += transaction.amount
            else:
                balance -= transaction.amount

        print("\nCurrent Balance: "
              f"${balance:.2f}")

    def menu(self):
        while True:
            print("\n==========================")
            print(" PERSONAL FINANCE MANAGER")
            print("==========================")
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
                print("\nThank You!")
                break

            else:
                print("\nInvalid Choice!")


if __name__ == "__main__":
    app = FinanceManager()
    app.menu()