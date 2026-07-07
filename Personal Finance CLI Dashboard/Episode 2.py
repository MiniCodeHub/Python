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

    def add_income(self):

        amount = float(
            input("Enter Income Amount: ")
        )

        category = input(
            "Enter Income Category: "
        )

        transaction = Transaction(
            amount,
            category,
            "Income"
        )

        self.transactions.append(transaction)

        print("\nIncome Added Successfully!")

    def view_transactions(self):

        if not self.transactions:
            print("\nNo Transactions Found!")
            return

        print("\nTransaction History\n")

        for transaction in self.transactions:
            print(transaction)

    def menu(self):

        while True:

            print("\n==========================")
            print("PERSONAL FINANCE MANAGER")
            print("==========================")
            print("1. Add Income")
            print("2. View Transactions")
            print("3. Exit")

            choice = input("\nEnter Choice: ")

            if choice == "1":
                self.add_income()

            elif choice == "2":
                self.view_transactions()

            elif choice == "3":
                print("\nThank You!")
                break

            else:
                print("\nInvalid Choice!")


if __name__ == "__main__":

    app = FinanceManager()

    app.menu()