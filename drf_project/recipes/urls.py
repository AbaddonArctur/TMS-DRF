from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter

from .views import CommentViewSet, RecipeViewSet

router = DefaultRouter()
router.register(r"recipes", RecipeViewSet, basename="recipes")

recipes_router = NestedDefaultRouter(router, r"recipes", lookup="recipe")
recipes_router.register(r"comments", CommentViewSet, basename="recipe-comments")

urlpatterns = [
    path("", include(router.urls)),
    path("", include(recipes_router.urls)),
]
