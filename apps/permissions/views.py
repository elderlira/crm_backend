from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Profile, Permission, ProfilePermission
from .serializers import (ProfileSerializer, PermissionSerializer, ProfilePermissionSerializer)

class PermissionViewSet(viewsets.ModelViewSet):

    queryset = Permission.objects.all().order_by("name")

    serializer_class = PermissionSerializer

    permission_classes = [IsAuthenticated]


class ProfileViewSet(viewsets.ModelViewSet):

    queryset = Profile.objects.all().order_by("name")

    serializer_class = ProfileSerializer

    permission_classes = [IsAuthenticated]


class ProfilePermissionViewSet(viewsets.ModelViewSet):

    queryset = ProfilePermission.objects.all()

    serializer_class = ProfilePermissionSerializer

    permission_classes = [IsAuthenticated]