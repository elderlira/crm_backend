from rest_framework import viewsets
from .models import Profile
from .serializers import ProfileSerializer

class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_staff and not user.company:
            return Profile.objects.all()
        
        return Profile.objects.filter(user__company=user.company)

    def perform_create(self, serializer):
        serializer.save()