from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.conf import settings

# Create your models here.


class Comment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL)

    # generic relation to other commentable models
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    replies = GenericRelation("self", related_query_name="parent_comment")
    ratings = GenericRelation("Rating", related_query_name="comment")

    text = models.TextField()

    created_on = models.DateTimeField(auto_now_add=True)
    is_public = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)


class Rating(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL)

    is_positive = models.BooleanField(default=True)

    # generic relation to other rateable models
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
