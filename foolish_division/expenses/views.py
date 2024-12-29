from django.db.models import Q
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.response import Response

from foolish_division.expenses.models import Expense, ExpenseGroupMember, ExpenseGroup
from foolish_division.expenses.permissions import IsInExpenseGroup, IsExpenseOwnedOrShared
from foolish_division.expenses.serializers import ExpenseSerializer, ExpenseGroupSerializer


class ExpenseGroupViewset(viewsets.ModelViewSet):
    serializer_class = ExpenseGroupSerializer
    permission_classes = [IsInExpenseGroup]

    def get_queryset(self):
        user = self.request.user
        group_ids = ExpenseGroupMember.objects\
            .filter(profile__owner=user)\
            .values_list("group__uuid", flat=True)

        return ExpenseGroup.objects.filter(uuid__in=group_ids)


class ExpenseViewset(viewsets.ModelViewSet):
    serializer_class = ExpenseSerializer
    permission_classes = [IsExpenseOwnedOrShared]

    def get_queryset(self):
        user = self.request.user
        if not user or user.is_anonymous:
            raise PermissionDenied("You must be logged in")

        return Expense.objects.filter(
            Q(payer=user) | Q(submitter=user)
        )

    def update(self, request, *args, **kwargs):
        # FIXME this shouldn't be necessary to implement
        obj = self.get_object()
        slzrc = self.get_serializer_class()
        slzr = slzrc(obj, data=request.data, partial=True)
        if slzr.is_valid():
            slzr.save()

        return Response(slzr.data)


class StatusViewset(viewsets.ViewSet):
    @action(methods=["GET"], detail=False, url_name="up")
    def up(self, request):
        user = request.user

        user_data = dict()
        if user.is_anonymous:
            user_data["authenticated"] = False
        else:
            user_data["authenticated"] = True
            user_data["name"] = f"{user.first_name} {user.last_name}"
            user_data["email"] = user.email

        data = dict(
            up=True,
            user=user_data
        )
        return Response(data=data)

    @action(methods=["GET", "POST"], detail=False, url_name="cookie")
    def cookie(self, request):
        old_prof = request.COOKIES.get("test_cookie")

        if request.method == "POST":
            new_prof = request.data.get("test_cookie")
            if not new_prof:
                raise ValidationError("You must supply 'test_cookie' in the body")

            data = {
                "old_test_cookie": old_prof,
                "test_cookie": new_prof
            }
            resp = Response(data=data)
            resp.set_cookie("test_cookie", new_prof, max_age=7200)
            return resp
        elif request.method == "GET":
            return Response(data={"test_cookie": old_prof})