from apps.shots.models import Shot, Location, Tag
from rest_framework import serializers
from typing import Literal

from exif import GpsAltitudeRef

from PIL import Image

from pydantic import BaseModel, Field


class Coords(BaseModel):
    gps_latitude: tuple[float, float, float]
    gps_latitude_ref: Literal["N", "S"]
    gps_longitude: tuple[float, float, float]
    gps_longitude_ref: Literal["W", "E"]
    gps_altitude: float
    gps_altitude_ref: GpsAltitudeRef

    @property
    def dec_latitude(self) -> float:
        h, m, s = self.gps_latitude
        res = h + m / 60 + s / 3600
        if self.gps_latitude_ref == "S":
            res = -res
        return res

    @property
    def dec_longitude(self) -> float:
        h, m, s = self.gps_longitude
        res = h + m / 60 + s / 3600
        if self.gps_longitude_ref == "W":
            res = -res
        return res

    @property
    def dec_altitude(self) -> float:
        return (
            -self.gps_altitude
            if self.gps_altitude_ref == GpsAltitudeRef.BELOW_SEA_LEVEL
            else self.gps_altitude
        )


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
    created_on = serializers.DateTimeField(allow_null=True, read_only=True)

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
        validated_data["created_on"] = self._get_datetime(image=Image.open(photo.path))
        new_shot = Shot.objects.create(**validated_data)
        return new_shot

    def _get_datetime(self, image: Image):
        ...

    def _get_location(self, image: Image) -> Location:
        ...
