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
            f"{self.category.title()} | "
            f"{sign}${self.amount:.2f}"
        )


class FinanceManager:
    def __init__(self):
        self.transactions = []

    def add_income(self):
        amount = float(input("Enter Income Amount: "))
        category = input("Enter Income Category: ")

        self.transactions.append(
            Transaction(amount, category, "Income")
        )

        print("\nIncome Added Successfully!")

    def add_expense(self):
        amount = float(input("Enter Expense Amount: "))
        category = input("Enter Expense Category: ")

        self.transactions.append(
            Transaction(amount, category, "Expense")
        )

        print("\nExpense Added Successfully!")

    def view_transactions(self):
        if not self.transactions:
            print("\nNo Transactions Found!")
            return

        print("\n========== TRANSACTIONS ==========\n")

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

        balance = income - expenses

        print("\n========== MONTHLY SUMMARY ==========")
        print(f"Total Income   : ${income:.2f}")
        print(f"Total Expenses : ${expenses:.2f}")
        print(f"Balance        : ${balance:.2f}")
        print("====================================")

    def expense_analysis(self):

        expense_categories = {}

        for transaction in self.transactions:

            if transaction.transaction_type == "Expense":

                category = transaction.category.title()

                expense_categories[category] = (
                    expense_categories.get(category, 0)
                    + transaction.amount
                )

        if not expense_categories:
            print("\nNo Expense Data Available!")
            return

        print("\n====== EXPENSE ANALYSIS ======\n")

        highest_category = ""
        highest_amount = 0

        for category, amount in expense_categories.items():

            print(f"{category:<20} ${amount:.2f}")

            if amount > highest_amount:
                highest_amount = amount
                highest_category = category

        print("\n------------------------------")
        print(
            f"Highest Spending : "
            f"{highest_category} (${highest_amount:.2f})"
        )

    def menu(self):

        while True:

            print("\n========== FINANCE MANAGER ==========")
            print("1. Add Income")
            print("2. Add Expense")
            print("3. View Transactions")
            print("4. Monthly Summary")
            print("5. Expense Analysis")
            print("6. Exit")

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
                self.expense_analysis()

            elif choice == "6":
                print("\nThank You!")
                break

            else:
                print("\nInvalid Choice!")


if __name__ == "__main__":
    app = FinanceManager()
    app.menu()