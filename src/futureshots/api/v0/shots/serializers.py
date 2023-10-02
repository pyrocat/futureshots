from apps.shots.models import Shot, Location, Tag
from rest_framework import serializers
from typing import Literal

from datetime import time, date, datetime, timezone

from exif import GpsAltitudeRef, Image

# from PIL import Image

from pydantic import BaseModel, Field, ValidationError


class GPSdata(BaseModel):
    gps_latitude: tuple[float, float, float]
    gps_latitude_ref: Literal["N", "S"]
    gps_longitude: tuple[float, float, float]
    gps_longitude_ref: Literal["W", "E"]
    gps_altitude: float
    gps_altitude_ref: GpsAltitudeRef
    gps_datestamp: str
    gps_timestamp: tuple[int, int, int]

    @classmethod
    def from_image(cls, image) -> "GPSdata":
        return cls(
            gps_latitude=image.get("gps_latitude"),
            gps_latitude_ref=image.get("gps_latitude_ref"),
            gps_longitude=image.get("gps_longitude"),
            gps_longitude_ref=image.get("gps_longitude_ref"),
            gps_altitude=image.get("gps_altitude"),
            gps_altitude_ref=image.get("gps_altitude_ref"),
            gps_datestamp=image.get("gps_datestamp"),
            gps_timestamp=image.get("gps_timestamp"),
        )

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

    @property
    def datetime(self) -> datetime:
        _date = datetime.strptime(self.gps_datestamp, "%Y:%m:%d")
        _time = time(*self.gps_timestamp, tzinfo=timezone.utc)
        return datetime.combine(_date, _time, tzinfo=timezone.utc)


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


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"


class ShotSerializer(serializers.ModelSerializer):
    author = serializers.IntegerField(
        source="author.id", read_only=True, default=CurrentUser()
    )
    # Location author and date must be set programmatically
    location = LocationSerializer(many=False, read_only=True)
    created_on = serializers.DateTimeField(allow_null=True, read_only=True)

    tags = TagSerializer(many=True)
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

        with open(photo.temporary_file_path(), 'rb') as file:
            image = Image(img_file=file)

        gps_data = GPSdata.from_image(image)
        validated_data["location"] = self._get_location(gps_data)
        validated_data["created_on"] = gps_data.datetime
        print(validated_data["tags"])
        new_shot = Shot.objects.create(**validated_data)
        return new_shot

    def _get_location(self, gps_data: GPSdata) -> Location:
        location, _ = Location.objects.get_or_create(
            latitude=gps_data.dec_latitude,
            longitude=gps_data.dec_longitude,
            altitude=gps_data.dec_altitude,
        )
        return location


