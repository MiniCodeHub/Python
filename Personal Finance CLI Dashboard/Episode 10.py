import json
import os
from collections import defaultdict
import matplotlib.pyplot as plt


FILE_NAME = "transactions.json"


def load_transactions():
    if not os.path.exists(FILE_NAME):
        return []

    with open(FILE_NAME, "r") as file:
        return json.load(file)


def income_vs_expense(transactions):

    income = 0
    expense = 0

    for transaction in transactions:

        if transaction["transaction_type"] == "Income":
            income += transaction["amount"]
        else:
            expense += transaction["amount"]

    plt.figure(figsize=(6, 5))

    plt.bar(
        ["Income", "Expense"],
        [income, expense]
    )

    plt.title("Income vs Expense")

    plt.ylabel("Amount")

    plt.show()


def expense_pie_chart(transactions):

    categories = defaultdict(float)

    for transaction in transactions:

        if transaction["transaction_type"] == "Expense":

            categories[
                transaction["category"]
            ] += transaction["amount"]

    if not categories:
        print("No expense data available.")
        return

    plt.figure(figsize=(7, 7))

    plt.pie(
        categories.values(),
        labels=categories.keys(),
        autopct="%1.1f%%",
        startangle=90
    )

    plt.title("Expenses by Category")

    plt.show()


def monthly_expense_trend(transactions):

    monthly = defaultdict(float)

    for transaction in transactions:

        if transaction["transaction_type"] == "Expense":

            month = transaction["date"][:7]

            monthly[month] += transaction["amount"]

    if not monthly:
        print("No monthly expense data.")
        return

    months = sorted(monthly.keys())

    values = [
        monthly[m]
        for m in months
    ]

    plt.figure(figsize=(8, 5))

    plt.plot(
        months,
        values,
        marker="o"
    )

    plt.title("Monthly Expense Trend")

    plt.xlabel("Month")

    plt.ylabel("Expense")

    plt.grid(True)

    plt.show()


def menu():

    transactions = load_transactions()

    while True:

        print("\n========== FINANCIAL CHARTS ==========")
        print("1. Income vs Expense")
        print("2. Expense Pie Chart")
        print("3. Monthly Expense Trend")
        print("4. Exit")

        choice = input("\nEnter Choice: ")

        if choice == "1":
            income_vs_expense(transactions)

        elif choice == "2":
            expense_pie_chart(transactions)

        elif choice == "3":
            monthly_expense_trend(transactions)

        elif choice == "4":
            print("\nThank You!")
            break

        else:
            print("\nInvalid Choice!")


if __name__ == "__main__":
    menu()