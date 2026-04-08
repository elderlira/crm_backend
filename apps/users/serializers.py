from rest_framework import serializers
from django.db import transaction
from .models import User
from apps.departments.models import Department


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class UserCreateSerializer(serializers.Serializer):

    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    cellphone = serializers.CharField(required=False, allow_blank=True)
    absence_message = serializers.CharField(required=False, allow_blank=True)

    company = serializers.IntegerField()
    profile = serializers.CharField()

    departments = serializers.ListField(
        child=serializers.IntegerField(),
        required=False
    )

    def validate_departments(self, value):

        company_id = self.initial_data.get("company")

        valid_departments = Department.objects.filter(
            company_id=company_id
        ).values_list("id", flat=True)

        for dep in value:
            if dep not in valid_departments:
                raise serializers.ValidationError(
                    "Invalid department for this company"
                )

        return value

    def validate_email(self, value):

        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already registered")

        return value

    @transaction.atomic
    def create(self, validated_data):

        departments = validated_data.pop("departments", [])
        company_id = validated_data.pop("company")

        password = validated_data.pop("password")
        username = validated_data.pop("username")

        user = User.objects.create(
            username=username,
            email=validated_data["email"],
            company_id=company_id,
            cellphone=validated_data.get("cellphone"),
            absence_message=validated_data.get("absence_message"),
            role=validated_data.get("profile")
        )

        user.set_password(password)
        user.save()

        # for department_id in departments:
        #     UserDepartment.objects.create(
        #         user=user,
        #         department_id=department_id
        #     )

        return user


class UserSerializer(serializers.ModelSerializer):

    department = serializers.SerializerMethodField()
    company = serializers.StringRelatedField()

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "cellphone",
            "department",
            "company"
        ]

    def get_department(self, obj):

        departments = obj.departments.select_related("department")

        return [
            {
                "id": d.department.id,
                "name": d.department.name
            }
            for d in departments
        ]