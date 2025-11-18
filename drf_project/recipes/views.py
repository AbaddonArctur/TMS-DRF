from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import Comment, Recipe
from .permissions import IsAuthorOrReadOnly
from .serializers import CommentSerializer, IngredientSerializer, RecipeSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [IsAuthorOrReadOnly]

    def get_permissions(self):
        if self.action in ("create", "update", "partial_update", "destroy"):
            return [IsAuthenticated(), IsAuthorOrReadOnly()]
        return [AllowAny()]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def add_ingredient(self, request, pk=None):
        recipe = self.get_object()
        serializer = IngredientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(recipe=recipe)
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

    def perform_create(self, serializer):
        recipe_pk = self.kwargs.get("recipe_pk")
        recipe = get_object_or_404(Recipe, pk=recipe_pk)
        serializer.save(author=self.request.user, recipe=recipe)
