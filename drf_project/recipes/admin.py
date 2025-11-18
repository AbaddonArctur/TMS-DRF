from django.contrib import admin

from .models import Comment, Ingredient, Recipe


class IngredientInline(admin.TabularInline):
    model = Ingredient
    extra = 1


class CommentInline(admin.TabularInline):
    model = Comment
    fk_name = "recipe"
    extra = 0
    fields = ("author", "text", "parent", "created_at")
    readonly_fields = ("created_at",)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "author", "created_at")
    inlines = [IngredientInline, CommentInline]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("author", "recipe", "parent", "created_at")
