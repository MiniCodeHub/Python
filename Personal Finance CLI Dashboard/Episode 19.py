import json
import os
from datetime import datetime
from collections import defaultdict


# =====================================================
# CONFIGURATION
# =====================================================

DATA_FILE = "transactions.json"


# =====================================================
# SAMPLE DATA
# =====================================================

SAMPLE_TRANSACTIONS = [

    {
        "id": 1,
        "title": "Salary",
        "category": "Salary",
        "type": "income",
        "amount": 60000,
        "date": "2026-04-01"
    },

    {
        "id": 2,
        "title": "Rent",
        "category": "Housing",
        "type": "expense",
        "amount": 12000,
        "date": "2026-04-03"
    },

    {
        "id": 3,
        "title": "Food",
        "category": "Food",
        "type": "expense",
        "amount": 5000,
        "date": "2026-04-10"
    },

    {
        "id": 4,
        "title": "Salary",
        "category": "Salary",
        "type": "income",
        "amount": 60000,
        "date": "2026-05-01"
    },

    {
        "id": 5,
        "title": "Rent",
        "category": "Housing",
        "type": "expense",
        "amount": 12000,
        "date": "2026-05-03"
    },

    {
        "id": 6,
        "title": "Shopping",
        "category": "Shopping",
        "type": "expense",
        "amount": 7000,
        "date": "2026-05-15"
    },

    {
        "id": 7,
        "title": "Salary",
        "category": "Salary",
        "type": "income",
        "amount": 62000,
        "date": "2026-06-01"
    },

    {
        "id": 8,
        "title": "Food",
        "category": "Food",
        "type": "expense",
        "amount": 6500,
        "date": "2026-06-12"
    },

    {
        "id": 9,
        "title": "Transport",
        "category": "Transport",
        "type": "expense",
        "amount": 3000,
        "date": "2026-06-18"
    },

    {
        "id": 10,
        "title": "Salary",
        "category": "Salary",
        "type": "income",
        "amount": 62000,
        "date": "2026-07-01"
    },

    {
        "id": 11,
        "title": "Rent",
        "category": "Housing",
        "type": "expense",
        "amount": 12000,
        "date": "2026-07-03"
    },

    {
        "id": 12,
        "title": "Entertainment",
        "category": "Entertainment",
        "type": "expense",
        "amount": 4000,
        "date": "2026-07-20"
    },

    {
        "id": 13,
        "title": "Salary",
        "category": "Salary",
        "type": "income",
        "amount": 65000,
        "date": "2026-08-01"
    },

    {
        "id": 14,
        "title": "Food",
        "category": "Food",
        "type": "expense",
        "amount": 7000,
        "date": "2026-08-09"
    },

    {
        "id": 15,
        "title": "Shopping",
        "category": "Shopping",
        "type": "expense",
        "amount": 6000,
        "date": "2026-08-16"
    },

    {
        "id": 16,
        "title": "Rent",
        "category": "Housing",
        "type": "expense",
        "amount": 12000,
        "date": "2026-08-03"
    },

    {
        "id": 17,
        "title": "Salary",
        "category": "Salary",
        "type": "income",
        "amount": 65000,
        "date": "2026-09-01"
    },

    {
        "id": 18,
        "title": "Rent",
        "category": "Housing",
        "type": "expense",
        "amount": 12000,
        "date": "2026-09-03"
    },

    {
        "id": 19,
        "title": "Food",
        "category": "Food",
        "type": "expense",
        "amount": 5500,
        "date": "2026-09-04"
    },

    {
        "id": 20,
        "title": "Transport",
        "category": "Transport",
        "type": "expense",
        "amount": 2500,
        "date": "2026-09-05"
    }

]


# =====================================================
# LOAD DATA
# =====================================================

def load_transactions():

    if not os.path.exists(DATA_FILE):

        save_transactions(
            SAMPLE_TRANSACTIONS
        )

        return SAMPLE_TRANSACTIONS.copy()


    try:

        with open(
            DATA_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)


        if isinstance(data, list):

            return data


    except (
        json.JSONDecodeError,
        OSError
    ):

        pass


    return []


# =====================================================
# SAVE DATA
# =====================================================

def save_transactions(
    transactions
):

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
# CURRENCY
# =====================================================

def currency(
    amount
):

    return f"₹{amount:,.2f}"


# =====================================================
# TOTAL INCOME
# =====================================================

def get_total_income(
    transactions
):

    return sum(
        float(transaction["amount"])
        for transaction in transactions
        if transaction["type"] == "income"
    )


# =====================================================
# TOTAL EXPENSE
# =====================================================

def get_total_expenses(
    transactions
):

    return sum(
        float(transaction["amount"])
        for transaction in transactions
        if transaction["type"] == "expense"
    )


# =====================================================
# BALANCE
# =====================================================

def get_balance(
    transactions
):

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

def get_savings_rate(
    transactions
):

    income = get_total_income(
        transactions
    )

    if income == 0:

        return 0


    balance = get_balance(
        transactions
    )


    return (
        balance /
        income
    ) * 100


# =====================================================
# CATEGORY SUMMARY
# =====================================================

def get_category_summary(
    transactions
):

    categories = defaultdict(float)


    for transaction in transactions:

        if (
            transaction["type"]
            != "expense"
        ):
            continue


        category =
            transaction.get(
                "category",
                "Other"
            )


        categories[category] += \
            float(
                transaction["amount"]
            )


    return dict(categories)


# =====================================================
# MONTHLY SUMMARY
# =====================================================

def get_monthly_summary(
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


        month =
            date[:7]


        amount =
            float(
                transaction["amount"]
            )


        if (
            transaction["type"]
            == "income"
        ):

            monthly[
                month
            ]["income"] += amount


        elif (
            transaction["type"]
            == "expense"
        ):

            monthly[
                month
            ]["expense"] += amount


    return dict(
        sorted(
            monthly.items()
        )
    )


# =====================================================
# HIGHEST EXPENSE CATEGORY
# =====================================================

def get_highest_category(
    transactions
):

    categories =
        get_category_summary(
            transactions
        )


    if not categories:

        return None, 0


    category =
        max(
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

def financial_health(
    savings_rate
):

    if savings_rate >= 30:

        return (
            "EXCELLENT",
            "Your savings rate is very strong."
        )


    if savings_rate >= 20:

        return (
            "GOOD",
            "You are maintaining a healthy savings rate."
        )


    if savings_rate >= 10:

        return (
            "MODERATE",
            "Try to increase your monthly savings."
        )


    if savings_rate > 0:

        return (
            "NEEDS IMPROVEMENT",
            "Your savings are currently quite low."
        )


    return (
        "CRITICAL",
        "Your expenses are equal to or greater than your income."
    )


# =====================================================
# DASHBOARD
# =====================================================

def show_dashboard(
    transactions
):

    income =
        get_total_income(
            transactions
        )


    expenses =
        get_total_expenses(
            transactions
        )


    balance =
        get_balance(
            transactions
        )


    savings_rate =
        get_savings_rate(
            transactions
        )


    print(
        "\n"
        + "=" * 60
    )

    print(
        "              PERSONAL FINANCE DASHBOARD"
    )

    print(
        "=" * 60
    )


    print(
        f"\nTotal Income   : "
        f"{currency(income)}"
    )


    print(
        f"Total Expenses : "
        f"{currency(expenses)}"
    )


    print(
        f"Balance        : "
        f"{currency(balance)}"
    )


    print(
        f"Savings Rate   : "
        f"{savings_rate:.1f}%"
    )


    print(
        "-" * 60
    )


    status, message =
        financial_health(
            savings_rate
        )


    print(
        f"Financial Health : {status}"
    )

    print(
        f"Advice           : {message}"
    )


    print(
        "=" * 60
    )


# =====================================================
# CATEGORY REPORT
# =====================================================

def show_category_report(
    transactions
):

    categories =
        get_category_summary(
            transactions
        )


    print(
        "\n"
        + "=" * 60
    )

    print(
        "             EXPENSE CATEGORY REPORT"
    )

    print(
        "=" * 60
    )


    if not categories:

        print(
            "\nNo expense data available."
        )

        return


    total =
        sum(
            categories.values()
        )


    sorted_categories =
        sorted(
            categories.items(),
            key=lambda item:
                item[1],
            reverse=True
        )


    for (
        category,
        amount
    ) in sorted_categories:

        percentage =
            (
                amount /
                total *
                100
            )


        print(
            f"\n{category:<20}"
            f"{currency(amount):>15}"
            f"   {percentage:>5.1f}%"
        )


    print(
        "\n"
        + "-" * 60
    )

    print(
        f"Total Expenses: "
        f"{currency(total)}"
    )


# =====================================================
# MONTHLY REPORT
# =====================================================

def show_monthly_report(
    transactions
):

    monthly =
        get_monthly_summary(
            transactions
        )


    print(
        "\n"
        + "=" * 70
    )

    print(
        "                    MONTHLY REPORT"
    )

    print(
        "=" * 70
    )


    if not monthly:

        print(
            "\nNo monthly data available."
        )

        return


    print(
        f"\n{'Month':<12}"
        f"{'Income':>15}"
        f"{'Expense':>15}"
        f"{'Savings':>15}"
    )


    print(
        "-" * 70
    )


    for (
        month,
        data
    ) in monthly.items():

        savings =
            data["income"] -
            data["expense"]


        print(
            f"{month:<12}"
            f"{currency(data['income']):>15}"
            f"{currency(data['expense']):>15}"
            f"{currency(savings):>15}"
        )


# =====================================================
# TOP EXPENSE
# =====================================================

def show_highest_category(
    transactions
):

    category, amount =
        get_highest_category(
            transactions
        )


    print(
        "\n"
        + "=" * 60
    )

    print(
        "              HIGHEST EXPENSE CATEGORY"
    )

    print(
        "=" * 60
    )


    if category is None:

        print(
            "\nNo expense data available."
        )

        return


    print(
        f"\nCategory : {category}"
    )

    print(
        f"Amount   : {currency(amount)}"
    )


# =====================================================
# TRANSACTION COUNT
# =====================================================

def show_transaction_statistics(
    transactions
):

    income_count =
        sum(
            1
            for transaction
            in transactions
            if transaction["type"]
            == "income"
        )


    expense_count =
        sum(
            1
            for transaction
            in transactions
            if transaction["type"]
            == "expense"
        )


    print(
        "\n"
        + "=" * 60
    )

    print(
        "             TRANSACTION STATISTICS"
    )

    print(
        "=" * 60
    )


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

    print(
        "\n\n"
    )

    print(
        "#" * 70
    )

    print(
        "#                 FINANCIAL REPORT                 #"
    )

    print(
        "#" * 70
    )


    show_dashboard(
        transactions
    )


    show_category_report(
        transactions
    )


    show_monthly_report(
        transactions
    )


    show_highest_category(
        transactions
    )


    show_transaction_statistics(
        transactions
    )


    print(
        "\n"
        + "#" * 70
    )

    print(
        "#              END OF FINANCIAL REPORT             #"
    )

    print(
        "#" * 70
    )


# =====================================================
# ADD TRANSACTION
# =====================================================

def add_transaction(
    transactions
):

    print(
        "\n========== ADD TRANSACTION =========="
    )


    title =
        input(
            "Title: "
        ).strip()


    category =
        input(
            "Category: "
        ).strip()


    transaction_type =
        input(
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

        amount =
            float(
                input(
                    "Amount: ₹"
                )
            )

    except ValueError:

        print(
            "\nInvalid amount."
        )

        return


    date =
        input(
            "Date (YYYY-MM-DD): "
        ).strip()


    try:

        datetime.strptime(
            date,
            "%Y-%m-%d"
        )

    except ValueError:

        print(
            "\nInvalid date format."
        )

        return


    new_id =
        max(
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
# VIEW TRANSACTIONS
# =====================================================

def view_transactions(
    transactions
):

    print(
        "\n"
        + "=" * 80
    )

    print(
        "                    TRANSACTIONS"
    )

    print(
        "=" * 80
    )


    if not transactions:

        print(
            "\nNo transactions found."
        )

        return


    for transaction in transactions:

        print(
            f"\nID       : "
            f"{transaction['id']}"
        )

        print(
            f"Title    : "
            f"{transaction['title']}"
        )

        print(
            f"Category : "
            f"{transaction['category']}"
        )

        print(
            f"Type     : "
            f"{transaction['type']}"
        )

        print(
            f"Amount   : "
            f"{currency(transaction['amount'])}"
        )

        print(
            f"Date     : "
            f"{transaction['date']}"
        )

        print(
            "-" * 80
        )


# =====================================================
# MENU
# =====================================================

def show_menu():

    print(
        "\n\n"
        + "=" * 60
    )

    print(
        "             PERSONAL FINANCE MANAGER"
    )

    print(
        "=" * 60
    )

    print(
        "1. Dashboard"
    )

    print(
        "2. Add Transaction"
    )

    print(
        "3. View Transactions"
    )

    print(
        "4. Expense Category Report"
    )

    print(
        "5. Monthly Report"
    )

    print(
        "6. Highest Expense Category"
    )

    print(
        "7. Transaction Statistics"
    )

    print(
        "8. Complete Financial Report"
    )

    print(
        "9. Save Data"
    )

    print(
        "10. Exit"
    )

    print(
        "=" * 60
    )


# =====================================================
# MAIN
# =====================================================

def main():

    transactions =
        load_transactions()


    print(
        "\nPersonal Finance Manager started."
    )


    while True:

        show_menu()


        choice =
            input(
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

            show_highest_category(
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
                "\nData saved."
            )

            print(
                "Thank you for using Personal Finance Manager!"
            )

            break


        else:

            print(
                "\nInvalid choice. Try again."
            )


# =====================================================
# PROGRAM START
# =====================================================

if __name__ == "__main__":

    main()