import uuid
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Model

from foolish_division.profiles.models import ExpenseProfile


class ExpenseGroupMember(Model):

    MEMBER_TYPE_OWNER = "own"
    MEMBER_TYPE_MEMBER = "mem"
    MEMBER_TYPE_CHOICES = (
        (MEMBER_TYPE_OWNER, "Owner"),
        (MEMBER_TYPE_MEMBER, "Normal Member"),
    )

    profile = models.ForeignKey(ExpenseProfile, on_delete=models.CASCADE)
    group = models.ForeignKey("expenses.ExpenseGroup", on_delete=models.CASCADE, related_name="members")
    type = models.CharField(max_length=3, choices=MEMBER_TYPE_CHOICES, default=MEMBER_TYPE_MEMBER)

    class Meta:
        unique_together = ("profile", "group")

class ExpenseGroup(Model):

    uuid = models.UUIDField(default=uuid.uuid4, auto_created=True, primary_key=True)

    name = models.CharField(max_length=128, blank=False, null=False)
    description = models.CharField(max_length=1024, blank=True, null=True)

    @property
    def expenses(self):
        return Expense.objects.filter(group=self)

    def create_owner(self, profile) -> ExpenseGroupMember:
        return ExpenseGroupMember.objects.get_or_create(profile=profile, group=self, type=ExpenseGroupMember.MEMBER_TYPE_OWNER)[0]

    def create_member(self, profile) -> ExpenseGroupMember:
        return ExpenseGroupMember.objects.get_or_create(profile=profile, group=self, type=ExpenseGroupMember.MEMBER_TYPE_MEMBER)[0]


class Expense(Model):

    SHARETYPE_FRACTIONAL = "frac"
    SHARETYPE_FULL = "full"
    SHARETYPE_CHOICES = (
        (SHARETYPE_FRACTIONAL, "Payer Owed Fraction of Expense"),
        (SHARETYPE_FULL, "Payer Owed Full Expense"),
    )

    uuid = models.UUIDField(default=uuid.uuid4, auto_created=True, primary_key=True)

    payer = models.ForeignKey(ExpenseProfile, blank=True, null=True, on_delete=models.SET_NULL, related_name="expenses_payer_set")
    submitter = models.ForeignKey(ExpenseProfile, blank=True, null=True, on_delete=models.SET_NULL, related_name="expenses_submitted_set")
    group = models.ForeignKey(ExpenseGroup, blank=True, null=True, on_delete=models.SET_NULL)

    name = models.CharField(max_length=128, blank=False, null=False)
    amount = models.FloatField(default=0.00, blank=False, null=False)
    share_type = models.CharField(max_length=4, choices=SHARETYPE_CHOICES)


