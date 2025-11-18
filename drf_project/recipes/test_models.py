from django.contrib.auth import get_user_model
from django.test import TestCase

from recipes.models import Comment, Ingredient, Recipe

User = get_user_model()


class ModelsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test", password="pass")
        self.recipe = Recipe.objects.create(
            title="Test recipe",
            category="Супы",
            author=self.user,
            description="Desc",
            instructions="Instr",
        )

    def test_ingredient_creation(self):
        Ingredient.objects.create(recipe=self.recipe, name="Соль", amount="10 г")
        self.assertEqual(self.recipe.ingredients.count(), 1)

    def test_comment_creation(self):
        c = Comment.objects.create(recipe=self.recipe, author=self.user, text="Хорошо")
        self.assertEqual(self.recipe.comments.count(), 1)
        self.assertEqual(c.text, "Хорошо")

    def test_reply_creation(self):
        parent = Comment.objects.create(
            recipe=self.recipe, author=self.user, text="Осн."
        )
        reply = Comment.objects.create(
            recipe=self.recipe, author=self.user, text="Ответ", parent=parent
        )
        self.assertEqual(parent.replies.count(), 1)
        self.assertEqual(parent.replies.first().text, "Ответ")
