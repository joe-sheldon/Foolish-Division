from rest_framework import serializers

from foolish_division.expenses.models import ExpenseGroup, Expense, ExpenseGroupMember


class ExpenseGroupMemberSerializer(serializers.ModelSerializer):

    user_id = serializers.CharField(source='user.id', read_only=True)
    user_fname = serializers.CharField(source='user.first_name', read_only=True)
    user_lname = serializers.CharField(source='user.last_name', read_only=True)
    user_email = serializers.CharField(source='user.email', read_only=True)

    class Meta:
        model = ExpenseGroupMember
        fields = (
            "user_id", "user_fname", "user_lname", "user_email", "type",
        )


class ExpenseSerializer(serializers.Serializer):

    class Meta:
        model = Expense
        fields = (
            "uuid", "payer", "submitter", "name", "amount", "share_type", "group"
        )


class ExpenseGroupSerializer(serializers.ModelSerializer):

    expenses = ExpenseSerializer(
        many=True,
        default=None,
        allow_null=True
    )

    members = ExpenseGroupMemberSerializer(
        many=True,
        default=None,
        allow_null=True
    )

    class Meta:
        model = ExpenseGroup
        fields = (
            "uuid", "name", "description", "members",
        )