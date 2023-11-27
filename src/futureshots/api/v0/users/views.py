from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAdminUser
from rest_framework_nested.viewsets import NestedViewSetMixin

from apps.users.models import Community, Ban

from utils.permisssions import AuthorPermission


from .serializers import (
    UserSerializer,
    GroupSerializer,
    CommunitySerializer,
    BanSerializer,
)

from loguru import logger

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    serializer_class = UserSerializer
    queryset = User.objects.all().order_by("-date_joined")
    permission_classes = ((AuthorPermission | IsAdminUser),)

    @action(detail=True, methods=["post"])
    def ban(self, request, pk=None):
        if not self.request.user.is_staff:
            raise PermissionDenied("Cannot ban a user")

        data = {
            "banned_user": pk,
            "until": request.data.get("until"),
            "reason": request.data.get("reason"),
        }

        serializer = BanSerializer(data=data, context={"request": request})
        serializer.is_valid(raise_exception=True)

        ban, created = Ban.objects.get_or_create(
            author=serializer.validated_data.pop("author"),
            user=serializer.validated_data.pop("user"),
            defaults=serializer.validated_data,
        )

        ban.until = serializer.validated_data["until"]
        ban.position = serializer.validated_data["reason"]
        ban.save()

        if created:
            return Response(serializer.validated_data, status=status.HTTP_201_CREATED)

        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class UserBansViewSet(NestedViewSetMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Ban.objects.all()
    serializer_class = BanSerializer

    parent_lookup_kwargs = {"user_pk": "user_id"}


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """

    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommunityViewSet(viewsets.ModelViewSet):
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer
    permission_classes = ((AuthorPermission | IsAdminUser),)
