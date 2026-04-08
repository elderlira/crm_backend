from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from apps.core.viewsets import BaseCompanyViewSet

from .models import Client
from .serializers import ClientSerializer


class ClientViewSet(BaseCompanyViewSet):

    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]
    queryset = Client.objects.all()