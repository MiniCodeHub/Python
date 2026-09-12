import json
import os
from datetime import datetime
from typing import Any


DATA_FILE = "finance_data.json"


# ============================================================
# DATA MANAGEMENT
# ============================================================

def load_data() -> dict[str, Any]:
    if not os.path.exists(DATA_FILE):
        return {
            "transactions": [],
            "budgets": {},
            "goals": []
        }

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, dict):
            return {
                "transactions": [],
                "budgets": {},
                "goals": []
            }

        data.setdefault("transactions", [])
        data.setdefault("budgets", {})
        data.setdefault("goals", [])

        return data

    except (json.JSONDecodeError, OSError):
        print("Could not read data file. Starting with empty data.")
        return {
            "transactions": [],
            "budgets": {},
            "goals": []
        }


def save_data(data: dict[str, Any]) -> None:
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as file:
            json.dump(
                data,
                file,
                indent=4
            )
    except OSError as error:
        print(f"Could not save data: {error}")


# ============================================================
# INPUT HELPERS
# ============================================================

def get_non_empty_input(prompt: str) -> str:
    while True:
        value = input(prompt).strip()

        if value:
            return value

        print("Input cannot be empty.")


def get_amount(prompt: str) -> float:
    while True:
        try:
            amount = float(input(prompt).strip())

            if amount <= 0:
                print("Amount must be greater than 0.")
                continue

            return round(amount, 2)

        except ValueError:
            print("Please enter a valid amount.")


def get_integer(prompt: str) -> int:
    while True:
        try:
            return int(input(prompt).strip())

        except ValueError:
            print("Please enter a valid number.")


def get_date(prompt: str) -> str:
    while True:
        value = input(prompt).strip()

        if not value:
            return datetime.now().strftime("%Y-%m-%d")

        try:
            datetime.strptime(
                value,
                "%Y-%m-%d"
            )

            return value

        except ValueError:
            print("Use date format YYYY-MM-DD.")


def pause() -> None:
    input("\nPress Enter to continue...")


# ============================================================
# TRANSACTION VALIDATION
# ============================================================

def normalize_transaction(
    transaction: dict[str, Any]
) -> dict[str, Any]:

    return {
        "id": transaction.get("id", 0),
        "type": transaction.get("type", "expense"),
        "category": transaction.get(
            "category",
            "Other"
        ),
        "amount": float(
            transaction.get(
                "amount",
                0
            )
        ),
        "description": transaction.get(
            "description",
            ""
        ),
        "date": transaction.get(
            "date",
            datetime.now().strftime("%Y-%m-%d")
        )
    }


def normalize_data(
    data: dict[str, Any]
) -> dict[str, Any]:

    transactions = []

    for index, transaction in enumerate(
        data.get("transactions", []),
        start=1
    ):
        if isinstance(transaction, dict):
            normalized = normalize_transaction(
                transaction
            )

            if not normalized["id"]:
                normalized["id"] = index

            transactions.append(normalized)

    data["transactions"] = transactions

    if not isinstance(
        data.get("budgets"),
        dict
    ):
        data["budgets"] = {}

    if not isinstance(
        data.get("goals"),
        list
    ):
        data["goals"] = []

    return data


# ============================================================
# TRANSACTION FUNCTIONS
# ============================================================

def get_next_transaction_id(
    transactions: list[dict[str, Any]]
) -> int:

    valid_ids = []

    for transaction in transactions:
        try:
            valid_ids.append(
                int(transaction.get("id", 0))
            )
        except (ValueError, TypeError):
            pass

    if not valid_ids:
        return 1

    return max(valid_ids) + 1


def add_transaction(
    data: dict[str, Any]
) -> None:

    print("\n" + "=" * 50)
    print("ADD TRANSACTION")
    print("=" * 50)

    print("1. Income")
    print("2. Expense")

    while True:
        transaction_type = input(
            "Choose type: "
        ).strip()

        if transaction_type == "1":
            transaction_type = "income"
            break

        if transaction_type == "2":
            transaction_type = "expense"
            break

        print("Choose 1 or 2.")

    category = get_non_empty_input(
        "Category: "
    )

    amount = get_amount(
        "Amount: ₹"
    )

    description = input(
        "Description: "
    ).strip()

    date = get_date(
        "Date (YYYY-MM-DD, Enter for today): "
    )

    transaction = {
        "id": get_next_transaction_id(
            data["transactions"]
        ),
        "type": transaction_type,
        "category": category,
        "amount": amount,
        "description": description,
        "date": date
    }

    data["transactions"].append(
        transaction
    )

    save_data(data)

    print("\nTransaction added successfully.")


def show_transactions(
    data: dict[str, Any]
) -> None:

    transactions = data["transactions"]

    if not transactions:
        print("\nNo transactions found.")
        return

    print("\n" + "=" * 90)
    print("ALL TRANSACTIONS")
    print("=" * 90)

    print(
        f"{'ID':<5}"
        f"{'Date':<15}"
        f"{'Type':<10}"
        f"{'Category':<18}"
        f"{'Amount':>12}"
    )

    print("-" * 90)

    for transaction in transactions:

        transaction_type = transaction.get(
            "type",
            "expense"
        )

        sign = "+" if transaction_type == "income" else "-"

        print(
            f"{transaction.get('id', 0):<5}"
            f"{transaction.get('date', ''):<15}"
            f"{transaction_type:<10}"
            f"{transaction.get('category', ''):<18}"
            f"{sign}₹{transaction.get('amount', 0):>10.2f}"
        )

        description = transaction.get(
            "description",
            ""
        )

        if description:
            print(
                f"      Description: {description}"
            )

    print("-" * 90)


def delete_transaction(
    data: dict[str, Any]
) -> None:

    show_transactions(data)

    if not data["transactions"]:
        return

    transaction_id = get_integer(
        "\nEnter transaction ID to delete: "
    )

    transaction = next(
        (
            item
            for item in data["transactions"]
            if item.get("id") == transaction_id
        ),
        None
    )

    if transaction is None:
        print("Transaction not found.")
        return

    data["transactions"].remove(
        transaction
    )

    save_data(data)

    print("Transaction deleted successfully.")


# ============================================================
# FINANCIAL CALCULATIONS
# ============================================================

def get_total_income(
    transactions: list[dict[str, Any]]
) -> float:

    return round(
        sum(
            float(transaction.get("amount", 0))
            for transaction in transactions
            if transaction.get("type") == "income"
        ),
        2
    )


def get_total_expenses(
    transactions: list[dict[str, Any]]
) -> float:

    return round(
        sum(
            float(transaction.get("amount", 0))
            for transaction in transactions
            if transaction.get("type") == "expense"
        ),
        2
    )


def get_balance(
    transactions: list[dict[str, Any]]
) -> float:

    return round(
        get_total_income(transactions)
        - get_total_expenses(transactions),
        2
    )


def get_category_expenses(
    transactions: list[dict[str, Any]]
) -> dict[str, float]:

    categories: dict[str, float] = {}

    for transaction in transactions:

        if transaction.get("type") != "expense":
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

        categories[category] = round(
            categories.get(category, 0)
            + amount,
            2
        )

    return categories


# ============================================================
# DASHBOARD
# ============================================================

def show_dashboard(
    data: dict[str, Any]
) -> None:

    transactions = data["transactions"]

    income = get_total_income(
        transactions
    )

    expenses = get_total_expenses(
        transactions
    )

    balance = income - expenses

    print("\n")
    print("=" * 60)
    print("              PERSONAL FINANCE DASHBOARD")
    print("=" * 60)

    print(f"\nTotal Income   : ₹{income:,.2f}")
    print(f"Total Expenses : ₹{expenses:,.2f}")
    print(f"Balance        : ₹{balance:,.2f}")

    print("\n" + "-" * 60)
    print("EXPENSES BY CATEGORY")
    print("-" * 60)

    categories = get_category_expenses(
        transactions
    )

    if not categories:
        print("No expenses recorded.")

    else:
        for category, amount in sorted(
            categories.items(),
            key=lambda item: item[1],
            reverse=True
        ):
            print(
                f"{category:<25} ₹{amount:>10,.2f}"
            )

    print("\n" + "-" * 60)
    print("FINANCIAL STATUS")
    print("-" * 60)

    if balance > 0:
        print("You currently have a positive balance.")

    elif balance < 0:
        print("Warning: Your expenses are higher than your income.")

    else:
        print("Your income and expenses are balanced.")

    print("=" * 60)


# ============================================================
# MONTHLY SUMMARY
# ============================================================

def monthly_summary(
    data: dict[str, Any]
) -> None:

    month = input(
        "Enter month (YYYY-MM): "
    ).strip()

    try:
        datetime.strptime(
            month,
            "%Y-%m"
        )
    except ValueError:
        print("Invalid month format.")
        return

    monthly_transactions = [
        transaction
        for transaction in data["transactions"]
        if transaction.get(
            "date",
            ""
        ).startswith(month)
    ]

    income = get_total_income(
        monthly_transactions
    )

    expenses = get_total_expenses(
        monthly_transactions
    )

    print("\n" + "=" * 50)
    print(f"MONTHLY SUMMARY — {month}")
    print("=" * 50)

    print(f"Income   : ₹{income:,.2f}")
    print(f"Expenses : ₹{expenses:,.2f}")
    print(f"Balance  : ₹{income - expenses:,.2f}")

    print("=" * 50)


# ============================================================
# BUDGET SYSTEM
# ============================================================

def set_budget(
    data: dict[str, Any]
) -> None:

    category = get_non_empty_input(
        "Budget category: "
    )

    amount = get_amount(
        "Budget amount: ₹"
    )

    data["budgets"][category] = amount

    save_data(data)

    print(
        f"Budget set for {category}: ₹{amount:,.2f}"
    )


def show_budgets(
    data: dict[str, Any]
) -> None:

    budgets = data["budgets"]

    if not budgets:
        print("\nNo budgets created.")
        return

    expenses = get_category_expenses(
        data["transactions"]
    )

    print("\n" + "=" * 60)
    print("BUDGET STATUS")
    print("=" * 60)

    for category, budget in budgets.items():

        spent = expenses.get(
            category,
            0
        )

        remaining = budget - spent

        print(f"\nCategory : {category}")
        print(f"Budget   : ₹{budget:,.2f}")
        print(f"Spent    : ₹{spent:,.2f}")
        print(f"Remaining: ₹{remaining:,.2f}")

        if remaining < 0:
            print("STATUS   : OVER BUDGET")

        else:
            print("STATUS   : Within budget")


# ============================================================
# SAVINGS GOALS
# ============================================================

def add_goal(
    data: dict[str, Any]
) -> None:

    print("\n" + "=" * 50)
    print("ADD SAVINGS GOAL")
    print("=" * 50)

    name = get_non_empty_input(
        "Goal name: "
    )

    target = get_amount(
        "Target amount: ₹"
    )

    goal = {
        "id": len(data["goals"]) + 1,
        "name": name,
        "target": target,
        "saved": 0.0
    }

    data["goals"].append(
        goal
    )

    save_data(data)

    print("Savings goal created.")


def add_goal_saving(
    data: dict[str, Any]
) -> None:

    show_goals(data)

    if not data["goals"]:
        return

    goal_id = get_integer(
        "\nGoal ID: "
    )

    goal = next(
        (
            item
            for item in data["goals"]
            if item.get("id") == goal_id
        ),
        None
    )

    if goal is None:
        print("Goal not found.")
        return

    amount = get_amount(
        "Amount saved: ₹"
    )

    goal["saved"] = round(
        float(goal.get("saved", 0))
        + amount,
        2
    )

    save_data(data)

    print("Saving added successfully.")


def show_goals(
    data: dict[str, Any]
) -> None:

    goals = data["goals"]

    if not goals:
        print("\nNo savings goals.")
        return

    print("\n" + "=" * 70)
    print("SAVINGS GOALS")
    print("=" * 70)

    for goal in goals:

        target = float(
            goal.get("target", 0)
        )

        saved = float(
            goal.get("saved", 0)
        )

        remaining = max(
            target - saved,
            0
        )

        percentage = (
            saved / target * 100
            if target > 0
            else 0
        )

        print(f"\nID       : {goal.get('id')}")
        print(f"Goal     : {goal.get('name')}")
        print(f"Target   : ₹{target:,.2f}")
        print(f"Saved    : ₹{saved:,.2f}")
        print(f"Remaining: ₹{remaining:,.2f}")
        print(f"Progress : {percentage:.1f}%")

        if saved >= target:
            print("STATUS   : GOAL COMPLETED")
        else:
            print("STATUS   : IN PROGRESS")


# ============================================================
# SEARCH
# ============================================================

def search_transactions(
    data: dict[str, Any]
) -> None:

    keyword = get_non_empty_input(
        "Search keyword: "
    ).lower()

    results = []

    for transaction in data["transactions"]:

        searchable = " ".join(
            [
                str(transaction.get("type", "")),
                str(transaction.get("category", "")),
                str(transaction.get("description", "")),
                str(transaction.get("date", "")),
            ]
        ).lower()

        if keyword in searchable:
            results.append(transaction)

    if not results:
        print("\nNo matching transactions.")
        return

    print("\n" + "=" * 70)
    print("SEARCH RESULTS")
    print("=" * 70)

    for transaction in results:

        print(
            f"ID: {transaction.get('id')} | "
            f"{transaction.get('date')} | "
            f"{transaction.get('type')} | "
            f"{transaction.get('category')} | "
            f"₹{transaction.get('amount', 0):,.2f}"
        )

        if transaction.get("description"):
            print(
                f"Description: {transaction.get('description')}"
            )


# ============================================================
# DATA RESET
# ============================================================

def reset_data(
    data: dict[str, Any]
) -> None:

    confirmation = input(
        "\nType DELETE to erase all financial data: "
    ).strip()

    if confirmation != "DELETE":
        print("Reset cancelled.")
        return

    data["transactions"] = []
    data["budgets"] = {}
    data["goals"] = []

    save_data(data)

    print("All financial data has been deleted.")


# ============================================================
# MENU
# ============================================================

def show_menu() -> None:

    print("\n")
    print("=" * 60)
    print("       PERSONAL FINANCE CLI + DASHBOARD")
    print("=" * 60)

    print("\n1. Dashboard")
    print("2. Add Transaction")
    print("3. View Transactions")
    print("4. Search Transactions")
    print("5. Delete Transaction")
    print("6. Monthly Summary")
    print("7. Set Budget")
    print("8. View Budgets")
    print("9. Add Savings Goal")
    print("10. Add Goal Saving")
    print("11. View Savings Goals")
    print("12. Reset All Data")
    print("0. Exit")

    print("=" * 60)


# ============================================================
# MAIN PROGRAM
# ============================================================

def main() -> None:

    data = load_data()

    data = normalize_data(data)

    save_data(data)

    while True:

        show_menu()

        choice = input(
            "Enter your choice: "
        ).strip()

        if choice == "1":
            show_dashboard(data)
            pause()

        elif choice == "2":
            add_transaction(data)
            pause()

        elif choice == "3":
            show_transactions(data)
            pause()

        elif choice == "4":
            search_transactions(data)
            pause()

        elif choice == "5":
            delete_transaction(data)
            pause()

        elif choice == "6":
            monthly_summary(data)
            pause()

        elif choice == "7":
            set_budget(data)
            pause()

        elif choice == "8":
            show_budgets(data)
            pause()

        elif choice == "9":
            add_goal(data)
            pause()

        elif choice == "10":
            add_goal_saving(data)
            pause()

        elif choice == "11":
            show_goals(data)
            pause()

        elif choice == "12":
            reset_data(data)
            pause()

        elif choice == "0":
            save_data(data)
            print("\nThank you for using Personal Finance Manager.")
            print("Goodbye!")
            break

        else:
            print("\nInvalid choice.")
            pause()


# ============================================================
# PROGRAM START
# ============================================================

if __name__ == "__main__":
    main()
