from foolish_division.expenses.models import Expense, ExpenseCategory


class ExpenseHelper:
    def __init__(self, expense: Expense):
        self.expense = expense


class ExpenseCategoryHelper:
    def __init__(self, category: ExpenseCategory):
        self.category = category
