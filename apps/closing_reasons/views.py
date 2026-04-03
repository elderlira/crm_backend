from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import ClosingReason
from .serializers import ClosingReasonSerializer


class ClosingReasonViewSet(viewsets.ModelViewSet):

    queryset = ClosingReason.objects.all().order_by("id")

    serializer_class = ClosingReasonSerializer

    permission_classes = [IsAuthenticated]