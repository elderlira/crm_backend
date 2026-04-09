from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import User

User = get_user_model()

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

class UserSerializer(serializers.ModelSerializer):
    role_name = serializers.ReadOnlyField(source='role.name')
    company_name = serializers.ReadOnlyField(source='company.name')
    class Meta:
        model = User
        fields = (
            'id', 'email', 'name', 'phone', 'role', 'role_name', 
            'company', 'company_name', 'away_message', 
            'is_online', 'last_login', 'last_logout'
        )

class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'email', 'password', 'name', 'phone', 'company', 
            'role', 'away_message', 'no_auto_assign', 
            'see_department_tickets'
        )
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user