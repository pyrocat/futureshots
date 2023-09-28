
from django.urls import path, include

from rest_framework_nested import routers

from api.v0.users.views import UserViewSet, GroupViewSet, CommunityViewSet
from api.v0.findings.views import ShotViewSet, ShotCommentViewSet


app_name = "api_v0"

router = routers.SimpleRouter()

router.register(r"users", UserViewSet)
router.register(r"groups", GroupViewSet)
router.register(r"communities", CommunityViewSet)
router.register(r"shots", ShotViewSet)

shots_router = routers.NestedSimpleRouter(router, parent_prefix="shots", lookup="shot")
shots_router.register("comments", ShotCommentViewSet, basename="shot-comment")

urlpatterns = [
    path("", include(router.urls)),
    path("", include(shots_router.urls)),
]
