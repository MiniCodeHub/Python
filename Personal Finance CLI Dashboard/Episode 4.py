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
        amount = float(
            input("Enter Income Amount: ")
        )

        category = input(
            "Enter Income Category: "
        )

        self.transactions.append(
            Transaction(
                amount,
                category,
                "Income"
            )
        )

        print("\nIncome Added Successfully!")

    def add_expense(self):
        amount = float(
            input("Enter Expense Amount: ")
        )

        category = input(
            "Enter Expense Category: "
        )

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

        print("\nTransaction History\n")

        for transaction in self.transactions:
            print(transaction)

    def monthly_summary(self):
        income = 0
        expenses = 0

        for transaction in self.transactions:

            if transaction.transaction_type == "Income":
                income += transaction.amount
            else:
                expenses += transaction.amount

        savings = income - expenses

        savings_rate = (
            (savings / income) * 100
            if income > 0
            else 0
        )

        print("\n========== MONTHLY SUMMARY ==========")
        print(f"Total Income   : ${income:.2f}")
        print(f"Total Expenses : ${expenses:.2f}")
        print(f"Current Balance: ${savings:.2f}")
        print(f"Savings        : ${savings:.2f}")
        print(f"Savings Rate   : {savings_rate:.2f}%")
        print("=====================================")

    def menu(self):
        while True:

            print("\n========== FINANCE MANAGER ==========")
            print("1. Add Income")
            print("2. Add Expense")
            print("3. View Transactions")
            print("4. Monthly Summary")
            print("5. Exit")

            choice = input("\nEnter Choice: ")

            if choice == "1":
                self.add_income()

            elif choice == "2":
                self.add_expense()

            elif choice == "3":
                self.view_transactions()

            elif choice == "4":
                self.monthly_summary()

            elif choice == "5":
                print("\nThank You!")
                break

            else:
                print("\nInvalid Choice!")


if __name__ == "__main__":
    app = FinanceManager()
    app.menu()