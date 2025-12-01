from django.conf import settings
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    TokenRefreshSerializer,
)
from rest_framework_simplejwt.views import TokenObtainPairView


class CookieTokenObtainPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = TokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        access = data.get("access")
        refresh = data.get("refresh")

        response = Response(
            {"detail": "OK", "access": access, "refresh": refresh},
            status=status.HTTP_200_OK,
        )

        cookie_secure = settings.SESSION_COOKIE_SECURE
        samesite = "Lax"

        response.set_cookie(
            "access", access, httponly=True, secure=cookie_secure, samesite=samesite
        )
        response.set_cookie(
            "refresh", refresh, httponly=True, secure=cookie_secure, samesite=samesite
        )
        return response


class CookieTokenRefreshView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        refresh = request.COOKIES.get("refresh") or request.data.get("refresh")
        if not refresh:
            return Response(
                {"detail": "refresh not provided"}, status=status.HTTP_400_BAD_REQUEST
            )
        s = TokenRefreshSerializer(data={"refresh": refresh})
        s.is_valid(raise_exception=True)
        access = s.validated_data["access"]
        response = Response(
            {"access": access, "detail": "refreshed"}, status=status.HTTP_200_OK
        )
        response.set_cookie(
            "access",
            access,
            httponly=True,
            secure=settings.SESSION_COOKIE_SECURE,
            samesite="Lax",
        )
        return response


class CookieLogoutView(APIView):
    def post(self, request, *args, **kwargs):
        response = Response({"detail": "logged out"}, status=status.HTTP_200_OK)
        response.delete_cookie("access")
        response.delete_cookie("refresh")
        return response
