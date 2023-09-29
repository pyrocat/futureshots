from apps.shots.models import Shot, Location, Tag
from rest_framework import serializers

from PIL import Image


class CurrentUser(serializers.CurrentUserDefault):
    """
    Supply the current user as a default value,
    """

    def __call__(self, serializer_field) -> int | None:
        user = super().__call__(serializer_field)
        return user


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = "__all__"


class ShotSerializer(serializers.ModelSerializer):
    # Location author and date must be set programmatically
    location = LocationSerializer(many=False, read_only=True)
    author = serializers.IntegerField(
        source="author.id", read_only=True, default=CurrentUser()
    )
    created_on = serializers.DateTimeField(read_only=True)

    tags = serializers.SlugRelatedField(slug_field="id", queryset=Tag.objects.all())
    photo = serializers.ImageField()
    text = serializers.CharField(allow_blank=True)
    is_private = serializers.BooleanField()

    class Meta:
        model = Shot
        fields = [
            "author",
            "location",
            "tags",
            "created_on",
            "photo",
            "text",
            "is_private",
        ]

    def create(self, validated_data):
        photo = validated_data.get("photo")
        validated_data["location"] = self._get_location(image=Image.open(photo.path))
        new_shot = Shot.objects.create(**validated_data)
        return new_shot

    def _get_location(self, image: Image) -> Location:
        ...
