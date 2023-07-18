from django.contrib.auth import login, logout

from rest_framework import generics, views, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache


from .serializers import UserSerializer, LoginSerializer

method_never_cache = method_decorator(never_cache)


class LoginView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    @method_never_cache
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.serializer = self.get_serializer(
            data=self.request.data, context={"request": self.request}
        )

        self.serializer.is_valid(raise_exception=True)

        self.user = self.serializer.validated_data["user"]

        login(self.request, self.user)

        user_serializer = UserSerializer(self.user)

        return Response(data=user_serializer.data, status=status.HTTP_200_OK)
