# DONE apart from exception handling
import json
from datetime import date
from typing import Literal
from pathlib import Path

# make directory to store app data
APP_DIR = Path.home() / "ExpenseTracker"
DATA_DIR = APP_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

EXPENSE_FILE = DATA_DIR / "expenses.json"

categories = ["Food", "Transport", "Shopping", "Entertainment", "Bills", "Health", "Education", "Groceries", "Rent", "Travel", "Savings", "Gifts", "Subscriptions", "Personal Care", "Miscellaneous"]

# to read the json file
def load_file():

    if not EXPENSE_FILE.exists():
        return[]
    else:
        with open(EXPENSE_FILE, 'r') as f:
            return json.load(f)
        
# to save the expenses into the json file
def save_expenses(expenses):
    with open(EXPENSE_FILE, 'w') as f:
        json.dump(expenses, f, indent=2)

# To prompt user to select an option and execute it
def show_options():
    print("""Hello User! Select one of the numbers below to execute the corresponding option: 

1. Enter expense(s)
2. Display all expenses
3. Filter expenses by date
4. Filter expenses by category
5. Show expense report for a month
6. Exit""")

# to filter by either date or category. add parameter while using it in show options
def filter_by_parameter(parameter: Literal["date", "category"]):
    expenses = load_file()
    total_expense_for_parameter = 0

    if parameter == "date":
        req_parameter = input("Enter the date for which total expense is required in DD-MM-YYYY format: ")

    elif parameter == "category":
        display_categories()
        req_parameter = input("Enter the category for which total expense is required: ").capitalize()

        if req_parameter not in categories:
            print("Please enter a valid category!\n")
            return
        
    for expense in expenses:
        if expense[parameter] == req_parameter:
            total_expense_for_parameter += expense["amount"]
    
    if total_expense_for_parameter == 0:
        print(f"No expense found for the {parameter} '{req_parameter}'! (Or the {parameter} '{req_parameter}' is not valid.)\n")
    else:

        print(f"The total expense for the {parameter} {req_parameter} is {total_expense_for_parameter}\n")

# not for the user but req in the program as it might be repititve
def display_categories():
    print(''' The expenditure categories are: 
1. Food
2. Transport
3. Shopping
4. Entertainment
5. Bills
6. Health
7. Education
8. Groceries
9. Rent
10. Travel
11. Savings
12. Gifts
13. Subscriptions
14. Personal Care
15. Miscellaneous\n''')

# To prompt the user to enter an expenditure amount, the category of the expense and any remarks for that expense and store the expense by category
def ask_expense():
    more = 'y'
    while more.lower() == 'y':
        try:
            amount = float(input("Enter amount spent: "))
            if amount <= 0:
                print("Amount should be a positive number!\n")
                return
        except ValueError:
                print("Amount should be a positive number!\n")
                return

        display_categories()

        while True:
            category = input("Enter the category of the expense from the above options: ").capitalize()
            if category not in categories:
                print("Please enter a valid category!\n")
            else:
                break

        remarks = input("Enter remarks for this expenditure: ")
        current_date = date.today().strftime("%d-%m-%Y")
        data = {"category": category.capitalize(), "amount": amount, "remarks": remarks, "date": current_date}

        expenses = load_file()
        expenses.append(data)
        save_expenses(expenses)
        
        print("Expense recorded succeefully\n")
        while True:
            more = input("Add more expenses? [y/n]")
            if more.lower() in ('y','n'):
                print()
                break
            else:
                print("Please enter a valid answer [y/n]\n")

# shows the total monthly expense along with the total expense for each category in the month
def show_monthly_expense_report():
    month = input("Enter the month and year in MM-YYYY format to get the expense report for the month: ")
    print()
    expenses = load_file()
    total_expense_for_month = 0

    category_total = {category: 0 for category in categories}

    for expense in expenses:
        if expense["date"].endswith(month):
            total_expense_for_month += expense["amount"]

            for category in categories:
                if category == expense["category"]:
                    category_total[category] += expense["amount"]
    
    print(f"The total expenditure of the month is Rs. {total_expense_for_month}\n")

    for category in category_total:
        print(f"Rs. {category_total[category]} was spent on {category}")
    print()

# displays all the recorded expenses and the total of the expenses
def show_all_expenses():
    expenses = load_file()
    expenses.reverse()
    
    for expense in expenses:
        print(f"{expense["amount"]}, spent for {expense["category"]} on {expense["date"]}.\nRemark: {expense["remarks"]}\n")
    print()

if __name__ == "__main__":
    while True:
        
        try:
            show_options()
            selected_option = int(input("Enter the option: "))
            print()

            if selected_option == 1:
                ask_expense()

            elif selected_option == 2:
                show_all_expenses()

            elif selected_option == 3:
                filter_by_parameter("date")

            elif selected_option == 4:
                filter_by_parameter("category")

            elif selected_option == 5:
                show_monthly_expense_report()

            elif selected_option == 6:
                break
            elif selected_option not in range(1,7):
                print("Please enter a valid option!\n")

        except ValueError:
            print("\nPlease enter a valid option!\n")