from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from recipes.models import Recipe

from .test_auth_utils import obtain_access_token

User = get_user_model()


class RecipeViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user("u", password="1")

        token = obtain_access_token(self.client, "u", "1")
        self.auth = {"HTTP_AUTHORIZATION": f"Bearer {token}"}

        self.recipe = Recipe.objects.create(title="R", category="C", author=self.user)

    def test_create_recipe(self):
        url = reverse("recipes-list")
        resp = self.client.post(
            url,
            {"title": "New", "category": "X"},
            format="json",
            **self.auth,
        )
        self.assertEqual(resp.status_code, 201)

    def test_add_ingredient(self):
        url = reverse("recipes-add-ingredient", kwargs={"pk": self.recipe.id})
        resp = self.client.post(
            url,
            {"name": "Salt", "amount": "1g"},
            format="json",
            **self.auth,
        )
        self.assertEqual(resp.status_code, 201)

        self.recipe.refresh_from_db()
        self.assertEqual(self.recipe.ingredients.count(), 1)
