from rest_framework import serializers
from django.db import transaction
from .models import User, UserDepartment
from apps.departments.models import Department
from apps.companies.models import Company


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

class UserCreateSerializer(serializers.Serializer):

    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    cellphone = serializers.CharField(required=False, allow_blank=True)
    absence_message = serializers.CharField(required=False, allow_blank=True)

    company = serializers.PrimaryKeyRelatedField(queryset=Company.objects.all())
    role = serializers.ChoiceField(choices=["admin", "supervisor", "agent"])

    departments = serializers.ListField(
        child=serializers.IntegerField(),
        required=False
    )

    def validate_departments(self, value):
        try:
            company_id = int(self.initial_data.get("company"))
        except (TypeError, ValueError):
            raise serializers.ValidationError("Invalid company")

        valid_department_ids = set(
            Department.objects.filter(
                company_id=company_id
            ).values_list("id", flat=True)
        )

        for dep in value:
            if dep not in valid_department_ids:
                raise serializers.ValidationError(
                    f"Department {dep} does not belong to company {company_id}"
                )
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already registered")
        return value

    @transaction.atomic
    def create(self, validated_data):
        departments = validated_data.pop("departments", [])
        company = validated_data.pop("company")
        password = validated_data.pop("password")
        username = validated_data.pop("username")
        role = validated_data.pop("role")

        user = User.objects.create(
            username=username,
            email=validated_data["email"],
            company=company,
            cellphone=validated_data.get("cellphone"),
            absence_message=validated_data.get("absence_message"),
            role=role
        )

        user.set_password(password)
        user.save()

        for department_id in departments:
            UserDepartment.objects.create(
                user=user,
                department_id=department_id
            )

        return user


class UserSerializer(serializers.ModelSerializer):

    department = serializers.SerializerMethodField()
    company = serializers.SerializerMethodField()
    role = serializers.CharField()
    role_display = serializers.SerializerMethodField() 

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "cellphone",
            "department",
            "company",
            "role",
            "role_display",
            "is_superadmin",
        ]

    def get_role_display(self, obj):
        role_map = {
            "admin": "Administrador",
            "supervisor": "Supervisor",
            "agent": "Agente"
        }
        if obj.is_superadmin:
            return "Super Admin"
        return role_map.get(obj.role, obj.role)
    
    def get_company(self, obj):
        if obj.company:
            return {"id": obj.company.id, "name": obj.company.name}
        return None

    def get_department(self, obj):
        departments = obj.departments.all().select_related("department")
        return [
            {"id": d.department.id, "name": d.department.name}
            for d in departments
        ]