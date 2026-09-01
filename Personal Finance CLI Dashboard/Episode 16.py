import csv
import json
import os
from collections import defaultdict


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
# NORMALIZE TYPE
# =========================

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


# =========================
# EXPORT ALL TRANSACTIONS
# =========================

def export_all_transactions():

    transactions = load_transactions()

    if not transactions:

        print("\nNo transactions found.")

        return


    filename = "all_transactions.csv"


    with open(
        filename,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)


        writer.writerow([
            "Date",
            "Title",
            "Category",
            "Type",
            "Amount"
        ])


        for transaction in transactions:

            writer.writerow([

                transaction.get(
                    "date",
                    ""
                ),

                transaction.get(
                    "title",
                    ""
                ),

                transaction.get(
                    "category",
                    "Other"
                ),

                get_type(
                    transaction
                ).title(),

                transaction.get(
                    "amount",
                    0
                )
            ])


    print(
        f"\nReport exported successfully: "
        f"{filename}"
    )


# =========================
# MONTHLY TRANSACTIONS
# =========================

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


# =========================
# MONTHLY SUMMARY
# =========================

def calculate_summary(
    transactions
):

    income = 0
    expense = 0


    categories = defaultdict(float)


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

            expense += amount


            category = (
                transaction.get(
                    "category",
                    "Other"
                )
            )


            categories[category] += (
                amount
            )


    savings = income - expense


    savings_rate = (

        savings / income * 100

        if income > 0

        else 0

    )


    return {

        "income": income,

        "expense": expense,

        "savings": savings,

        "savings_rate":
            savings_rate,

        "categories":
            categories

    }


# =========================
# EXPORT MONTHLY REPORT
# =========================

def export_monthly_report():

    transactions = load_transactions()


    if not transactions:

        print(
            "\nNo transactions found."
        )

        return


    month = input(
        "\nEnter Month (YYYY-MM): "
    ).strip()


    monthly_transactions = (
        get_month_transactions(
            transactions,
            month
        )
    )


    if not monthly_transactions:

        print(
            "\nNo transactions found "
            "for this month."
        )

        return


    summary = calculate_summary(
        monthly_transactions
    )


    filename = (
        f"financial_report_{month}.csv"
    )


    with open(
        filename,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)


        # =========================
        # REPORT TITLE
        # =========================

        writer.writerow([
            "PERSONAL FINANCE REPORT"
        ])

        writer.writerow([
            "Month",
            month
        ])

        writer.writerow([])


        # =========================
        # SUMMARY
        # =========================

        writer.writerow([
            "SUMMARY"
        ])


        writer.writerow([
            "Total Income",
            summary["income"]
        ])


        writer.writerow([
            "Total Expenses",
            summary["expense"]
        ])


        writer.writerow([
            "Net Savings",
            summary["savings"]
        ])


        writer.writerow([
            "Savings Rate",
            f"{summary['savings_rate']:.2f}%"
        ])


        writer.writerow([])


        # =========================
        # CATEGORY BREAKDOWN
        # =========================

        writer.writerow([
            "CATEGORY EXPENSES"
        ])


        writer.writerow([
            "Category",
            "Amount",
            "Percentage"
        ])


        total_expense = (
            summary["expense"]
        )


        for category, amount in (
            sorted(
                summary[
                    "categories"
                ].items(),
                key=lambda item:
                    item[1],
                reverse=True
            )
        ):

            percentage = (

                amount /
                total_expense *
                100

                if total_expense > 0

                else 0

            )


            writer.writerow([

                category,

                amount,

                f"{percentage:.2f}%"

            ])


        writer.writerow([])


        # =========================
        # TRANSACTIONS
        # =========================

        writer.writerow([
            "TRANSACTIONS"
        ])


        writer.writerow([
            "Date",
            "Title",
            "Category",
            "Type",
            "Amount"
        ])


        for transaction in (
            monthly_transactions
        ):

            writer.writerow([

                transaction.get(
                    "date",
                    ""
                ),

                transaction.get(
                    "title",
                    ""
                ),

                transaction.get(
                    "category",
                    "Other"
                ),

                get_type(
                    transaction
                ).title(),

                transaction.get(
                    "amount",
                    0
                )
            ])


    print(
        f"\nMonthly report exported: "
        f"{filename}"
    )


# =========================
# PREVIEW REPORT
# =========================

def preview_monthly_report():

    transactions = (
        load_transactions()
    )


    if not transactions:

        print(
            "\nNo transactions found."
        )

        return


    month = input(
        "\nEnter Month (YYYY-MM): "
    ).strip()


    monthly_transactions = (
        get_month_transactions(
            transactions,
            month
        )
    )


    if not monthly_transactions:

        print(
            "\nNo transactions found "
            "for this month."
        )

        return


    summary = calculate_summary(
        monthly_transactions
    )


    print(
        "\n========== MONTHLY REPORT =========="
    )


    print(
        f"Month          : {month}"
    )


    print(
        f"Total Income   : "
        f"₹{summary['income']:,.2f}"
    )


    print(
        f"Total Expenses : "
        f"₹{summary['expense']:,.2f}"
    )


    print(
        f"Net Savings    : "
        f"₹{summary['savings']:,.2f}"
    )


    print(
        f"Savings Rate   : "
        f"{summary['savings_rate']:.2f}%"
    )


    print(
        "\n========== CATEGORY EXPENSES =========="
    )


    for category, amount in (
        sorted(
            summary[
                "categories"
            ].items(),
            key=lambda item:
                item[1],
            reverse=True
        )
    ):

        percentage = (

            amount /
            summary["expense"] *
            100

            if summary[
                "expense"
            ] > 0

            else 0

        )


        print(
            f"{category:<20}"
            f"₹{amount:>10,.2f}"
            f"   {percentage:>6.2f}%"
        )


# =========================
# MENU
# =========================

def menu():

    while True:

        print(
            "\n\n========== FINANCIAL REPORT EXPORT =========="
        )


        print(
            "1. Export All Transactions"
        )

        print(
            "2. Export Monthly Report"
        )

        print(
            "3. Preview Monthly Report"
        )

        print(
            "4. Exit"
        )


        choice = input(
            "\nEnter Choice: "
        ).strip()


        if choice == "1":

            export_all_transactions()


        elif choice == "2":

            export_monthly_report()


        elif choice == "3":

            preview_monthly_report()


        elif choice == "4":

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