from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    LoginView,
    RefreshView,
    LogoutView,
    MeView,
    CompanyViewSet,
    DepartmentViewSet,
    UserViewSet,
    RoleViewSet # <-- 1. ADICIONE AQUI
)

router = DefaultRouter()

router.register("companies", CompanyViewSet)
router.register("departments", DepartmentViewSet)
router.register("users", UserViewSet)
router.register("roles", RoleViewSet) # <-- 2. ADICIONE ESTA LINHA

urlpatterns = [
    path("login/", LoginView.as_view()),
    path("refresh/", RefreshView.as_view()),
    path("logout/", LogoutView.as_view()),
    path("me/", MeView.as_view()),
    path("", include(router.urls)),
]