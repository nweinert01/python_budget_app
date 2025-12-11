import json
from pathlib import Path

INCOMES_FILE = Path("data/incomes.json")
EXPENSES_FILE = Path("data/expenses.json")

class BudgetManager:
    def __init__(self):
        self.incomes = self.load_data(INCOMES_FILE)
        self.expenses = self.load_data(EXPENSES_FILE)

    # ----------------------------
    #   Load / Save
    # ----------------------------
    @staticmethod
    def load_data(filename):
        try:
            with open(filename, "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    @staticmethod
    def save_data(filename, data):
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)

    # ----------------------------
    #   Budget actions
    # ----------------------------
    def add_income(self, source=None, amount=None):
        if source is None:
            source = input("Enter income source: ")
        if amount is None:
            while True:
                try:
                    amount = float(input("Enter income amount: "))
                    break
                except ValueError:
                    print("Please enter a valid number for amount.")
        self.incomes.append({"source": source, "amount": amount})
        self.save_data(INCOMES_FILE, self.incomes)
        print(f"Added income: {source} - ${amount:.2f}")

    def add_expense(self, category=None, amount=None):
        if category is None:
            category = input("Enter expense category: ")
        if amount is None:
            while True:
                try:
                    amount = float(input("Enter expense amount: "))
                    break
                except ValueError:
                    print("Please enter a valid number for amount.")
        self.expenses.append({"category": category, "amount": amount})
        self.save_data(EXPENSES_FILE, self.expenses)
        print(f"Added expense: {category} - ${amount:.2f}")

    def view_balance(self):
        total_income = sum(item["amount"] for item in self.incomes)
        total_expense = sum(item["amount"] for item in self.expenses)
        balance = total_income - total_expense
        print("\n----- BALANCE SUMMARY -----")
        print(f"Total Income:  ${total_income:.2f}")
        print(f"Total Expenses: ${total_expense:.2f}")
        print(f"Balance:       ${balance:.2f}")
        print("---------------------------")
