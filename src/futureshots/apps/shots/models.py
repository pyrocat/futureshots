from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from django.utils import timezone

# Create your models here.


class Location(models.Model):
    latitude_ref = models.CharField(max_length=20)

    latitude = models.DecimalField(
        decimal_places=2, max_digits=10, null=True, blank=True
    )
    longitude_ref = models.CharField(max_length=20)
    longitude = models.DecimalField(
        decimal_places=2, max_digits=10, null=True, blank=True
    )

    altitude = models.PositiveIntegerField(
        verbose_name="Altitude above sea level, meters", null=True, blank=True
    )


class Shot(models.Model):
    """
    A draft for future photos
    """
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    photo = models.ImageField(
        upload_to="images/shots",
        verbose_name="A snapshot picturing a possible interesting place for photos",
    )
    text = models.TextField(null=True, blank=True)

    location = models.OneToOneField(Location, on_delete=models.CASCADE, null=True)
    tags = models.ManyToManyField("Tag")
    created_on = models.DateTimeField(default=timezone.now)
    is_private = models.BooleanField(default=True)

    comments = GenericRelation("comments.Comment", related_query_name="shot")
    ratings = GenericRelation("comments.Rating", related_query_name="shot")


class Project(models.Model):
    """
    A concept comprising multiple findings
    """

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )
    community = models.ForeignKey(
        "users.Community", on_delete=models.SET_NULL, null=True
    )

    title = models.CharField(max_length=255)
    text = models.TextField(blank=True, null=True)

    created_on = models.DateTimeField(auto_now_add=True)

    comments = GenericRelation("comments.Comment", related_query_name="project")


class Tag(models.Model):
    name = models.CharField(max_length=50)
