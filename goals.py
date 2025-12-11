from datetime import datetime
import json
from pathlib import Path

GOALS_FILE = Path("data/goals.json")


class Goal:
    """Represents a single financial goal."""

    def __init__(self, name, target_amount, current_amount=0, due_date=None):
        self.name = name
        self.target_amount = target_amount
        self.current_amount = current_amount

        # Convert due_date string ("YYYY-MM-DD") to datetime object
        if isinstance(due_date, str):
            self.due_date = datetime.strptime(due_date, "%Y-%m-%d")
        else:
            self.due_date = due_date

    # --------------------
    #   Calculated Fields
    # --------------------

    @property
    def remaining(self):
        return max(0, self.target_amount - self.current_amount)

    @property
    def progress(self):
        if self.target_amount == 0:
            return 0
        return round((self.current_amount / self.target_amount) * 100, 2)

    @property
    def days_left(self):
        if not self.due_date:
            return None
        return (self.due_date - datetime.now()).days

    @property
    def overdue(self):
        return self.days_left is not None and self.days_left < 0

    # --------------------
    #   Update Methods
    # --------------------

    def add_progress(self, amount):
        """Add to current progress toward the goal."""
        self.current_amount += amount

    # --------------------
    #   Serialization
    # --------------------

    def to_dict(self):
        """Convert goal to a dict for JSON saving."""
        return {
            "name": self.name,
            "target_amount": self.target_amount,
            "current_amount": self.current_amount,
            "due_date": self.due_date.strftime("%Y-%m-%d") if self.due_date else None,
        }

    @staticmethod
    def from_dict(data):
        """Recreate a Goal object from a saved JSON dict."""
        return Goal(
            name=data["name"],
            target_amount=data["target_amount"],
            current_amount=data.get("current_amount", 0),
            due_date=data.get("due_date"),
        )


class GoalManager:
    """Handles storage, updates, and retrieval of all user goals."""

    def __init__(self):
        self.goals = self.load_goals()

    # --------------------
    #   Storage Handling
    # --------------------

    def load_goals(self):
        if not GOALS_FILE.exists():
            return []
        with open(GOALS_FILE, "r") as f:
            data = json.load(f)
        return [Goal.from_dict(g) for g in data]

    def save_goals(self):
        with open(GOALS_FILE, "w") as f:
            json.dump([g.to_dict() for g in self.goals], f, indent=4)

    # --------------------
    #   Goal Control
    # --------------------

    def add_goal(self, name, target_amount, due_date=None):
        """Create a new financial goal."""
        goal = Goal(name, target_amount, due_date=due_date)
        self.goals.append(goal)
        self.save_goals()

    def update_goal(self, name, amount):
        """Add progress to an existing goal."""
        for goal in self.goals:
            if goal.name.lower() == name.lower():
                goal.add_progress(amount)
                self.save_goals()
                return True
        return False

    def list_goals(self):
        """Return clean dictionaries for display or CLI output."""
        return [
            {
                "name": g.name,
                "target": g.target_amount,
                "current": g.current_amount,
                "progress": g.progress,
                "remaining": g.remaining,
                "due_date": g.due_date.strftime("%Y-%m-%d") if g.due_date else "No due date",
                "days_left": g.days_left,
                "overdue": g.overdue,
            }
            for g in self.goals
        ]
