import json
import os


GOALS_FILE = "goals.json"


# =========================
# LOAD JSON
# =========================

def load_goals():

    if not os.path.exists(GOALS_FILE):
        return []

    try:

        with open(GOALS_FILE, "r") as file:
            return json.load(file)

    except (json.JSONDecodeError, OSError):

        return []


# =========================
# SAVE JSON
# =========================

def save_goals(goals):

    with open(GOALS_FILE, "w") as file:

        json.dump(
            goals,
            file,
            indent=4
        )


# =========================
# CREATE GOAL
# =========================

def create_goal():

    goals = load_goals()

    print("\n========== CREATE FINANCIAL GOAL ==========")

    name = input(
        "Enter goal name: "
    ).strip()

    if not name:

        print("\nGoal name cannot be empty.")

        return


    try:

        target = float(
            input("Enter target amount: ₹")
        )

    except ValueError:

        print("\nInvalid amount.")

        return


    if target <= 0:

        print(
            "\nTarget amount must be greater than 0."
        )

        return


    goal_id = (
        max(
            [goal["id"] for goal in goals],
            default=0
        ) + 1
    )


    goal = {

        "id": goal_id,

        "name": name,

        "target": target,

        "saved": 0,

    }


    goals.append(goal)

    save_goals(goals)


    print(
        f"\nGoal '{name}' created successfully."
    )

    print(
        f"Target: ₹{target:,.2f}"
    )


# =========================
# ADD SAVINGS
# =========================

def add_savings():

    goals = load_goals()

    if not goals:

        print(
            "\nNo financial goals found."
        )

        return


    view_goals()


    try:

        goal_id = int(
            input("\nEnter Goal ID: ")
        )

    except ValueError:

        print("\nInvalid Goal ID.")

        return


    goal = next(
        (
            goal
            for goal in goals
            if goal["id"] == goal_id
        ),
        None
    )


    if goal is None:

        print("\nGoal not found.")

        return


    if goal["saved"] >= goal["target"]:

        print(
            "\nThis goal has already been completed."
        )

        return


    try:

        amount = float(
            input(
                "Enter amount to add: ₹"
            )
        )

    except ValueError:

        print("\nInvalid amount.")

        return


    if amount <= 0:

        print(
            "\nAmount must be greater than 0."
        )

        return


    remaining = (
        goal["target"]
        - goal["saved"]
    )


    if amount > remaining:

        print(
            f"\nYou only need "
            f"₹{remaining:,.2f} "
            f"to complete this goal."
        )

        amount = remaining


    goal["saved"] += amount

    save_goals(goals)


    print(
        f"\n₹{amount:,.2f} added successfully."
    )


    if goal["saved"] >= goal["target"]:

        print(
            "\nCongratulations!"
        )

        print(
            f"Goal '{goal['name']}' completed."
        )


# =========================
# PROGRESS BAR
# =========================

def progress_bar(
    percentage,
    width=30
):

    filled = int(
        width * percentage / 100
    )

    empty = width - filled

    return (
        "["
        + "#" * filled
        + "-" * empty
        + "]"
    )


# =========================
# VIEW GOALS
# =========================

def view_goals():

    goals = load_goals()

    if not goals:

        print(
            "\nNo financial goals found."
        )

        return


    print(
        "\n========== FINANCIAL GOALS =========="
    )


    for goal in goals:

        target = float(
            goal["target"]
        )

        saved = float(
            goal["saved"]
        )


        remaining = max(
            target - saved,
            0
        )


        percentage = (
            saved / target
        ) * 100


        percentage = min(
            percentage,
            100
        )


        print(
            "\n----------------------------------------"
        )


        print(
            f"ID       : {goal['id']}"
        )

        print(
            f"Goal     : {goal['name']}"
        )

        print(
            f"Target   : ₹{target:,.2f}"
        )

        print(
            f"Saved    : ₹{saved:,.2f}"
        )

        print(
            f"Remaining: ₹{remaining:,.2f}"
        )

        print(
            f"Progress : {percentage:.1f}%"
        )


        print(
            progress_bar(percentage)
        )


        if percentage >= 100:

            print(
                "Status   : COMPLETED"
            )

        elif percentage >= 75:

            print(
                "Status   : Almost There!"
            )

        elif percentage >= 50:

            print(
                "Status   : Good Progress"
            )

        elif percentage > 0:

            print(
                "Status   : Started"
            )

        else:

            print(
                "Status   : Not Started"
            )


    print(
        "\n----------------------------------------"
    )


# =========================
# DELETE GOAL
# =========================

def delete_goal():

    goals = load_goals()

    if not goals:

        print(
            "\nNo goals found."
        )

        return


    view_goals()


    try:

        goal_id = int(
            input(
                "\nEnter Goal ID to delete: "
            )
        )

    except ValueError:

        print("\nInvalid Goal ID.")

        return


    goal = next(
        (
            goal
            for goal in goals
            if goal["id"] == goal_id
        ),
        None
    )


    if goal is None:

        print("\nGoal not found.")

        return


    print(
        f"\nGoal selected: {goal['name']}"
    )


    confirmation = input(
        "Delete this goal? (Y/N): "
    ).strip().lower()


    if confirmation != "y":

        print(
            "\nDeletion cancelled."
        )

        return


    goals.remove(goal)

    save_goals(goals)


    print(
        "\nGoal deleted successfully."
    )


# =========================
# GOAL SUMMARY
# =========================

def goal_summary():

    goals = load_goals()

    if not goals:

        print(
            "\nNo financial goals found."
        )

        return


    total_target = sum(
        float(goal["target"])
        for goal in goals
    )


    total_saved = sum(
        float(goal["saved"])
        for goal in goals
    )


    total_remaining = max(
        total_target - total_saved,
        0
    )


    overall_progress = (
        total_saved / total_target * 100
        if total_target > 0
        else 0
    )


    print(
        "\n========== GOAL SUMMARY =========="
    )


    print(
        f"\nTotal Target    : "
        f"₹{total_target:,.2f}"
    )


    print(
        f"Total Saved     : "
        f"₹{total_saved:,.2f}"
    )


    print(
        f"Total Remaining : "
        f"₹{total_remaining:,.2f}"
    )


    print(
        f"Overall Progress: "
        f"{overall_progress:.1f}%"
    )


    print(
        "\n"
        + progress_bar(
            min(overall_progress, 100)
        )
    )


# =========================
# MENU
# =========================

def menu():

    while True:

        print(
            "\n\n========== PERSONAL FINANCE =========="
        )

        print(
            "1. Create Financial Goal"
        )

        print(
            "2. View Goals"
        )

        print(
            "3. Add Savings"
        )

        print(
            "4. Goal Summary"
        )

        print(
            "5. Delete Goal"
        )

        print(
            "6. Exit"
        )


        choice = input(
            "\nEnter Choice: "
        )


        if choice == "1":

            create_goal()


        elif choice == "2":

            view_goals()


        elif choice == "3":

            add_savings()


        elif choice == "4":

            goal_summary()


        elif choice == "5":

            delete_goal()


        elif choice == "6":

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