from django.contrib.auth import authenticate, get_user_model
from django.utils import timezone # Importado aqui para o LoginView funcionar

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.exceptions import PermissionDenied

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView

from apps.core.viewsets import BaseCompanyViewSet

from .serializers import LoginSerializer, UserSerializer
from .serializers import UserCreateSerializer

User = get_user_model()

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]

        user = authenticate(request, email=email, password=password)

        if user is None:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        
        # Sincronização de Status Online e Login
        user.is_online = True
        user.last_login = timezone.now()
        user.save(update_fields=['is_online', 'last_login']) 

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
        
        user = request.user
        user.is_online = False
        user.last_logout = timezone.now()
        user.save(update_fields=['is_online', 'last_logout'])

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Logout successful"})
        except Exception:
            return Response({"error": "Invalid token"}, status=400)
               
class MeView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        return Response(UserSerializer(request.user).data)
    
class UserViewSet(BaseCompanyViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    # --- O SEGREDO ESTÁ AQUI ---
    def get_queryset(self):
        # Se for superadmin, removemos o filtro de empresa do BaseCompanyViewSet
        if self.request.user.is_superadmin:
            return User.objects.all().select_related("company").prefetch_related(
                "departments__department"
            )
        # Se não for, mantém o comportamento padrão do BaseCompanyViewSet (filtrar por empresa)
        return super().get_queryset()

    def get_serializer_class(self):
        if self.action == "create":
            return UserCreateSerializer
        return UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if not request.user.is_superadmin:
            raise PermissionDenied("Only superadmin can create users")

        user = serializer.save()

        user = User.objects.select_related("company").prefetch_related(
            "departments__department"
        ).get(pk=user.pk)

        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)

    def perform_update(self, serializer):

        if self.request.user.is_superadmin:
            serializer.save()
            return

  
        if serializer.instance.company != self.request.user.company:
            raise PermissionDenied("Você não tem permissão para editar este usuário.")
        
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        
        # REGRA DE OURO: Se for superadmin, deleta qualquer um
        if request.user.is_superadmin:
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)

        # Se não for, trava por empresa
        if instance.company != request.user.company:
            raise PermissionDenied("Você não tem permissão para excluir usuários")

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)