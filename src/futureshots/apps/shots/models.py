from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation

# Create your models here.


class Snapshot(models.Model):
    photo = models.ImageField(
        verbose_name="A snapshot picturing a possible interesting place for photos"
    )
    created_on = models.DateTimeField(auto_now_add=True)

    latitude = models.DecimalField(null=True, blank=True)
    longitude = models.DecimalField(null=True, blank=True)

    altitude = models.PositiveIntegerField(
        verbose_name="Altitude above sea level, meters", null=True, blank=True
    )
    direction = models.DecimalField(null=True, blank=True)


class Finding(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tags = models.ManyToManyField("Tag", null=True)

    shapshot = models.OneToOneField(Snapshot, on_delete=models.CASCADE)

    desired_lighting_direction = models.DecimalField(null=True, blank=True)

    description = models.TextField(null=True, blank=True)
    audio_description = models.FileField(null=True, blank=True)

    is_private = models.BooleanField(default=True)

    comments = GenericRelation(
        "discussions.Comment", related_name="finding", related_query_name="finding"
    )


class Picture(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    draft = models.ForeignKey(Finding, on_delete=models.SET_NULL, null=True)
    project = models.ForeignKey("Concept", on_delete=models.SET_NULL, null=True)

    photo = models.ImageField()
    description = models.TextField(blank=True, null=True)

    comments = GenericRelation(
        "discussions.Comment", related_name="picture", related_query_name="picture"
    )


class Concept(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )
    community = models.ForeignKey(
        "users.Community", on_delete=models.SET_NULL, null=True
    )

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    created_on = models.DateTimeField(auto_now_add=True)

    comments = GenericRelation(
        "discussions.Comment", related_name="concept", related_query_name="concept"
    )


class Tag(models.Model):
    name = models.CharField(max_length=50)
