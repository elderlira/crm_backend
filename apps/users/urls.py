from django.urls import path
from .views import LoginView, RefreshView, LogoutView, MeView, UserCreateView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('refresh/', RefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('me/', MeView.as_view(), name='me'),
    path('register/', UserCreateView.as_view(), name='user_register'),
]