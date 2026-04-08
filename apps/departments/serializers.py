from rest_framework import serializers
from .models import Department

class DepartmentSerializer(serializers.ModelSerializer):

    class Meta:

        model = Department

        fields = "__all__"

    def validate_departments(self, value):

        company_id = self.initial_data.get("company")

        valid_departments = Department.objects.filter(
            company_id=company_id
        ).values_list("id", flat=True)

        for dep in value:
            if dep not in valid_departments:
                raise serializers.ValidationError(
                    "Department does not belong to this company"
                )

        return value