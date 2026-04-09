from django.urls import path,include
from .views import LoginView, RefreshView, LogoutView, MeView, UserCreateView, UserViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users',UserViewSet,basename='user')


urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('refresh/', RefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', include(router.urls)),
    path('me/', MeView.as_view(), name='me'),
    path('register/', UserCreateView.as_view(), name='user_register'),
]