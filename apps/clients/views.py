from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Client
from .serializers import ClientSerializer


class ClientViewSet(viewsets.ModelViewSet):

    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        user = self.request.user

        if user.is_superadmin:
            return Client.objects.all().order_by("name")

        return Client.objects.filter(client_users__user=user)