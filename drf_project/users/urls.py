from django.urls import path

from .views import (
    CookieLogoutView,
    CookieTokenObtainPairView,
    CookieTokenRefreshView,
    UserRegisterView,
)

urlpatterns = [
    path("register/", UserRegisterView.as_view(), name="user-register"),
    path("login/", CookieTokenObtainPairView.as_view(), name="cookie_login"),
    path("refresh/", CookieTokenRefreshView.as_view(), name="cookie_refresh"),
    path("logout/", CookieLogoutView.as_view(), name="cookie_logout"),
]
