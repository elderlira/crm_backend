from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import viewsets, permissions
from django.contrib.auth import authenticate, get_user_model
from .serializers import UserSerializer, CreateUserSerializer, RoleSerializer
from .models import Role, Company, Department
from django.utils import timezone

User = get_user_model()

class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role_id == 1)

class LoginView(APIView):
    authentication_classes = []
    permission_classes = []
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(request, email=email, password=password)
        if user:

            user.is_online = True
            user.last_login_at = timezone.now()
            user.save(update_fields=['is_online', 'last_login_at'])

            refresh = RefreshToken.for_user(user)
            return Response({
                "access_token": str(refresh.access_token),
                "user": UserSerializer(user).data
            })
        return Response({"error": "Credenciais inválidas"}, status=401)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        if user:
            # --- LÓGICA DE LOGOUT ---
            user.is_online = False
            user.last_logout_at = timezone.now()
            user.save(update_fields=['is_online', 'last_logout_at'])
            
        return Response({"message": "Logout realizado com sucesso"}, status=204)
    
class MeView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        return Response(UserSerializer(request.user).data)

class UserViewSet(viewsets.ModelViewSet):
    # O select_related carrega os nomes de Role, Company e Dept em uma única consulta
    queryset = User.objects.select_related('role', 'company', 'department').all()
    
    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return CreateUserSerializer
        return UserSerializer

    def get_permissions(self):
        # Apenas Admin pode deletar ou criar
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [permissions.IsAuthenticated()]

# Viewsets simples para os selects do Vue
class RoleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer

from .models import Role, Company, Department
from .serializers import RoleSerializer, CompanySerializer, DepartmentSerializer

# Adicione estes ViewSets simples ao final do seu views.py
class CompanyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated]

class DepartmentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated]