from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from recipes.models import Recipe

from .test_auth_utils import obtain_access_token

User = get_user_model()


class PermissionsTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.author = User.objects.create_user("author", password="1")
        self.other = User.objects.create_user("other", password="1")

        self.recipe = Recipe.objects.create(
            title="Test", category="C", author=self.author
        )

        self.author_token = obtain_access_token(self.client, "author", "1")
        self.other_token = obtain_access_token(self.client, "other", "1")

        self.author_headers = {"HTTP_AUTHORIZATION": f"Bearer {self.author_token}"}
        self.other_headers = {"HTTP_AUTHORIZATION": f"Bearer {self.other_token}"}

    def test_anonymous_can_read(self):
        url = reverse("recipes-detail", kwargs={"pk": self.recipe.id})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_anonymous_cannot_edit(self):
        url = reverse("recipes-detail", kwargs={"pk": self.recipe.id})
        resp = self.client.patch(url, {"title": "Hacked"}, format="json")
        self.assertIn(resp.status_code, (401, 403))

    def test_author_can_edit(self):
        url = reverse("recipes-detail", kwargs={"pk": self.recipe.id})
        resp = self.client.patch(
            url,
            {"title": "Updated"},
            format="json",
            **self.author_headers,
        )
        self.assertEqual(resp.status_code, 200)

        self.recipe.refresh_from_db()
        self.assertEqual(self.recipe.title, "Updated")

    def test_other_cannot_edit(self):
        url = reverse("recipes-detail", kwargs={"pk": self.recipe.id})
        resp = self.client.patch(
            url,
            {"title": "Wrong"},
            format="json",
            **self.other_headers,
        )
        self.assertEqual(resp.status_code, 403)
