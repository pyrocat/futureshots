from rest_framework.viewsets import ModelViewSet
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework_nested.viewsets import NestedViewSetMixin


from .serializers import ShotSerializer
from apps.shots.models import Shot
from apps.comments.models import Comment


class ShotViewSet(ModelViewSet):
    queryset = Shot.objects.all()
    serializer_class = ShotSerializer
    parser_classes = MultiPartParser, FormParser



class ShotCommentViewSet(NestedViewSetMixin, ModelViewSet):
    queryset = Comment.objects.all()
    parent_lookup_kwargs = {"shot_pk": "shot__pk"}
