from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.response import Response

from foolish_division.expenses.models import ExpenseGroupMember
from foolish_division.profiles.models import ExpenseProfile
from foolish_division.profiles.permissions import IsProfileOwner
from foolish_division.profiles.serializers import ExpenseProfileSerializer
from foolish_division.settings import ACTIVE_PROFILE_COOKIE_MAX_AGE_SECONDS


# Create your views here.
class UserExpenseProfileViewset(viewsets.ModelViewSet):
    """Profiles belonging to the user"""
    serializer_class = ExpenseProfileSerializer
    permission_classes = [IsProfileOwner]

    def get_queryset(self):
        user = self.request.user
        if not user or user.is_anonymous:
            raise PermissionDenied("You must be logged in")

        return ExpenseProfile.objects.filter(owner=user)

    def get_active_profile_via_cookie(self):
        user = self.request.user
        if not user or user.is_anonymous:
            raise PermissionDenied("You must be logged in")

        active_profile_uuid = self.request.COOKIES.get("active_profile")

        return (ExpenseProfile.objects
                  .filter(owner=self.request.user)
                  .get(uuid=active_profile_uuid))

    @action(methods=["GET", "POST", "PATCH"], detail=False, url_name="active")
    def active(self, request):
        if request.method == "GET":
            # Get active profile details
            active_profile = self.get_active_profile_via_cookie()
            return ExpenseProfileSerializer(active_profile).data

        if request.method == "POST":
            # Change the active profile
            new_active_profile_uuid = request.data.get("active_profile")
            if not new_active_profile_uuid:
                raise ValidationError("You must supply 'new_active_profile_uuid' in the body")

            new_active_profile = None
            try:
                new_active_profile = (ExpenseProfile.objects
                                      .filter(owner=self.request.user)
                                      .get(uuid=new_active_profile_uuid))
            except ExpenseProfile.DoesNotExist:
                raise ValidationError("Could not find profile")

            resp = Response(data=ExpenseProfileSerializer(new_active_profile).data)
            resp.set_cookie(
                "active_profile",
                new_active_profile_uuid,
                max_age=ACTIVE_PROFILE_COOKIE_MAX_AGE_SECONDS
            )
            return resp

    def update(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.owner.user != self.request.user:
            raise PermissionDenied("You must own this object in order to update it")

class ContactedExpenseProfileViewset(viewsets.ReadOnlyModelViewSet):
    """Profiles that the user has shared expenses with"""
    serializer_class = ExpenseProfileSerializer

    def get_active_profile_via_cookie(self):
        user = self.request.user
        if not user or user.is_anonymous:
            raise PermissionDenied("You must be logged in")

        active_profile_uuid = self.request.COOKIES.get("active_profile")

        return (ExpenseProfile.objects
                .filter(owner=self.request.user)
                .get(uuid=active_profile_uuid))

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

        active_profile = self.get_active_profile_via_cookie()
        friends = self.get_friends_of_profile(active_profile)

        return ExpenseProfileSerializer(friends, context={"active_profile": active_profile}).data