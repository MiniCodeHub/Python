import json
import os


TRANSACTIONS_FILE = "transactions.json"


# =========================
# LOAD TRANSACTIONS
# =========================

def load_transactions():

    if not os.path.exists(TRANSACTIONS_FILE):
        return []

    try:

        with open(
            TRANSACTIONS_FILE,
            "r"
        ) as file:

            return json.load(file)

    except (
        json.JSONDecodeError,
        OSError
    ):

        return []


# =========================
# CATEGORY TOTALS
# =========================

def category_totals(transactions):

    categories = {}


    for transaction in transactions:

        if transaction.get("type") != "expense":
            continue


        category = (
            transaction
            .get("category", "Other")
            .strip()
        )


        amount = float(
            transaction.get(
                "amount",
                0
            )
        )


        categories[category] = (
            categories.get(category, 0)
            + amount
        )


    return categories


# =========================
# TOTAL EXPENSE
# =========================

def total_expense(transactions):

    return sum(

        float(
            transaction.get(
                "amount",
                0
            )
        )

        for transaction in transactions

        if transaction.get("type")
        == "expense"

    )


# =========================
# HIGHEST CATEGORY
# =========================

def highest_category(categories):

    if not categories:
        return None, 0


    category = max(
        categories,
        key=categories.get
    )


    return category, categories[category]


# =========================
# LOWEST CATEGORY
# =========================

def lowest_category(categories):

    if not categories:
        return None, 0


    category = min(
        categories,
        key=categories.get
    )


    return category, categories[category]


# =========================
# LARGEST EXPENSE
# =========================

def largest_expense(transactions):

    expenses = [

        transaction

        for transaction in transactions

        if transaction.get("type")
        == "expense"

    ]


    if not expenses:
        return None


    return max(
        expenses,
        key=lambda transaction:
            float(
                transaction.get(
                    "amount",
                    0
                )
            )
    )


# =========================
# AVERAGE EXPENSE
# =========================

def average_expense(transactions):

    expenses = [

        transaction

        for transaction in transactions

        if transaction.get("type")
        == "expense"

    ]


    if not expenses:
        return 0


    total = sum(

        float(
            transaction.get(
                "amount",
                0
            )
        )

        for transaction in expenses

    )


    return total / len(expenses)


# =========================
# CATEGORY PERCENTAGE
# =========================

def category_percentage(
    amount,
    total
):

    if total <= 0:
        return 0


    return (
        amount / total
    ) * 100


# =========================
# PROGRESS BAR
# =========================

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


    empty = (
        width -
        filled
    )


    return (
        "["
        + "#" * filled
        + "-" * empty
        + "]"
    )


# =========================
# CATEGORY REPORT
# =========================

def category_report(transactions):

    categories = category_totals(
        transactions
    )


    total = total_expense(
        transactions
    )


    if not categories:

        print(
            "\nNo expense data available."
        )

        return


    print(
        "\n========== CATEGORY ANALYSIS =========="
    )


    sorted_categories = sorted(
        categories.items(),
        key=lambda item: item[1],
        reverse=True
    )


    for category, amount in sorted_categories:

        percentage = category_percentage(
            amount,
            total
        )


        print(
            f"\n{category}"
        )


        print(
            f"Spent: ₹{amount:,.2f}"
        )


        print(
            f"Share: {percentage:.1f}%"
        )


        print(
            progress_bar(
                percentage
            )
        )


# =========================
# FULL ANALYTICS
# =========================

def show_analytics():

    transactions = load_transactions()


    if not transactions:

        print(
            "\nNo transactions found."
        )

        return


    expenses = [

        transaction

        for transaction in transactions

        if transaction.get("type")
        == "expense"

    ]


    if not expenses:

        print(
            "\nNo expenses found."
        )

        return


    total = total_expense(
        transactions
    )


    categories = category_totals(
        transactions
    )


    highest_name, highest_amount = (
        highest_category(
            categories
        )
    )


    lowest_name, lowest_amount = (
        lowest_category(
            categories
        )
    )


    largest = largest_expense(
        transactions
    )


    average = average_expense(
        transactions
    )


    print(
        "\n\n========== EXPENSE ANALYTICS =========="
    )


    print(
        f"\nTotal Expenses:"
        f" ₹{total:,.2f}"
    )


    print(
        f"Number of Expenses:"
        f" {len(expenses)}"
    )


    print(
        f"Average Expense:"
        f" ₹{average:,.2f}"
    )


    if largest:

        print(
            f"Largest Expense:"
            f" ₹{float(largest.get('amount', 0)):,.2f}"
        )

        print(
            f"Expense:"
            f" {largest.get('title', 'Unknown')}"
        )


    if highest_name:

        print(
            f"\nHighest Category:"
            f" {highest_name}"
        )

        print(
            f"Amount:"
            f" ₹{highest_amount:,.2f}"
        )


    if lowest_name:

        print(
            f"Lowest Category:"
            f" {lowest_name}"
        )

        print(
            f"Amount:"
            f" ₹{lowest_amount:,.2f}"
        )


    category_report(
        transactions
    )


# =========================
# MENU
# =========================

def menu():

    while True:

        print(
            "\n\n========== EXPENSE ANALYTICS =========="
        )

        print(
            "1. Full Analytics"
        )

        print(
            "2. Category Report"
        )

        print(
            "3. Exit"
        )


        choice = input(
            "\nEnter Choice: "
        ).strip()


        if choice == "1":

            show_analytics()


        elif choice == "2":

            transactions = (
                load_transactions()
            )

            category_report(
                transactions
            )


        elif choice == "3":

            print(
                "\nReturning..."
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