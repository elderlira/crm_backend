from django.contrib.auth import authenticate, get_user_model

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, viewsets

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView

from .serializers import LoginSerializer, UserSerializer, UserCompanySerializer
from .models import UserCompany
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
    

class UserCompanyViewSet(viewsets.ModelViewSet):

    serializer_class = UserCompanySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        user = self.request.user

        if user.is_superadmin:
            return UserCompany.objects.all()

        return UserCompany.objects.filter(user=user)
    
class UserCreateView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        if not request.user.is_superadmin:
            return Response(
                {"error": "Only superadmin can create users"},
                status=403
            )

        serializer = UserCreateSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        return Response(
            UserSerializer(user).data,
            status=status.HTTP_201_CREATED
        )