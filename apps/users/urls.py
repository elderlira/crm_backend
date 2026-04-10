from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    LoginView, 
    RefreshView, 
    LogoutView, 
    MeView, 
    UserViewSet
)

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="users")

urlpatterns = [
    path("login/", LoginView.as_view()),
    path("refresh/", RefreshView.as_view()),
    path("logout/", LogoutView.as_view()),
    path("me/", MeView.as_view()),
    path("", include(router.urls)),
]