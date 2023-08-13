from django.urls import path, include
from rest_framework.authtoken import views

from rest_framework import routers

from .views import LoginView, LogoutView


app_name = "api_v0"

urlpatterns = [
    path("login", LoginView.as_view()),
    path("logout", LogoutView.as_view()),
    path('obtain-token/', views.obtain_auth_token)
]
