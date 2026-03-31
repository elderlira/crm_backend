from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LoginView, LogoutView, MeView, UserViewSet, RoleViewSet, CompanyViewSet, DepartmentViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'roles', RoleViewSet)
router.register(r'companies', CompanyViewSet) # ADICIONE ESTA LINHA
router.register(r'departments', DepartmentViewSet) # ADICIONE ESTA LINHA

urlpatterns = [
    path('', include(router.urls)),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('me/', MeView.as_view(), name='me'),
]