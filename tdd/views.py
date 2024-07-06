from knox.views import LoginView as KnoxLoginView
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import User, Book
from .serializers import SignupSerializer, LoginSerializer, BookSerializer


class SignupView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SignupSerializer


class LoginView(KnoxLoginView):
    serializer_class = LoginSerializer
    authentication_classes = (BasicAuthentication,)


class BookViewCreate(CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class MyBookViewList(ListAPIView):
    serializer_class = BookSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Book.objects.filter(author=self.request.user)

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        response_detail = {
            "status": "success",
            "message": "Books retrieved successfully",
            "data": {
                "books": response.data,
            },
        }
        return Response(response_detail, status=status.HTTP_200_OK)


class BookViewList(ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = (IsAuthenticated,)


class BookViewDetail(RetrieveAPIView):
    serializer_class = BookSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        book_id = self.kwargs.get("pk")
        return Book.objects.filter(author=self.request.user, pk=book_id)

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        if not response.data:
            return response
        response_detail = {
            "status": "success",
            "message": "Book retrieved successfully",
            "data": {
                "book": response.data,
            },
        }
        return Response(response_detail, status=status.HTTP_200_OK)
