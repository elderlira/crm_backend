from django.contrib.auth import authenticate, get_user_model

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, viewsets
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import PermissionDenied

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView

from apps.core.viewsets import BaseCompanyViewSet

from .serializers import LoginSerializer, UserSerializer
from .serializers import UserCreateSerializer

User = get_user_model()

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
            return Response(
                {"error": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED
            )

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

            return Response({"message": "Logout successful"})

        except Exception:

            return Response({"error": "Invalid token"}, status=400)
        
class MeView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        return Response(UserSerializer(request.user).data)
    
class UserViewSet(BaseCompanyViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "create":
            return UserCreateSerializer
        return UserSerializer

    def perform_create(self, serializer):

        user = self.request.user

        if not user.is_superadmin:
            raise PermissionDenied("Only superadmin can create users")

        serializer.save()

    def perform_update(self, serializer):

        if serializer.instance.company != self.request.user.company:
            raise PermissionDenied("You cannot edit this user")

        serializer.save()

    def perform_destroy(self, instance):

        if self.request.user.company != instance.company:
            raise PermissionDenied("You cannot delete this user")

        instance.delete()