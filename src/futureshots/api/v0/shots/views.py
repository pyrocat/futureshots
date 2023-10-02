from rest_framework.viewsets import ModelViewSet
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework_nested.viewsets import NestedViewSetMixin


from .serializers import ShotSerializer, TagSerializer
from apps.shots.models import Shot, Tag
from apps.comments.models import Comment


class ShotViewSet(ModelViewSet):
    queryset = Shot.objects.all()
    serializer_class = ShotSerializer
    parser_classes = MultiPartParser, FormParser

    # def create(self, request, *args, **kwargs):
    #     serialize_object = ShotSerializer(data=request.data, context={"request": request})
    #     if serialize_object.is_valid():
    #         serialize_object.save()


class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

class ShotCommentViewSet(NestedViewSetMixin, ModelViewSet):
    queryset = Comment.objects.all()
    parent_lookup_kwargs = {"shot_pk": "shot__pk"}
