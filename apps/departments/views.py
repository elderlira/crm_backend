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
        queryset = Department.objects.all()
        company = self.request.query_params.get("company")

        if user.is_superadmin:
            return Department.objects.all()
        
        if company:
            queryset = queryset.filter(company_id=company)

        return queryset

    #     return Department.objects.filter(
    #     company=user.company
    # )
    
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
    
    