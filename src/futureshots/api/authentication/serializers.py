from django.contrib.auth import get_user_model, authenticate, models
from rest_framework import serializers
from rest_framework.exceptions import (
    AuthenticationFailed,
    PermissionDenied,
    ValidationError,
)

from apps.users.models import Profile

User: models.AbstractUser = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, style={"input_style": "password"})

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        user: User = authenticate(
            self.context["request"], username=username, password=password
        )

        if not user:
            raise AuthenticationFailed
        elif not user.is_active:
            raise PermissionDenied

        attrs["user"] = user

        return attrs


class RegisterUserSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    email = serializers.EmailField()
    password = serializers.CharField(required=True, style={"input_style": "password"})

    def validate(self, attrs):
        username = attrs.get("username")
        email = attrs.get("email")
        password = attrs.get("password")

        try:
            User.objects.get(username=username)
        except Profile.DoesNotExist:
            new_user = User.objects.create_user(
                username, email, password, slug=self._create_slug(username)
            )
        else:
            raise ValidationError(detail=f"User <{username}> already exists")

        attrs["user"] = new_user
        return attrs

    def _create_slug(self, username: str):
        return username.lower()


class ObtainTokenSerializer(serializers.Serializer):
    user = serializers.CharField()
    token = serializers.CharField()
    created_at = serializers.DateTimeField()


class SuccessSerializer(serializers.Serializer):
    success = serializers.CharField()
