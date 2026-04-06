from rest_framework import serializers
from django.db import transaction
from .models import User, UserCompany
from apps.departments.models import DepartmentUser, Department


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

class UserCreateSerializer(serializers.Serializer):

    name = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    cellphone = serializers.CharField(required=False, allow_blank=True)
    absence_message = serializers.CharField(required=False, allow_blank=True)

    company = serializers.IntegerField()
    profile = serializers.IntegerField()

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
        profile_id = validated_data.pop("profile")

        password = validated_data.pop("password")
        name = validated_data.pop("name")
        email = validated_data.pop("email")

        user = User.objects.create(
            email=email,
            username=email,
            first_name=name,
            cellphone=validated_data.get("cellphone"),
            absence_message=validated_data.get("absence_message")
        )

        user.set_password(password)
        user.save()

        UserCompany.objects.create(
            user=user,
            company_id=company_id,
            profile_id=profile_id
        )

        for department_id in departments:

            DepartmentUser.objects.create(
                user=user,
                department_id=department_id
            )

        return user


class UserSerializer(serializers.ModelSerializer):

    role = serializers.SerializerMethodField()
    company = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "username",
            "role",
            "company"
        ]

    def get_role(self, obj):

        if obj.is_superadmin:
            return "superadmin"

        uc = obj.user_companies.select_related("profile", "company").first()

        if uc and uc.profile:
            return uc.profile.name

        return None

    def get_company(self, obj):

        uc = obj.user_companies.select_related("company").first()

        if uc:
            return uc.company.name

        return None
    
class UserCompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = UserCompany
        fields = [
            "id",
            "user",
            "company",
            "profile",
            "active",
            "created_at"
        ]