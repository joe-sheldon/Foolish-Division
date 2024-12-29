from django.db.models import Q
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from foolish_division.expenses.models import Expense, ExpenseGroup, ExpenseGroupMember
from foolish_division.expenses.serializers import ExpenseSerializer, ExpenseGroupSerializer


class ExpenseGroupViewset(viewsets.ModelViewSet):
    serializer_class = ExpenseGroupSerializer

    def get_queryset(self):
        user = self.request.user
        if not user or user.is_anonymous:
            raise PermissionDenied("You must be logged in")

        # Get all ExpenseCategories owned by this user.
        return ExpenseGroupMember.objects\
            .filter(user=user)\
            .values_list("group", flat=True)


class ExpenseViewset(viewsets.ModelViewSet):
    serializer_class = ExpenseSerializer

    def get_queryset(self):
        user = self.request.user
        if not user or user.is_anonymous:
            raise PermissionDenied("You must be logged in")

        return Expense.objects.filter(
            Q(payer=user) | Q(submitter=user)
        )


class StatusViewset(viewsets.ViewSet):
    @action(methods=["GET"], detail=False, url_name="ok")
    def ok(self, request):
        return Response(data={"status": "ok bruh"})