from django.urls import include, path

from api.v0.users import urls as auth_urls
from api.v0 import urls as api_v0_urls

urlpatterns = [
    path("auth/", include(auth_urls, namespace="auth")),
    path("v0/", include(api_v0_urls, namespace="v0")),
]
