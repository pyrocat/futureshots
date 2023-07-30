
from django.urls import path, include

from rest_framework import routers

from api.v0.users.views import UserViewSet, GroupViewSet

app_name = "api_v0"


router = routers.DefaultRouter()

router.register(r"users", UserViewSet)
router.register(r"groups", GroupViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
