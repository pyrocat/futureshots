# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/
from pathlib import Path


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "static/"


MEDIA_ROOT = BASE_DIR / "media/"
MEDIA_URL = "/media/"

TEMPLATES_DIR = BASE_DIR / "templates"


__all__ = [
    "BASE_DIR",
    "STATIC_URL",
    "STATIC_ROOT",
    "MEDIA_URL",
    "MEDIA_ROOT",
    "TEMPLATES_DIR",
]
