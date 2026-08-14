import json
import os
from datetime import date, timedelta
from calendar import monthrange


TRANSACTIONS_FILE = "transactions.json"
RECURRING_FILE = "recurring.json"


def load_json(filename, default):
    if not os.path.exists(filename):
        return default

    try:
        with open(filename, "r") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        return default


def save_json(filename, data):
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)


def load_transactions():
    return load_json(TRANSACTIONS_FILE, [])


def load_recurring():
    return load_json(RECURRING_FILE, [])


def add_recurring_rule():

    title = input("Title: ").strip()

    if not title:
        print("Title cannot be empty.")
        return

    try:
        amount = float(input("Amount: "))
    except ValueError:
        print("Invalid amount.")
        return

    if amount <= 0:
        print("Amount must be greater than 0.")
        return

    transaction_type = input(
        "Type (Income/Expense): "
    ).strip().capitalize()

    if transaction_type not in ["Income", "Expense"]:
        print("Invalid transaction type.")
        return

    category = input(
        "Category: "
    ).strip()

    frequency = input(
        "Frequency (Daily/Weekly/Monthly): "
    ).strip().capitalize()

    if frequency not in ["Daily", "Weekly", "Monthly"]:
        print("Invalid frequency.")
        return

    start_date = input(
        "Start Date (YYYY-MM-DD): "
    ).strip()

    try:
        date.fromisoformat(start_date)
    except ValueError:
        print("Invalid date.")
        return

    rule = {
        "id": len(load_recurring()) + 1,
        "title": title,
        "amount": amount,
        "transaction_type": transaction_type,
        "category": category,
        "frequency": frequency,
        "start_date": start_date
    }

    recurring = load_recurring()

    recurring.append(rule)

    save_json(RECURRING_FILE, recurring)

    print("\nRecurring transaction added successfully.")


def next_date(current_date, frequency):

    if frequency == "Daily":
        return current_date + timedelta(days=1)

    if frequency == "Weekly":
        return current_date + timedelta(days=7)

    if frequency == "Monthly":

        year = current_date.year
        month = current_date.month

        if month == 12:
            year += 1
            month = 1
        else:
            month += 1

        day = min(
            current_date.day,
            monthrange(year, month)[1]
        )

        return date(year, month, day)

    return current_date


def transaction_exists(transactions, rule, transaction_date):

    for transaction in transactions:

        if (
            transaction.get("recurring_id") == rule["id"]
            and transaction.get("date") == transaction_date
        ):
            return True

    return False


def generate_recurring_transactions():

    transactions = load_transactions()
    recurring = load_recurring()

    today = date.today()

    generated = 0

    for rule in recurring:

        current_date = date.fromisoformat(
            rule["start_date"]
        )

        while current_date <= today:

            date_string = current_date.isoformat()

            if not transaction_exists(
                transactions,
                rule,
                date_string
            ):

                transactions.append({
                    "amount": rule["amount"],
                    "category": rule["category"],
                    "transaction_type":
                        rule["transaction_type"],
                    "date": date_string,
                    "title": rule["title"],
                    "recurring_id": rule["id"]
                })

                generated += 1

            current_date = next_date(
                current_date,
                rule["frequency"]
            )

    save_json(
        TRANSACTIONS_FILE,
        transactions
    )

    print(
        f"\n{generated} recurring transaction(s) generated."
    )


def show_recurring_rules():

    recurring = load_recurring()

    if not recurring:
        print("\nNo recurring transactions found.")
        return

    print("\n========== RECURRING TRANSACTIONS ==========")

    for rule in recurring:

        print(
            f"\nID        : {rule['id']}"
        )

        print(
            f"Title     : {rule['title']}"
        )

        print(
            f"Amount    : ₹{rule['amount']:,.2f}"
        )

        print(
            f"Type      : {rule['transaction_type']}"
        )

        print(
            f"Category  : {rule['category']}"
        )

        print(
            f"Frequency : {rule['frequency']}"
        )

        print(
            f"Start Date: {rule['start_date']}"
        )


def delete_recurring_rule():

    recurring = load_recurring()

    if not recurring:
        print("\nNo recurring transactions found.")
        return

    try:
        rule_id = int(
            input("Enter recurring ID to delete: ")
        )
    except ValueError:
        print("Invalid ID.")
        return

    updated = [
        rule
        for rule in recurring
        if rule["id"] != rule_id
    ]

    if len(updated) == len(recurring):

        print("\nRecurring transaction not found.")
        return

    save_json(
        RECURRING_FILE,
        updated
    )

    print("\nRecurring transaction deleted.")


def menu():

    while True:

        print("\n========== PERSONAL FINANCE ==========")

        print("1. Add Recurring Transaction")
        print("2. View Recurring Transactions")
        print("3. Generate Transactions")
        print("4. Delete Recurring Transaction")
        print("5. Exit")

        choice = input("\nEnter Choice: ")

        if choice == "1":

            add_recurring_rule()

        elif choice == "2":

            show_recurring_rules()

        elif choice == "3":

            generate_recurring_transactions()

        elif choice == "4":

            delete_recurring_rule()

        elif choice == "5":

            print("\nGoodbye!")
            break

        else:

            print("\nInvalid choice.")


if __name__ == "__main__":

    generate_recurring_transactions()

    menu()