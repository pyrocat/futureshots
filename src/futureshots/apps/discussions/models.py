from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.conf import settings

# Create your models here.


class Comment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    replies = GenericRelation(
        "self", related_name="parent_comment", related_query_name="parent_comment"
    )

    text = models.TextField()

    created_on = models.DateTimeField(auto_now_add=True)
    is_public = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
