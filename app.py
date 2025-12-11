from budget import BudgetManager
from goals import GoalManager
from debts import show_debts

def main_menu():
    budget_manager = BudgetManager()
    goal_manager = GoalManager()

    while True:
        print("\n===== BUDGET APP MENU =====")
        print("1. Budget")
        print("2. Goals")
        print("3. Debts")
        print("4. Quit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            budget_menu(budget_manager)
        elif choice == "2":
            goals_menu(goal_manager)
        elif choice == "3":
            show_debts()
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

def budget_menu(manager):
    while True:
        print("\n--- Budget Menu ---")
        print("1. Add Income")
        print("2. Add Expense")
        print("3. View Balance")
        print("4. Back to Main Menu")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            manager.add_income()
        elif choice == "2":
            manager.add_expense()
        elif choice == "3":
            manager.view_balance()
        elif choice == "4":
            break
        else:
            print("Invalid choice. Try again.")

def goals_menu(manager):
    while True:
        print("\n--- Goals Menu ---")
        print("1. View Goals")
        print("2. Add Goal")
        print("3. Update Progress")
        print("4. Back to Main Menu")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            show_goals(manager)
        elif choice == "2":
            name = input("Goal name: ")
            target = float(input("Target amount: "))
            due = input("Due date (YYYY-MM-DD or leave blank): ")
            due = due if due else None
            manager.add_goal(name, target, due)
        elif choice == "3":
            name = input("Goal name to update: ")
            amount = float(input("Amount added: "))
            if manager.update_goal(name, amount):
                print("Goal updated!")
            else:
                print("Goal not found.")
        elif choice == "4":
            break
        else:
            print("Invalid choice. Try again.")

# Keep your existing show_goals() function as-is

if __name__ == "__main__":
    print("\n--- Welcome to Your Budget App ---")
    main_menu()