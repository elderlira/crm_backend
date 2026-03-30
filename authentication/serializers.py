from rest_framework import serializers
from .models import User, Company, Department, Role

# --- SERIALIZERS DE APOIO ---

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'name']

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ["id", "name"]

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ["id", "name", "company"]

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

# --- SERIALIZER DE LISTAGEM (O que aparece na Tabela do Vue) ---

class UserSerializer(serializers.ModelSerializer):
    # 'source' busca o nome dentro do objeto relacionado para exibir na tabela
    role_name = serializers.CharField(source='role.name', read_only=True)
    company_name = serializers.CharField(source='company.name', read_only=True)
    department_name = serializers.CharField(source='department.name', read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "username",
            "role_name",      # Key para o header do Vue
            "company_name",   # Key para o header do Vue
            "department_name" # Key para o header do Vue
        ]

# --- SERIALIZER DE CRIAÇÃO/EDIÇÃO (O que recebe dados do Modal) ---

class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "email",
            "username",
            "password",
            "company",
            "department",
            "role"
        ]
        extra_kwargs = {
            "password": {"write_only": True}
        }

    def create(self, validated_data):
        # O método create_user do Django lida com a criptografia da senha
        user = User.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        # Se houver senha no payload, criptografa antes de salvar
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)
        
        # Atualiza os demais campos
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance