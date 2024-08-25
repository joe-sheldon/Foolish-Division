from rest_framework import serializers

from foolish_division.expenses.models import ExpenseCategory, Vendor, Expense
from foolish_division.user.models import User


class UnfriendedUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "email", "is_active",
        )


class FriendedUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "email", "first_name", "last_name", "username", "is_active",
        )