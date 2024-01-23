from django.contrib.auth.models import User
from django.db import models
from django.db.models import Model


class ExpenseCategoryOwner(Model):
    OWNER_ROLE_ADMIN = "admin"
    OWNER_ROLE_RESTRICTED = "restr"
    OWNER_ROLE_CHOICES = (
        (OWNER_ROLE_ADMIN, "Administrator"),
        (OWNER_ROLE_RESTRICTED, "Regular Owner")
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey("ExpenseCategory", blank=False, null=False)
    role = models.CharField(
        choices=OWNER_ROLE_CHOICES,
        default=OWNER_ROLE_ADMIN
    )

    class Meta:
        unique_together = ('user', 'category')


class ExpenseCategory(Model):
    uuid = models.UUIDField(auto_created=True, primary_key=True)
    owners = models.ManyToManyField(
        User,
        through=ExpenseCategoryOwner,
    )
    name = models.CharField(max_length=128, blank=False, null=False, unique=True)
    description = models.CharField(max_length=1024, blank=True, null=False)

    @property
    def expenses(self):
        return None


class VendorCategory(Model):
    uuid = models.UUIDField(auto_created=True, primary_key=True)
    name = models.CharField(max_length=128, blank=False, null=False, unique=True)
    description = models.CharField(max_length=1024, blank=True, null=False)


class Vendor(Model):
    uuid = models.UUIDField(auto_created=True, primary_key=True)
    name = models.CharField(max_length=128, blank=False, null=False)
    description = models.CharField(max_length=1024, blank=True, null=False)
    category = models.ForeignKey(
        "VendorCategory",
        blank=True,
        null=False,
        on_delete=models.CASCADE
    )


class Expense(Model):

    SHARETYPE_FRACTIONAL = "frac"
    SHARETYPE_FULL = "full"
    SHARETYPE_CHOICES = (
        (SHARETYPE_FRACTIONAL, "Payer Owed Fraction of Expense"),
        (SHARETYPE_FULL, "Payer Owed Full Expense"),
    )

    uuid = models.UUIDField(auto_created=True, primary_key=True)
    payer = models.ForeignKey(
        User,
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    submitter = models.ForeignKey(User, blank=True, null=True)
    name = models.CharField(max_length=128, blank=False, null=False)
    vendor = models.ForeignKey(
        "Vendor",
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    amount = models.FloatField(default=0.00, blank=False, null=False)
    share_type = models.CharField(max_length=4, choices=SHARETYPE_CHOICES)
    category = models.ForeignKey(
        "foolish_division.expenses.ExpenseCategory",
        blank=False,
        null=False
    )

