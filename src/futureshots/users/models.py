from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    bio = models.TextField()
    image = models.ImageField()
    last_login = models.DateTimeField()


class Ban(models.Model):
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
    users = models.ManyToManyField(User)
    name = models.CharField()
    description = models.TextField()


class Position(models.Model):
    name = models.CharField()
    permissions = models.JSONField()
