from django.db import models
from django.db.models import Model


# Create your models here.
class LogEntry(Model):

    TYPE_FRIEND_REQUEST_SENT = "frs"
    TYPE_FRIEND_CONFIRMED = "frc"
    TYPE_EXPENSE_CREATED = "exc"
    TYPE_EXPENSE_MODIFIED = "exm"
    TYPE_EXPENSE_DELETED = "exd"
    TYPE_EXPENSE_CATEGORY_CREATED = "ecc"
    TYPE_EXPENSE_CATEGORY_MODIFIED = "ecm"
    TYPE_EXPENSE_CATEGORY_DELETED = "ecd"
    TYPE_EXPENSES_SETTLED = "est"

    TYPE_CHOICES = (
        (TYPE_FRIEND_REQUEST_SENT, "Friend Request Sent"),
        (TYPE_FRIEND_CONFIRMED, "Friend Request Confirmed"),
        (TYPE_EXPENSE_CREATED, "Expense Created"),
        (TYPE_EXPENSE_MODIFIED, "Expense Modified"),
        (TYPE_EXPENSE_DELETED, "Expense Deleted"),
        (TYPE_EXPENSE_CATEGORY_CREATED, "Expense Category Created"),
        (TYPE_EXPENSE_CATEGORY_MODIFIED, "Expense Category Modified"),
        (TYPE_EXPENSE_CATEGORY_DELETED, "Expense Category Deleted"),
        (TYPE_EXPENSES_SETTLED, "Expenses Settled"),
    )

    created = models.DateTimeField(auto_created=True)
    type = models.CharField(max_length=3, choices=TYPE_CHOICES)
    message = models.CharField(max_length=256, blank=True, null=False)
    md = models.JSONField(default=dict(), blank=False, null=False)