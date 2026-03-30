from django.contrib.auth import authenticate, get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework import viewsets, permissions

from .serializers import (
    LoginSerializer, 
    UserSerializer, 
    CompanySerializer, 
    DepartmentSerializer, 
    RoleSerializer,
    CreateUserSerializer
)
from .models import Company, Department, Role

# --- CLASSES DE PERMISSÃO ---

class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        # Role 1 no seu Model é o Admin
        return bool(request.user and request.user.is_authenticated and request.user.role_id == 1)

class IsGerenteUser(permissions.BasePermission):
    def has_permission(self, request, view):
        # Role 1 (Admin) ou Role 2 (Gerente)
        return bool(request.user and request.user.is_authenticated and request.user.role_id in [1, 2])

User = get_user_model()

# --- VIEWS DE AUTENTICAÇÃO ---

class LoginView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]
        user = authenticate(request, email=email, password=password)

        if user is None:
            return Response({"error": "Credenciais inválidas"}, status=401)

        refresh = RefreshToken.for_user(user)
        return Response({
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh),
            "user": UserSerializer(user).data
        })

class RefreshView(TokenRefreshView):
    pass

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        refresh_token = request.data.get("refresh_token")
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Logout realizado com sucesso"})
        except Exception:
            return Response({"error": "Token inválido"}, status=400)

class MeView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        return Response(UserSerializer(request.user).data)

# --- VIEWSETS PROTEGIDOS ---

class RoleViewSet(viewsets.ModelViewSet):
    """
    ViewSet para listar os cargos (Roles) no v-select do Vue.
    """
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsAuthenticated]

class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

    def get_permissions(self):
        # Apenas Gerentes e Admins modificam empresas
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsGerenteUser()]
        return [IsAuthenticated()]

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsGerenteUser()]
        return [IsAuthenticated()]

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()

    def get_serializer_class(self):
        # Usa o serializer de criação (com password) apenas no POST
        if self.action == "create":
            return CreateUserSerializer
        return UserSerializer

    def get_permissions(self):
        # Regra rigorosa: Apenas ADMIN (Role 1) pode gerenciar usuários
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [IsAuthenticated()]