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
    departments = serializers.ListField(child=serializers.IntegerField(), required=False)

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("E-mail já cadastrado.")
        return value

    @transaction.atomic
    def create(self, validated_data):
        departments = validated_data.pop("departments", [])
        password = validated_data.pop("password")
        
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()

        for dep_id in departments:
            UserDepartment.objects.create(user=user, department_id=dep_id)
        return user

class UserSerializer(serializers.ModelSerializer):
    company_info = serializers.SerializerMethodField(read_only=True)
    company = serializers.PrimaryKeyRelatedField(
        queryset=Company.objects.all(), required=False, allow_null=True
    )
    department = serializers.SerializerMethodField(read_only=True)
    role_display = serializers.SerializerMethodField() 
    password = serializers.CharField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = User
        fields = [
            "id", "username", "email", "cellphone", "password",
            "department", "company", "company_info",
            "role", "role_display", "is_superadmin", 
            "is_online", "last_login", "last_logout", "absence_message"
        ]

    def get_role_display(self, obj):
        role_map = {"admin": "Administrador", "supervisor": "Supervisor", "agent": "Agente"}
        return "Super Admin" if obj.is_superadmin else role_map.get(obj.role, obj.role)
    
    def get_company_info(self, obj):
        if obj.company:
            return {"id": obj.company.id, "name": obj.company.name}
        return None

    def get_department(self, obj):
        return [{"id": d.department.id, "name": d.department.name} 
                for d in obj.departments.all().select_related("department")]

    @transaction.atomic
    def update(self, instance, validated_data):
        # 1. Extrai a senha e os departamentos antes de atualizar o restante
        password = validated_data.pop('password', None)
        # Pegamos os departamentos da initial_data porque o Vue envia como lista de IDs
        departments_ids = self.initial_data.get("departments", None)

        # 2. Atualiza apenas os campos reais do modelo que sobraram em validated_data
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # 3. CRUCIAL: Se veio senha nova, criptografa
        if password:
            instance.set_password(password)
        
        instance.save()

        # 4. Atualiza os departamentos (ManyToMany)
        if departments_ids is not None:
            UserDepartment.objects.filter(user=instance).delete()
            for dep_id in departments_ids:
                UserDepartment.objects.create(user=instance, department_id=dep_id)

        return instance