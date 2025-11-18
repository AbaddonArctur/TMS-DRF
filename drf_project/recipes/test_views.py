from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from recipes.models import Recipe

User = get_user_model()


class RecipeApiTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="user1", password="pass123")

        self.list_url = reverse("recipes-list")

        token_url = reverse("token_obtain_pair")
        resp = self.client.post(token_url, {"username": "user1", "password": "pass123"})
        self.access = resp.data["access"]

    def auth(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access}")

    def test_recipe_list(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)

    def test_create_recipe(self):
        self.auth()

        data = {
            "title": "Пицца",
            "category": "Главное",
            "description": "Вкусно",
            "instructions": "Печь 20 минут",
            "ingredients": [
                {"name": "Мука", "amount": "500 г"},
                {"name": "Сыр", "amount": "300 г"},
            ],
        }

        response = self.client.post(self.list_url, data, format="json")

        self.assertIn(response.status_code, [201, 200])
        self.assertEqual(Recipe.objects.count(), 1)


class CommentApiTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create_user(username="u1", password="123")
        self.user2 = User.objects.create_user(username="u2", password="123")

        self.recipe = Recipe.objects.create(
            title="Суп", category="Супы", author=self.user
        )

        token_url = reverse("token_obtain_pair")
        resp = self.client.post(token_url, {"username": "u2", "password": "123"})
        self.access = resp.data["access"]

    def auth(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access}")

    def test_add_comment(self):
        self.auth()

        url = reverse("recipe-comments-list", kwargs={"recipe_pk": self.recipe.id})
        resp = self.client.post(url, {"text": "Отличный рецепт!"}, format="json")

        self.assertIn(resp.status_code, [200, 201])
        self.assertEqual(self.recipe.comments.count(), 1)

    def test_add_reply(self):
        self.auth()

        url = reverse("recipe-comments-list", kwargs={"recipe_pk": self.recipe.id})
        parent = self.client.post(url, {"text": "Главный коммент"}, format="json").data

        resp2 = self.client.post(
            url, {"text": "Ответ", "parent": parent["id"]}, format="json"
        )

        self.assertIn(resp2.status_code, [200, 201])
        self.assertEqual(self.recipe.comments.first().replies.count(), 1)
