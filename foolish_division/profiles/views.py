from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.response import Response

from foolish_division.expenses.models import ExpenseGroupMember
from foolish_division.profiles.models import ExpenseProfile
from foolish_division.profiles.permissions import IsProfileOwner
from foolish_division.profiles.serializers import ExpenseProfileSerializer


# Create your views here.
class UserExpenseProfileViewset(viewsets.ModelViewSet):
    """Profiles belonging to the user"""
    serializer_class = ExpenseProfileSerializer
    permission_classes = [IsProfileOwner]

    def get_serializer_context(self):
        return dict(
            request=self.request,
        )

    def get_queryset(self):
        user = self.request.user
        if not user or user.is_anonymous:
            raise PermissionDenied("You must be logged in")

        return ExpenseProfile.objects.filter(owner=user)

    def get_primary_profile(self):
        user = self.request.user
        if not user or user.is_anonymous:
            raise PermissionDenied("You must be logged in")

        return (ExpenseProfile.objects
                          .filter(owner=self.request.user)
                          .filter(primary=True)
                          .first())

    @action(methods=["GET", "POST", "PATCH"], detail=False, url_name="active")
    def active(self, request):
        if request.method == "GET":
            # Get active profile details
            active_profile = self.get_primary_profile()
            return Response(self.get_serializer(active_profile).data)

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

                other_profiles = (ExpenseProfile.objects.filter(owner=self.request.user)
                                .exclude(uuid=new_active_profile_uuid))
                for profile in other_profiles:
                    profile.primary = False
                    profile.save(update_fields=["primary"])

                new_active_profile.primary = True
                new_active_profile.save(update_fields=["primary"])
            except ExpenseProfile.DoesNotExist:
                raise ValidationError("Could not find profile")

            resp = Response(data=self.get_serializer(new_active_profile).data)
            return resp

    def update(self, request, *args, **kwargs):
        # FIXME this shouldn't be necessary to implement
        slzrc = self.get_serializer_class()
        slzr = slzrc(self.get_object(), data=request.data, partial=True)
        if slzr.is_valid():
            slzr.save()

        return Response(slzr.data)

class ContactedExpenseProfileViewset(viewsets.ReadOnlyModelViewSet):
    """Profiles that the user has shared expenses with"""
    serializer_class = ExpenseProfileSerializer

    def get_primary_profile(self):
        user = self.request.user
        if not user or user.is_anonymous:
            raise PermissionDenied("You must be logged in")

        return (ExpenseProfile.objects
                .filter(owner=self.request.user)
                .filter(primary=True)
                .first())

    def get_friends_of_profile(self, profile: ExpenseProfile):

        group_ids = profile.expensegroupmember_set.values_list("group_id", flat=True)
        member_uuids = (ExpenseGroupMember.objects
                        .exclude(profile=profile)
                        .filter(group_id__in=group_ids)
                        .distinct()
                        .values_list("profile__uuid", flat=True))

        return ExpenseProfile.objects.filter(uuid__in=member_uuids)


    def get_queryset(self):
        user = self.request.user
        if not user or user.is_anonymous:
            raise PermissionDenied("You must be logged in")

        active_profile = self.get_primary_profile()
        friends = self.get_friends_of_profile(active_profile)

        return ExpenseProfileSerializer(friends, context={"active_profile": active_profile}).data