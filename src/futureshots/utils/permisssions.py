from rest_framework import permissions


class AuthorPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        """Доступ к объекту."""
        if view.action in {"retrieve", "update", "partial_update"}:
            try:
                return obj.author_id == request.user.id
            except AttributeError:
                return obj.user_id == request.user.id
        return False
