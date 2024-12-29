from rest_framework import permissions

from foolish_division.expenses.models import ExpenseGroup, Expense
from foolish_division.profiles.models import ExpenseProfile


class IsInExpenseGroup(permissions.BasePermission):
    # for view permission
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    # for object level permissions
    def has_object_permission(self, request, view, expense_group: ExpenseGroup):
        return expense_group.members.filter(profile__owner=request.user).exists()

class IsExpenseOwnedOrShared(permissions.BasePermission):
    # for view permission
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    # for object level permissions
    def has_object_permission(self, request, view, expense: Expense):
        is_payer_or_submitter = expense.submitter.owner == request.user or expense.payer.owner == request.user
        is_in_group = expense.group.members.filter(owner=request.user).exists()
        return is_payer_or_submitter or is_in_group
