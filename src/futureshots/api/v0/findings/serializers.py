from apps.shots.models import Finding, Location
from rest_framework import serializers


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = "__all__"


class FindingSerializer(serializers.ModelSerializer):
    location = LocationSerializer(many=False, read_only=True)
    author = serializers.IntegerField(source="author.id", required=False)
    tags = serializers.SlugRelatedField(
        slug_field="id"
    )
    created_on = serializers.DateTimeField(read_only=True)
    photo = serializers.ImageField(source="photo")
    description = serializers.CharField()
    is_private = serializers.BooleanField()


    class Meta:
        model = Finding
        fields = ["author",
                  "location",
                  "tags",
                  "created_on",
                  "photo",
                  "created_on",
                  "description",
                  "is_private"]
