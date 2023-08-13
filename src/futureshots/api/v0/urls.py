
from django.urls import path, include

from rest_framework import routers

from api.v0.users.views import UserViewSet, GroupViewSet, CommunityViewSet

app_name = "api_v0"


router = routers.DefaultRouter()

router.register(r"users", UserViewSet)
router.register(r"groups", GroupViewSet)
router.register(r"communities", CommunityViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
