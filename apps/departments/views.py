from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import Department
from .serializers import DepartmentSerializer

from apps.core.permissions import IsSuperAdmin


class DepartmentViewSet(viewsets.ModelViewSet):

    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        company_id = self.request.query_params.get("company")

        if user.is_superadmin:
            if company_id:
                return Department.objects.filter(company_id=company_id)
            return Department.objects.all()

        queryset = Department.objects.filter(company=user.company)
        if company_id:
            queryset = queryset.filter(company_id=company_id)
        return queryset
    
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
    
    