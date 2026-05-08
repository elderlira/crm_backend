from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Permission
from .serializers import PermissionSerializer

class PermissionViewSet(viewsets.ModelViewSet):
    """
    ViewSet apenas para listar e gerenciar o catálogo de rotas disponíveis.
    """
    queryset = Permission.objects.all().order_by("name")
    serializer_class = PermissionSerializer
    permission_classes = [IsAuthenticated]