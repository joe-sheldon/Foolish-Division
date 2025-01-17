from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.decorators import action, authentication_classes
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.response import Response

from foolish_division.expenses.models import Expense, ExpenseGroupMember, ExpenseGroup
from foolish_division.expenses.permissions import IsInExpenseGroup, IsExpenseOwnedOrShared
from foolish_division.expenses.serializers import ExpenseSerializer, ExpenseGroupSerializer, \
    ExpenseGroupMemberSerializer
from foolish_division.profiles.models import ExpenseProfile


class ExpenseGroupViewset(viewsets.ModelViewSet):
    serializer_class = ExpenseGroupSerializer
    permission_classes = [IsInExpenseGroup]

    def get_queryset(self):
        user = self.request.user
        group_ids = ExpenseGroupMember.objects\
            .filter(profile__owner=user)\
            .values_list("group__uuid", flat=True)

        return ExpenseGroup.objects.filter(uuid__in=group_ids)

    @action(methods=["POST"], detail=True, url_name="add_member")
    def add_member(self, request, pk=None):
        group = self.get_object()
        profile_uuid = request.data.get("profile")
        profile = ExpenseProfile.objects.get(uuid=profile_uuid)
        group_member = group.create_member(profile=profile)

        return Response(ExpenseGroupMemberSerializer(group_member).data, status=status.HTTP_201_CREATED)


    @action(methods=["DELETE"], detail=True, url_path="del_member/(?P<second_pk>[^/.]+)")
    def del_member(self, request, pk=None, second_pk=None):
        group = self.get_object()

        group.members.filter(profile__uuid=second_pk).delete()

        return Response(dict(), status=status.HTTP_204_NO_CONTENT)


class ExpenseViewset(viewsets.ModelViewSet):
    serializer_class = ExpenseSerializer
    permission_classes = [IsExpenseOwnedOrShared]

    def get_serializer_context(self):
        return dict(
            request=self.request,
        )

    def get_queryset(self):
        user = self.request.user
        if not user or user.is_anonymous:
            raise PermissionDenied("You must be logged in")

        profile = ExpenseProfile.get_primary_profile(user)
        return Expense.objects.filter(
            Q(payer=profile) | Q(submitter=profile)
        )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        # FIXME this shouldn't be necessary to implement
        obj = self.get_object()
        slzrc = self.get_serializer_class()
        slzr = slzrc(obj, data=request.data, partial=True)
        slzr.is_valid(raise_exception=True)
        slzr.save()

        return Response(slzr.data)


class StatusViewset(viewsets.ViewSet):

    @authentication_classes([])
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

    @action(methods=["GET"], detail=False, url_name="check_token")
    def check_token(self, request):
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