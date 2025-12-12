from pathlib import Path
import json
from datetime import datetime

DEBTS_FILE = Path("data/debts.json")


class Debt:
    """Represents a single debt account."""

    def __init__(self, name, total_amount, current_balance=None):
        self.name = name
        self.total_amount = total_amount
        self.current_balance = (
            current_balance if current_balance is not None else total_amount
        )

    # --------------------
    #   Calculated Fields
    # --------------------

    @property
    def paid_amount(self):
        return self.total_amount - self.current_balance

    @property
    def progress(self):
        if self.total_amount == 0:
            return 0
        return round((self.paid_amount / self.total_amount) * 100, 2)

    @property
    def is_paid_off(self):
        return self.current_balance <= 0

    # --------------------
    #   Update Methods
    # --------------------

    def make_payment(self, amount):
        self.current_balance = max(0, self.current_balance - amount)

    # --------------------
    #   Serialization
    # --------------------

    def to_dict(self):
        return {
            "name": self.name,
            "total_amount": self.total_amount,
            "current_balance": self.current_balance,
        }

    @staticmethod
    def from_dict(data):
        return Debt(
            name=data["name"],
            total_amount=data["total_amount"],
            current_balance=data.get("current_balance"),
        )


class DebtManager:
    """Handles storage and updates for all debts."""

    def __init__(self):
        self.debts = self.load_debts()

    # --------------------
    #   Storage
    # --------------------

    def load_debts(self):
        if not DEBTS_FILE.exists():
            return []
        with open(DEBTS_FILE, "r") as f:
            data = json.load(f)
        return [Debt.from_dict(d) for d in data]

    def save_debts(self):
        DEBTS_FILE.parent.mkdir(exist_ok=True)
        with open(DEBTS_FILE, "w") as f:
            json.dump([d.to_dict() for d in self.debts], f, indent=4)

    # --------------------
    #   Debt Control
    # --------------------

    def add_debt(self, name, total_amount):
        debt = Debt(name, total_amount)
        self.debts.append(debt)
        self.save_debts()

    def make_payment(self, name, amount):
        for debt in self.debts:
            if debt.name.lower() == name.lower():
                debt.make_payment(amount)
                self.save_debts()
                return True
        return False

    def list_debts(self):
        return [
            {
                "name": d.name,
                "total": d.total_amount,
                "balance": d.current_balance,
                "paid": d.paid_amount,
                "progress": d.progress,
                "status": "PAID OFF 🎉" if d.is_paid_off else "IN PROGRESS",
            }
            for d in self.debts
        ]


# --------------------
#   CLI DISPLAY
# --------------------

def show_debts():
    manager = DebtManager()
    debts = manager.list_debts()

    print("\n===== DEBTS =====")

    if not debts:
        print("No debts added yet.")
        return

    for d in debts:
        print(
            f"- {d['name']}: "
            f"${d['balance']:.2f} remaining "
            f"({d['progress']}% paid) "
            f"[{d['status']}]"
        )