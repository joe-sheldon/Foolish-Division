from django.db.models import Q
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from foolish_division.expenses.models import Expense, Vendor, ExpenseCategory, ExpenseCategoryOwner
from foolish_division.expenses.serializers import ExpenseSerializer, VendorSerializer, ExpenseCategorySerializer


class VendorViewset(viewsets.ModelViewSet):
    serializer_class = VendorSerializer

    def get_queryset(self):
        user = self.request.user
        if not user:
            return Vendor.objects.none()

        return Vendor.objects.all()


class ExpenseCategoryViewset(viewsets.ModelViewSet):
    serializer_class = ExpenseCategorySerializer

    def get_queryset(self):
        user = self.request.user
        if not user:
            return ExpenseCategory.objects.none()

        # Get all ExpenseCategories owned by this user.
        return ExpenseCategoryOwner.objects\
            .filter(user=user)\
            .values_list("category", flat=True)


class ExpenseViewset(viewsets.ModelViewSet):
    serializer_class = ExpenseSerializer

    def get_queryset(self):
        user = self.request.user
        if not user:
            return Expense.objects.none()
        else:
            return Expense.objects.filter(
                Q(payer=user) | Q(submitter=user)
            )


class StatusViewset(viewsets.ViewSet):
    @action(methods=["GET"], detail=False, url_name="ok")
    def ok(self, request):
        return Response(data={"status": "up"})