from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed, PermissionDenied


User = get_user_model()


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
