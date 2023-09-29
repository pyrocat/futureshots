from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.conf import settings

from mptt.models import MPTTModel, TreeForeignKey

# Create your models here.


class Comment(MPTTModel):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="comments",
    )
    parent = TreeForeignKey(
        "self",
        null=True,
        blank=True,
        db_index=True,
        on_delete=models.CASCADE,
        related_name="children",
    )
    ratings = GenericRelation("Rating", related_query_name="comment")

    text = models.TextField()
    image = models.ImageField(upload_to="images/", max_length=255)

    created_on = models.DateTimeField(auto_now_add=True, editable=False)
    edited_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    is_public = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    # generic relation to other commentable models
    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, blank=True, null=True
    )
    object_id = models.PositiveIntegerField(blank=True, null=True)
    content_object = GenericForeignKey()

    class MPTTMeta:
        order_insertion_by = "created_on"


class Rating(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )

    is_positive = models.BooleanField(default=True)

    # generic relation to other rateable models
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
