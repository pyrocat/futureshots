from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django.utils.timezone import now

from apps.users.models import Community, Ban
from datetime import timedelta, datetime
from rest_framework import serializers
from loguru import logger
from rest_framework.exceptions import (
    ValidationError,
)

User = get_user_model()


def _get_default_date():
    return now() + timedelta(weeks=4)


class BriefUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "date_joined",
            "about",
            "userpic",
            "slug",
            "last_active",
        ]
        read_only_fields = ["username", "slug", "date_joined", "last_active"]


class UserSerializer(BriefUserSerializer):
    class Meta:
        model = User
        fields = BriefUserSerializer.Meta.fields + ["email"]
        read_only_fields = ["username", "slug", "date_joined", "last_active"]


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = "__all__"


class CommunitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Community
        fields = "__all__"


class BanSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field="username",
        many=False,
        read_only=True,
        default=serializers.CurrentUserDefault(),
    )
    banned_user = serializers.PrimaryKeyRelatedField(
        source="user",
        queryset=User.objects.all(),
        many=False,
        write_only=True,
    )
    until = serializers.DateTimeField(allow_null=True)
    reason = serializers.CharField(default="Sad useless creature")

    class Meta:
        model = Ban
        fields = ["id", "author", "banned_user", "until", "reason"]

    def run_validators(self, value):
        """
        Add read_only fields with defaults to value before running validators.
        """
        # в родительском методе дефолтные значения полей не добавлялись
        # к value как заявлено.
        if isinstance(value, dict):
            to_validate = self._read_only_defaults()
            value.update(to_validate)
            to_validate = value
        else:
            to_validate = value
        super().run_validators(to_validate)

    def validate(self, attrs):
        logger.debug(attrs)
        if not attrs["until"]:
            attrs["until"] = _get_default_date()
        elif attrs["until"] < now():
            raise ValidationError(detail="Wrong datetime")

        logger.debug(Ban.objects.filter(
            author=attrs["author"], user=attrs["user"], until__gte=attrs["until"]
        ).count())

        if Ban.objects.filter(
            author=attrs["author"], user=attrs["user"], until__gte=attrs["until"]
        ).count():
            raise ValidationError(
                detail="This user is already banned for a longer period of time."
            )

        return attrs
