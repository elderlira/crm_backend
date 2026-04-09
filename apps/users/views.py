from django.contrib.auth import authenticate, get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status, viewsets
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from django.utils import timezone

from .serializers import LoginSerializer, UserSerializer, UserCreateSerializer

User = get_user_model()

class UserCreateView(APIView):
    """
    Endpoint para registrar um novo usuário.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Usuário criado com sucesso!"}, 
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
            return Response({"error": "Credenciais inválidas"}, status=status.HTTP_401_UNAUTHORIZED)

        # Atualiza status para Online e salva o login
        user.is_online = True
        user.last_login = timezone.now()
        user.save()

        refresh = RefreshToken.for_user(user)

        return Response({
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh),
            "user": UserSerializer(user).data
        })

class RefreshView(TokenRefreshView):
    """
    View para renovar o access_token.
    """
    pass

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        # Registra logout e muda status para Offline
        user.is_online = False
        user.last_logout = timezone.now()
        user.save()

        try:
            refresh_token = request.data.get("refresh_token")
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Logout realizado com sucesso"})
        except Exception:
            return Response({"error": "Token inválido"}, status=status.HTTP_400_BAD_REQUEST)

class MeView(APIView):
    """
    Retorna os dados do usuário logado.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestão completa de usuários (CRUD).
    """
    queryset = User.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        return UserSerializer