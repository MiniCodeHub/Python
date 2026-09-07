import json
import os
from collections import defaultdict


# =====================================================
# CONFIGURATION
# =====================================================

DATA_FILE = "transactions.json"


# =====================================================
# LOAD TRANSACTIONS
# =====================================================
def load_transactions():

    if not os.path.exists(DATA_FILE):
        return []

    try:
        with open(
            DATA_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            transactions = json.load(file)

    except (
        json.JSONDecodeError,
        OSError
    ):

        return []

    if not isinstance(transactions, list):
        return []


    # ==========================================
    # REPAIR OLD TRANSACTIONS
    # ==========================================

    for index, transaction in enumerate(transactions):

        # --------------------------------------
        # ID
        # --------------------------------------

        if "id" not in transaction:

            transaction["id"] = index + 1


        # --------------------------------------
        # TITLE
        # --------------------------------------

        if "title" not in transaction:

            transaction["title"] = "Unknown"


        # --------------------------------------
        # CATEGORY
        # --------------------------------------

        if "category" not in transaction:

            transaction["category"] = "Other"


        # --------------------------------------
        # AMOUNT
        # --------------------------------------

        if "amount" not in transaction:

            transaction["amount"] = 0


        # --------------------------------------
        # DATE
        # --------------------------------------

        if "date" not in transaction:

            transaction["date"] = "Unknown"


        # --------------------------------------
        # TYPE
        # --------------------------------------

        if "type" not in transaction:

            category = str(
                transaction.get(
                    "category",
                    ""
                )
            ).lower()


            title = str(
                transaction.get(
                    "title",
                    ""
                )
            ).lower()


            income_keywords = [
                "salary",
                "income",
                "freelance",
                "business",
                "bonus",
                "investment",
                "interest"
            ]


            if (
                category in income_keywords
                or any(
                    word in title
                    for word in income_keywords
                )
            ):

                transaction["type"] = "income"

            else:

                transaction["type"] = "expense"


    # ==========================================
    # FIX DUPLICATE IDs
    # ==========================================

    used_ids = set()

    next_id = 1


    for transaction in transactions:

        transaction_id = transaction.get(
            "id"
        )


        if (
            transaction_id is None
            or transaction_id in used_ids
        ):

            while next_id in used_ids:

                next_id += 1


            transaction["id"] = next_id


        used_ids.add(
            transaction["id"]
        )


        next_id = max(
            next_id,
            transaction["id"] + 1
        )


    # ==========================================
    # SAVE REPAIRED DATA
    # ==========================================

    save_transactions(
        transactions
    )


    return transactions


# =====================================================
# SAVE TRANSACTIONS
# =====================================================

def save_transactions(transactions):

    try:

        with open(
            DATA_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                transactions,
                file,
                indent=4
            )

    except OSError as error:

        print(
            f"Error saving data: {error}"
        )


# =====================================================
# CURRENCY FORMAT
# =====================================================

def currency(amount):

    return f"₹{amount:,.2f}"


# =====================================================
# TOTAL INCOME
# =====================================================

def get_total_income(transactions):

    return sum(
        float(transaction["amount"])
        for transaction in transactions
        if transaction["type"] == "income"
    )


# =====================================================
# TOTAL EXPENSES
# =====================================================

def get_total_expenses(transactions):

    return sum(
        float(transaction["amount"])
        for transaction in transactions
        if transaction["type"] == "expense"
    )


# =====================================================
# BALANCE
# =====================================================

def get_balance(transactions):

    income = get_total_income(
        transactions
    )

    expenses = get_total_expenses(
        transactions
    )

    return income - expenses


# =====================================================
# SAVINGS RATE
# =====================================================

def get_savings_rate(transactions):

    income = get_total_income(
        transactions
    )

    if income == 0:
        return 0

    balance = get_balance(
        transactions
    )

    return (
        balance / income
    ) * 100


# =====================================================
# CATEGORY-WISE EXPENSES
# =====================================================

def get_category_expenses(
    transactions
):

    categories = defaultdict(float)

    for transaction in transactions:

        if transaction["type"] != "expense":
            continue

        category = transaction.get(
            "category",
            "Other"
        )

        categories[category] += float(
            transaction["amount"]
        )

    return dict(categories)


# =====================================================
# MONTHLY ANALYSIS
# =====================================================

def get_monthly_analysis(
    transactions
):

    monthly = defaultdict(
        lambda: {
            "income": 0,
            "expense": 0
        }
    )

    for transaction in transactions:

        date = transaction.get(
            "date",
            ""
        )

        if len(date) < 7:
            continue

        month = date[:7]

        amount = float(
            transaction["amount"]
        )

        if transaction["type"] == "income":

            monthly[month]["income"] += amount

        elif transaction["type"] == "expense":

            monthly[month]["expense"] += amount

    return dict(
        sorted(monthly.items())
    )


# =====================================================
# HIGHEST SPENDING CATEGORY
# =====================================================

def get_highest_spending_category(
    transactions
):

    categories = get_category_expenses(
        transactions
    )

    if not categories:
        return None, 0

    category = max(
        categories,
        key=categories.get
    )

    return (
        category,
        categories[category]
    )


# =====================================================
# FINANCIAL HEALTH
# =====================================================

def get_financial_health(
    savings_rate
):

    if savings_rate >= 30:

        return (
            "EXCELLENT",
            "You are saving a strong portion of your income."
        )

    elif savings_rate >= 20:

        return (
            "GOOD",
            "Your savings level is healthy."
        )

    elif savings_rate >= 10:

        return (
            "MODERATE",
            "Try to increase your savings."
        )

    elif savings_rate > 0:

        return (
            "NEEDS IMPROVEMENT",
            "Your expenses are consuming most of your income."
        )

    else:

        return (
            "CRITICAL",
            "Your expenses are equal to or greater than your income."
        )


# =====================================================
# DASHBOARD SUMMARY
# =====================================================

def show_dashboard(
    transactions
):

    income = get_total_income(
        transactions
    )

    expenses = get_total_expenses(
        transactions
    )

    balance = get_balance(
        transactions
    )

    savings_rate = get_savings_rate(
        transactions
    )

    status, message = get_financial_health(
        savings_rate
    )


    print("\n")
    print("=" * 60)
    print("              FINANCIAL SUMMARY")
    print("=" * 60)

    print(
        f"\nTotal Income   : {currency(income)}"
    )

    print(
        f"Total Expenses : {currency(expenses)}"
    )

    print(
        f"Current Balance: {currency(balance)}"
    )

    print(
        f"Savings Rate   : {savings_rate:.2f}%"
    )

    print(
        f"\nFinancial Health: {status}"
    )

    print(
        f"Advice          : {message}"
    )

    print("=" * 60)


# =====================================================
# CATEGORY REPORT
# =====================================================

def show_category_report(
    transactions
):

    categories = get_category_expenses(
        transactions
    )

    print("\n")
    print("=" * 60)
    print("             EXPENSE CATEGORY REPORT")
    print("=" * 60)


    if not categories:

        print("\nNo expense data available.")

        return


    total_expenses = sum(
        categories.values()
    )


    sorted_categories = sorted(
        categories.items(),
        key=lambda item: item[1],
        reverse=True
    )


    print(
        f"\n{'Category':<20}"
        f"{'Amount':>15}"
        f"{'Percentage':>15}"
    )

    print("-" * 60)


    for category, amount in sorted_categories:

        percentage = (
            amount /
            total_expenses
        ) * 100


        print(
            f"{category:<20}"
            f"{currency(amount):>15}"
            f"{percentage:>14.2f}%"
        )


    print("-" * 60)

    print(
        f"{'TOTAL':<20}"
        f"{currency(total_expenses):>15}"
    )


# =====================================================
# MONTHLY REPORT
# =====================================================

def show_monthly_report(
    transactions
):

    monthly = get_monthly_analysis(
        transactions
    )


    print("\n")
    print("=" * 70)
    print("                    MONTHLY REPORT")
    print("=" * 70)


    if not monthly:

        print("\nNo monthly data available.")

        return


    print(
        f"\n{'Month':<12}"
        f"{'Income':>18}"
        f"{'Expense':>18}"
        f"{'Savings':>18}"
    )

    print("-" * 70)


    for month, data in monthly.items():

        savings = (
            data["income"]
            -
            data["expense"]
        )


        print(
            f"{month:<12}"
            f"{currency(data['income']):>18}"
            f"{currency(data['expense']):>18}"
            f"{currency(savings):>18}"
        )


# =====================================================
# HIGHEST SPENDING REPORT
# =====================================================

def show_highest_spending(
    transactions
):

    category, amount = (
        get_highest_spending_category(
            transactions
        )
    )


    print("\n")
    print("=" * 60)
    print("             HIGHEST SPENDING CATEGORY")
    print("=" * 60)


    if category is None:

        print("\nNo expense data available.")

        return


    print(
        f"\nCategory : {category}"
    )

    print(
        f"Amount   : {currency(amount)}"
    )


# =====================================================
# TRANSACTION STATISTICS
# =====================================================

def show_transaction_statistics(
    transactions
):

    income_count = sum(
        1
        for transaction in transactions
        if transaction["type"] == "income"
    )


    expense_count = sum(
        1
        for transaction in transactions
        if transaction["type"] == "expense"
    )


    print("\n")
    print("=" * 60)
    print("             TRANSACTION STATISTICS")
    print("=" * 60)


    print(
        f"\nTotal Transactions : "
        f"{len(transactions)}"
    )

    print(
        f"Income Transactions : "
        f"{income_count}"
    )

    print(
        f"Expense Transactions: "
        f"{expense_count}"
    )


# =====================================================
# COMPLETE REPORT
# =====================================================

def generate_complete_report(
    transactions
):

    print("\n\n")

    print("#" * 70)
    print("#              COMPLETE FINANCIAL REPORT              #")
    print("#" * 70)


    show_dashboard(
        transactions
    )

    show_category_report(
        transactions
    )

    show_monthly_report(
        transactions
    )

    show_highest_spending(
        transactions
    )

    show_transaction_statistics(
        transactions
    )


    print("\n")
    print("#" * 70)
    print("#                  END OF REPORT                      #")
    print("#" * 70)


# =====================================================
# VIEW TRANSACTIONS
# =====================================================

def view_transactions(
    transactions
):

    print("\n")
    print("=" * 70)
    print("                    TRANSACTIONS")
    print("=" * 70)


    if not transactions:

        print("\nNo transactions found.")

        return


    for transaction in transactions:

        print(
            f"\nID       : {transaction['id']}"
        )

        print(
            f"Title    : {transaction['title']}"
        )

        print(
            f"Category : {transaction['category']}"
        )

        print(
            f"Type     : {transaction['type']}"
        )

        print(
            f"Amount   : {currency(transaction['amount'])}"
        )

        print(
            f"Date     : {transaction['date']}"
        )

        print("-" * 70)


# =====================================================
# ADD TRANSACTION
# =====================================================

def add_transaction(
    transactions
):

    print("\n")
    print("=" * 50)
    print("              ADD TRANSACTION")
    print("=" * 50)


    title = input(
        "Title: "
    ).strip()


    category = input(
        "Category: "
    ).strip()


    transaction_type = input(
        "Type (income/expense): "
    ).strip().lower()


    if transaction_type not in (
        "income",
        "expense"
    ):

        print(
            "\nInvalid transaction type."
        )

        return


    try:

        amount = float(
            input(
                "Amount: ₹"
            )
        )

    except ValueError:

        print(
            "\nInvalid amount."
        )

        return


    date = input(
        "Date (YYYY-MM-DD): "
    ).strip()


    new_id = max(
        (
            transaction["id"]
            for transaction
            in transactions
        ),
        default=0
    ) + 1


    transaction = {

        "id": new_id,

        "title": title,

        "category": category,

        "type": transaction_type,

        "amount": amount,

        "date": date
    }


    transactions.append(
        transaction
    )


    save_transactions(
        transactions
    )


    print(
        "\nTransaction added successfully."
    )


# =====================================================
# MENU
# =====================================================

def show_menu():

    print("\n")
    print("=" * 60)
    print("             PERSONAL FINANCE MANAGER")
    print("=" * 60)

    print("1. Financial Dashboard")
    print("2. Add Transaction")
    print("3. View Transactions")
    print("4. Expense Category Report")
    print("5. Monthly Report")
    print("6. Highest Spending Category")
    print("7. Transaction Statistics")
    print("8. Complete Financial Report")
    print("9. Save Data")
    print("10. Exit")

    print("=" * 60)


# =====================================================
# MAIN
# =====================================================

def main():

    transactions = load_transactions()


    print(
        "\nPersonal Finance Manager Started."
    )


    while True:

        show_menu()


        choice = input(
            "\nEnter choice: "
        ).strip()


        if choice == "1":

            show_dashboard(
                transactions
            )


        elif choice == "2":

            add_transaction(
                transactions
            )


        elif choice == "3":

            view_transactions(
                transactions
            )


        elif choice == "4":

            show_category_report(
                transactions
            )


        elif choice == "5":

            show_monthly_report(
                transactions
            )


        elif choice == "6":

            show_highest_spending(
                transactions
            )


        elif choice == "7":

            show_transaction_statistics(
                transactions
            )


        elif choice == "8":

            generate_complete_report(
                transactions
            )


        elif choice == "9":

            save_transactions(
                transactions
            )

            print(
                "\nData saved successfully."
            )


        elif choice == "10":

            save_transactions(
                transactions
            )

            print(
                "\nData saved successfully."
            )

            print(
                "Thank you for using Personal Finance Manager!"
            )

            break


        else:

            print(
                "\nInvalid choice. Please try again."
            )


# =====================================================
# START PROGRAM
# =====================================================

if __name__ == "__main__":

    main()