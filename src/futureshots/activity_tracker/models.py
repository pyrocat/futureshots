from django.conf import settings
from django.db import models


class JoinUserManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related("user")


class ApiLog(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )
    ip = models.GenericIPAddressField()

    requested_at = models.DateTimeField(db_index=True)
    response_ms = models.PositiveIntegerField(default=0)

    method = models.CharField(max_length=10)
    path = models.CharField(max_length=255)
    query_params = models.TextField(null=True, blank=True)
    query_data = models.TextField(null=True, blank=True)

    status_code = models.PositiveIntegerField(null=True, blank=True)
    errors = models.TextField(null=True, blank=True)

    objects = JoinUserManager()

    class Meta:
        verbose_name = "ApiLog"

    def __str__(self):
        return f"{self.user.username} {self.method} {self.path}"
