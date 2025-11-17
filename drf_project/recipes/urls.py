from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RecipeViewSet, CommentViewSet

router = DefaultRouter()
router.register(r"recipes", RecipeViewSet, basename="recipes")

recipes_router = NestedDefaultRouter(router, r"recipes", lookup="recipe")
recipes_router.register(r"comments", CommentViewSet, basename="recipe-comments")

urlpatterns = [
    path("", include(router.urls)),
    path("", include(recipes_router.urls)),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]