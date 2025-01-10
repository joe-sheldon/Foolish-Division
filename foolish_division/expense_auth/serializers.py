from django.contrib.auth.models import User
from rest_framework import serializers


class NewUserSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)


class LogInSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            "username", "first_name", "last_name", "email", "is_active", "is_staff", "is_superuser",
        )
