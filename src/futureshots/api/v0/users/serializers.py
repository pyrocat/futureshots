from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model

from apps.users.models import Community, Ban

from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = "__all__"


class CommunitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Community
        fields = "__all__"


class BanSerializer(serializers.ModelSerializer):
    imposed_by = UserSerializer(
        many=False,
    )
    banned_user = serializers.HyperlinkedRelatedField(queryset=User.objects.all(), view_name="user-detail", many=False)

    until = serializers.DateTimeField()
    reason = serializers.CharField()

    class Meta:
        model = Ban
        fields = ["id", "imposed_by", "banned_user", "until", "reason"]