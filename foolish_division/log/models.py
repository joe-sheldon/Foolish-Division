from django.contrib.auth.models import User
from django.db import models
from django.db.models import Model

from foolish_division.profiles.models import ExpenseProfile


# Create your models here.
class LogEntry(Model):

    TYPE_EXPENSE_CREATED = "exc"
    TYPE_EXPENSE_MODIFIED = "exm"
    TYPE_EXPENSE_DELETED = "exd"
    TYPE_EXPENSE_GROUP_CREATED = "ecc"
    TYPE_EXPENSE_GROUP_MODIFIED = "ecm"
    TYPE_EXPENSE_GROUP_DELETED = "ecd"
    TYPE_EXPENSES_SETTLED = "est"

    TYPE_CHOICES = (
        (TYPE_EXPENSE_CREATED, "Expense Created"),
        (TYPE_EXPENSE_MODIFIED, "Expense Modified"),
        (TYPE_EXPENSE_DELETED, "Expense Deleted"),
        (TYPE_EXPENSE_GROUP_CREATED, "Expense Group Created"),
        (TYPE_EXPENSE_GROUP_MODIFIED, "Expense Group Modified"),
        (TYPE_EXPENSE_GROUP_DELETED, "Expense Group Deleted"),
        (TYPE_EXPENSES_SETTLED, "Expenses Settled"),
    )

    created = models.DateTimeField(auto_created=True)

    type = models.CharField(max_length=3, choices=TYPE_CHOICES)
    message = models.CharField(max_length=256, blank=True, null=False)

    profile = models.ForeignKey(ExpenseProfile, on_delete=models.SET_NULL, blank=True, null=True, related_name="logs")
    group = models.ForeignKey("expenses.ExpenseGroup", on_delete=models.SET_NULL, blank=True, null=True, related_name="logs")

    md = models.JSONField(default=dict, blank=False, null=False)