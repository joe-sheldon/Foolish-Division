from foolish_division.expenses.models import Expense, ExpenseGroup
from foolish_division.profiles.models import ExpenseProfile

"""
Convention:
Owed: Profile is OWED. This is signed +
Owe: Profile OWES. This is signed -
"""

class ExpenseHelper:

    def __init__(self, expense: Expense, profile: ExpenseProfile):
        self.expense = expense
        self.profile = profile

    @property
    def is_party_to_expense(self):
        if self.expense.payer == self.profile:
            return True

        group_member_uuids = self.expense.group.members.values_list("profile__uuid", flat=True)
        if self.profile.uuid in group_member_uuids:
            return True

        return False

    @property
    def owed_amount(self):
        """+ means profile is owed, - means profile owes"""
        if not self.is_party_to_expense:
            return 0.0

        group_size = self.expense.group.members.count()
        if group_size <= 1:
            # This shouldn't exist
            # FIXME catch this sooner
            return 0.0

        if self.expense.share_type == Expense.SHARETYPE_FULL:
            # Payer bought for everyone else.
            # Payer is owed the full amount
            # Everyone else owes TOTAL / (N - 1)
            if self.expense.payer == self.profile:
                return self.expense.amount
            else:
                return - self.expense.amount / (group_size - 1)
        elif self.expense.share_type == Expense.SHARETYPE_FRACTIONAL:
            # Payer bought for everyone including themself
            # Payer is owed TOTAL * (N - 1) / N
            # Everyone else owes TOTAL / N
            if self.expense.payer == self.profile:
                return self.expense.amount * (group_size - 1) / group_size
            else:
                return - self.expense.amount / group_size
        return 0.0



class ExpenseGroupHelper:

    DIRECTION_OWE = "owe"
    DIRECTION_OWED = "owed"

    def __init__(self, group: ExpenseGroup, profile: ExpenseProfile):
        self.group = group
        self.profile = profile

    @property
    def owed_amount(self):
        """+ means profile is owed, - means profile owes"""
        amount = sum(
            list(
                map(
                    lambda eh: eh.owed_amount,
                    filter(
                        lambda eh: eh.is_party_to_expense,
                        map(
                            lambda e: ExpenseHelper(e, self.profile),
                            self.group.expenses.all()
                        )
                    )
                )
            )
        )

        return amount



