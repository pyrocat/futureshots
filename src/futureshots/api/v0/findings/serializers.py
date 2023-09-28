from apps.shots.models import Shot, Location
from rest_framework import serializers


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = "__all__"


class ShotSerializer(serializers.ModelSerializer):
    location = LocationSerializer(many=False, read_only=True)
    author = serializers.IntegerField(source="author.id", required=False)
    tags = serializers.SlugRelatedField(slug_field="id")
    created_on = serializers.DateTimeField(read_only=True)
    photo = serializers.CharField()
    text = serializers.CharField()
    is_private = serializers.BooleanField()

    class Meta:
        model = Shot
        fields = [
            "author",
            "location",
            "tags",
            "created_on",
            "photo",
            "created_on",
            "text",
            "is_private",
        ]
