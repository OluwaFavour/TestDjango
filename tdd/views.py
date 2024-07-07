from knox.views import LoginView as KnoxLoginView
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import Serializer

from .models import User, Book
from .serializers import SignupSerializer, LoginSerializer, BookSerializer


class CustomSerializerErrorResponse:
    def __init__(self, serializer: Serializer):
        self.serializer = serializer

    def format(self):
        formatted_errors = []
        for field, errors in self.serializer.errors.items():
            for error in errors:
                formatted_errors.append({"field": field, "message": error})
        return formatted_errors

    @property
    def response(self):
        return Response({"errors": self.format()}, status=status.HTTP_400_BAD_REQUEST)


class SignupView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SignupSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=False):
            return super().create(request, *args, **kwargs)
        return CustomSerializerErrorResponse(serializer).response


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
