from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from recipes.models import Comment, Recipe

from .test_auth_utils import obtain_access_token

User = get_user_model()


class CommentTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create_user("u", password="1")
        self.recipe = Recipe.objects.create(title="R", category="C", author=self.user)

        token = obtain_access_token(self.client, "u", "1")
        self.auth = {"HTTP_AUTHORIZATION": f"Bearer {token}"}

    def test_create_comment(self):
        url = reverse("recipe-comments-list", kwargs={"recipe_pk": self.recipe.id})
        resp = self.client.post(url, {"text": "hello"}, format="json", **self.auth)
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(self.recipe.comments.filter(parent__isnull=True).count(), 1)

    def test_reply_comment(self):
        parent = Comment.objects.create(recipe=self.recipe, author=self.user, text="p")

        url = reverse("recipe-comments-list", kwargs={"recipe_pk": self.recipe.id})
        resp = self.client.post(
            url,
            {"text": "reply", "parent": parent.id},
            format="json",
            **self.auth,
        )

        self.assertEqual(resp.status_code, 201)
        self.assertEqual(parent.replies.count(), 1)
        self.assertEqual(parent.replies.first().text, "reply")
