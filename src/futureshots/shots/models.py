from django.db import models
from django.conf import settings

# Create your models here.


class Shot(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL)

    photo_file = models.ImageField()

    created_on = models.DateTimeField()

    latitude = models.DecimalField()
    longitude = models.DateTimeField()

    altitude = models.PositiveIntegerField(
        verbose_name="Altitude above sea level, meters"
    )
    direction = models.DecimalField()
