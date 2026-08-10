import json
import os
from collections import defaultdict

import matplotlib.pyplot as plt


FILE_NAME = "transactions.json"


def load_transactions():

    if not os.path.exists(FILE_NAME):
        print("transactions.json not found.")
        return []

    with open(FILE_NAME, "r") as file:
        return json.load(file)


def get_expenses(transactions):

    return [
        transaction
        for transaction in transactions
        if transaction["transaction_type"] == "Expense"
    ]


def expense_pie_chart(transactions):

    expenses = get_expenses(transactions)

    if not expenses:
        print("\nNo expense data available.")
        return

    categories = defaultdict(float)

    for transaction in expenses:

        category = transaction["category"]

        categories[category] += float(
            transaction["amount"]
        )

    plt.figure(figsize=(7, 7))

    plt.pie(
        categories.values(),
        labels=categories.keys(),
        autopct="%1.1f%%",
        startangle=90
    )

    plt.title("Expense Breakdown by Category")

    plt.tight_layout()

    plt.show()


def monthly_expense_trend(transactions):

    expenses = get_expenses(transactions)

    if not expenses:
        print("\nNo expense data available.")
        return

    monthly_expenses = defaultdict(float)

    for transaction in expenses:

        date = transaction["date"]

        month = date[:7]

        monthly_expenses[month] += float(
            transaction["amount"]
        )

    months = sorted(monthly_expenses.keys())

    amounts = [
        monthly_expenses[month]
        for month in months
    ]

    plt.figure(figsize=(9, 5))

    plt.plot(
        months,
        amounts,
        marker="o"
    )

    plt.title("Monthly Expense Trend")

    plt.xlabel("Month")

    plt.ylabel("Total Expense")

    plt.grid(True)

    plt.xticks(rotation=45)

    plt.tight_layout()

    plt.show()


def monthly_expense_report(transactions):

    expenses = get_expenses(transactions)

    monthly_expenses = defaultdict(float)

    for transaction in expenses:

        month = transaction["date"][:7]

        monthly_expenses[month] += float(
            transaction["amount"]
        )

    print("\n========== MONTHLY EXPENSES ==========")

    if not monthly_expenses:
        print("No expense records found.")
        return

    for month in sorted(monthly_expenses):

        print(
            f"{month}: "
            f"₹{monthly_expenses[month]:,.2f}"
        )


def menu():

    transactions = load_transactions()

    while True:

        print("\n========== FINANCE DASHBOARD ==========")

        print("1. Expense Pie Chart")
        print("2. Monthly Expense Trend")
        print("3. Monthly Expense Report")
        print("4. Exit")

        choice = input("\nEnter Choice: ")

        if choice == "1":

            expense_pie_chart(transactions)

        elif choice == "2":

            monthly_expense_trend(transactions)

        elif choice == "3":

            monthly_expense_report(transactions)

        elif choice == "4":

            print("\nThank You!")
            break

        else:

            print("\nInvalid Choice!")


if __name__ == "__main__":
    menu()