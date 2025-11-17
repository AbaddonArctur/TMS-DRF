from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Recipe, Ingredient, Comment

User = get_user_model()

class IngredientSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Ingredient
        fields = ("id", "name", "amount")

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ("id", "text", "author", "created_at", "parent", "replies")
        read_only_fields = ("author", "created_at", "replies")

    def get_replies(self, obj):
        qs = obj.replies.all()
        return CommentSerializer(qs, many=True).data

class RecipeSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    ingredients = IngredientSerializer(many=True)
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ("id", "title", "category", "description", "instructions", "image",
                  "author", "created_at", "ingredients", "comments")

    def get_comments(self, obj):
        qs = obj.comments.filter(parent__isnull=True)
        return CommentSerializer(qs, many=True).data

    def create(self, validated_data):
        ing_data = validated_data.pop("ingredients", [])
        recipe = Recipe.objects.create(**validated_data)
        for i in ing_data:
            Ingredient.objects.create(recipe=recipe, **i)
        return recipe

    def update(self, instance, validated_data):
        ing_data = validated_data.pop("ingredients", None)
        for attr, val in validated_data.items():
            setattr(instance, attr, val)
        instance.save()

        if ing_data is not None:
            instance.ingredients.all().delete()
            for i in ing_data:
                Ingredient.objects.create(recipe=instance, **i)
        return instance
