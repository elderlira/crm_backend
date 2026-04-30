from rest_framework import viewsets
from .models import Label
from rest_framework.permissions import IsAuthenticated
from .serializers import LabelSerializer

class LabelViewSet(viewsets.ModelViewSet): 
    serializer_class = LabelSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.is_superadmin:
          return Label.objects.all()
        
        if not user.company:
            return Label.objects.none()

        return Label.objects.filter(company=user.company)

    def perform_create(self, serializer):
           if self.request.user.company:
            serializer.save(company=self.request.user.company)

           else:
            serializer.save()