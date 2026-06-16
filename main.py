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
    
    with open(EXPENSE_FILE, 'r') as f:
        total_expense_for_parameter = 0
        if parameter == "date":
            i = 3
            req_parameter = input("Enter the date for which expenditure is required in DD-MM-YYYY format: ")
        elif parameter == "category":
            i = 0
            display_categories()
            category = input("Enter the required category for displaying expenses: ")
            req_parameter = category.capitalize()

        data = json.load(f)
        if data[i] == req_parameter:
            total_expense_for_parameter += data[1]
            print(f"{data}")

    print(f"The total expense for the {parameter} {req_parameter} is {total_expense_for_parameter}")
    print()

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
15. Miscellaneous''')

# To prompt the user to enter an expenditure amount, the category of the expense and any remarks for that expense and store the expense by category
def ask_expense():
    more = 'y'
    while more.lower() == 'y':
        try:
            amount = int(input("Enter amount spent: "))
            if amount <= 0:
                print("Amount should be a natural number!\n")
                return
        except ValueError:
            print("Amount should be a natural number!\n")
            return

        display_categories()
        category = input("Enter the category of the expense from the above options: ").capitalize()
        remarks = input("Enter remarks for this expenditure: ")
        current_date = date.today().strftime("%d-%m-%Y")
        data = [category.capitalize(), amount, remarks, current_date]

        with open(EXPENSE_FILE, "a") as f:
            json.dump(data, f)
        print("Expense recorded succeefully")

        more = input("Add more expenses? [y/n]")
    print()

# shows the total monthly expense along with the total expense for each category in the month
def show_monthly_expense_report():
    month = input("Enter the month and year in MM-YYYY format to get the expense report for the month: ")
    with open(EXPENSE_FILE, 'r') as f:
        total_expense_for_month = 0
        category_total = {"Food":0,"Transport":0,"Shopping":0,"Entertainment":0,"Bills":0,"Health":0,"Education":0,"Groceries":0,"Rent":0,"Travel":0,"Savings":0,"Gifts":0,"Subscriptions":0,"Personal Care":0,"Miscellaneous":0}

        data = json.load(f)
        if data[3].endswith(month):
            total_expense_for_month += data[1]
            category_total[data[0]] += data[1]
    
    print(f"The total expenditure of the month is Rs. {total_expense_for_month} ")
    print(category_total)
    print()

# displays all the recorded expenses and the total of the expenses
def show_all_expenses():
    with open(EXPENSE_FILE, 'r') as f:
        data = json.load(f)
        print(data)
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
            elif selected_option not in (1,7):
                print("Please enter a valid option!\n")

        except ValueError:
            print("Please enter a valid option!\n")