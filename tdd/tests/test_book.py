from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from knox.models import AuthToken
from tdd.models import Book


class BookTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="Test@1234"
        )
        _, self.token = AuthToken.objects.create(self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)

    def test_create_book(self):
        url = reverse("book-create")
        data = {"title": "Test Book", "year": 2024}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 1)
        self.assertEqual(Book.objects.get().title, "Test Book")

    def test_list_my_books(self):
        Book.objects.create(title="Test Book", author=self.user, year=2024)
        url = reverse("book-list-own")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["data"]["books"]), 1)
        self.assertEqual(response.data["data"]["books"][0]["title"], "Test Book")

    def test_list_all_books(self):
        user2 = User.objects.create_user(
            username="anotheruser", email="another@example.com", password="Test@1234"
        )
        Book.objects.create(title="Test Book 1", author=self.user, year=2024)
        Book.objects.create(title="Test Book 2", author=user2, year=2023)
        url = reverse("book-list-all")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_retrieve_book(self):
        book = Book.objects.create(title="Test Book", author=self.user, year=2024)
        url = reverse("book-detail", kwargs={"pk": book.id})
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["data"]["book"]["title"], "Test Book")

    def test_retrieve_nonexistent_book(self):
        url = reverse("book-detail", kwargs={"pk": 999})
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
