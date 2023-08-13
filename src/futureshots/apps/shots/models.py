from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from django.utils import timezone

# Create your models here.


class Location(models.Model):


    latitude_ref = models.CharField(max_length=20)

    latitude = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)
    longitude_ref = models.CharField(max_length=20)
    longitude = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)

    altitude = models.PositiveIntegerField(
        verbose_name="Altitude above sea level, meters", null=True, blank=True
    )



class Finding(models.Model):
    """
    A draft for future photos
    """

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    location = models.OneToOneField(Location, on_delete=models.CASCADE)
    tags = models.ManyToManyField("Tag", null=True)

    created_on = models.DateTimeField(default=timezone.now)

    photo = models.ImageField(
        verbose_name="A snapshot picturing a possible interesting place for photos"
    )

    description = models.TextField(null=True, blank=True)
    audio_description = models.FileField(null=True, blank=True)

    is_private = models.BooleanField(default=True)

    comments = GenericRelation("discussions.Comment", related_query_name="finding")
    ratings = GenericRelation("discussions.Rating", related_query_name="finding")


class Picture(models.Model):
    """
    Final picture made from the draft
    """

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="Photographer",
        related_name="pictures",
        on_delete=models.CASCADE,
    )
    draft = models.ForeignKey(
        Finding,
        verbose_name="The prototype for this picture",
        related_name="pictures",
        on_delete=models.SET_NULL,
        null=True,
    )
    concept = models.ForeignKey(
        "Concept", on_delete=models.SET_NULL, related_name="pictures", null=True
    )

    photo = models.ImageField(verbose_name="Actual photo file")
    description = models.TextField(blank=True, null=True)

    comments = GenericRelation("discussions.Comment", related_query_name="picture")
    ratings = GenericRelation("discussions.Rating", related_query_name="finding")


class Concept(models.Model):
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
    description = models.TextField(blank=True, null=True)

    created_on = models.DateTimeField(auto_now_add=True)

    comments = GenericRelation("discussions.Comment", related_query_name="concept")


class Tag(models.Model):
    name = models.CharField(max_length=50)
