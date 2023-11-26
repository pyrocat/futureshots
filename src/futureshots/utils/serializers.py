from rest_framework import serializers


class CurrentUser(serializers.CurrentUserDefault):
    """
    Supply the current user as a default value,
    """

    def __call__(self, serializer_field) -> int | None:
        user = super().__call__(serializer_field)
        return user
