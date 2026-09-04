import json
import os
from collections import defaultdict


TRANSACTIONS_FILE = "transactions.json"
BUDGET_FILE = "budgets.json"


# ==================================================
# LOAD JSON
# ==================================================

def load_json(filename, default):

    if not os.path.exists(filename):
        return default

    try:

        with open(
            filename,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    except (
        json.JSONDecodeError,
        OSError
    ):

        return default


# ==================================================
# LOAD TRANSACTIONS
# ==================================================

def load_transactions():

    return load_json(
        TRANSACTIONS_FILE,
        []
    )


# ==================================================
# LOAD BUDGETS
# ==================================================

def load_budgets():

    return load_json(
        BUDGET_FILE,
        {}
    )


# ==================================================
# GET TRANSACTION TYPE
# ==================================================

def get_type(transaction):

    return str(
        transaction.get(
            "transaction_type",
            transaction.get(
                "type",
                ""
            )
        )
    ).lower()


# ==================================================
# GET MONTH TRANSACTIONS
# ==================================================

def get_month_transactions(
    transactions,
    month
):

    return [

        transaction

        for transaction in transactions

        if str(
            transaction.get(
                "date",
                ""
            )
        ).startswith(month)

    ]


# ==================================================
# CALCULATE SUMMARY
# ==================================================

def calculate_summary(
    transactions
):

    income = 0
    expenses = 0

    categories = defaultdict(float)

    highest_expense = None


    for transaction in transactions:

        amount = float(
            transaction.get(
                "amount",
                0
            )
        )


        transaction_type = (
            get_type(transaction)
        )


        if transaction_type == "income":

            income += amount


        elif transaction_type == "expense":

            expenses += amount


            category = transaction.get(
                "category",
                "Other"
            )


            categories[category] += amount


            if (
                highest_expense is None
                or amount >
                float(
                    highest_expense.get(
                        "amount",
                        0
                    )
                )
            ):

                highest_expense = transaction


    balance = income - expenses


    savings_rate = (

        balance / income * 100

        if income > 0

        else 0

    )


    return {
        "income": income,
        "expenses": expenses,
        "balance": balance,
        "savings_rate": savings_rate,
        "categories": dict(categories),
        "highest_expense": highest_expense
    }


# ==================================================
# CURRENCY
# ==================================================

def currency(amount):

    return f"₹{amount:,.2f}"


# ==================================================
# PROGRESS BAR
# ==================================================

def progress_bar(
    percentage,
    width=30
):

    percentage = max(
        0,
        min(
            percentage,
            100
        )
    )


    filled = int(
        width *
        percentage /
        100
    )


    empty = width - filled


    return (
        "█" * filled +
        "░" * empty
    )


# ==================================================
# FINANCIAL HEALTH
# ==================================================

def financial_health(
    income,
    expenses,
    savings_rate
):

    if income <= 0:

        return (
            "⚠️  No income recorded"
        )


    if expenses > income:

        return (
            "🔴 Critical - "
            "Expenses exceed income"
        )


    if savings_rate < 10:

        return (
            "🟠 Needs Improvement"
        )


    if savings_rate < 25:

        return (
            "🟡 Fair"
        )


    if savings_rate < 40:

        return (
            "🟢 Good"
        )


    return (
        "💚 Excellent"
    )


# ==================================================
# DISPLAY CATEGORY ANALYSIS
# ==================================================

def display_categories(
    categories,
    total_expenses
):

    print(
        "\n========== CATEGORY ANALYSIS =========="
    )


    if not categories:

        print(
            "No expense categories found."
        )

        return


    sorted_categories = sorted(
        categories.items(),
        key=lambda item:
            item[1],
        reverse=True
    )


    for category, amount in (
        sorted_categories
    ):

        percentage = (

            amount /
            total_expenses *
            100

            if total_expenses > 0

            else 0

        )


        print(
            f"\n{category}"
        )


        print(
            f"{currency(amount)} "
            f"({percentage:.1f}%)"
        )


        print(
            progress_bar(
                percentage
            )
        )


# ==================================================
# DISPLAY BUDGET STATUS
# ==================================================

def display_budget_status(
    categories,
    budgets
):

    print(
        "\n========== BUDGET STATUS =========="
    )


    if not budgets:

        print(
            "No category budgets configured."
        )

        return


    for category, budget in budgets.items():

        spent = categories.get(
            category,
            0
        )


        budget = float(budget)


        percentage = (

            spent /
            budget *
            100

            if budget > 0

            else 0

        )


        remaining = budget - spent


        print(
            f"\n{category}"
        )


        print(
            f"Budget    : "
            f"{currency(budget)}"
        )


        print(
            f"Spent     : "
            f"{currency(spent)}"
        )


        print(
            f"Remaining : "
            f"{currency(remaining)}"
        )


        print(
            progress_bar(
                percentage
            ),
            f"{percentage:.1f}%"
        )


        if spent > budget:

            print(
                "🔴 OVER BUDGET"
            )

        elif percentage >= 80:

            print(
                "🟠 Almost at limit"
            )

        else:

            print(
                "🟢 Within budget"
            )


# ==================================================
# DISPLAY RECENT TRANSACTIONS
# ==================================================

def display_recent_transactions(
    transactions
):

    print(
        "\n========== RECENT TRANSACTIONS =========="
    )


    if not transactions:

        print(
            "No transactions found."
        )

        return


    sorted_transactions = sorted(
        transactions,
        key=lambda transaction:
            str(
                transaction.get(
                    "date",
                    ""
                )
            ),
        reverse=True
    )


    for transaction in (
        sorted_transactions[:5]
    ):

        transaction_type = (
            get_type(transaction)
        )


        amount = float(
            transaction.get(
                "amount",
                0
            )
        )


        symbol = (
            "+"
            if transaction_type ==
            "income"
            else "-"
        )


        print(
            f"{transaction.get('date', '')}"
            f" | "
            f"{transaction.get('title', 'Transaction'):<20}"
            f" | "
            f"{symbol}{currency(amount)}"
        )


# ==================================================
# DISPLAY DASHBOARD
# ==================================================

def display_dashboard(month):

    transactions = (
        load_transactions()
    )

    budgets = (
        load_budgets()
    )


    month_transactions = (
        get_month_transactions(
            transactions,
            month
        )
    )


    summary = calculate_summary(
        month_transactions
    )


    income = summary["income"]

    expenses = summary["expenses"]

    balance = summary["balance"]

    savings_rate = summary["savings_rate"]

    categories = summary["categories"]


    print(
        "\n"
        + "=" * 65
    )

    print(
        "              PERSONAL FINANCE DASHBOARD"
    )

    print(
        "=" * 65
    )


    print(
        f"Month: {month}"
    )


    print(
        "=" * 65
    )


    # ------------------------------------------------
    # SUMMARY
    # ------------------------------------------------

    print(
        "\n========== MONTHLY SUMMARY =========="
    )


    print(
        f"💰 Income       : "
        f"{currency(income)}"
    )


    print(
        f"💸 Expenses     : "
        f"{currency(expenses)}"
    )


    print(
        f"💵 Balance      : "
        f"{currency(balance)}"
    )


    print(
        f"📈 Savings Rate : "
        f"{savings_rate:.2f}%"
    )


    # ------------------------------------------------
    # SAVINGS BAR
    # ------------------------------------------------

    print(
        "\nSavings Progress:"
    )


    print(
        progress_bar(
            savings_rate
        ),
        f"{savings_rate:.1f}%"
    )


    # ------------------------------------------------
    # FINANCIAL HEALTH
    # ------------------------------------------------

    print(
        "\nFinancial Health:"
    )


    print(
        financial_health(
            income,
            expenses,
            savings_rate
        )
    )


    # ------------------------------------------------
    # CATEGORY
    # ------------------------------------------------

    display_categories(
        categories,
        expenses
    )


    # ------------------------------------------------
    # TOP CATEGORY
    # ------------------------------------------------

    if categories:

        top_category = max(
            categories,
            key=categories.get
        )


        print(
            "\n========== TOP SPENDING CATEGORY =========="
        )


        print(
            f"🏆 {top_category}"
        )


        print(
            f"Spent: "
            f"{currency(categories[top_category])}"
        )


    # ------------------------------------------------
    # HIGHEST EXPENSE
    # ------------------------------------------------

    highest_expense = (
        summary["highest_expense"]
    )


    if highest_expense:

        print(
            "\n========== HIGHEST EXPENSE =========="
        )


        print(
            f"Title    : "
            f"{highest_expense.get('title', '')}"
        )


        print(
            f"Category : "
            f"{highest_expense.get('category', 'Other')}"
        )


        print(
            f"Amount   : "
            f"{currency(float(highest_expense.get('amount', 0)))}"
        )


        print(
            f"Date     : "
            f"{highest_expense.get('date', '')}"
        )


    # ------------------------------------------------
    # BUDGET
    # ------------------------------------------------

    display_budget_status(
        categories,
        budgets
    )


    # ------------------------------------------------
    # RECENT TRANSACTIONS
    # ------------------------------------------------

    display_recent_transactions(
        month_transactions
    )


    print(
        "\n"
        + "=" * 65
    )


# ==================================================
# MAIN
# ==================================================

def main():

    print(
        "\nPERSONAL FINANCE DASHBOARD"
    )


    month = input(
        "Enter month (YYYY-MM): "
    ).strip()


    if len(month) != 7:

        print(
            "\nInvalid month format."
        )

        return


    display_dashboard(
        month
    )


if __name__ == "__main__":

    main()