import json

# Functions for saving/loading data
def save_data(filename, data):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

def load_data(filename):
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

# Functions for adding entries
def add_income(incomes):
    source = input("Enter income source: ")
    while True:
        try:
            amount = float(input("Enter income amount: "))
            break
        except ValueError:
            print("Please enter a valid number for amount.")
    incomes.append({"source": source, "amount": amount})
    print(f"Added income: {source} - ${amount:.2f}")

def add_expense(expenses):
    category = input("Enter expense category: ")
    while True:
        try:
            amount = float(input("Enter expense amount: "))
            break
        except ValueError:
            print("Please enter a valid number for amount.")
    expenses.append({"category": category, "amount": amount})
    print(f"Added expense: {category} - ${amount:.2f}")

# Function to calculate balance
def calculate_balance(incomes, expenses):
    total_income = sum(item["amount"] for item in incomes)
    total_expense = sum(item["amount"] for item in expenses)
    balance = total_income - total_expense
    print("\n----- BALANCE SUMMARY -----")
    print(f"Total Income:  ${total_income:.2f}")
    print(f"Total Expenses: ${total_expense:.2f}")
    print(f"Balance:       ${balance:.2f}")
    print("---------------------------")

# Main menu function
def show_budget():
    incomes = load_data("incomes.json")
    expenses = load_data("expenses.json")

    while True:
        print("\n===== BUDGET APP MENU =====")
        print("1. Add Income")
        print("2. Add Expense")
        print("3. View Balance")
        print("4. Quit")
        choice = input("Choose an option: ")

        if choice == "1":
            add_income(incomes)
            save_data("incomes.json", incomes)
        elif choice == "2":
            add_expense(expenses)
            save_data("expenses.json", expenses)
        elif choice == "3":
            calculate_balance(incomes, expenses)
        elif choice == "4":
            print("Exiting budget app. Goodbye!")
            break
        else:
            print("Invalid option, try again.")

# Run the app if executed directly
if __name__ == "__main__":
    show_budget()