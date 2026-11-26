import csv
import os

DATA_FILE = "expenses.csv"


def load_expenses():
    expenses = []

    if not os.path.exists(DATA_FILE):
        return expenses

    try:
        with open(DATA_FILE, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                if row.get("Date") and row.get("Category") and row.get("Amount"):
                    expenses.append({
                        "Date": row["Date"],
                        "Category": row["Category"],
                        "Amount": float(row["Amount"]),
                        "Description": row.get("Description", "")
                    })

    except (OSError, ValueError, csv.Error):
        print("There was a problem reading the expense file.")

    return expenses


def save_expenses(expenses):
    try:
        with open(DATA_FILE, "w", newline="", encoding="utf-8") as file:
            fieldnames = ["Date", "Category", "Amount", "Description"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            writer.writeheader()

            for expense in expenses:
                writer.writerow({
                    "Date": expense["Date"],
                    "Category": expense["Category"],
                    "Amount": expense["Amount"],
                    "Description": expense["Description"]
                })

    except OSError:
        print("Could not save the expense data.")


def get_valid_amount():
    while True:
        try:
            amount = float(input("Enter amount (Rs.): "))

            if amount <= 0:
                print("Amount must be greater than 0.")
            else:
                return amount

        except ValueError:
            print("Please enter a valid number.")


def add_expense(expenses):
    print("\n--- Add Expense ---")

    date = input("Enter date (DD-MM-YYYY): ").strip()
    category = input("Enter category: ").strip()
    amount = get_valid_amount()
    description = input("Enter description: ").strip()

    if category == "":
        category = "Other"

    expense = {
        "Date": date,
        "Category": category,
        "Amount": amount,
        "Description": description
    }

    expenses.append(expense)
    save_expenses(expenses)

    print("Expense added successfully.")


def show_all_expenses(expenses):
    print("\n--- All Expenses ---")

    if len(expenses) == 0:
        print("No expenses found.")
        return

    print("-" * 70)
    print("{:<15} {:<15} {:>12}  {:<20}".format(
        "Date", "Category", "Amount", "Description"
    ))
    print("-" * 70)

    for expense in expenses:
        print("{:<15} {:<15} {:>12.2f}  {:<20}".format(
            expense["Date"],
            expense["Category"],
            expense["Amount"],
            expense["Description"]
        ))

    print("-" * 70)


def calculate_total(expenses):
    total = 0

    for expense in expenses:
        total = total + expense["Amount"]

    return total


def category_summary(expenses):
    summary = {}

    for expense in expenses:
        category = expense["Category"]
        amount = expense["Amount"]

        if category in summary:
            summary[category] = summary[category] + amount
        else:
            summary[category] = amount

    return summary


def show_summary(expenses):
    print("\n--- Expense Summary ---")

    if len(expenses) == 0:
        print("No expenses available.")
        return

    total = calculate_total(expenses)
    summary = category_summary(expenses)

    print("Total spending: Rs. {:.2f}".format(total))
    print("\nCategory-wise spending:")

    for category in summary:
        print("{}: Rs. {:.2f}".format(category, summary[category]))


def show_budget_status(expenses):
    print("\n--- Budget Status ---")

    if len(expenses) == 0:
        print("No expenses available.")
        return

    while True:
        try:
            budget = float(input("Enter your budget (Rs.): "))

            if budget <= 0:
                print("Budget must be greater than 0.")
            else:
                break

        except ValueError:
            print("Please enter a valid number.")

    total = calculate_total(expenses)

    print("Total spending: Rs. {:.2f}".format(total))
    print("Budget: Rs. {:.2f}".format(budget))

    if total < budget:
        remaining = budget - total
        print("You are within budget.")
        print("Remaining budget: Rs. {:.2f}".format(remaining))

    elif total == budget:
        print("You have used your complete budget.")

    else:
        extra = total - budget
        print("You are over budget.")
        print("Amount over budget: Rs. {:.2f}".format(extra))


def highest_category(expenses):
    print("\n--- Highest Spending Category ---")

    if len(expenses) == 0:
        print("No expenses available.")
        return

    summary = category_summary(expenses)

    highest = ""
    highest_amount = 0

    for category in summary:
        if summary[category] > highest_amount:
            highest = category
            highest_amount = summary[category]

    print("Highest spending category:", highest)
    print("Amount spent: Rs. {:.2f}".format(highest_amount))


def show_menu():
    print("\n==============================")
    print(" PERSONAL EXPENSE TRACKER")
    print("==============================")
    print("1. Add Expense")
    print("2. View All Expenses")
    print("3. Show Expense Summary")
    print("4. Check Budget")
    print("5. Highest Spending Category")
    print("6. Exit")
    print("==============================")


def main():
    expenses = load_expenses()

    while True:
        show_menu()

        choice = input("Enter your choice (1-6): ").strip()

        if choice == "1":
            add_expense(expenses)

        elif choice == "2":
            show_all_expenses(expenses)

        elif choice == "3":
            show_summary(expenses)

        elif choice == "4":
            show_budget_status(expenses)

        elif choice == "5":
            highest_category(expenses)

        elif choice == "6":
            print("Thank you for using Personal Expense Tracker.")
            break

        else:
            print("Invalid choice. Please enter a number from 1 to 6.")


if __name__ == "__main__":
    main()
