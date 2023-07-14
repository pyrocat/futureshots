from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    bio = models.TextField()
    userpic = models.ImageField()
    last_active = models.DateTimeField(auto_now=True)


class Ban(models.Model):
    imposed_by = models.ForeignKey(User, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    banned_until = models.DateTimeField(null=True)


class Membership(models.Model):
    user = models.ForeignKey(User, related_name="communities", on_delete=models.CASCADE)
    community = models.ForeignKey(
        "Community", related_name="users", on_delete=models.CASCADE
    )
    position = models.ForeignKey("Position", on_delete=models.DO_NOTHING)
    date_started = models.DateTimeField(auto_now_add=True)


class Community(models.Model):
    users = models.ManyToManyField(User, through=Membership)
    name = models.CharField()
    description = models.TextField()


class Position(models.Model):
    class PositionChoices(models.TextChoices):
        ADMIN = "admin"
        MEMBER = "member"

    name = models.CharField(choices=PositionChoices, default=PositionChoices.MEMBER)
    permissions = models.JSONField()
