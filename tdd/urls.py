from django.urls import path

from knox.views import LogoutView as KnoxLogoutView, LogoutAllView as KnoxLogoutAllView

from .views import (
    SignupView,
    LoginView,
    BookViewCreate,
    MyBookViewList,
    BookViewList,
    BookViewDetail,
)

urlpatterns = [
    path("auth/signup/", SignupView.as_view(), name="signup"),
    path("auth/login/", LoginView.as_view(), name="login"),
    path("auth/logout/", KnoxLogoutView.as_view(), name="logout"),
    path("auth/logoutall/", KnoxLogoutAllView.as_view(), name="logoutall"),
    path("books/create/", BookViewCreate.as_view(), name="book-create"),
    path("books/", MyBookViewList.as_view(), name="book-list-own"),
    path("books/all/", BookViewList.as_view(), name="book-list-all"),
    path("books/<int:pk>/", BookViewDetail.as_view(), name="book-detail"),
]
