import json
import os


TRANSACTIONS_FILE = "transactions.json"
BUDGETS_FILE = "budgets.json"


# =========================
# JSON HELPERS
# =========================

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

        json.dump(
            data,
            file,
            indent=4
        )


# =========================
# LOAD DATA
# =========================

def load_transactions():

    return load_json(
        TRANSACTIONS_FILE,
        []
    )


def load_budgets():

    return load_json(
        BUDGETS_FILE,
        {}
    )


# =========================
# SET BUDGET
# =========================

def set_budget():

    category = input(
        "\nEnter category: "
    ).strip()

    if not category:

        print("Category cannot be empty.")
        return

    try:

        amount = float(
            input("Enter monthly budget: ")
        )

    except ValueError:

        print("Invalid amount.")
        return

    if amount <= 0:

        print("Budget must be greater than 0.")
        return

    budgets = load_budgets()

    budgets[category] = amount

    save_json(
        BUDGETS_FILE,
        budgets
    )

    print(
        f"\nBudget for {category} "
        f"set to ₹{amount:,.2f}"
    )


# =========================
# CALCULATE CATEGORY SPENDING
# =========================

def calculate_category_spending():

    transactions = load_transactions()

    spending = {}

    for transaction in transactions:

        transaction_type = (
            transaction.get(
                "transaction_type",
                transaction.get("type", "")
            )
        )

        if transaction_type.lower() != "expense":

            continue

        category = transaction.get(
            "category",
            "Other"
        )

        amount = float(
            transaction.get(
                "amount",
                0
            )
        )

        spending[category] = (
            spending.get(category, 0)
            + amount
        )

    return spending


# =========================
# BUDGET STATUS
# =========================

def get_budget_status(
    budget,
    spent
):

    remaining = budget - spent

    percentage = (
        spent / budget
    ) * 100

    if spent > budget:

        status = "OVER BUDGET"

    elif percentage >= 80:

        status = "WARNING"

    else:

        status = "OK"

    return (
        remaining,
        percentage,
        status
    )


# =========================
# VIEW BUDGETS
# =========================

def view_budgets():

    budgets = load_budgets()

    spending = (
        calculate_category_spending()
    )

    if not budgets:

        print(
            "\nNo budgets have been created."
        )

        return

    print(
        "\n========== BUDGET STATUS =========="
    )

    for category, budget in budgets.items():

        spent = spending.get(
            category,
            0
        )

        remaining, percentage, status = (
            get_budget_status(
                budget,
                spent
            )
        )

        print(
            f"\nCategory : {category}"
        )

        print(
            f"Budget   : ₹{budget:,.2f}"
        )

        print(
            f"Spent    : ₹{spent:,.2f}"
        )

        print(
            f"Used     : {percentage:.1f}%"
        )

        if remaining >= 0:

            print(
                f"Remaining: ₹{remaining:,.2f}"
            )

        else:

            print(
                f"Exceeded : ₹{abs(remaining):,.2f}"
            )

        print(
            f"Status   : {status}"
        )


# =========================
# OVERSpending ALERTS
# =========================

def show_overspending_alerts():

    budgets = load_budgets()

    spending = (
        calculate_category_spending()
    )

    if not budgets:

        print(
            "\nNo budgets have been created."
        )

        return

    print(
        "\n========== BUDGET ALERTS =========="
    )

    alert_found = False

    for category, budget in budgets.items():

        spent = spending.get(
            category,
            0
        )

        percentage = (
            spent / budget
        ) * 100

        if percentage >= 80:

            alert_found = True

            if spent > budget:

                exceeded = spent - budget

                print(
                    f"\nOVER BUDGET: {category}"
                )

                print(
                    f"Budget: ₹{budget:,.2f}"
                )

                print(
                    f"Spent : ₹{spent:,.2f}"
                )

                print(
                    f"Exceeded by: "
                    f"₹{exceeded:,.2f}"
                )

            else:

                remaining = budget - spent

                print(
                    f"\nWARNING: {category}"
                )

                print(
                    f"Budget: ₹{budget:,.2f}"
                )

                print(
                    f"Spent : ₹{spent:,.2f}"
                )

                print(
                    f"Only ₹{remaining:,.2f} remaining"
                )


    if not alert_found:

        print(
            "\nNo overspending alerts."
        )


# =========================
# DELETE BUDGET
# =========================

def delete_budget():

    budgets = load_budgets()

    if not budgets:

        print(
            "\nNo budgets found."
        )

        return

    category = input(
        "\nEnter category to delete: "
    ).strip()

    if category not in budgets:

        print(
            "\nBudget not found."
        )

        return

    del budgets[category]

    save_json(
        BUDGETS_FILE,
        budgets
    )

    print(
        "\nBudget deleted successfully."
    )


# =========================
# MENU
# =========================

def menu():

    while True:

        print(
            "\n========== PERSONAL FINANCE =========="
        )

        print("1. Set Budget")
        print("2. View Budgets")
        print("3. Budget Alerts")
        print("4. Delete Budget")
        print("5. Exit")

        choice = input(
            "\nEnter Choice: "
        )

        if choice == "1":

            set_budget()

        elif choice == "2":

            view_budgets()

        elif choice == "3":

            show_overspending_alerts()

        elif choice == "4":

            delete_budget()

        elif choice == "5":

            print(
                "\nGoodbye!"
            )

            break

        else:

            print(
                "\nInvalid choice."
            )


# =========================
# MAIN
# =========================

if __name__ == "__main__":

    menu()