from rest_framework import serializers

from foolish_division.expenses.models import ExpenseGroup, Expense, ExpenseGroupMember
from foolish_division.expenses.serializers import ExpenseGroupSerializer
from foolish_division.profiles.models import ExpenseProfile


class ExpenseProfileSerializer(serializers.ModelSerializer):

    owner_id = serializers.CharField(source='owner.uuid', read_only=True)
    owner_fname = serializers.CharField(source='owner.first_name', read_only=True)
    owner_lname = serializers.CharField(source='owner.last_name', read_only=True)
    owner_email = serializers.CharField(source='owner.email', read_only=True)

    groups = ExpenseGroupSerializer(many=True, read_only=True)
    amount_owed = serializers.SerializerMethodField()

    class Meta:
        model = ExpenseProfile
        fields = (
            "owner_id", "owner_fname", "owner_lname", "owner_email", "name", "bio", "created", "groups"
        )

    def get_amount_owed(self):
        """ Positive indicates active profile owes, negative indicates active profile IS owed"""
        # FIXME implement
        active_profile: ExpenseProfile = self.context.get("active_profile")
        if active_profile:
            return 10.0

        return None

