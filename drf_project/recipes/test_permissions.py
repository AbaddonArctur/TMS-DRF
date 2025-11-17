from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from recipes.models import Recipe

User = get_user_model()

class PermissionsTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.author = User.objects.create_user("author", password="1")
        self.other = User.objects.create_user("other", password="1")

        self.recipe = Recipe.objects.create(
            title="Test",
            category="C",
            author=self.author
        )

        token = self.client.post(
            reverse("token_obtain_pair"),
            {"username": "author", "password": "1"}
        ).data["access"]
        self.author_headers = {"HTTP_AUTHORIZATION": f"Bearer {token}"}

        token2 = self.client.post(
            reverse("token_obtain_pair"),
            {"username": "other", "password": "1"}
        ).data["access"]
        self.other_headers = {"HTTP_AUTHORIZATION": f"Bearer {token2}"}

    def test_author_can_update(self):
        url = reverse("recipes-detail", kwargs={"pk": self.recipe.id})

        resp = self.client.patch(url, {"title": "New title"},
                                 format="json", **self.author_headers)

        self.assertEqual(resp.status_code, 200)
        self.recipe.refresh_from_db()
        self.assertEqual(self.recipe.title, "New title")

    def test_other_cannot_update(self):
        url = reverse("recipes-detail", kwargs={"pk": self.recipe.id})

        resp = self.client.patch(url, {"title": "Wrong edit"},
                                 format="json", **self.other_headers)

        self.assertEqual(resp.status_code, 403)