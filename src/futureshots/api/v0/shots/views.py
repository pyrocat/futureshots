from rest_framework.viewsets import ModelViewSet
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework_nested.viewsets import NestedViewSetMixin
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAdminUser

from django_filters import rest_framework as filters


from .serializers import ShotSerializer, TagSerializer

from futureshots.utils.permisssions import AuthorPermission
from apps.shots.models import Shot, Tag
from apps.comments.models import Comment


class ShotViewSet(ModelViewSet):
    queryset = Shot.objects.all()
    serializer_class = ShotSerializer
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = ((AuthorPermission | IsAdminUser),)
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ("author_id",)


class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class ShotCommentViewSet(NestedViewSetMixin, ModelViewSet):
    queryset = Comment.objects.all()
    parent_lookup_kwargs = {"shot_pk": "shot__pk"}
