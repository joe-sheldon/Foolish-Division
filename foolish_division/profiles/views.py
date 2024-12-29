from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied, MethodNotAllowed

from foolish_division.expenses.models import Expense, ExpenseGroup, ExpenseGroupMember
from foolish_division.profiles.models import ExpenseProfile
from foolish_division.profiles.serializers import ExpenseProfileSerializer


# Create your views here.
class UserExpenseProfileViewset(viewsets.ModelViewSet):
    """Profiles belonging to the user"""
    serializer_class = ExpenseProfileSerializer

    def get_queryset(self):
        user = self.request.user
        if not user or user.is_anonymous:
            raise PermissionDenied("You must be logged in")

        return ExpenseProfile.objects.filter(owner=user)


class ContactedExpenseProfileViewset(viewsets.ReadOnlyModelViewSet):
    """Profiles that the user has shared expenses with"""
    serializer_class = ExpenseProfileSerializer

    def get_active_profile(self):
        profile_uuid = self.request.GET.get("active_profile")
        if not profile_uuid:
            raise PermissionDenied("You must be within context of a Profile")

        profile = ExpenseProfile.objects.get(name=profile_uuid)
        return profile

    def get_friends_of_profile(self, profile: ExpenseProfile):
        member_uuids = (ExpenseGroupMember.objects
                        .exclude(profile=profile)
                        .filter(group__in=profile.expensegroup_set)
                        .distinct()
                        .values_list("profile__uuid", flat=True))

        return ExpenseProfile.objects.filter(uuid__in=member_uuids)


    def get_queryset(self):
        user = self.request.user
        if not user or user.is_anonymous:
            raise PermissionDenied("You must be logged in")

        active_profile = self.get_active_profile()
        friends = self.get_friends_of_profile(active_profile)

        return ExpenseProfileSerializer(friends, context={"active_profile": active_profile}).data