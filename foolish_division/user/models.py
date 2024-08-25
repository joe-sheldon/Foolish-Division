from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Model


class FriendshipRequest(Model):
    from_user = models.ForeignKey("user.User", on_delete=models.CASCADE)
    to_user = models.ForeignKey("user.User", on_delete=models.CASCADE)

    message = models.CharField(max_length=512, default="", blank=True, null=False)

    class Meta:
        unique_together = ("from_user", "to_user")


class User(AbstractUser):

    friends = models.ManyToManyField("user.User", blank=True, null=True)

    def send_friend_request(self, to_user, message=None):
        return FriendshipRequest.objects.create(
            user=self,
            prospect=to_user,
            message=message if message else f"{self.get_full_name()} has requested to befriend you"
        )

    def confirm_friend_request(self, request: FriendshipRequest):
        from_user = request.from_user
        if from_user not in self.friends:
            self.friends.add(from_user)
        if self not in from_user.friends:
            from_user.friends.add(self)
        request.delete()

    def reject_friend_request(self, request: FriendshipRequest):
        request.delete()

    def unfriend(self, user):
        if user in self.friends:
            self.friends.remove(user)
        if self in user.friends:
            user.friends.remove(self)

    def owes_user(self, user):
        return 0
