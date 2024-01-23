from rest_framework import serializers

from foolish_division.expenses.models import ExpenseCategory, Vendor, Expense


class ExpenseCategorySerializer(serializers.ModelSerializer):

    expenses = serializers.ModelSerializer(
        many=True,
        default=None,
        allow_null=True
    )

    class Meta:
        model = ExpenseCategory
        fields = (
            "uuid", "owners", "name", "description", "expenses",
        )


class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = (
            "uuid", "name", "description", "category",
        )


class ExpenseSerializer(serializers.Serializer):
    class Meta:
        model = Expense
        fields = (
            "uuid", "payer", "submitter", "name", "vendor", "amount", "share_type", "category"
        )