from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Recipe(models.Model):
    title = models.CharField("Название", max_length=200)
    category = models.CharField("Категория", max_length=100)
    description = models.TextField("Краткое описание", blank=True)
    instructions = models.TextField("Пошаговая инструкция", blank=True)
    image = models.ImageField("Изображение", upload_to="recipes/", blank=True, null=True)
    author = models.ForeignKey(User, related_name="recipes", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return self.title

class Ingredient(models.Model):
    recipe = models.ForeignKey(Recipe, related_name="ingredients", on_delete=models.CASCADE)
    name = models.CharField("Ингредиент", max_length=150)
    amount = models.CharField("Количество", max_length=100, blank=True)

    def __str__(self):
        return f"{self.name} — {self.amount or ''}"

class Comment(models.Model):
    recipe = models.ForeignKey(Recipe, related_name="comments", on_delete=models.CASCADE)
    author = models.ForeignKey(User, related_name="comments", on_delete=models.CASCADE)
    text = models.TextField("Текст")
    parent = models.ForeignKey("self", null=True, blank=True, related_name="replies", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("created_at",)

    def __str__(self):
        return f"{self.author}: {self.text[:30]}"
