from rest_framework import serializers
from .models import User, Company, Department, Role

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'name']

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'name']

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name', 'company'] # IMPORTANTE: 'company' deve estar aqui

class UserSerializer(serializers.ModelSerializer):
    role_name = serializers.CharField(source='role.name', read_only=True)
    company_name = serializers.CharField(source='company.name', read_only=True)
    department_name = serializers.CharField(source='department.name', read_only=True)
    last_login_at = serializers.DateTimeField(format="%d/%m/%Y %H:%M", read_only=True)
    last_logout_at = serializers.DateTimeField(format="%d/%m/%Y %H:%M", read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'role', 'role_name', 
            'company', 'company_name', 'department', 'department_name',
            'phone', 'is_online', 'last_login_at', 'last_logout_at'
        ]

class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # ADICIONADO: 'phone' na lista de campos para permitir o salvamento no cadastro
        fields = ['id', 'username', 'email', 'password', 'role', 'company', 'department', 'phone']
        extra_kwargs = {
            'password': {'write_only': True, 'required': False} # False permite editar sem trocar senha
        }

    def create(self, validated_data):
        # O create_user do Django lida com o hash da senha automaticamente
        return User.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance