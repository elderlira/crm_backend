from rest_framework import viewsets
from .models import Label
from rest_framework.permissions import IsAuthenticated
from .serializers import LabelSerializer

class LabelViewSet(viewsets.ModelViewSet): 
    serializer_class = LabelSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
          return Label.objects.all()
        
    