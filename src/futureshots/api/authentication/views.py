from django.contrib.auth import login, logout, get_user_model

from rest_framework import generics, views, status, serializers
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache


User = get_user_model()


from .serializers import (
    ObtainTokenSerializer,
    LoginSerializer,
    SuccessSerializer,
    RegisterUserSerializer,
)

method_never_cache = method_decorator(never_cache)


# class LoginView(generics.GenericAPIView):
#     permission_classes = (AllowAny,)
#     serializer_class = LoginSerializer
#
#     @method_never_cache
#     def dispatch(self, request, *args, **kwargs):
#         return super().dispatch(request, *args, **kwargs)
#
#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(
#             data=self.request.data, context={"request": request}
#         )
#
#         serializer.is_valid(raise_exception=True)
#
#         self.user = serializer.validated_data["user"]
#
#         login(self.request, self.user)
#
#         user_serializer = ObtainTokenSerializer(self.user)
#
#         return Response(data=user_serializer.data, status=status.HTTP_200_OK)


class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterUserSerializer
    permission_classes = (IsAdminUser,)

    @method_never_cache
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer: serializers.Serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        new_user = serializer.validated_data["user"]

        response_serializer = SuccessSerializer(
            data={"success": f"User <{new_user.username}> created."}
        )

        return Response(
            data=response_serializer.initial_data,
            status=status.HTTP_201_CREATED,
        )


class LoginView(ObtainAuthToken):
    permission_classes = (AllowAny,)

    @method_never_cache
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class LogoutView(generics.GenericAPIView):
    serializer_class = SuccessSerializer
    pagination_class = None

    def post(self, request, *args, **kwargs):
        user = request.user
        try:
            Token.objects.get(user=user).delete()
        except Token.DoesNotExist:
            pass

        # logout(self.request)
        return Response(
            data={"success": f"Revoked token for user <{user.username}>"},
            status=status.HTTP_200_OK,
        )
