from typing import Dict, List
import uuid


# -------------------- USER --------------------
class User:
    def __init__(self, name: str):
        self.user_id = str(uuid.uuid4())
        self.name = name

    def __repr__(self):
        return self.name


# -------------------- EXPENSE --------------------
class Expense:
    def __init__(
        self,
        description: str,
        total_amount: float,
        paid_by: User,
        splits: Dict[User, float]
    ):
        self.expense_id = str(uuid.uuid4())
        self.description = description
        self.total_amount = total_amount
        self.paid_by = paid_by
        self.splits = splits


# -------------------- GROUP --------------------
class Group:
    def __init__(self, name: str, members: List[User]):
        self.group_id = str(uuid.uuid4())
        self.name = name
        self.members = members
        self.expenses: List[Expense] = []

        # balances[A][B] = amount A owes B
        self.balances: Dict[User, Dict[User, float]] = {}

        for user in members:
            self.balances[user] = {}

    # ---------- ADD EXPENSE ----------
    def add_expense(
        self,
        description: str,
        amount: float,
        paid_by: User,
        split_type: str,
        split_data: Dict[User, float] = None
    ):
        splits = {}

        if split_type == "EQUAL":
            share = amount / len(self.members)
            for user in self.members:
                splits[user] = share

        elif split_type == "EXACT":
            if sum(split_data.values()) != amount:
                raise ValueError("Exact split amounts do not sum to total.")
            splits = split_data

        elif split_type == "PERCENT":
            if sum(split_data.values()) != 100:
                raise ValueError("Percentages must sum to 100.")
            for user, percent in split_data.items():
                splits[user] = (percent / 100) * amount

        else:
            raise ValueError("Invalid split type")

        expense = Expense(description, amount, paid_by, splits)
        self.expenses.append(expense)

        self._update_balances(expense)

    # ---------- UPDATE BALANCES ----------
    def _update_balances(self, expense: Expense):
        for user, share in expense.splits.items():
            if user == expense.paid_by:
                continue

            if expense.paid_by not in self.balances[user]:
                self.balances[user][expense.paid_by] = 0

            self.balances[user][expense.paid_by] += share

    # ---------- USER BALANCE ----------
    def get_user_balance(self, user: User):
        owes = sum(self.balances[user].values())
        gets = 0

        for u in self.members:
            if user in self.balances[u]:
                gets += self.balances[u][user]

        return owes, gets

    # ---------- SIMPLIFY BALANCES ----------
    def simplify_balances(self):
        net = {}

        for user in self.members:
            owes, gets = self.get_user_balance(user)
            net[user] = gets - owes

        creditors = []
        debtors = []

        for user, amount in net.items():
            if amount > 0:
                creditors.append([user, amount])
            elif amount < 0:
                debtors.append([user, -amount])

        simplified = []

        i = j = 0
        while i < len(debtors) and j < len(creditors):
            debtor, debt = debtors[i]
            creditor, credit = creditors[j]

            settle_amount = min(debt, credit)
            simplified.append((debtor, creditor, settle_amount))

            debtors[i][1] -= settle_amount
            creditors[j][1] -= settle_amount

            if debtors[i][1] == 0:
                i += 1
            if creditors[j][1] == 0:
                j += 1

        return simplified

    # ---------- SETTLE PAYMENT ----------
    def settle(self, payer: User, receiver: User, amount: float):
        if receiver not in self.balances[payer]:
            raise ValueError("No balance to settle")

        self.balances[payer][receiver] -= amount

        if self.balances[payer][receiver] <= 0:
            del self.balances[payer][receiver]

    # ---------- DISPLAY ----------
    def show_balances(self):
        print("\n--- BALANCES ---")
        for user in self.members:
            for owed_to, amount in self.balances[user].items():
                print(f"{user} owes {owed_to}: ₹{amount:.2f}")


# -------------------- DEMO --------------------
if __name__ == "__main__":
    # Create users
    A = User("A")
    B = User("B")
    C = User("C")

    # Create group
    group = Group("Trip", [A, B, C])

    # Equal split
    group.add_expense(
        description="Dinner",
        amount=300,
        paid_by=A,
        split_type="EQUAL"
    )

    # Exact split
    group.add_expense(
        description="Taxi",
        amount=300,
        paid_by=B,
        split_type="EXACT",
        split_data={A: 100, B: 100, C: 100}
    )

    # Percentage split
    group.add_expense(
        description="Hotel",
        amount=500,
        paid_by=C,
        split_type="PERCENT",
        split_data={A: 50, B: 30, C: 20}
    )

    group.show_balances()

    print("\n--- SIMPLIFIED BALANCES ---")
    for payer, receiver, amount in group.simplify_balances():
        print(f"{payer} pays {receiver}: ₹{amount:.2f}")
