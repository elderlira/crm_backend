from rest_framework import serializers
from .models import User


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):

    role = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "username",
            "role"
        ]

    def get_role(self, obj):
        user_client = obj.user_clients.first()

        if user_client and user_client.profile:
            return user_client.profile.name

        return None