from rest_framework import serializers

from foolish_division.expenses.models import ExpenseGroup, Expense, ExpenseGroupMember
from foolish_division.profiles.models import ExpenseProfile


class ExpenseGroupMemberSerializer(serializers.ModelSerializer):

    profile_name = serializers.CharField(source='profile.name', read_only=True)
    profile_uuid = serializers.CharField(source='profile.uuid', read_only=True)

    class Meta:
        model = ExpenseGroupMember
        fields = (
            "profile_name", "profile_uuid", "type",
        )

    def create(self, validated_data):
        # FIXME do a log here
        request = self.context["request"]
        user = request.user
        return super().create(validated_data)


class ExpenseSerializer(serializers.Serializer):

    class Meta:
        model = Expense
        fields = (
            "uuid", "payer", "submitter", "name", "amount", "share_type", "group"
        )

    def create(self, validated_data):
        # FIXME do a log here

        request = self.context["request"]
        profile = ExpenseProfile.objects.filter(owner=request.user).filter(primary=True).first()

        data = dict(
            submitter=profile,
            **validated_data
        )
        return super().create(data)


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
            "uuid", "name", "description", "members", "expenses"
        )

    def create(self, validated_data):
        # FIXME do a log here

        request = self.context["request"]
        group = super().create(request.data)

        # Create first member
        profile = ExpenseProfile.objects.filter(owner=request.user).filter(primary=True).first()
        ExpenseGroupMember.objects.create(profile=profile, group=group, type=ExpenseGroupMember.MEMBER_TYPE_OWNER)

        return group