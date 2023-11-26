from rest_framework import permissions

from django.contrib.auth import get_user_model

User = get_user_model()

from loguru import logger


class AuthorPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        """Доступ к редактированию своего объекта."""
        if view.action not in {"update", "partial_update"}:
            return True

        if isinstance(obj, User):
            return obj.id == request.user.id

        try:
            return obj.author_id == request.user.id
        except AttributeError:
            return obj.user_id == request.user.id
