from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class Profile(AbstractUser):
    about = models.TextField(null=True, blank=True)
    userpic = models.ImageField(null=True, blank=True)
    slug = models.SlugField(max_length=100, unique=True, db_index=True)
    last_active = models.DateTimeField(auto_now=True)


class Ban(models.Model):
    imposed_by = models.ForeignKey(Profile, related_name="bans_imposed", on_delete=models.CASCADE)
    user = models.ForeignKey(Profile, related_name="bans_subjected", on_delete=models.CASCADE)
    until = models.DateTimeField()
    reason = models.TextField(null=True)


class Membership(models.Model):
    user = models.ForeignKey(Profile, related_name="memberships", on_delete=models.CASCADE)
    community = models.ForeignKey(
        "Community", related_name="members", on_delete=models.CASCADE
    )
    position = models.ForeignKey("Position", on_delete=models.DO_NOTHING)
    date_started = models.DateTimeField(auto_now_add=True)


class Community(models.Model):
    users = models.ManyToManyField(Profile, related_name="communities", through=Membership)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField()


class Position(models.Model):
    class PositionChoices(models.TextChoices):
        ADMIN = "admin"
        MEMBER = "member"

    name = models.CharField(max_length=255, choices=PositionChoices.choices, default=PositionChoices.MEMBER)
    permissions = models.JSONField()
