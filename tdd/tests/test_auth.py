import base64
from django.contrib.auth.models import User
from django.urls import reverse

from knox.models import AuthToken
from rest_framework import status
from rest_framework.test import APITestCase


class AuthTests(APITestCase):
    def get_basic_auth_header(self, username: str, password: str) -> str:
        credentials = f"{username}:{password}"
        encoded_credentials = base64.b64encode(credentials.encode("utf-8")).decode(
            "utf-8"
        )
        return f"Basic {encoded_credentials}"

    def test_signup(self):
        url = reverse("signup")
        data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "Test@1234",
            "password_confirm": "Test@1234",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("id", response.data)

    def test_login(self):
        user = User.objects.create_user(
            username="testuser", email="test@example.com", password="Test@1234"
        )
        url = reverse("login")
        data = {"username": "testuser", "password": "Test@1234"}
        username = data.get("username")
        password = data.get("password")
        self.client.credentials(
            HTTP_AUTHORIZATION=f"{self.get_basic_auth_header(username, password)}"
        )
        response = self.client.post(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)

    def test_logout(self):
        user = User.objects.create_user(
            username="testuser", email="test@example.com", password="Test@1234"
        )
        _, token = AuthToken.objects.create(user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)
        url = reverse("logout")
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_logout_all(self):
        user = User.objects.create_user(
            username="testuser", email="test@example.com", password="Test@1234"
        )
        _, token = AuthToken.objects.create(user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)
        url = reverse("logoutall")
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
