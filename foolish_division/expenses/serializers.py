from rest_framework import serializers

from foolish_division.expenses.expense_helper import ExpenseHelper, ExpenseGroupHelper
from foolish_division.expenses.models import ExpenseGroup, Expense, ExpenseGroupMember
from foolish_division.profiles.models import ExpenseProfile


class ExpenseGroupMemberSerializer(serializers.ModelSerializer):

    profile_name = serializers.CharField(source='profile.name', read_only=True, required=False)

    class Meta:
        model = ExpenseGroupMember
        fields = (
            "profile", "profile_name", "type",
        )

    def create(self, validated_data):
        # FIXME do a log here
        request = self.context["request"]
        user = request.user
        return super().create(validated_data)


class ExpenseSerializer(serializers.ModelSerializer):

    payer_name = serializers.CharField(source='payer.name', read_only=True, required=False)
    submitter_name = serializers.CharField(source='submitter.name', read_only=True, required=False)
    group_name = serializers.CharField(source='group.name', read_only=True, required=False)

    owed_amount = serializers.SerializerMethodField()

    class Meta:
        model = Expense
        fields = (
            "uuid", "payer", "payer_name", "submitter", "submitter_name", "name", "amount", "owed_amount", "share_type", "group", "group_name"
        )

    def create(self, validated_data):
        request = self.context["request"]
        profile = ExpenseProfile.get_primary_profile(request.user)

        data = dict(
            submitter=profile,
            **validated_data
        )
        return super().create(data)

    def get_owed_amount(self, obj):
        request = self.context["request"]
        profile = ExpenseProfile.get_primary_profile(request.user)

        helper = ExpenseHelper(obj, profile)
        return helper.owed_amount



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

    owed_amount = serializers.SerializerMethodField()

    class Meta:
        model = ExpenseGroup
        fields = (
            "uuid", "name", "description", "members", "expenses", "owed_amount",
        )

    def create(self, validated_data):
        # FIXME do a log here

        request = self.context["request"]
        group = super().create(request.data)

        # Create first member
        profile = ExpenseProfile.get_primary_profile(request.user)
        group.create_owner(profile)

        return group

    def get_owed_amount(self, obj):
        request = self.context["request"]
        profile = ExpenseProfile.get_primary_profile(request.user)

        helper = ExpenseGroupHelper(obj, profile)
        return helper.owed_amount