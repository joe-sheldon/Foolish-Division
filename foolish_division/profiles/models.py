import uuid
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Model


class ExpenseProfile(Model):
    """This allows one expense_auth user to manage many expense accounts (eg. personal, business, etc)"""
    uuid = models.UUIDField(default=uuid.uuid4, auto_created=True, primary_key=True)
    created = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=128, blank=False, null=False)
    bio = models.CharField(max_length=500, blank=True, null=False)

    primary = models.BooleanField(default=False) # ACTIVE

    owner = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name="profile_set")

    class Meta:
        unique_together = ("owner", "name")
