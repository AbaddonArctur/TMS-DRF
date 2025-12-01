from django.core.cache import cache
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import Comment, Recipe
from .permissions import IsAuthorOrReadOnly
from .serializers import CommentSerializer, IngredientSerializer, RecipeSerializer

CACHE_TIME = 60


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [IsAuthorOrReadOnly]

    def get_permissions(self):
        if self.action in (
            "create",
            "update",
            "partial_update",
            "destroy",
            "add_ingredient",
        ):
            return [IsAuthenticated(), IsAuthorOrReadOnly()]
        return [AllowAny()]

    @method_decorator(cache_page(CACHE_TIME))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @method_decorator(cache_page(CACHE_TIME))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def perform_create(self, serializer):
        recipe = serializer.save(author=self.request.user)
        cache.clear()
        return recipe

    def perform_update(self, serializer):
        recipe = serializer.save()
        cache.clear()
        return recipe

    def perform_destroy(self, instance):
        instance.delete()
        cache.clear()

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def add_ingredient(self, request, pk=None):
        recipe = self.get_object()
        serializer = IngredientSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(recipe=recipe)
            cache.clear()
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrReadOnly]

    def get_queryset(self):
        recipe_pk = self.kwargs.get("recipe_pk")
        if recipe_pk:
            return Comment.objects.filter(recipe_id=recipe_pk, parent__isnull=True)
        return Comment.objects.filter(parent__isnull=True)

    @method_decorator(cache_page(CACHE_TIME))
    def list(self, *args, **kwargs):
        return super().list(*args, **kwargs)

    def perform_create(self, serializer):
        recipe_pk = self.kwargs.get("recipe_pk")
        recipe = get_object_or_404(Recipe, pk=recipe_pk)
        serializer.save(author=self.request.user, recipe=recipe)
        cache.clear()

    def perform_update(self, serializer):
        serializer.save()
        cache.clear()

    def perform_destroy(self, instance):
        instance.delete()
        cache.clear()
