from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import Company
from .serializers import CompanySerializer

from apps.core.permissions import IsSuperAdmin


class CompanyViewSet(viewsets.ModelViewSet):

    queryset = Company.objects.all().order_by("name")
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        user = self.request.user

        if user.is_superadmin:
            return Company.objects.all()

        return Company.objects.filter(id=user.company_id)

    def create(self, request, *args, **kwargs):

        if not request.user.is_superadmin:
            return Response(
                {"error": "Only superadmin can create companies"},
                status=status.HTTP_403_FORBIDDEN
            )

        return super().create(request, *args, **kwargs)

    def get_permissions(self):

        if self.action == "create":
            return [IsAuthenticated(), IsSuperAdmin()]

        return [IsAuthenticated()]