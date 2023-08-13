from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model

from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied

from apps.users.models import Community, Ban


from .serializers import UserSerializer, GroupSerializer, CommunitySerializer, BanSerializer

User = get_user_model()





class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    serializer_class = UserSerializer
    queryset = User.objects.all().order_by("-date_joined")


    @action(detail=True, methods=['post'])
    def ban(self, request, pk=None):

        if not self.request.user.is_staff:
            raise PermissionDenied("Cannot ban a user")

        banned_user = User.objects.get(pk=pk)

        data = {
            "imposed_by": request.user,
            "banned_user": banned_user,
            "until": request.data.get("until"),
            "reason": request.data.get("reason"),
        }

        serializer = BanSerializer(data=data, context={"request": request})

        serializer.is_valid()

        ban = Ban.objects.get_or_create(**serializer.validated_data)
        ban.save()
        return Response(serializer.validated_data)


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """

    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommunityViewSet(viewsets.ModelViewSet):
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer
