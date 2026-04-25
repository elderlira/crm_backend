from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.models import update_last_login 
from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, viewsets
from rest_framework.exceptions import PermissionDenied

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView

from apps.core.viewsets import BaseCompanyViewSet
from .serializers import LoginSerializer, UserSerializer, UserCreateSerializer

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

        user.is_online = True
        user.save(update_fields=['is_online']) 
        update_last_login(None, user) 

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
        try:
            user = request.user
            
            user.is_online = False
            user.last_logout = timezone.now()
            user.save(update_fields=['is_online', 'last_logout'])

            refresh_token = request.data.get("refresh_token")
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()

            return Response({"message": "Logout com sucesso"}, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=400)
        
class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)
    
class UserViewSet(BaseCompanyViewSet):
    queryset = User.objects.all().select_related("company").prefetch_related(
        "departments__department"
    )
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if getattr(user, 'is_superadmin', False):
            return User.objects.all().select_related("company").prefetch_related(
                "departments__department"
            )
        return super().get_queryset()

    def get_serializer_class(self):
        if self.action == "create":
            return UserCreateSerializer
        return UserSerializer

    def create(self, request, *args, **kwargs):
        if not request.user.is_superadmin:
            raise PermissionDenied("Only superadmin can create users")

        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user = User.objects.select_related("company").prefetch_related(
            "departments__department"
        ).get(pk=user.pk)

        response_serializer = UserSerializer(user)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


    def perform_update(self, serializer):
        role = self.request.data.get('role')
        if role and role != 'admin':
            serializer.validated_data['is_superadmin'] = False
            
        serializer.save()

    def perform_destroy(self, instance):
        request_user = self.request.user
        
        if request_user.is_superadmin or instance.company == request_user.company:
            instance.delete()
        else:
            raise PermissionDenied("You cannot delete users from other companies.")